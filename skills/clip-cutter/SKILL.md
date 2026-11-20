---
name: clip-cutter
description: Taglia un momento scelto in una clip verticale 1080x1920 finita, con sottotitoli parola per parola e un box con il gancio. Usala dopo moment-finder, o quando l'utente dice «tagliala», «fai la clip», «mettila in verticale».
---

# Taglio clip

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/cut.py" jobs/<id> --pick <n> --layout fill|blur|facecam --hook "TEXT"`

- `fill`: ritaglia il video di gioco per riempire il fotogramma. Predefinito per il gameplay.
- `blur`: video intero al centro, sopra una copia sfocata. Usalo quando il ritaglio taglierebbe via l'azione.
- `facecam`: gioco con la webcam dello streamer visibile. Usalo per le reazioni.

I sottotitoli mascherano anche le parolacce italiane, e mascherano sempre gli insulti e le bestemmie italiane (per esempio «porco dio» diventa «p**** d**»). `--allow-profanity` sblocca solo le parolacce comuni.

Prima di eseguire:

1. Chiedi 3 opzioni di gancio alla skill `hook-writer` e usa la migliore.

Dopo l'esecuzione:

1. L'output è un mp4 in `media/edits`. Controlla che sia 1080x1920, che il gancio compaia nei primi 2 secondi e che i sottotitoli siano leggibili. Nel video non va nessun testo di credito; chi pubblica accredita il creatore nel post.
2. Fai passare la clip da `rule-check`. Correggi e ritaglia di nuovo finché non passa.
3. Per la maggior parte delle clip, taglia tra 7 e 30 secondi. Chiudi sul punto più forte.
4. Mostra all'utente il file e il testo della didascalia e chiedi un «sì». Non caricare niente.
