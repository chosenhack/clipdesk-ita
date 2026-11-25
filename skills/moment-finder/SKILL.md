---
name: moment-finder
description: Trova i momenti clou per le clip nella live finita (VOD) di uno streamer, in un video lungo o in un file locale. Usala quando l'utente dà un link di una live finita, di Twitch o YouTube, o un file video e vuole gli highlight, «trova i momenti», «i momenti clou» o candidati da tagliare.
---

# Ricerca momenti

## La fonte giusta

I momenti clou nascono dalle live: lo streamer che reagisce, l'azione, la chat che esplode. Usa la live finita (VOD) di uno streamer: su Twitch `https://www.twitch.tv/videos/<id>`, su YouTube una diretta conclusa. Non usare video di notizie, guide, trucchi o trailer: danno clip di informazioni, non momenti. Se l'utente non ha un link, prima `stream-finder`.

Le ultime live finite di un canale Twitch:

`python -m yt_dlp --flat-playlist --playlist-end 3 --print "%(url)s | %(title)s | %(duration_string)s" "https://www.twitch.tv/<canale>/videos?filter=archives&sort=time"`

Una diretta ancora in corso non va qui: lo script la rifiuta. Usa `live-mode`.

## Esegui

`python "${CLAUDE_PLUGIN_ROOT}/scripts/moments.py" <url-or-file> --top 8 --lang it`

- `--lang it` è la lingua dello streamer: serve a riconoscere le scene del gioco, che è in inglese. La trascrizione riconosce la lingua a ogni tratto, così i dialoghi del gioco restano in inglese, anche nei sottotitoli.
- Di un link analizza 90 minuti (`--max-minutes`). Se la live di Twitch inizia con un'altra categoria (Just Chatting), parte da dove inizia GTA 6. Per un'altra parte della live usa `--from <minuto>`: per esempio `--from 120` per la terza ora.
- La chat di una VOD di Twitch non si legge da sola. Se hai il file della chat di TwitchDownloader, passalo con `--chat chat.json`. Su YouTube la chat delle dirette concluse viene letta da sola.

Scrive `jobs/<id>/candidates.md`. Segnali: picchi di volume, reazioni dello streamer nella trascrizione («non ci credo», «oddio», «mamma mia», risate), la mappa di calore «più rivisto» di YouTube e i picchi della chat, quando ci sono. Un segnale mancante viene saltato, non inventato. Vengono abbassati due tipi di tratto: le scene del gioco con i dialoghi in inglese (spesso trama, quindi spoiler) e lo streamer che parla al pubblico (saluti, annunci, giveaway, sponsor, spiegazioni).

## Poi

1. Leggi `jobs/<id>/candidates.md` e mostra ogni candidato: numero, inizio-fine, durata, minuto nella live, perché ha preso punteggio, riga della trascrizione. Le motivazioni sono «picco di volume», «reazione», «parole d'entusiasmo», «più rivisto», «la chat esplode», «energia generale».
2. Scarta i candidati con la riga «attenzione»: dialoghi del gioco (probabile scena di trama) o parlato al pubblico. Tienili solo se non c'è altro, e dillo.
3. Se in testa c'è «pochi segnali», i momenti vengono solo dal volume e possono essere menu o mappa: guarda un fotogramma di ognuno prima di consigliarlo.
4. Scarta gli spoiler di trama nella settimana di lancio, la nudità e tutto ciò che sembra una fuga di contenuti.
5. Consiglia i 3 migliori e indica quale angolo di gancio suggerisce ognuno.
6. Passo successivo: `clip-cutter` con `--pick <n>`.

Annota link della fonte e creatore nelle note di `media/raw`. Accredita il creatore nella didascalia del post.
