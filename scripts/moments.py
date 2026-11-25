"""Find the best clip moments in a video or VOD: the highlights, not the explanations.

Signals per second: loudness bursts, the streamer's reactions in the transcript ("non ci credo", "oddio", laughter),
YouTube's "most replayed" heatmap and live-chat spikes (YouTube VOD chat replay or a TwitchDownloader chat.json).
Two kinds of stretch are scored down, because they turn into clips of information instead of highlights:
- the game's own scenes: English dialogue in an Italian stream (GTA 6 is voiced in English), often story spoilers;
- talking to the audience: greetings, announcements, giveaways, sponsors, "vi spiego".
Live streams still running are refused (use live.py). A Twitch VOD that opens on another category (Just Chatting)
starts where GTA 6 starts; --from picks another starting minute.
Writes jobs/<id>/candidates.md + candidates.json.

usage: python moments.py <url-or-file> [--top 8] [--min 15] [--max 40] [--chat chat.json] [--from MIN] [--max-minutes 90] [--lang it]
"""
import argparse, bisect, json, math, re, sys, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from common import ffprobe, is_url, job_dir, join_elisions, load_json, run, save_json, tool, ytdlp_base, ytdlp_json

# Reactions: exclamations, swearing, laughter. A reaction on a loudness burst is the typical highlight.
REACT_IT = re.compile(r"\b(oddio|madonna|mamma mia|no vabb[eè]|non ci credo|ma sei serio|ma stai scherzando|assurd[oaie]"
                      r"|pazzesc[oa]|pazzesch[ie]|incredibile|godo|daje|evvai|porc[oa] \w+|cazzo|minchia|aiuto|che botta"
                      r"|oh no|no no no|noo+|s[iì]{3,}|(?:ah){2,}h?|(?:ha){2,}h?)\b", re.I)
REACT_EN = re.compile(r"\b(no way|oh my god|omg|holy \w+|insane|crazy|let'?s go|wtf|what the \w+|dude|bro|lmao|(?:ha){2,}h?)\b", re.I)
# Said while explaining ("raga, guardate...") or by the game's characters: they count little.
WEAK_IT = re.compile(r"\b(raga|ragazzi|guardate|aspetta|corri|scappa|vai vai|dai dai|andiamo|ma che|ma cosa)\b", re.I)
WEAK_EN = re.compile(r"\b(what|wait|look at|run|go go|nah|yo+)\b", re.I)
# Talking to the audience: greetings, announcements, giveaways, sponsors, explanations. Information, not highlights.
INFO = re.compile(r"\b(a proposito|vi ricordate|potete vincere|in palio|giveaway|sorteggi\w*|link (?:in|nella|nel) (?:descrizione|bio|chat)"
                  r"|iscriv\w+|seguitemi|codice (?:sconto|creator)|sponsor\w*|instant ?gaming|prime gaming|abbonat\w+|abbonament\w+"
                  r"|donazion\w+|discord|telegram|nel prossimo video|lasciate un like|mi raccomando|vi spiego|vi faccio vedere"
                  r"|vi lascio|vi mostro|bentornati|benvenuti|ciao a tutti|ciao ragazzi|oggi facciamo|la live di oggi"
                  r"|il video di oggi|per chi non lo sapesse|subscribe|use code|link in (?:the )?description)\b", re.I)
# Function words tell which language a stretch is in. In an Italian stream, English speech is the game talking.
EN_WORDS = set("the you your you're i'm i'll it's to and is are was were we what that this my of on for have has get got know just "
               "like gonna wanna right here there he she they him her them be been can can't not yeah with at but if going want "
               "need let's don't did does".split())
IT_WORDS = set("il lo la gli le un una uno di da con su per che chi non si mi ti ci vi è e ho hai ha abbiamo sono sei siamo "
               "questo questa quello quella del della dei delle nel nella al alla ma poi perché però anche già qui qua lì là ora "
               "adesso cioè tipo allora comunque dove come cosa quando più niente tutto fare devo".split())
