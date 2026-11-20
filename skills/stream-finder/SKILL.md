---
name: stream-finder
description: Trova le live YouTube su GTA 6 ordinate per spettatori contemporanei. Usala quando l'utente chiede chi sta trasmettendo ora, vuole momenti in diretta da tagliare, dice «trova le live» o «chi streamma adesso», o prima di live-mode.
---

# Ricerca live

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/streams.py" --query "gta 6"`

Per trovare streamer italiani esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/streams.py" --query "gta 6 ita" --lang it`

Su Twitch il filtro segue la lingua dello streamer; su YouTube basta la query italiana. Senza `--lang` elenca le dirette in tutte le lingue.

Poi:

1. Mostra le prime 10 live: canale, titolo, spettatori contemporanei, link.
2. Salta le dirette che sono chiaramente fughe di contenuti, trucchi di accesso anticipato («gioca prima») o copie pirata. Dillo in una riga.
3. Consiglia da 1 a 3 dirette. Preferisci canali ufficiali e creator che permettono la condivisione.
4. Proponi il passo successivo: `live-mode <url> --minutes 60` per registrare e tagliare i picchi di chat, oppure `moment-finder` su un VOD finito.

I numeri di spettatori sono quelli che lo script restituisce in quel momento. Non indovinare né arrotondare per eccesso.
