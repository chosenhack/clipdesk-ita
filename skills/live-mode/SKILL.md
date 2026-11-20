---
name: live-mode
description: Registra una live YouTube con la sua chat e i picchi di chat in quasi tempo reale. Usala quando l'utente dà il link di una live, dice «modalità live» o vuole clip da un evento in diretta mentre succede.
---

# Modalità live

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/live.py" <youtube-live-url> --minutes 60`

Registra la diretta a blocchi, con la chat, e taglia intorno ai picchi di chat: 15 secondi prima e 20 secondi dopo ogni picco.

Prima di iniziare:

1. Verifica che la diretta sia pubblica e non sia una fuga di contenuti, una copia pirata o contenuti «gioca prima». Se hai dubbi, non avviare.
2. Annota il nome utente (@) dello streamer per il credito.

Mentre gira:

1. Controlla le nuove clip in `jobs/` ogni pochi minuti. Rivedi ciascuna: scegli la migliore, salta spoiler e nudità.
2. Per ogni clip da tenere, usa `hook-writer`, poi `clip-cutter` (oppure il taglio automatico se lo script ne ha prodotto uno), poi `rule-check`.
3. Manda all'utente un unico messaggio con le 1-3 clip migliori (didascalia, credito, percorso del file). L'utente dice «sì» e pubblica. La velocità conta, quindi tieni tutto in un solo messaggio.

A fine lavoro: elenca cosa è stato registrato e cosa è stato tagliato, poi registra i post con `learning-loop`. Chiedi il permesso allo streamer quando è raggiungibile.
