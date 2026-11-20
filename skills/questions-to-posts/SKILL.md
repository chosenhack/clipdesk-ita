---
name: questions-to-posts
description: Trasforma le domande ricorrenti dei fan (thread su Reddit e commenti sui nostri post) in bozze di post HOW TO. Usala quando l'utente chiede cosa chiedono le persone, vuole idee HOW TO, o dice di trasformare le domande dei commenti in post.
---

# Domande in post

Trova le domande che i fan continuano a fare, controlla se `facts.md` le risponde e scrive bozze di post HOW TO solo da fatti verificati.

## Comando

Esegui dalla cartella della pagina (dove sta `facts.md`):

```
python scripts/questions.py --subs GTA6,GTA,GrandTheftAutoV --days 3 [--comments comments.txt] --out questions.md
```

- `--comments comments.txt`: commenti copiati dai nostri post, uno per riga. Le domande in italiano vengono riconosciute («come», «dove», «cosa», «quando», «perché», «si può», «qualcuno sa»...) e diventano titoli come «GTA 6: COME SI SBLOCCA LA MOTO?».
- `--facts facts.md` (predefinito), `--ideas idea-bank.md` (predefinito), `--top 25`, `--min-count 1`.
- Usa il JSON pubblico di Reddit, 1 richiesta al secondo, aspetta e riprova sul 429. Se Reddit lo blocca, incolla i commenti in `comments.txt` e rilancia.

## Cosa ottieni

- `questions.md`: gruppi di domande ordinati per numero e poi per voti positivi. Ognuno ha la domanda canonica, il conteggio, link di esempio e uno tra `answer found in facts.md: <line>` o `UNANSWERED: needs an official source`.
- Sotto i gruppi: una bozza HOW TO per ogni gruppo con risposta, nel modello del playbook (`HOW TO [DO THE THING] IN GTA 6`, passi numerati).
- `idea-bank.md`: ogni gruppo senza risposta viene aggiunto come compito di ricerca.

## Dopo l'esecuzione

1. Leggi ogni bozza. Lo script copia i passi dalle righe di `facts.md`; non sa giudicare l'ordine né se una riga è davvero un passo. Correggi l'ordine, riduci a 3-5 passi, mantieni le parole fedeli al fatto.
2. Per ogni gruppo senza risposta, trova una fonte ufficiale, aggiungila a `facts.md` con il link, poi rilancia.
3. Fai passare il testo finale da `rule-check`, poi pubblica. Per le domande ripetute, rispondere lo stesso giorno conta più della rifinitura.

## Regole

1. Solo fatti da fonti ufficiali (Rockstar, Take-Two, PlayStation, Xbox), registrati in `facts.md` con il link. Ricontrolla tutto ciò che ha più di 48 ore.
2. Mai inventare passi, numeri, date o nomi di menu. Niente fonte, niente passo. Una domanda senza risposta resta un compito di ricerca.
3. Niente fughe di contenuti, voci, pirateria, exploit o trucchi «gioca prima», anche se i fan li chiedono. Salta quei gruppi.
4. Credito: se un post si basa sulla clip o sulla scoperta di un fan, accredita con `🎥 @creator`. Non citare né nominare utenti Reddit: le domande sono solo un segnale su cosa coprire.
5. Non far pensare che la pagina sia di Rockstar. Usa «GTA 6».
6. Il maiuscolo solo per la riga del gancio.
