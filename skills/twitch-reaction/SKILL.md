---
name: twitch-reaction
description: Guarda lo streamer Twitch di GTA 6 più seguito e fai clip di reazione, con volto in alto, gioco sotto e titolo grande. Usala quando l'utente vuole clip di reazione di streamer, clip «faccia in alto», clip Twitch, o chiede chi sta trasmettendo GTA 6 adesso.
---

# Clip di reazione Twitch

Volto in alto, gioco sotto, un titolo grande sulla linea di giunzione. È il formato della maggior parte delle clip virali di streamer su GTA 6.

## 1. Trova lo streamer (non serve un account o una chiave Twitch)

`python "${CLAUDE_PLUGIN_ROOT}/scripts/streams.py" --query "gta 6"` elenca le prime live di Grand Theft Auto VI su Twitch e YouTube, ordinate per spettatori. Scegli uno streamer che ha una campagna di clip (controlla `campaigns.md`), oppure uno le cui clip puoi pubblicare con il permesso.

## 2. Ottieni il momento

- In diretta: `python "${CLAUDE_PLUGIN_ROOT}/scripts/live.py" https://twitch.tv/<login> --minutes 60` registra la live, legge la chat di Twitch in forma anonima e taglia una clip ogni volta che la chat esplode.
- A posteriori: `python "${CLAUDE_PLUGIN_ROOT}/scripts/moments.py" <twitch VOD or clip URL> --top 8` assegna un punteggio al VOD e scrive `candidates.md`.

## 3. Taglia la clip di reazione

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/cut.py" jobs/<id> --pick 1 --layout react --cam auto \
  --title "Speed HA CAPITO perché GTA 6 ci ha messo 13 ANNI" --title-style box --captions bubble
```

- `--cam auto` trova da solo la webcam dello streamer (riconoscimento del volto più il riquadro della webcam intorno). Stampa dove l'ha trovata. Se non trova un volto stabile, passa al layout sfocato e lo dice. Controlla una volta il primo fotogramma; se il ritaglio è sbagliato, passa le frazioni `--cam x:y:w:h`.
- `--title-style box`: banda bianca con testo nero in grassetto sulla giunzione. `--title-style outline`: testo bianco con contorno nero spesso sopra la parte alta del gioco, per titoli brevi («Scontri con la polizia in GTA 6»).
- `--captions bubble`: fumetto bianco («Oddio!»). `word`: sottotitoli parola per parola. `none`: solo il titolo.
- Scrivi il titolo con `hook-writer` (sezione dei titoli di reazione).

## Regole

- Clip uno streamer solo dentro la sua campagna o con il suo permesso. Accreditalo nella didascalia del post, non sul video.
- I titoli descrivono quello che è successo. Mai inventare una citazione o un'opinione.
- Fai passare `rule-check` prima di pubblicare. Niente spoiler nel titolo durante la settimana di lancio.
