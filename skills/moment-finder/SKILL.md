---
name: moment-finder
description: Trova i momenti migliori per le clip in un video lungo, VOD di una live o file locale. Usala quando l'utente dà un link YouTube o un file video e vuole gli highlight, «trova i momenti» o candidati da tagliare.
---

# Ricerca momenti

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/moments.py" <url-or-file> --top 8`

Se il video è in italiano, aggiungi `--lang it`: la trascrizione viene meglio sulle live rumorose.

Scrive `jobs/<id>/candidates.md`. Segnali usati: trascrizione con i tempi parola per parola (faster-whisper), picchi di volume, la mappa di calore «più rivisto» di YouTube e i picchi della chat in diretta, quando disponibili. Un segnale mancante viene saltato, non inventato.

Poi:

1. Leggi `jobs/<id>/candidates.md` e mostra ogni candidato: numero, inizio-fine, durata, perché ha preso punteggio, riga della trascrizione. Le motivazioni in candidates.md sono in italiano: «picco di volume», «parole d'entusiasmo», «più rivisto», «la chat esplode», «energia generale».
2. Scarta gli spoiler sui momenti di trama nella settimana di lancio, la nudità e tutto ciò che sembra una fuga di contenuti.
3. Consiglia i 3 migliori e indica quale angolo di gancio suggerisce ognuno.
4. Passo successivo: `clip-cutter` con `--pick <n>`.

Annota link della fonte e creatore nelle note di `media/raw`. Accredita il creatore nella didascalia del post.
