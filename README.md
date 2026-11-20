<div align="center">

<h1 align="center">clipdesk-ita</h1>

<p align="center"><b>Le live di GTA 6 diventano clip verticali. In italiano.</b></p>

<p align="center">Un plugin per Claude Code: guarda le live e i video di GTA 6, trova il momento in cui la chat esplode e ti prepara la clip 1080×1920 con sottotitoli e gancio. Tu la guardi, la approvi e la pubblichi.</p>

<p align="center"><img src="https://img.shields.io/badge/Claude_Code-plugin-A66BFF" alt="Claude Code: plugin"> <img src="https://img.shields.io/badge/skill-16-A66BFF" alt="skill: 16"> <img src="https://img.shields.io/badge/clip-1080x1920-A66BFF" alt="clip: 1080x1920"> <img src="https://img.shields.io/badge/licenza-MIT-A66BFF" alt="licenza: MIT"></p>
<p align="center"><sub>Progetto non ufficiale di fan. Nessun legame con Rockstar Games, Take-Two o Anthropic.</sub></p>
<p align="center"><a href="#la-prima-volta-incolla-questo-in-claude-code">Si parte</a> · <a href="#cosa-ti-serve">Cosa ti serve</a> · <a href="#le-skill">Le skill</a> · <a href="#le-regole-delle-clip-che-funzionano">Regole delle clip</a> · <a href="#gli-script-a-mano">Script</a></p>

</div>

```
/plugin marketplace add chosenhack/clipdesk-ita
/plugin install clipdesk-ita@clipdesk-ita
```

Due righe in Claude Code. Poi la skill `setup` installa gli strumenti e in una sola sessione hai la cartella della tua pagina, i video di GTA 6 che stanno andando oggi, i momenti migliori già scelti e le prime clip verticali da guardare.

## La prima volta: incolla questo in Claude Code

```
Usa clipdesk-ita. Prepara la mia pagina di clip di GTA 6: fammi le tue 4 domande in un
messaggio solo, poi dopo un mio "sì" fai tutto: cerca le campagne di clipping aperte,
mostrami i video e le live italiane di GTA 6 che vanno di più oggi, trova i momenti
migliori nel primo, taglia le prime 3 clip con il gancio, controllale con le regole
della campagna e dimmi cosa pubblicare e dove.
```

## Cosa ti serve

- **Claude Code**, con un piano Claude a pagamento.
- **Python 3.10 o più recente** e **ffmpeg con i sottotitoli** (su Mac `brew install ffmpeg-full`: il semplice `ffmpeg` di Homebrew non li ha). Al resto (yt-dlp, faster-whisper) ci pensa la skill `setup`.
- Mac, Windows o Linux. Una scheda video NVIDIA rende la trascrizione più veloce; senza, un video di 12 minuti richiede circa 5 minuti.

Non ti serve un account Twitch: le live e la chat si leggono dalle pagine pubbliche.

## Cosa cambia rispetto all'originale

Questa versione parte da gtavi-claudecode di Bodila51 (licenza MIT), che oggi non è più online. La storia dei commit originali è conservata qui. Le aggiunte:

- **Streamer italiani.** `streams.py --lang it` mostra solo le live di GTA 6 in italiano su Twitch, ordinate per spettatori.
- **Momenti in italiano.** `moments.py --lang it` trascrive in italiano e riconosce le esclamazioni delle live ("non ci credo", "mamma mia", "no vabbè", "daje"), anche quando sono più parole di fila.
- **Sottotitoli puliti.** Le parolacce italiane vengono mascherate come quelle inglesi; insulti e bestemmie sempre ("porco dio" diventa "p**** d**").
- **Dall'inglese all'italiano.** `translate.py` ora traduce in italiano di base: prendi la clip di un grande streamer americano e ne fai la versione italiana. Le pagine GTA italiane sono ancora poche.
- **Domande italiane.** `questions.py` riconosce le domande nei tuoi commenti ("come si sblocca…", "dove trovo…") e le trasforma in titoli come "GTA 6: COME SI SBLOCCA LA MOTO?".
- **Regole in italiano.** Il controllo prima di pubblicare blocca anche "gioca prima", "download gratis", "codici gratis", "soldi infiniti".
- **Funziona sul Mac.** L'ffmpeg di Homebrew non ha libass e le clip non venivano tagliate: ora gli script usano `ffmpeg-full` se c'è, e se manca ti dicono cosa installare.
- **Tutto tradotto**: skill, playbook e trucchi. Il logo di GTA dell'originale è stato tolto: non è nostro.

## Due modi per usarlo

