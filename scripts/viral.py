"""Viral clips of the streamers playing GTA 6: the most-watched clips of the last hours, ranked by views per hour.

Where the streamers come from:
- the GTA 6 lives on right now in that language: Twitch and YouTube (same search as streams.py), Kick when it answers;
- the channels in your watchlist (lines with twitch.tv/<canale>, kick.com/<canale>, youtube.com/@canale);
- the streamers seen live in the last 7 days, remembered in streamer-gta6.json: a live that ended this morning counts too.
Clips: Twitch and Kick keep the clips their viewers cut, with views (read with yt-dlp, no account needed; Kick needs
curl_cffi). YouTube has no list of viewers' clips: its lives are listed, for live.py while they run or moments.py after.
--scarica N downloads the top N into jobs/, ready for cut.py: transcript plus one candidate, the clip (at most --max-sec
seconds, around its payoff). --prepara does the same for one clip: a link, or a file such as a live.py spike.

usage: python viral.py [--lang it] [--ore 24] [--top 15] [--min-views 30] [--canali watchlist.md]
                       [--scarica N | --prepara URL-o-file [--streamer nome]] [--max-sec 50] [--out virali.md]
"""
import argparse, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, ffprobe, job_dir, run, save_json, tool, ytdlp_base, ytdlp_json

GTA6 = re.compile(r"grand\s*theft\s*auto\s*(?:vi|6)\b|\bgta\s*(?:vi|6)\b", re.I)
CHANNEL_URL = re.compile(r"(?:https?://)?(?:www\.|m\.)?(twitch\.tv|kick\.com|youtube\.com)/(@?[\w.-]+)", re.I)
NOT_CHANNELS = {"videos", "directory", "search", "categories", "watch", "shorts", "results", "channel", "c"}
MEMORY = ROOT / "streamer-gta6.json"
MEMORY_DAYS = 7


def live_now(query, lang, limit):
    """GTA 6 lives on right now: [{platform, id, name, url, viewers, title}]."""
    import streams
    out = []
    try:
        for r in streams.twitch(query, lang=lang) or []:
            login = r["url"].rstrip("/").split("/")[-1].lower()
            out.append({"platform": "twitch", "id": login, "name": r["channel"] or login, "url": f"https://www.twitch.tv/{login}",
                        "viewers": r["viewers"], "title": r["title"]})
    except Exception as e:
        print(f"twitch: {e}", file=sys.stderr)
    try:
        for r in streams.youtube(query, limit):
            out.append({"platform": "youtube", "id": r["url"], "name": r["channel"], "url": r["url"], "viewers": r["viewers"],
                        "title": r["title"]})
    except Exception as e:
        print(f"youtube: {e}", file=sys.stderr)
    for r in streams.kick(query):  # silent on failure
        if GTA6.search(r.get("title") or ""):
            slug = r["url"].rstrip("/").split("/")[-1].lower()
            out.append({"platform": "kick", "id": slug, "name": r["channel"], "url": r["url"], "viewers": r["viewers"],
                        "title": r["title"]})
    return out


def watchlist(path):
    """Channels named in the watchlist: [(platform, id)]."""
    if not path or not Path(path).exists():
        return []
    out = []
    for host, ch in CHANNEL_URL.findall(Path(path).read_text(encoding="utf-8", errors="replace")):
        host, low = host.lower(), ch.lower()
        if low in NOT_CHANNELS:
            continue
        if host == "twitch.tv":
            out.append(("twitch", low))
        elif host == "kick.com":
            out.append(("kick", low))
        elif ch.startswith("@"):
            out.append(("youtube", ch))
    return out


