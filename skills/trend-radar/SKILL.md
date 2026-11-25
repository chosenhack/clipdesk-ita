---
name: trend-radar
description: Classifica i video recenti su GTA 6 su YouTube per visualizzazioni all'ora, ognuno con il suo tipo (live finita, gameplay, spiegazione), per vedere cosa è di tendenza adesso. Usala quando l'utente chiede cosa va di moda, vuole video fonte freschi, o dice «trova le tendenze» o «cosa è hot». Per le clip dei momenti clou degli streamer la fonte è stream-finder.
---

# Radar delle tendenze

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/trends.py" --query "gta 6 ita" --hours 24 --limit 30`

Per quelli di tutto il mondo, `--query "gta 6"` semplice. Cambia `--query` per altri angoli («gta 6 mappa», il nome di uno streamer) e `--hours` per una finestra più ampia. Con `--solo-live` restano solo le dirette concluse.

Ogni video ha un tipo:

- **live finita**: una diretta conclusa. È la fonte dei momenti clou.
- **gameplay**: walkthrough e partite lunghe. Vanno bene per azione e posti, ma le scene di trama sono spoiler.
- **spiegazione**: notizie, guide, trucchi, trailer, recensioni. Danno clip di informazioni, non momenti: non passarle a `moment-finder` per fare clip di momenti. Servono per i post «come si fa» (`questions-to-posts`) e per i fatti.

Poi:

1. Mostra le prime 10 in una tabella breve: tipo, titolo, canale, visualizzazioni, visualizzazioni all'ora, età, link.
2. Scegli 3 video che si adattano all'angolo di nicchia della pagina. Per le clip dei momenti preferisci «live finita», poi «gameplay». Preferisci creator che permettono la condivisione.
3. Segnala quelli che sembrano fughe di contenuti, «gioca prima» o trucchi per soldi infiniti: scartali e dillo.
4. Proponi il passo successivo per i video scelti: `moment-finder <url> --top 8 --lang it`. Se nella tabella non c'è nessuna live finita, proponi `stream-finder`: gli streamer italiani sono quasi tutti su Twitch.

Se lo script dà errore, mostra l'ultima riga di errore e correggi la causa (yt-dlp mancante, rete). Non inventare un elenco.