GTA6 = re.compile(r"grand\s*theft\s*auto\s*(?:vi|6)\b|\bgta\s*(?:vi|6)\b", re.I)
CHAT_HYPE = re.compile(r"(LMAO|LOL|KEKW|OMEGALUL|W+\b|CLIP|💀|😂|🔥|NO WAY|HOLY"
                       r"|AH(?:AH)+|\bXD+\b|ASSURD|PAZZESC|MADONNA|DAJE|GODO|NOO+\b)", re.I)


def probe(src):
    """yt-dlp metadata of a URL ({} for a local file). Refuses live streams that are still running."""
    if not is_url(src):
        return {}
    info = ytdlp_json(src)
    if info.get("is_live") or info.get("live_status") in ("is_live", "is_upcoming"):
        sys.exit("È una diretta ancora in corso: moments.py lavora su video finiti.\n"
                 f"- Per tagliare i momenti mentre succedono: python live.py {src} --minutes 60\n"
                 "- Per i momenti a posteriori aspetta la live finita (su Twitch: twitch.tv/<canale>/videos?filter=archives).")
    return info


def section_start(info, start_min):
    """Second of the VOD where the analysis starts: --from if given, else where GTA 6 starts in a Twitch VOD
    that opens on another category (Just Chatting); 0 otherwise."""
    if start_min is not None:
        return max(0.0, start_min * 60)
    ch = [c for c in (info.get("chapters") or []) if c.get("start_time") is not None]
    if ch and not GTA6.search(ch[0].get("title") or ""):
        for c in ch[1:]:
            if GTA6.search(c.get("title") or ""):
                print(f"la live inizia con {ch[0].get('title') or 'altro'}: parto dal minuto {c['start_time'] / 60:.0f}, "
                      f"dove inizia {c['title']}")
                return float(c["start_time"])
    return 0.0


def fetch(src, d, info, start, length):
    """The part of the video to analyse, from `start` (s) for `length` (s, None = to the end)."""
    if is_url(src):
        save_json(d / "info.json", {**{k: info.get(k) for k in ("id", "title", "uploader", "channel", "uploader_id", "webpage_url",
                                                                 "duration", "view_count", "upload_date", "heatmap", "is_live",
                                                                 "was_live", "chapters")}, "offset": start})
        vid = d / "source.mp4"
        if not vid.exists():
            args = ytdlp_base() + ["-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]/b", "--merge-output-format", "mp4",
                                   "-o", str(vid)]
            dur = info.get("duration") or 0
            if start > 0 or (length and dur > start + length):
                args += ["--download-sections", f"*{start:.0f}-{start + length if length else dur:.0f}"]
            run(args + [src])
        if info.get("was_live") and not list(d.glob("chat*.live_chat.json")):  # YouTube chat replay
            run(ytdlp_base() + ["--skip-download", "--write-subs", "--sub-langs", "live_chat", "-o", str(d / "chat"), src], check=False)
    else:
        vid = Path(src).resolve()
        save_json(d / "info.json", {"title": vid.stem, "webpage_url": str(vid), "offset": start})
        if start > 0 or length:
            part = d / ("source" + vid.suffix)
            if not part.exists():
                run([tool("ffmpeg"), "-y", "-v", "error", "-ss", f"{start:.2f}", "-i", str(vid)]
                    + (["-t", f"{length:.2f}"] if length else []) + ["-map", "0:v?", "-map", "0:a?", "-c", "copy", str(part)])
            vid = part
    return vid


