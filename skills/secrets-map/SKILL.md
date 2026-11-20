---
name: secrets-map
description: Costruisci e pubblica una mappa verificata di luoghi nascosti, auto rare, collezionabili, punti soldi ed easter egg di GTA 6 trovati dai creator. Usala quando l'utente vuole segreti, luoghi nascosti, easter egg o post sempre validi tipo «nascosto a Leonida», o dice «scansiona un video per i segreti».
---

# Mappa dei segreti

Le voci stanno in `secrets.csv` (id, category, name, where, how, source_channel, source_url_with_timestamp, found_on, status, verified_by, notes). Categorie: place, money, car, collectible, easter_egg, other. Stato: unverified, verified, wrong.

## Comandi

Esegui dalla cartella del progetto con `.venv\Scripts\python scripts\secrets_map.py ...` (`--csv path` prima del sottocomando per usare un altro file).

- `scan jobs/<id>`: legge `transcript.json` e `info.json`, trova le menzioni di segreti (in italiano: nascosto, segreto, soldi, contanti, bottino, collezionabile, auto rara, posizione, sblocca; in inglese: hidden, secret, easter egg, money, cash, stash, collectible, rare car, location, spawn, unlock) e le aggiunge come `unverified` con una citazione e un link `?t=` alla fonte. I duplicati vengono saltati. Le menzioni di exploit vengono saltate e stampate.
- `add --name N --where W --how H --category place --channel C --url U`: inserimento manuale.
- `verify <id> --by "<who/how>"`: solo dopo aver controllato il posto nel gioco (o confermato da materiale ufficiale). Servono where, how e source_channel compilati.
- `wrong <id>`: il suggerimento non ha retto alla verifica.
- `posts --out secrets-posts.md`: bozze di suggerimento HOW TO e Spotlight per ogni voce verificata, più la traccia di un carosello «5 luoghi nascosti a Leonida» quando le voci verificate sono 3 o più.
- `map --out secrets.md`: tabella raggruppata per categoria.

## Flusso

1. Fai `scan` su un video trascritto. Apri ogni link `?t=`, leggi la citazione e riscrivi nome, where e how automatici in `secrets.csv` come un vero suggerimento.
2. Controllalo nel gioco. Poi `verify` o `wrong`.
3. `posts`, poi `rule-check` sulle bozze prima che escano.

## Regole

1. Pubblica solo le voci verificate. Una voce non verificata è una pista, non un fatto.
2. Accredita chi ha trovato il segreto in ogni post (`🎥 canale` più il link con il tempo). Mai presentare la scoperta di un creator come nostra.
3. Niente glitch, exploit, glitch dei soldi, duplicazioni, fughe di contenuti o «gioca prima». Lo script li rifiuta; non aggirarlo.
4. L'output di `scan` è un'ipotesi dalla trascrizione. Riscrivi a mano nome, where e how; non pubblicare la citazione grezza.
5. Niente spoiler sui momenti di trama nella settimana di lancio. Non far pensare che la pagina sia di Rockstar. Usa «GTA 6». I post su X non hanno hashtag.
