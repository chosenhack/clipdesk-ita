---
name: stream-finder
description: Trova chi è in live su GTA 6 adesso, su Twitch e YouTube, ordinato per spettatori, e le loro live finite da cui tagliare i momenti clou. Usala quando l'utente chiede chi sta trasmettendo ora, vuole clip delle live o dei momenti clou, dice «trova le live» o «chi streamma adesso», o prima di live-mode e moment-finder.
---

# Ricerca live

Per gli streamer italiani esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/streams.py" --query "gta 6 ita" --lang it`

Per tutte le lingue: `--query "gta 6"` senza `--lang`. Su Twitch il filtro segue la lingua dello streamer; su YouTube conta la query. Di YouTube restano solo le dirette con GTA 6 nel titolo: lo script toglie i canali 24/7, i conti alla rovescia e gli altri giochi, che la ricerca di YouTube mette in mezzo.

Gli streamer italiani di GTA 6 sono quasi tutti su Twitch: guarda prima quella tabella.

Poi:

1. Mostra le prime 10 live: canale, titolo, spettatori, da quanto sono in live, link.
2. Salta le dirette che sono chiaramente fughe di contenuti, trucchi di accesso anticipato («gioca prima») o copie pirata. Dillo in una riga.
3. Consiglia da 1 a 3 streamer. Preferisci chi ha una campagna di clip (`campaigns.md`) o permette la condivisione.
4. Proponi il passo successivo, a scelta dell'utente:
   - **Adesso, in diretta**: `live-mode <url> --minutes 60` registra la live e taglia una clip ogni volta che la chat esplode.
   - **Dalla live finita**: prendi l'ultima live finita del canale e passala a `moment-finder`. Su Twitch:
     `python -m yt_dlp --flat-playlist --playlist-end 3 --print "%(url)s | %(title)s | %(duration_string)s" "https://www.twitch.tv/<canale>/videos?filter=archives&sort=time"`

Per le clip che gli spettatori di questi streamer hanno già reso virali, usa `viral-clips`: parte da questa stessa lista.

Non passare a `moment-finder` una diretta ancora in corso: lavora solo su video finiti.

I numeri di spettatori sono quelli che lo script restituisce in quel momento. Non indovinare né arrotondare per eccesso.
