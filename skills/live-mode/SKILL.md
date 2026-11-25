---
name: live-mode
description: Registra una live di Twitch o YouTube con la sua chat e taglia una clip ogni volta che la chat esplode, in quasi tempo reale. Usala quando l'utente dà il link di una live in corso, dice «modalità live», «cattura la live» o vuole clip di un momento mentre succede, prima che qualcuno lo clippi.
---

# Modalità live

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/live.py" <link della live> --minutes 60`

Funziona con Twitch (`https://twitch.tv/<canale>`, la chat si legge senza account) e con YouTube. Registra la diretta a blocchi, con la chat, e taglia intorno ai picchi di chat: 15 secondi prima e 20 secondi dopo ogni picco. Le clip sono in `jobs/<id>/live/spike_N.mp4`, l'elenco in `spikes.md`. Su Kick la chat non si legge: lì usa `viral-clips`.

Prima di iniziare:

1. Verifica che la diretta sia pubblica e non sia una fuga di contenuti, una copia pirata o contenuti «gioca prima». Se hai dubbi, non avviare.
2. Annota il nome dello streamer per il credito.

Mentre gira:

1. Controlla le nuove clip in `spikes.md` ogni pochi minuti. Rivedi ciascuna: scegli la migliore, salta spoiler e nudità.
2. Per ogni clip da tenere: `python "${CLAUDE_PLUGIN_ROOT}/scripts/viral.py" --prepara jobs/<id>/live/spike_N.mp4 --streamer <nome>` la prepara (trascrizione e momento clou). Poi `hook-writer` per gancio e CTA, poi `clip-cutter` con `--hook` e `--cta` per intro, clip e chiusura, poi `rule-check`.
3. Manda all'utente un unico messaggio con le 1-3 clip migliori (didascalia, credito, percorso del file). L'utente dice «sì» e pubblica. La velocità conta, quindi tieni tutto in un solo messaggio.

A fine lavoro: elenca cosa è stato registrato e cosa è stato tagliato, poi registra i post con `learning-loop`. Chiedi il permesso allo streamer quando è raggiungibile.
