---
name: trend-radar
description: Classifica i video recenti su GTA 6 per visualizzazioni all'ora, per vedere cosa è di tendenza adesso. Usala quando l'utente chiede cosa va di moda, cosa tagliare oggi o vuole video fonte freschi, o dice «trova le tendenze» o «cosa è hot».
---

# Radar delle tendenze

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/trends.py" --query "gta 6" --hours 24 --limit 30`

Per i video italiani usa `--query "gta 6 ita"`; per quelli di tutto il mondo, `--query "gta 6"` semplice.

Cambia `--query` per altri angoli («gta 6 mappa», «gta 6 trailer», il nome di uno streamer). Cambia `--hours` per una finestra più ampia.

Poi:

1. Mostra le prime 10 in una tabella breve: titolo, canale, visualizzazioni, visualizzazioni all'ora, età, link.
2. Scegli 3 video che si adattano all'angolo di nicchia della pagina. Preferisci fonti ufficiali e creator che permettono la condivisione.
3. Segnala quelli che sembrano fughe di contenuti o «gioca prima»: scartali e dillo.
4. Proponi il passo successivo per i video scelti: `moment-finder <url> --top 8`.

Se lo script dà errore, mostra l'ultima riga di errore e correggi la causa (yt-dlp mancante, rete). Non inventare un elenco.