def audio_rms(vid, d):
    wav = d / "audio.wav"
    if not wav.exists():
        run([tool("ffmpeg"), "-y", "-v", "error", "-i", str(vid), "-ac", "1", "-ar", "16000", str(wav)])
    with wave.open(str(wav)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    n = len(x) // 16000
    rms = np.sqrt((x[: n * 16000].reshape(n, 16000) ** 2).mean(1) + 1e-9)
    return wav, 20 * np.log10(rms)


def transcribe(wav, d, lang=None):
    out = d / "transcript.json"
    if out.exists():
        return load_json(out)
    from faster_whisper import WhisperModel
    try:
        import ctranslate2
        cuda = ctranslate2.get_cuda_device_count() > 0
    except Exception:
        cuda = False
    with wave.open(str(wav)) as w:  # pass samples directly (16 kHz mono), no extra decoder needed
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768

    def run_on(device):
        model = WhisperModel("small", device=device, compute_type="float16" if device == "cuda" else "int8")
        if not lang or lang == "en":
            segs, _ = model.transcribe(pcm, word_timestamps=True, vad_filter=True, language=lang or None)
            return [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in (s.words or [])]
        return two_languages(model, pcm, lang)
    try:
        words = run_on("cuda" if cuda else "cpu")
    except RuntimeError as e:  # GPU present but CUDA libraries missing: fall back to CPU
        print(f"GPU transcription unavailable ({str(e)[:80]}), using CPU")
        words = run_on("cpu")
    words = join_elisions(words)
    save_json(out, words)
    return words


def two_languages(model, pcm, lang, rate=16000):
    """The streamer speaks `lang`, GTA 6 is voiced in English. Each stretch of speech is transcribed in whichever of the
    two Whisper hears, never translated: forced to Italian, Whisper turns the game's dialogue into Italian (the scenes look
    like the streamer talking, captions come out wrong); left free, it hears shouting as Portuguese or German.
    Every word is tagged with its language."""
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    spans = get_speech_timestamps(pcm, VadOptions(min_silence_duration_ms=600, speech_pad_ms=200, max_speech_duration_s=28))
    chunks = []
    for sp in spans:  # join close stretches up to 28 s, so Whisper keeps some context
        if chunks and sp["start"] - chunks[-1][1] < 0.8 * rate and sp["end"] - chunks[-1][0] <= 28 * rate:
            chunks[-1][1] = sp["end"]
        else:
            chunks.append([sp["start"], sp["end"]])
    words = []
    for a, b in chunks:
        part = pcm[a:b]
        if len(part) < 0.3 * rate:
            continue
        _, _, probs = model.detect_language(audio=part)
        p = dict(probs)
        use = "en" if p.get("en", 0) > p.get(lang, 0) else lang
        segs, _ = model.transcribe(part, word_timestamps=True, vad_filter=False, language=use, condition_on_previous_text=False)
        off = a / rate
        words += [{"w": w.word.strip(), "s": round(off + w.start, 2), "e": round(off + w.end, 2), "lang": use}
                  for s in segs for w in (s.words or [])]
    return words


def chat_series(d, n, chat_arg, start=0.0):
    """Messages per second from YouTube live_chat json lines or a TwitchDownloader chat.json, on the analysed part."""
    c = np.zeros(n)
    yt = list(d.glob("chat*.live_chat.json"))
    if yt:
        for line in yt[0].read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                a = json.loads(line)["replayChatItemAction"]
                t = int(a["videoOffsetTimeMsec"]) / 1000 - start
                txt = json.dumps(a["actions"], ensure_ascii=False)
            except Exception:
                continue
            if 0 <= t < n:
                c[int(t)] += 2 if CHAT_HYPE.search(txt) else 1
    elif chat_arg:
        js = load_json(chat_arg)
        for m in js.get("comments", []):
            t = m.get("content_offset_seconds", 0) - start
            body = (m.get("message") or {}).get("body", "")
            if 0 <= t < n:
                c[int(t)] += 2 if CHAT_HYPE.search(body) else 1
    return c


def word_series(words, n, lang=None):
    """Per-second series from the transcript.
    Returns (lang, reactions, strong reactions, game's own dialogue 0-1, talking to the audience 0-1)."""
    toks = [(re.sub(r"[^\w']+", "", w["w"].lower()), w["s"]) for w in words]
    toks = [(t, s) for t, s in toks if t]
    en = sum(t in EN_WORDS for t, _ in toks); it = sum(t in IT_WORDS for t, _ in toks)
    lang = (lang or ("it" if it >= en else "en")).lower()
    if lang == "it":
        rules = ((REACT_IT, 1.0), (WEAK_IT, 0.3), (REACT_EN, 0.3))
    elif lang == "en":
        rules = ((REACT_EN, 1.0), (WEAK_EN, 0.3))
    else:
        rules = ((REACT_IT, 1.0), (REACT_EN, 1.0), (WEAK_IT, 0.3), (WEAK_EN, 0.3))
    # search the whole transcript, so phrases like "mamma mia" or "non ci credo" count too,
    # and credit each match to the second where its first word starts
    text, offs, secs = "", [], []
    for t, s in toks:
        text += " " if text else ""
        offs.append(len(text)); secs.append(s)
        text += t

    def second(m):
        return int(secs[bisect.bisect_right(offs, m.start()) - 1])

    react, strong, info = np.zeros(n), np.zeros(n), np.zeros(n)
    for rx, weight in rules:
        for m in rx.finditer(text):
            t = second(m)
            if 0 <= t < n:
                react[t] += weight
                strong[t] += weight == 1.0
    for m in INFO.finditer(text):
        t = second(m)
        if 0 <= t < n:
            info[t] = 1
    game = np.zeros(n)
    if lang != "en":  # English speech in a non-English stream: the game's cutscenes and characters
        en_s, it_s = np.zeros(n), np.zeros(n)
        tagged = [w for w in words if w.get("lang") and w["w"]]
        if tagged:  # transcribed by two_languages: every word says its language
            for w in tagged:
                if 0 <= int(w["s"]) < n:
                    en_s[int(w["s"])] += w["lang"] == "en"
                    it_s[int(w["s"])] += w["lang"] != "en"
        else:  # older transcript: tell the language from the function words
            for t, s in toks:
                if 0 <= int(s) < n:
                    en_s[int(s)] += t in EN_WORDS
                    it_s[int(s)] += t in IT_WORDS
        e, i = np.convolve(en_s, np.ones(17), "same"), np.convolve(it_s, np.ones(17), "same")
        share = np.where(e + i >= 4, e / np.maximum(e + i, 1), 0)
        game = np.clip((share - 0.5) / 0.3, 0, 1)
    info = np.clip(np.convolve(info, np.ones(21), "same"), 0, 1)
    return lang, react, strong, game, info


def z(a):
    a = np.asarray(a, dtype=float)
    if a.std() < 1e-9:
        return np.zeros_like(a)
    return (a - np.median(a)) / (a.std() + 1e-9)


def smooth(a, k):
    k = max(1, int(k))
    return np.convolve(a, np.ones(k) / k, mode="same")


def hms(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--min", type=float, default=15); ap.add_argument("--max", type=float, default=40)
    ap.add_argument("--chat")
    ap.add_argument("--from", dest="start_min", type=float,
                    help="minuto della live da cui partire (es. 60 per saltare l'inizio); di base salta il Just Chatting di Twitch")
    ap.add_argument("--max-minutes", type=float, help="quanti minuti analizzare: di base 90 per i link, tutto per i file")
    ap.add_argument("--lang", help="lingua dello streamer, es. it: serve a riconoscere le scene del gioco, che è in inglese; "
                                   "vuoto = la riconosce da sola")
    a = ap.parse_args()
    info = probe(a.src)
    start = section_start(info, a.start_min) if is_url(a.src) else max(0.0, (a.start_min or 0) * 60)
    length = a.max_minutes * 60 if a.max_minutes else (90 * 60 if is_url(a.src) else None)
    d = job_dir(a.src if not start else f"{a.src}#t={start:.0f}")
    vid = fetch(a.src, d, info, start, length)
    dur = float(ffprobe(vid)["format"]["duration"])
    wav, db = audio_rms(vid, d)
    n = len(db)
    words = transcribe(wav, d, a.lang)
    # signals
    loud = smooth(np.clip(z(db - smooth(db, 30)), 0, None), 3)          # jumps above the local level
    lang, react, strong, game, info_talk = word_series(words, n, a.lang)
    react_s = np.clip(smooth(react, 5) * 5, 0, 3) / 3 * 2               # reactions within ±2 s, 0..2
    heat = np.zeros(n)
    for h in (info.get("heatmap") or []):
        s, e = h["start_time"] - start, h["end_time"] - start
        if e > 0 and s < n:
            heat[max(0, int(s)):min(n, int(math.ceil(e)))] = h["value"]
    chat = chat_series(d, n, a.chat, start)
    chatz = smooth(np.clip(z(smooth(chat, 10)), 0, None), 3)
    w_heat = 2.0 if heat.any() else 0
    w_chat = 1.5 if chat.any() else 0
    score = 1.0 * loud + react_s + w_heat * z(heat).clip(0) + w_chat * chatz
    score = score * (1 - 0.75 * game) * (1 - 0.6 * info_talk)           # game's scenes, talking to the audience
    # pick non-overlapping windows around peaks: the build-up before, the payoff after
    picks, used = [], np.zeros(n, bool)
    for p in np.argsort(-score):
        if len(picks) >= a.top or score[p] <= 0:
            break
        if used[p]:
            continue
        s0 = max(0.0, p - 0.55 * a.max); e0 = min(dur, s0 + a.max)
        for w in words:  # never cut a word in half at the edges
            if w["s"] < s0 < w["e"]:
                s0 = max(0.0, w["s"] - 0.2)
            if w["s"] < e0 < w["e"]:
                e0 = min(dur, w["e"] + 0.3)
        if e0 - s0 < a.min:
            e0 = min(dur, s0 + a.min)
        span = slice(int(s0), int(math.ceil(e0)))
        if used[span].any():
            continue
        used[span] = True
        text = " ".join(x["w"] for x in words if s0 <= x["s"] < e0)
        near = slice(max(0, p - 3), p + 4)
        why, warn = [], []
        if loud[p] > 1: why.append("picco di volume")
        if strong[near].any(): why.append("reazione")
        elif react[near].any(): why.append("parole d'entusiasmo")
        if heat[p] > 0.5: why.append(f"più rivisto {heat[p]:.2f}")
        if w_chat and chatz[p] > 1: why.append("la chat esplode")
        if game[span].mean() > 0.5: warn.append("dialoghi del gioco in inglese: forse una scena di trama, attento agli spoiler")
        if info_talk[span].mean() > 0.3: warn.append("parla al pubblico (saluti, annunci, spiegazioni)")
        picks.append({"n": len(picks) + 1, "start": round(s0, 2), "end": round(e0, 2), "peak": int(p),
                      "vod_time": round(start + s0, 2), "score": round(float(score[p]), 2),
                      "why": why or ["energia generale"], "warn": warn, "text": text[:400]})
    picks.sort(key=lambda x: x["start"])
    for i, x in enumerate(picks, 1):
        x["n"] = i
    meta = load_json(d / "info.json")
    game_s, info_s = int((game > 0.5).sum()), int((info_talk > 0.5).sum())
    save_json(d / "candidates.json", {"source": str(vid), "info": meta, "duration": dur, "offset": start, "lang": lang,
                                      "candidates": picks,
                                      "signals": {"heatmap": bool(w_heat), "chat": bool(w_chat), "words": len(words),
                                                  "game_dialogue_s": game_s, "audience_talk_s": info_s}})
    fmt = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
    md = [f"# Momenti: {meta.get('title', '')}", f"fonte: {meta.get('webpage_url', '')}",
          f"segnali: volume, reazioni nella trascrizione ({len(words)} parole, lingua {lang})" + (", più rivisti" if w_heat else "")
          + (", chat" if w_chat else ", niente chat"),
          f"abbassati: {game_s // 60} min di scene del gioco in inglese, {info_s // 60} min di parlato al pubblico"]
    if start:
        md.append(f"analizzato dal minuto {start / 60:.0f} della live" + (f" per {length / 60:.0f} minuti" if length else ""))
    if not (w_chat or w_heat) and strong.sum() < 5:
        md.append("pochi segnali: lo streamer reagisce poco e la chat non c'è, quindi i momenti vengono quasi solo dal volume "
                  "(possono essere menu o mappa): guardali prima di tagliare")
    md.append("")
    for x in picks:
        md += [f"## {x['n']}. {fmt(x['start'])}-{fmt(x['end'])} ({x['end'] - x['start']:.0f}s) score {x['score']}"
               + (f" · nella live {hms(x['vod_time'])}" if start else ""),
               f"perché: {', '.join(x['why'])}"] + ([f"attenzione: {'; '.join(x['warn'])}"] if x["warn"] else []) + [f"> {x['text']}", ""]
    (d / "candidates.md").write_text("\n".join(md), encoding="utf-8")
    print(f"lavoro: {d}\n{len(picks)} momenti -> {d / 'candidates.md'}")


if __name__ == "__main__":
    main()
