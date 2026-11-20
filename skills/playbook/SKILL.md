---
name: playbook
description: Esegui la routine giornaliera della pagina GTA 6 dal playbook completo. Usala quando l'utente dice «routine giornaliera», «cosa faccio oggi», «manda avanti la pagina», o chiede del kickoff di 7 giorni, del giorno di lancio, dei pilastri dei contenuti, delle fasce di pubblicazione o delle regole di sicurezza.
---

# Playbook

1. Leggi `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/playbook.md`. Se la cartella della pagina ha un suo `playbook.md`, leggi quello: è la copia personalizzata.
2. Se la cartella della pagina non esiste, esegui prima la skill `setup`.
3. Trova a che punto è la pagina: il giorno di kickoff (sezione 17) o il piano giornaliero normale (sezione 9). Controlla `log.md` e `scoreboard.csv`.
4. Esegui la giornata:
   - Prima le fonti ufficiali (sezione 5). Registra ogni fatto verificato con il suo link in `facts.md`.
   - Trova materiale: `trend-radar`, `stream-finder`, `campaign-finder`.
   - Taglia le clip: `moment-finder`, poi `clip-cutter`, con i ganci da `hook-writer`.
   - Fai passare ogni clip da `rule-check`.
   - Registra e impara con `learning-loop`.
5. Manda all'utente UN solo messaggio con la didascalia esatta, il percorso del file e il credito per ogni post. L'utente risponde «sì» per approvare. L'utente lo pubblica da sé o lo programma. Mai caricare in automatico.
6. Chiudi la giornata con il breve report (sezione 16): cosa è uscito, il post migliore con i numeri, una lezione, il test di domani.

Regole ferme: niente fughe di contenuti, niente «gioca prima», niente pirateria, niente soldi di GTA Online o bot AFK, niente fatti o numeri inventati, accredita ogni creatore, niente promesse di guadagno. Tutto ciò che esce dal mix normale richiede prima il «sì» dell'utente.
