---
name: hook-writer
description: Scrivi i ganci a video e le CTA di chiusura per le clip di GTA 6. Usala ogni volta che una clip ha bisogno di un gancio, di una CTA, di un titolo o di un'apertura per la didascalia, o quando l'utente dice «scrivi i ganci», «trova un titolo» o «che CTA metto».
---

# Scrittura ganci e CTA

Scrivi 3 opzioni per clip, in stile frase (solo la prima lettera maiuscola). Brevi: da 3 a 8 parole entrano nel box del gancio. I ganci sono in italiano. Un gancio crea curiosità, non descrive: sbagliato «Clip divertente di GTA 6», giusto «Ha trovato l'auto che nessuno aveva visto».

## Cosa funziona

- Promessa con un numero: "3 cose che ti sei perso in questo trailer"
- Fatto che sorprende: "Questa auto è nascosta in bella vista"
- Situazione: "Quando la polizia insegue il giocatore sbagliato"
- Negazione: "Questo non si può fare in GTA 5"
- Domanda: "Riusciresti a sopravvivere a questo inseguimento?"
- Nome dello streamer o del creator, quando è noto: "Anche [nome] non se l'aspettava"

## Titoli di reazione (layout twitch-reaction)

Per una clip di reazione di uno streamer, il titolo sta sulla linea di giunzione tra volto e gioco per tutta la clip. Formula: nome dello streamer + verbo di reazione + cosa ha reagito, con MAIUSCOLO su 2 o 3 parole chiave.

- "Speed HA CAPITO perché GTA 6 ci ha messo 13 ANNI"
- "Kai HA PERSO LA TESTA quando sono arrivati i poliziotti in GTA 6"
- "Scontri con la polizia in GTA 6" (stile contorno: breve, da 3 a 6 parole)

Descrivi quello che succede sullo schermo. Mai mettere parole in bocca allo streamer: niente citazioni che non ha detto, niente opinioni inventate. Le emoji sono facoltative, al massimo 2.

## Il gancio dell'intro

Nel montaggio (`cut.py --hook`) il gancio sta sui primi 2 secondi, sopra il momento clou mostrato in anteprima. Le immagini fanno già vedere l'azione: il testo apre la curiosità su come va a finire, non la racconta. Da 3 a 8 parole, niente emoji (il font del video non le disegna).

- Giusto: "Ha rubato un aereo, guarda il decollo"
- Sbagliato: "Si schianta con l'aereo" (svela il finale)

## La CTA di chiusura

Ogni clip finisce con una chiamata all'azione (`cut.py --cta`), sull'ultimo fotogramma. Scrivi 3 opzioni, da 4 a 8 parole, e segna la migliore. Deve chiedere un'azione precisa, mai solo «seguimi»:

- Domanda da commentare, legata alla clip: "Commenta: tu saresti decollato?"
- Scelta tra due: "Commenta: avresti sparato o guidato?"
- Condivisione: "Mandalo a chi guida come lui"
- Serie: "Segui per la clip di domani" solo se domani la clip c'è davvero.

Niente emoji nella CTA a video. Nella didascalia la stessa domanda può tornare, con un'emoji.

## Cosa non funziona

- Etichette generiche: "Clip di GTA 6", "Momento divertente"
- "Aspetta e vedrai", "Non ci crederai", "Guarda fino alla fine"
- Urgenza finta o MAIUSCOLO ovunque
- CTA vaghe: "Seguimi", "Like e iscriviti"

## Regole

1. La clip deve mantenere la promessa del gancio. Se il gancio dice 3 cose, mostrane 3. Niente clickbait.
2. Niente spoiler sui momenti di trama nella settimana di lancio. Segna queste clip con SPOILER nella didascalia, non nel gancio.
3. Non far pensare che la pagina sia di Rockstar. Non scrivere «ufficiale» per i contenuti dei fan.
4. Usa «GTA 6». Al massimo una emoji.
5. Non riusare lo stesso gancio nell'arco di una settimana. Controlla `log.md`.
6. I fatti nel gancio devono essere veri e verificati. I numeri devono corrispondere alla clip.

Restituisci le 3 opzioni di gancio e le 3 di CTA, e segna quelle che consigli.
