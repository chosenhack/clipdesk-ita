---
name: multilang
description: Trasforma una clip finita in versioni localizzate, di default in italiano, poi spagnolo, portoghese, tedesco, russo e altre, con sottotitoli tradotti parola per parola, gancio tradotto, voce fuori campo opzionale del gancio e didascalie per piattaforma. Usala quando l'utente dice «traduci la clip», «in italiano», «altre lingue», «localizza», «5 lingue».
---

# Multilingua

Le pagine GTA in lingue diverse dall'inglese sono poco servite, quindi una clip può alimentare più pubblici. Il caso principale: prendi una clip da uno streamer inglese grosso e fanne una versione italiana, perché le pagine italiane su GTA 6 sono poche.

Esegui dopo `clip-cutter` (la clip deve già esistere come `jobs/<id>/edits/clip_<n>.mp4` + `.json`):

`python "${CLAUDE_PLUGIN_ROOT}/scripts/translate.py" jobs/<id> --pick <n> --langs it [--voice]`

Altre lingue: `--langs it,es,pt,de,ru`.

Output in `jobs/<id>/edits/`: un `clip_<n>_<lang>.mp4` per lingua e un solo `clip_<n>_captions.md` con le didascalie per X, Instagram e TikTok/Shorts in ogni lingua.

- Layout, box del gancio e volume restano uguali al taglio originale. Se serve, sovrascrivi con `--layout` e `--hook`.
- `--voice` aggiunge una voce sintetica standard (edge-tts: it-IT-DiegoNeural per l'italiano, es-ES-AlvaroNeural, pt-BR-AntonioNeural, de-DE-ConradNeural, ru-RU-DmitryNeural e altre) che legge solo il gancio tradotto, nei primi 2,5 secondi, con l'audio originale abbassato sotto.
- Mai clonare o imitare la voce di una persona o di uno streamer reale. Solo voci standard, e non far passare la voce fuori campo come se parlasse il creatore.

Regole:

2. Traduci i fatti, non inventarli. Non aggiungere affermazioni, date, prezzi o nomi che non sono nella clip originale o nel gancio. La traduzione automatica può sbagliare: leggi didascalie e gancio di ogni lingua prima che l'utente pubblichi, e correggi le righe sbagliate o strane (chiedi all'utente se non conosce la lingua).
3. Fai passare ogni versione linguistica da `rule-check`, come l'originale.
4. Pubblica le versioni localizzate su pagine o account separati, oppure come caricamenti multilingua dove la piattaforma lo supporta (per esempio tracce audio multiple e titoli tradotti su YouTube). Non intasare la stessa pagina con cinque versioni della stessa clip.
5. Didascalie: su X niente hashtag; su Instagram da 3 a 5 hashtag; su TikTok e Shorts brevi più qualche hashtag.
6. Non caricare niente. Mostra file e didascalie all'utente e aspetta il «sì».
