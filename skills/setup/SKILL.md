---
name: setup
description: Configurazione iniziale del desk per le clip di GTA 6. Usala quando l'utente installa il plugin, dice «configura», «setup» o «inizia», o quando ffmpeg, yt-dlp o faster-whisper mancano o la cartella della pagina non esiste ancora.
---

# Configurazione

Parla con l'utente in italiano.

Fai il lavoro da solo. Chiedi all'utente solo ciò che è elencato qui.

## 1. Installa gli strumenti (senza domande)

Controlla ciascuno con `ffmpeg -version`, `yt-dlp --version`, `python -c "import faster_whisper, numpy"`. Installa solo ciò che manca:

- ffmpeg, con i sottotitoli (libass). Windows: `winget install --id Gyan.FFmpeg -e --source winget`. macOS: `brew install ffmpeg-full` (il semplice `brew install ffmpeg` non ha libass e le clip uscirebbero senza sottotitoli; `ffmpeg-full` non finisce nel PATH, ma gli script lo trovano da soli). Linux: `sudo apt install -y ffmpeg`. Per controllare: `ffmpeg -hide_banner -filters` deve elencare `subtitles` (su Mac usa `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg`).
- Pacchetti Python, tutti i sistemi: `python -m pip install -U -r "${CLAUDE_PLUGIN_ROOT}/requirements.txt"` (faster-whisper, numpy, requests e un yt-dlp aggiornato; gli script preferiscono il yt-dlp di pip, perché un yt-dlp vecchio riceve HTTP 403 da YouTube)
- Rilancia la riga pip una volta a settimana: YouTube cambia spesso e yt-dlp va aggiornato di conseguenza.

Se un'installazione con winget, brew o apt richiede un nuovo terminale per il PATH, dillo in una riga e ricontrolla. Mai spendere soldi né aggiungere una carta.

## 2. Chiedi al massimo 4 domande, in UN solo messaggio numerato

1. Nome della pagina e nome utente (@).
2. Piattaforme (per esempio X, Instagram Reels, TikTok, YouTube Shorts).
3. Angolo di nicchia (una sola corsia: consigli e luoghi nascosti, notizie veloci, momenti divertenti, auto e personalizzazioni).
4. Fuso orario (se l'utente non lo indica, usa Europe/Rome).

Se l'utente ha già risposto, non chiederlo di nuovo. Salta il messaggio se tutte e quattro le risposte sono note.

## 3. Mostra il piano, chiedi UN solo «sì»

Elenca la cartella che creerai e i file al suo interno, poi chiedi un solo «sì». Dopo il sì, crea (nella directory corrente, in una cartella con il nome della pagina):

- `playbook.md` (copia da `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/playbook.md` e compila i campi tra [PARENTESI QUADRE] con le risposte)
- `facts.md` (solo fatti verificati, ciascuno con il link a una fonte ufficiale)
- `idea-bank.md`, `watchlist.md`, `log.md`
- `scoreboard.csv` con solo questa riga di intestazione:
  `post_id,date,time,platform,pillar,format,hook,length_sec,credit,views_12h,views_24h,views_72h,likes,reposts_or_shares,replies_or_comments,saves_or_bookmarks,followers_at_read,test_name,notes`
- `learning.md` con le sezioni Vittorie, Sconfitte, Regole attuali
- `takedowns.md`
- `campaigns.md` (riga del titolo e una tabella vuota: nome, piattaforma, tariffa ogni 1K visualizzazioni, budget rimasto, regole, link, data di controllo)
- `payouts.csv` con intestazione `date,campaign,platform,post_url,views,rate_per_1k,est_payout,status` (gestito da `scripts/payouts.py`)
- cartelle `media/official`, `media/raw`, `media/edits`

## 4. Conclusione

Dillo all'utente, in 3 righe: cosa è stato installato, dove si trova la cartella e il passo successivo (`campaign-finder`, poi `trend-radar`). Ricordagli che approva ogni post e che niente viene caricato in automatico.
