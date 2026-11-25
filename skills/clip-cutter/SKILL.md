---
name: clip-cutter
description: Monta un momento scelto in una clip verticale 1080x1920 finita: intro di 2 secondi con il gancio sul momento clou, la clip con i sottotitoli parola per parola, la CTA in chiusura. Usala dopo moment-finder o viral-clips, o quando l'utente dice «tagliala», «montala», «fai la clip», «mettila in verticale».
---

# Montaggio clip

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/cut.py" jobs/<id> --pick <n> --layout react|blur|fill|facecam --hook "GANCIO" --cta "CTA"`

La clip esce in tre parti:

1. **Intro** (`--intro-secs`, 2 di base): il momento più forte della clip in anteprima, con il gancio grande. Il primo fotogramma è già azione.
2. **Clip**: il momento, con i sottotitoli parola per parola. Quando lo streamer è italiano, i sottotitoli riportano solo lui: i dialoghi del gioco sono in inglese e il gioco ha già i suoi sottotitoli.
3. **CTA** (`--cta-secs`, 2,5 di base): l'ultimo fotogramma sfocato e scurito, con la chiamata all'azione.

Il volume finale è normalizzato a -14 LUFS su tutta la clip. Con `--intro-secs 0` il gancio torna a stare sopra i primi secondi della clip, senza intro.

Layout:

- `react`: volto dello streamer sopra, gioco sotto. Il formato delle clip di streamer. `--cam auto` trova la webcam da solo.
- `blur`: video intero al centro, sopra una copia sfocata. Per il gameplay senza webcam.
- `fill`: ritaglia il gioco per riempire il fotogramma.
- `facecam`: webcam in alto e gioco ritagliato sotto.

I sottotitoli mascherano anche le parolacce italiane, e mascherano sempre gli insulti e le bestemmie italiane (per esempio «porco dio» diventa «p**** d**»). `--allow-profanity` sblocca solo le parolacce comuni.

Prima di eseguire:

1. Chiedi a `hook-writer` 3 ganci e 3 CTA e usa i migliori.
2. Se il momento è lungo, stringilo con `--start` e `--end` (secondi della fonte): tra 7 e 30 secondi per la maggior parte delle clip, chiuso sul punto più forte.

Dopo l'esecuzione:

1. L'output è `jobs/<id>/edits/clip_<n>.mp4`. Guarda un fotogramma dell'intro, uno a metà e uno della CTA: il gancio leggibile e lontano dal volto, i sottotitoli leggibili. Nel video non va nessun testo di credito; chi pubblica accredita il creatore nel post.
2. Fai passare la clip da `rule-check`: controlla anche intro e CTA. Correggi e rimonta finché non passa.
3. Mostra all'utente il file e il testo della didascalia e chiedi un «sì». Non caricare niente.