def remember(lives):
    """Add the streamers live now to streamer-gta6.json; return everyone seen in the last MEMORY_DAYS days."""
    try:
        mem = json.loads(MEMORY.read_text(encoding="utf-8")) if MEMORY.exists() else {}
    except Exception:
        mem = {}
    now = time.time()
    for r in lives:
        if r["platform"] in ("twitch", "kick"):
            mem[f"{r['platform']}:{r['id']}"] = {"platform": r["platform"], "id": r["id"], "name": r["name"], "seen": now}
    mem = {k: v for k, v in mem.items() if now - v.get("seen", 0) < MEMORY_DAYS * 86400}
    try:
        MEMORY.write_text(json.dumps(mem, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass
    return mem


def clips_of(platform, cid, hours):
    """Clips of one Twitch or Kick channel over the period, most viewed first (yt-dlp, no account)."""
    if platform == "twitch":
        rng = "24hr" if hours <= 24 else "7d" if hours <= 168 else "30d"
        url = f"https://www.twitch.tv/{cid}/clips?filter=clips&range={rng}"
    else:
        rng = "day" if hours <= 24 else "week" if hours <= 168 else "month"
        url = f"https://kick.com/{cid}/clips?sort=view&range={rng}"
    r = run(ytdlp_base() + ["--flat-playlist", "-J", "--playlist-end", "20", url], capture=True, check=False)
    if r.returncode != 0 or not r.stdout.strip():
        return None  # the platform did not answer
    out = []
    for e in json.loads(r.stdout).get("entries") or []:
        if not e or not e.get("url"):
            continue
        cats = e.get("categories") or []
        if cats and not any(GTA6.search(c) for c in cats):  # Kick tells the game of each clip
            continue
        out.append({"platform": platform, "channel": e.get("channel") or cid, "url": e["url"], "title": e.get("title") or "",
                    "views": e.get("view_count") or 0, "ts": e.get("timestamp"), "duration": e.get("duration") or 0})
    return out


def youtube_recent(handle):
    """Latest lives of a YouTube channel (for moments.py): [{url, title, views}]."""
    r = run(ytdlp_base() + ["--flat-playlist", "-J", "--playlist-end", "3", f"https://www.youtube.com/{handle}/streams"],
            capture=True, check=False)
    if r.returncode != 0 or not r.stdout.strip():
        return []
    return [{"url": e.get("url"), "title": e.get("title") or "", "views": e.get("view_count")}
            for e in json.loads(r.stdout).get("entries") or [] if e and e.get("url")]


def black_spans(vid):
    """[(start, end)] of the black stretches of a video (fades, the screen after "wasted"), from ffmpeg blackdetect."""
    r = run([tool("ffmpeg"), "-hide_banner", "-i", str(vid), "-vf", "blackdetect=d=0.4:pix_th=0.12", "-an", "-f", "null", "-"],
            capture=True, check=False)
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:\s*([\d.]+)\s+black_end:\s*([\d.]+)", r.stderr or "")]


def prepare(clip, lang, max_sec):
    """Download one clip (or take a local file, e.g. a live.py spike) into jobs/<id>/ and write what cut.py reads:
    info, transcript, one candidate."""
    import shutil
    import numpy as np
    import moments
    d = job_dir(clip["url"])
    vid = d / "source.mp4"
    if not vid.exists():
        if Path(clip["url"]).is_file():
            shutil.copyfile(clip["url"], vid)
        else:
            run(ytdlp_base() + ["-f", "b[height<=1080][ext=mp4]/bv*[height<=1080]+ba/b[height<=1080]/b", "--merge-output-format", "mp4",
                                "-o", str(vid), clip["url"]])
    info = {"title": clip.get("title"), "channel": clip.get("channel"), "uploader": clip.get("channel"),
            "webpage_url": clip["url"], "platform": clip.get("platform"), "view_count": clip.get("views"),
            "timestamp": clip.get("ts"), "offset": 0}
    save_json(d / "info.json", info)
    dur = float(ffprobe(vid)["format"]["duration"])
    wav, db = moments.audio_rms(vid, d)
    words = moments.transcribe(wav, d, lang)
    n = len(db)
    # black at the start or the end (fades, the screen after "wasted") is cut away
    black = black_spans(vid)
    lo = next((b for a, b in black if a <= 0.3), 0.0)
    hi = next((min(dur, a + 0.4) for a, b in black if b >= dur - 0.5 and a > dur * 0.5), dur)
    if hi - lo < 5:
        lo, hi = 0.0, dur
    peak = int((lo + hi) / 2)
    if n:  # the payoff: loudness plus the streamer's reactions (laughs, "oddio"), minus the game's own dialogue
        loud = moments.smooth(np.clip(moments.z(db - moments.smooth(db, 30)), 0, None), 3)
        _, react, _, game, _ = moments.word_series(words, n, lang)
        score = (loud + np.clip(moments.smooth(react, 5) * 5, 0, 3) / 3 * 2) * (1 - 0.75 * game)
        score[: int(lo)] = 0; score[int(hi):] = 0
        peak = int(np.argmax(score))
    s0, e0 = lo, hi
    if hi - lo > max_sec:  # keep the build-up before the payoff and a little after it
        s0 = max(lo, min(peak - 0.6 * max_sec, hi - max_sec)); e0 = s0 + max_sec
    text = " ".join(w["w"] for w in words if s0 <= w["s"] < e0)
    views = clip.get("views")
    cand = {"n": 1, "start": round(s0, 2), "end": round(e0, 2), "peak": peak, "vod_time": None, "score": 0,
            "why": [f"clip virale: {views} visualizzazioni" if views else "clip scelta"], "warn": [], "text": text[:400]}
    save_json(d / "candidates.json", {"source": str(vid), "info": info, "duration": dur, "offset": 0, "lang": lang,
                                      "candidates": [cand], "signals": {"heatmap": False, "chat": False, "words": len(words)}})
    (d / "candidates.md").write_text(
        f"# Clip virale: {clip.get('title') or ''}\nfonte: {clip['url']}\nstreamer: {clip.get('channel') or ''}\n\n"
        f"## 1. {s0:.0f}-{e0:.0f} s ({e0 - s0:.0f}s), picco a {peak} s\nperché: {cand['why'][0]}\n> {cand['text']}\n",
        encoding="utf-8")
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="it", help="lingua degli streamer (Twitch), es. it")
    ap.add_argument("--query", default="gta 6 ita", help="ricerca delle live su YouTube e Kick")
    ap.add_argument("--ore", type=float, default=24, help="clip delle ultime N ore")
    ap.add_argument("--top", type=int, default=15); ap.add_argument("--min-views", type=int, default=30)
    ap.add_argument("--canali", default="watchlist.md", help="file con i link dei canali da seguire sempre")
    ap.add_argument("--scarica", type=int, default=0, help="scarica le prime N e prepara i lavori per cut.py")
    ap.add_argument("--prepara", "--scarica-url", dest="prepara",
                    help="prepara per cut.py una clip: un link (Twitch, Kick, YouTube) o un file, come le spike_N.mp4 di live.py")
    ap.add_argument("--streamer", help="con --prepara di un file: il nome dello streamer, per il credito")
    ap.add_argument("--max-sec", type=float, default=50, help="durata massima della clip da montare, in secondi")
    ap.add_argument("--out", default="virali.md")
    a = ap.parse_args()

    if a.prepara:
        if Path(a.prepara).is_file():
            clip = {"platform": "file", "channel": a.streamer, "url": str(Path(a.prepara).resolve()),
                    "title": Path(a.prepara).stem, "views": None, "ts": None}
        else:
            m = ytdlp_json(a.prepara, ["--skip-download"])
            clip = {"platform": (m.get("extractor_key") or "").lower(), "channel": m.get("channel") or m.get("uploader"),
                    "url": a.prepara, "title": m.get("title"), "views": m.get("view_count"), "ts": m.get("timestamp")}
        d = prepare(clip, a.lang, a.max_sec)
        print(f"pronta: {d}\npasso dopo: python cut.py {d} --pick 1 --hook \"...\" --cta \"...\"")
        return

    lives = live_now(a.query, a.lang, 20)
    mem = remember(lives)
    channels = {}
    for r in lives:
        if r["platform"] in ("twitch", "kick"):
            channels[(r["platform"], r["id"])] = r["name"]
    for v in mem.values():
        channels.setdefault((v["platform"], v["id"]), v.get("name") or v["id"])
    yt_handles = []
    for platform, cid in watchlist(a.canali):
        if platform == "youtube":
            yt_handles.append(cid)
        else:
            channels.setdefault((platform, cid), cid)
    print(f"controllo le clip di {len(channels)} canali ({sum(p == 'twitch' for p, _ in channels)} Twitch, "
          f"{sum(p == 'kick' for p, _ in channels)} Kick)...", flush=True)
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda k: (k, clips_of(k[0], k[1], a.ore)), channels))
    failed = sorted({k[0] for k, r in res if r is None})
    now, rows, seen = time.time(), [], set()
    for (platform, cid), clips in res:
        for c in clips or []:
            if c["url"] in seen:
                continue
            seen.add(c["url"])
            age = max(0.5, (now - c["ts"]) / 3600) if c["ts"] else None
            if age is not None and age > a.ore:
                continue
            if c["views"] < a.min_views or (c["duration"] and c["duration"] < 5):
                continue
            c["name"] = channels.get((platform, cid), cid)
            c["age"] = age
            c["vph"] = c["views"] / age if age else 0
            rows.append(c)
    rows.sort(key=lambda c: c["vph"], reverse=True)
    rows = rows[:a.top]

    stamp = time.strftime("%Y-%m-%d %H:%M")
    md = [f"# Clip virali di GTA 6, ultime {a.ore:.0f} ore (lingua {a.lang})", f"Controllato il {stamp} su {len(channels)} canali. "
          "Le visualizzazioni sono quelle di quel momento; l'ordine è per visualizzazioni all'ora.", ""]
    if failed:
        md += [f"Non hanno risposto: {', '.join(failed)}. " + ("Kick vuole curl_cffi: pip install curl_cffi." if "kick" in failed else ""), ""]
    if rows:
        md += ["| # | dove | streamer | titolo | views | ore fa | views/ora | sec | link |", "|---|---|---|---|---|---|---|---|---|"]
        for n, c in enumerate(rows, 1):
            age = f"{c['age']:.1f}" if c["age"] else "?"
            md.append(f"| {n} | {c['platform']} | {c['name']} | {c['title'].replace('|', '/')[:60]} | {c['views']:,} | {age} | "
                      f"{c['vph']:,.0f} | {c['duration']:.0f} | {c['url']} |")
    else:
        md += ["Nessuna clip sopra la soglia. Prova con più ore (--ore 72) o meno visualizzazioni (--min-views 10).", ""]
    yt_live = [r for r in lives if r["platform"] == "youtube"]
    yt_old = [(h, v) for h in yt_handles for v in youtube_recent(h)]
    if yt_live or yt_old:
        md += ["", "## YouTube", "",
               "YouTube non elenca le clip degli spettatori. Le live in corso si catturano con live.py, quelle finite con moments.py "
               "(legge la chat e i punti più rivisti).", ""]
        md += [f"- in live ora: {r['name']} · {r['title'][:60]} · {r['viewers']} spettatori · {r['url']}" for r in yt_live]
        md += [f"- live finita: {h} · {v['title'][:60]} · {v['url']}" for h, v in yt_old]
    Path(a.out).write_text("\n".join(md) + "\n", encoding="utf-8")
    save_json(Path(a.out).with_suffix(".json"), {"time": stamp, "clips": rows, "youtube_live": yt_live})
    for n, c in enumerate(rows, 1):
        print(f"{n:>2} {c['platform']:6} {str(c['name'])[:18]:18} {c['views']:>7} views {c['vph']:>7.0f}/h  {c['title'][:50]}  {c['url']}")
    print(f"scritto {a.out}")

    for c in rows[:a.scarica]:
        d = prepare(c, a.lang, a.max_sec)
        print(f"pronta: {d}")
    if a.scarica:
        print('passo dopo: python cut.py jobs/<id> --pick 1 --hook "..." --cta "..."')


if __name__ == "__main__":
    main()
