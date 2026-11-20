"""Shared helpers: paths, tool lookup, yt-dlp and ffmpeg wrappers."""
import hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(os.environ.get("CLIP_DESK_HOME", Path.cwd()))
JOBS = ROOT / "jobs"


# Homebrew's plain "ffmpeg" formula is built without libass, so it cannot burn captions; "ffmpeg-full" can,
# but it is keg-only (not on PATH). Prefer it when present. FFMPEG_DIR overrides everything.
_FFMPEG_DIRS = [os.environ.get("FFMPEG_DIR", ""), "/opt/homebrew/opt/ffmpeg-full/bin", "/usr/local/opt/ffmpeg-full/bin"]
_found = {}


def tool(name):
    if name in _found:
        return _found[name]
    p = None
    if name in ("ffmpeg", "ffprobe"):
        for d in filter(None, _FFMPEG_DIRS):
            c = Path(d) / (name + (".exe" if sys.platform == "win32" else ""))
            if c.is_file() and os.access(c, os.X_OK):
                p = str(c)
                break
    p = p or shutil.which(name)
    if not p:
        sys.exit(f"{name} non trovato. Lancia prima la skill setup (installa ffmpeg e yt-dlp).")
    _found[name] = p
    return p


def need_subtitles():
    """Exit with a clear message if this ffmpeg cannot burn ASS captions (no libass)."""
    r = run([tool("ffmpeg"), "-hide_banner", "-filters"], capture=True, check=False)
    if not re.search(r"^\s*\S*\s+subtitles\s", r.stdout or "", re.M):
        sys.exit(f"Il tuo ffmpeg ({tool('ffmpeg')}) non sa scrivere i sottotitoli: manca libass.\n"
                 "Mac: brew install ffmpeg-full (gli script lo trovano da soli). "
                 "Windows: winget install --id Gyan.FFmpeg -e. Linux: sudo apt install -y ffmpeg.")


def run(cmd, check=True, capture=False):
    r = subprocess.run(cmd, check=False, text=True, encoding="utf-8", errors="replace",
                       stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    if check and r.returncode != 0:
        msg = (r.stderr or "")[-1500:] if capture else ""
        sys.exit(f"command failed ({r.returncode}): {' '.join(map(str, cmd))[:200]}\n{msg}")
    return r


def ytdlp_base():
    import importlib.util
    exe = [sys.executable, "-m", "yt_dlp"] if importlib.util.find_spec("yt_dlp") else [tool("yt-dlp")]
    base = exe + ["--no-warnings", "--no-progress"]
    if sys.platform == "win32":
        base += ["--compat-options", "no-certifi"]  # use the Windows certificate store
    return base


def ytdlp_json(url, extra=()):
    r = run(ytdlp_base() + ["-J", *extra, url], capture=True)
    return json.loads(r.stdout)


def is_url(s):
    return bool(re.match(r"https?://", s))


def job_dir(src):
    key = hashlib.sha1(src.encode()).hexdigest()[:8]
    stem = re.sub(r"[^a-z0-9]+", "-", Path(src).stem.lower() if not is_url(src) else src.split("v=")[-1].split("/")[-1].lower())[:24].strip("-")
    d = JOBS / f"{stem or 'job'}-{key}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ffprobe(path):
    r = run([tool("ffprobe"), "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
             "-of", "json", str(path)], capture=True)
    return json.loads(r.stdout)


def join_elisions(words):
    """faster-whisper splits Italian elisions into two words ("dell" + "'auto"): glue them back ("dell'auto").
    Safe to run twice; English contractions ("it" + "'s") come out right too."""
    out = []
    for w in words:
        if out and str(w.get("w", "")).startswith("'") and out[-1]["w"][-1:].isalpha():
            out[-1] = dict(out[-1], w=out[-1]["w"] + w["w"], e=w["e"])
        else:
            out.append(dict(w))
    return out


def save_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
