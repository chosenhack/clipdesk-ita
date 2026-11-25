---
name: viral-clips
description: Trova le clip virali degli streamer italiani che giocano a GTA 6 in live (Twitch, YouTube, Kick), scarica le migliori e le monta nel formato intro col gancio, clip, CTA. Usala quando l'utente vuole le clip virali, «le clip migliori di oggi», «cosa è esploso nelle live», «fammi le clip», o il giro completo dalle live alla clip pronta da pubblicare.
---

# Clip virali delle live

Il giro completo: chi è in live su GTA 6, le clip più viste dei loro spettatori, il montaggio. Ogni clip esce con la stessa struttura:

1. **Intro (2 s)**: il momento clou in anteprima, con il gancio grande a video.
2. **Clip**: il momento, con i sottotitoli di quello che dice lo streamer (il gioco parla inglese e ha già i suoi sottotitoli).
3. **CTA (2,5 s)**: l'ultimo fotogramma sfocato, con la chiamata all'azione.

## 1. Trova le clip virali

`python "${CLAUDE_PLUGIN_ROOT}/scripts/viral.py" --lang it --ore 24 --top 15`

Guarda gli streamer italiani in live su GTA 6 adesso (Twitch, YouTube, Kick quando risponde), quelli visti in live negli ultimi 7 giorni (li ricorda in `streamer-gta6.json`) e i canali di `watchlist.md`. Per ognuno legge le clip che hanno tagliato i suoi spettatori, con le visualizzazioni, e le ordina per visualizzazioni all'ora. Scrive `virali.md`.

- Poche clip? `--ore 72` o `--min-views 10`.
- Kick vuole `curl_cffi` (lo installa `setup`). Se Kick non risponde, lo script lo dice e va avanti.
- YouTube non elenca le clip degli spettatori: lo script elenca le live italiane in corso. Per quelle usa il passo «In diretta» qui sotto, o `moment-finder` quando sono finite.

Mostra le prime 10: streamer, titolo, visualizzazioni, ore fa, link. Scarta fughe di contenuti, «gioca prima», trucchi per soldi infiniti, nudità. Consiglia le 3 migliori.

## 2. Scarica e prepara

`python "${CLAUDE_PLUGIN_ROOT}/scripts/viral.py" --scarica 3` scarica le prime 3 in `jobs/` e le prepara per il montaggio: trascrizione, punto clou, al massimo 50 secondi intorno al momento clou, senza il nero iniziale o finale. Per una clip scelta da te: `--prepara <link>`.

Leggi `jobs/<id>/candidates.md` e guarda un fotogramma: deve essere GTA 6. Se la clip è lunga, stringila con `--start`/`--end` al passo 3.

## 3. Gancio e CTA

Chiedi a `hook-writer` 3 ganci (da 3 a 8 parole, curiosità, niente spoiler) e 3 CTA per ogni clip. Usa i migliori. La CTA è un'azione precisa: una domanda da commentare o «mandalo a chi…», mai solo «seguimi».

## 4. Monta

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/cut.py" jobs/<id> --pick 1 --layout react --cam auto \
  --hook "Ha rubato un aereo, guarda il decollo" --cta "Commenta: tu saresti decollato?"
```

- `--layout react`: volto dello streamer sopra, gioco sotto. È il formato delle clip di streamer. Trova da solo la webcam; se non c'è, passa al layout sfocato e lo dice. Senza webcam usa `--layout blur`.
- `--intro-secs` (2 di base) e `--cta-secs` (2,5) cambiano la durata di intro e chiusura.
- Esce `jobs/<id>/edits/clip_1.mp4`.

Guarda 3 fotogrammi: l'intro (0,5 s), la metà, la CTA (l'ultimo secondo). Il gancio deve essere leggibile e non coprire il volto.

## 5. Controlla e consegna

`python "${CLAUDE_PLUGIN_ROOT}/scripts/check.py" jobs/<id>/edits/clip_1.mp4 --campaign campaigns.md --caption "<didascalia>"`

Controlla anche che ci siano intro col gancio e CTA. Se qualcosa fallisce, correggi e rimonta.

Poi manda all'utente in un messaggio solo, per ogni clip: il file, la didascalia con il credito («🎥 @streamer su Twitch») e il link della clip originale. Aspetta il «sì». Non pubblicare niente da solo.

## In diretta

Per catturare un momento mentre succede, prima che qualcuno lo clippi: `live-mode` su una live di Twitch o YouTube registra e taglia ogni volta che la chat esplode. Ogni `spike_N.mp4` si prepara con `viral.py --prepara jobs/<id>/live/spike_N.mp4 --streamer <nome>` e si monta come al passo 4.

## Regole

- Clippa uno streamer solo dentro una sua campagna o con il suo permesso. Il credito va nella didascalia, non nel video.
- I ganci descrivono quello che succede: niente citazioni inventate, niente spoiler di trama.
- Una clip ripubblicata così com'è non cresce: intro, sottotitoli e CTA la rendono tua.
