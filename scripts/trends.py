"""Trend radar: recent GTA 6 videos on YouTube ranked by views per hour.

Each video gets a kind: "live finita" (a past live stream: the source of stream highlights), "gameplay"
(walkthroughs, long play sessions) or "spiegazione" (news, guides, tips, trailers: they make clips of information,
not highlights). --solo-live keeps only past live streams.

usage: python trends.py [--query "gta 6"] [--hours 24] [--limit 30] [--solo-live] [--out trends.md]
"""
import argparse, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ytdlp_json

UPLOAD_DATE_SORT = "&sp=CAI%253D"  # YouTube search sorted by upload date
EXPLAINS = re.compile(r"\b(come|guida|tutorial|trucc\w*|segret\w*|news|notizi\w*|cose che|tutto quello|recensione|review|analisi"
                      r"|spiegat\w*|glitch|soldi infiniti|dove trovare|consigl\w*|leak\w*|trailer|reaction|reazione|how to|explained)\b", re.I)
PLAYS = re.compile(r"\b(gameplay|walkthrough|playthrough|live|diretta|stream|no commentary|parte \d+|part \d+|ep\.? ?\d+|episodio)\b", re.I)


def kind(i):
    if i.get("was_live") or i.get("live_status") == "was_live":
        return "live finita"
    t = i.get("title") or ""
    if EXPLAINS.search(t):
        return "spiegazione"
    if PLAYS.search(t):
        return "gameplay"
    return "video"


def detail(url):
    try:
        return ytdlp_json(url, ["--skip-download"])
    except SystemExit:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="gta 6"); ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--limit", type=int, default=30); ap.add_argument("--out", default="trends.md")
    ap.add_argument("--solo-live", action="store_true", help="solo le live finite: la fonte dei momenti clou degli streamer")
    a = ap.parse_args()
    q = a.query.replace(" ", "+")
    flat = ytdlp_json(f"https://www.youtube.com/results?search_query={q}{UPLOAD_DATE_SORT}",
                      ["--flat-playlist", "--playlist-end", str(a.limit)])
    urls = [e["url"] for e in flat.get("entries", []) if e.get("url") and "/shorts/" not in e["url"]]
    with ThreadPoolExecutor(6) as ex:
        infos = [i for i in ex.map(detail, urls) if i]
    now = time.time(); rows = []
    for i in infos:
        t = i.get("timestamp") or i.get("release_timestamp")
        if not t or i.get("is_live"):
            continue
        age = max(0.25, (now - t) / 3600)
        if age > a.hours:
            continue
        k = kind(i)
        if a.solo_live and k != "live finita":
            continue
        v = i.get("view_count") or 0
        rows.append((v / age, v, age, i.get("duration") or 0, i.get("channel") or "", i.get("title") or "", i.get("webpage_url"),
                     bool(i.get("heatmap")), k))
    rows.sort(reverse=True)
    md = [f"# Trend radar: \"{a.query}\", last {a.hours:.0f} h ({time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())})", "",
          "Per i momenti clou degli streamer prendi una \"live finita\". Le \"spiegazione\" (notizie, guide, trucchi) danno "
          "clip di informazioni, non momenti.", "",
          "| # | tipo | views/h | views | age h | min | channel | title | most replayed |", "|---|---|---|---|---|---|---|---|---|"]
    for n, r in enumerate(rows, 1):
        md.append(f"| {n} | {r[8]} | {r[0]:,.0f} | {r[1]:,} | {r[2]:.1f} | {r[3] / 60:.0f} | {r[4]} | [{r[5][:70]}]({r[6]}) | "
                  f"{'yes' if r[7] else ''} |")
    Path(a.out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:16]))
    print(f"... {len(rows)} videos -> {a.out}")


if __name__ == "__main__":
    main()