**1. Campagne di clipping.** Streamer e marchi pagano chi fa le clip in base alle visualizzazioni approvate, su piattaforme come Whop Content Rewards. Ogni campagna ha la sua tariffa ogni 1.000 views, il budget rimasto e le sue regole: `campaign-finder` le legge dal vivo e non inventa numeri. Tu leggi le regole, clippi solo quel creator, pubblichi e invii il link.

**2. La tua pagina di GTA 6 senza volto.** Il playbook la guida: cosa pubblicare ogni giorno, come citare chi crei, i modelli di didascalia e un ciclo per imparare dai numeri. Le piattaforme non pagano le clip ripubblicate: la pagina cresce con la velocità, i consigli utili e le clip citate, poi può lavorare con campagne e collaborazioni.

Nessun guadagno è garantito. Il risultato dipende da quanto sei veloce, da cosa scegli e dai ganci; la tabella dei risultati ti dice cosa funziona.

## Le regole delle clip che funzionano

- Il gancio nel primo secondo. Di' perché restare ("l'auto che nessuno aveva trovato").
- Da 7 a 30 secondi. Taglia i vuoti all'inizio, chiudi sul momento clou.
- Sottotitoli grandi nella zona sicura: quasi tutti guardano senza audio.
- Rendila tua: gancio, consiglio, commento. Mai ripubblicarla così com'è. Cita sempre il creator nel post.
- Ogni domanda che torna nei commenti diventa un post "come si fa".
- Un test al giorno. Nessun giudizio prima di 24 ore; meglio i numeri a 72 ore.

## Le skill

| Skill | Cosa fa |
|---|---|
| `setup` | Installa ffmpeg, yt-dlp e faster-whisper, ti fa 4 domande e crea la cartella della pagina |
| `campaign-finder` | Le campagne aperte: tariffa ogni 1.000 views, budget rimasto, regole, link |
| `trend-radar` | I video di GTA 6 delle ultime 24 ore, ordinati per visualizzazioni all'ora |
| `stream-finder` | Chi è in live su GTA 6 adesso, per spettatori; con `--lang it` solo gli italiani |
| `moment-finder` | I momenti migliori da 15 a 40 secondi: picchi di volume, parole d'entusiasmo, i punti più rivisti su YouTube e la chat che esplode |
| `live-mode` | Registra una live e taglia una clip ogni volta che la chat esplode |
| `twitch-reaction` | Clip di reazione: la faccia dello streamer sopra, il gioco sotto, un titolo grande in mezzo. Trova da solo la webcam |
| `clip-cutter` | La clip 1080×1920: sottotitoli parola per parola, riquadro del gancio, audio a -14 LUFS |
| `hook-writer` | 3 ganci per ogni clip, in italiano |
| `rule-check` | Durata, formato, hashtag e contenuti vietati, prima di pubblicare |
| `multilang` | La stessa clip in italiano o in altre lingue, con sottotitoli e gancio tradotti |
| `questions-to-posts` | Le domande che tornano su Reddit e nei tuoi commenti diventano post "come si fa" |
| `secrets-map` | Un archivio di posti nascosti, soldi, auto e collezionabili trovati nelle clip, con minuto e fonte |
| `cheat-codes` | I trucchi di GTA 6 segnalati, con le fonti, pronti per un carosello di 4 slide |
| `playbook` | La tua routine di ogni giorno |
| `learning-loop` | La tabella dei risultati: un test al giorno, guadagni solo dai numeri veri |

Niente viene pubblicato da solo: approvi tu ogni post.

## Le regole che non si toccano

Niente fughe di notizie, niente post "gioca prima" o "download gratis", niente pirateria, niente soldi di GTA Online o bot AFK, niente notizie false, mai fingersi Rockstar. Ogni fatto ha una fonte ufficiale. Clippa le live degli altri solo dove hai il permesso: dentro una campagna di quel creator o con il suo ok.

## Gli script a mano

```
pip install -r requirements.txt
python scripts/trends.py --query "gta 6 ita" --hours 24
python scripts/streams.py --query "gta 6 ita" --lang it
python scripts/moments.py "https://www.youtube.com/watch?v=..." --top 8 --lang it
python scripts/cut.py jobs/<id> --pick 2 --layout facecam --hook "Nessuno se n'era accorto"
python scripts/translate.py jobs/<id> --pick 2
python scripts/check.py jobs/<id>/edits/clip_2.mp4 --campaign campaigns.md
python scripts/live.py "https://twitch.tv/<canale>" --minutes 60
```

## Licenza

MIT. Il codice originale è di Bodila51, le modifiche e la traduzione italiana di [@chosen_hack](https://www.instagram.com/chosen_hack). Vedi `LICENSE`.
