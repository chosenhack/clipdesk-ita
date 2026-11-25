<div align="center">

<h1 align="center">clipdesk-ita</h1>

<p align="center"><b>Le clip virali delle live di GTA 6, montate. In italiano.</b></p>

<p align="center">Un plugin per Claude Code: trova le clip più viste degli streamer italiani in live su GTA 6 (Twitch, YouTube, Kick), o il momento in cui la chat esplode, e le monta in 1080×1920: intro col gancio, clip con i sottotitoli, chiamata all'azione. Tu la guardi, la approvi e la pubblichi.</p>

<p align="center"><img src="https://img.shields.io/badge/Claude_Code-plugin-A66BFF" alt="Claude Code: plugin"> <img src="https://img.shields.io/badge/skill-17-A66BFF" alt="skill: 17"> <img src="https://img.shields.io/badge/clip-1080x1920-A66BFF" alt="clip: 1080x1920"> <img src="https://img.shields.io/badge/licenza-MIT-A66BFF" alt="licenza: MIT"></p>
<p align="center"><sub>Progetto non ufficiale di fan. Nessun legame con Rockstar Games, Take-Two o Anthropic.</sub></p>
<p align="center"><a href="#la-prima-volta-incolla-questo-in-claude-code">Si parte</a> · <a href="#cosa-ti-serve">Cosa ti serve</a> · <a href="#le-skill">Le skill</a> · <a href="#le-regole-delle-clip-che-funzionano">Regole delle clip</a> · <a href="#gli-script-a-mano">Script</a></p>

</div>

```
/plugin marketplace add chosenhack/clipdesk-ita
/plugin install clipdesk-ita@clipdesk-ita
```

Due righe in Claude Code. Poi la skill `setup` installa gli strumenti e in una sola sessione hai la cartella della tua pagina, le clip virali di oggi degli streamer italiani di GTA 6 e le prime 3 già montate da guardare.

## La prima volta: incolla questo in Claude Code

```
Usa clipdesk-ita. Prepara la mia pagina di clip di GTA 6: fammi le tue 4 domande in un
messaggio solo, poi dopo un mio "sì" fai tutto: cerca le campagne di clipping aperte,
trova le clip più viste di oggi degli streamer italiani in live su GTA 6, scarica le
3 migliori e montale con intro col gancio, clip e CTA, controllale con le regole
della campagna e dimmi cosa pubblicare e dove.
```

Le clip vengono dalle live degli streamer, non dai video di notizie o guide: quelli danno clip di informazioni.

Ogni clip esce così: **2 secondi di intro** con il momento clou in anteprima e il gancio grande, **la clip** con i sottotitoli di quello che dice lo streamer, **2,5 secondi di chiusura** con la chiamata all'azione.

**Hai già il plugin?** Aggiornalo: in Claude Code `/plugin marketplace update clipdesk-ita`, poi `/reload-plugins` (o riapri Claude Code).

## Cosa ti serve

- **Claude Code**, con un piano Claude a pagamento.
- **Python 3.10 o più recente** e **ffmpeg con i sottotitoli** (su Mac `brew install ffmpeg-full`: il semplice `ffmpeg` di Homebrew non li ha). Al resto (yt-dlp, faster-whisper, curl_cffi per Kick) ci pensa la skill `setup`.
- Mac, Windows o Linux. Una scheda video NVIDIA rende la trascrizione più veloce; senza, un video di 12 minuti richiede circa 5 minuti.

Non ti serve un account Twitch o Kick: live, clip e chat si leggono dalle pagine pubbliche.

## Cosa cambia rispetto all'originale

Questa versione parte da gtavi-claudecode di Bodila51 (licenza MIT), che oggi non è più online. La storia dei commit originali è conservata qui. Le aggiunte:

