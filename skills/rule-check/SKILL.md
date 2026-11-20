---
name: rule-check
description: Controlla una clip finita contro specifiche tecniche, regole della campagna e contenuti vietati prima di pubblicarla. Usala prima di ogni caricamento, o quando l'utente chiede «posso pubblicarla?» o «è tutto a posto?».
---

# Controllo regole

Esegui:

`python "${CLAUDE_PLUGIN_ROOT}/scripts/check.py" <clip.mp4> --campaign campaigns.md`

Controlla: durata, 1080x1920, presenza dell'audio, le regole della campagna da `campaigns.md` e i contenuti vietati (fughe di contenuti, «gioca prima», pirateria). Nella lista dei vietati ci sono anche le frasi in italiano («gioca prima», «download gratis», «codici gratis», «soldi infiniti», «glitch dei soldi»).

Poi:

1. Mostra PASS o FAIL per ogni controllo, in un elenco breve.
2. Se c'è un FAIL: correggi la causa (ritaglia con `clip-cutter`, aggiungi il credito, accorcia) e rilancia. Non discutere con un controllo fallito.
3. Leggi anche la didascalia tu. Deve accreditare il creatore nel testo, niente fatti inventati, niente parole come «ufficiale», e rispettare le regole delle didascalie per piattaforma nel playbook.
4. Lo script non può giudicare tutto. Se le regole della campagna sono `unknown` o mancano, chiedi all'utente di incollarle.
5. Solo dopo che tutti i controlli passano, manda all'utente clip, didascalia e credito e aspetta il «sì». È l'utente a pubblicare. Mai caricare in automatico.
