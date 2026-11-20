---
name: learning-loop
description: Registra i post e impara dai numeri reali con scoreboard.csv, learning.md e payouts.csv. Usala dopo che un post esce, alle letture a 12, 24 e 72 ore, per la revisione giornaliera o settimanale, o quando l'utente chiede cosa funziona o quanto ha guadagnato.
---

# Ciclo di apprendimento

File nella cartella della pagina: `scoreboard.csv` (una riga per post), `learning.md` (Vittorie, Sconfitte, Regole attuali), `payouts.csv` (solo pagamenti reali), `log.md`.

## Regole

1. Solo numeri reali. Chiedi all'utente di incollare le metriche o uno screenshot. Se un numero non c'è, lascia la casella vuota. Mai indovinare.
2. Registra ogni post quando esce: post_id, date, time, platform, pillar, format, hook, length_sec, credit, test_name.
3. Le letture a 12, 24 e 72 ore riempiono views_12h, views_24h, views_72h, poi like, condivisioni, risposte, salvataggi, followers_at_read.
4. Un test al giorno. Cambia una sola variabile (stile del gancio, durata, orario di pubblicazione, lunghezza della didascalia, immagine fissa o clip). Dagli un nome in `test_name`.
5. Nessun giudizio sotto le 24 ore. Preferisci la lettura a 72 ore se il post sta ancora crescendo.
6. `payouts.csv`: registra solo gli importi che la campagna o la piattaforma mostra davvero. Mai proiettare guadagni.

## Giornaliera (sera)

Miglior e peggior post, una lezione scritta come regola. Aggiungila a `learning.md`. Scegli il test di domani.

## Settimanale

Top 3 e bottom 3 post, visualizzazioni mediane per pilastro, per fascia oraria e per piattaforma. Punta di più su ciò che sta sopra la mediana. Rifai o taglia ciò che è rimasto sotto la mediana per una settimana intera. Scegli i test della settimana successiva. Aggiorna il `playbook.md` personalizzato con ciò che è cambiato. Manda all'utente un breve riepilogo.

Letture a tarda notte: dì cosa manca ancora, invece di riempire i vuoti.