- **Clip virali.** `viral.py` prende gli streamer italiani in live su GTA 6 (Twitch, YouTube, Kick), quelli visti in live negli ultimi 7 giorni e i canali della tua watchlist, e trova le clip più viste che hanno tagliato i loro spettatori, ordinate per visualizzazioni all'ora. `--scarica 3` le scarica e le prepara: trascrizione, momento clou, niente nero all'inizio o alla fine.
- **Montaggio con gancio e CTA.** `cut.py --hook "…" --cta "…"` apre con 2 secondi del momento clou e il gancio grande, poi la clip con i sottotitoli, poi la chiusura con la chiamata all'azione. Volume normalizzato su tutto. Il controllo prima di pubblicare verifica che intro e CTA ci siano.
- **Streamer italiani.** `streams.py --lang it` mostra solo le live di GTA 6 in italiano su Twitch, ordinate per spettatori.
- **Momenti clou, non spiegazioni.** `moments.py --lang it` riconosce le reazioni degli streamer italiani ("non ci credo", "mamma mia", "no vabbè", "daje"), anche quando sono più parole di fila. Abbassa le scene del gioco, che è in inglese (spesso trama, quindi spoiler), e lo streamer che parla al pubblico (saluti, annunci, giveaway, sponsor). Trascrive ogni tratto nella sua lingua, così i dialoghi del gioco restano in inglese anche nei sottotitoli. Rifiuta le dirette ancora in corso (per quelle c'è `live.py`), salta il Just Chatting all'inizio delle live di Twitch e con `--from` analizza un'altra parte della live.
- **Solo dirette di GTA 6.** La ricerca live di YouTube riempie la pagina di dirette 24/7 di altro (telegiornali, cartoni, poker), che finivano in cima per spettatori: `streams.py` le toglie. `trends.py` dice di ogni video se è una live finita, gameplay o una spiegazione.
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
| `viral-clips` | Il giro completo: le clip più viste di oggi degli streamer italiani in live su GTA 6, scaricate e montate con intro col gancio, clip e CTA |
| `campaign-finder` | Le campagne aperte: tariffa ogni 1.000 views, budget rimasto, regole, link |
| `stream-finder` | Chi è in live su GTA 6 adesso, per spettatori, e le loro live finite da cui tagliare; con `--lang it` solo gli italiani |
| `trend-radar` | I video di GTA 6 delle ultime 24 ore, per visualizzazioni all'ora, ognuno col suo tipo: live finita, gameplay o spiegazione |
| `moment-finder` | I momenti clou da 15 a 40 secondi di una live finita: picchi di volume, reazioni dello streamer, i punti più rivisti su YouTube e la chat che esplode. Scarta le scene di trama e gli annunci |
| `live-mode` | Registra una live di Twitch o YouTube e taglia una clip ogni volta che la chat esplode, mentre succede |
| `twitch-reaction` | Clip di reazione: la faccia dello streamer sopra, il gioco sotto, un titolo grande in mezzo. Trova da solo la webcam |
| `clip-cutter` | Il montaggio 1080×1920: intro col gancio sul momento clou, clip con i sottotitoli dello streamer, CTA finale, audio a -14 LUFS |
| `hook-writer` | 3 ganci e 3 CTA per ogni clip, in italiano |
| `rule-check` | Durata, formato, intro e CTA, hashtag e contenuti vietati, prima di pubblicare |
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
python scripts/viral.py --lang it --ore 24 --scarica 3
python scripts/viral.py --prepara "https://www.twitch.tv/<canale>/clip/<id>"
python scripts/cut.py jobs/<id> --pick 1 --layout react --cam auto --hook "Ha rubato un aereo, guarda il decollo" --cta "Commenta: tu saresti decollato?"
python scripts/streams.py --query "gta 6 ita" --lang it
python -m yt_dlp --flat-playlist --playlist-end 3 --print "%(url)s %(title)s" "https://www.twitch.tv/<canale>/videos?filter=archives&sort=time"
python scripts/moments.py "https://www.twitch.tv/videos/<id>" --top 8 --lang it
python scripts/moments.py "https://www.twitch.tv/videos/<id>" --top 8 --lang it --from 120
python scripts/trends.py --query "gta 6 ita" --hours 24 --solo-live
python scripts/translate.py jobs/<id> --pick 2
python scripts/check.py jobs/<id>/edits/clip_2.mp4 --campaign campaigns.md
python scripts/live.py "https://twitch.tv/<canale>" --minutes 60
python scripts/viral.py --prepara jobs/<id>/live/spike_1.mp4 --streamer <nome>
```

## Licenza

MIT. Il codice originale è di Bodila51, le modifiche e la traduzione italiana di [@chosen_hack](https://www.instagram.com/chosen_hack). Vedi `LICENSE`.
