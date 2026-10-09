# Scansione tecnica — sito PrometeoRifiuti

**Data:** 2026-09-15
**URL:** https://www.prometeorifiuti.com/
**Metodo:** richiesta HTTP, analisi HTML/header/asset pubblici, WordPress REST API,
sitemap e ricerca pubblica.
**Provenienza:** documento sorgente prodotto in altra sessione, salvato nel workspace
il 2026-09-16 perché esisteva solo nella conversazione. Analisi derivata in
`16-FOUNDATION-HEALTH.md` e D-068/D-069.

## 1. Risultato sintetico

Il sito è una installazione WordPress server-rendered, costruita con Elementor e tema
Hello Elementor.

```text
Apache
  ↓
PHP / WordPress
  ↓
Hello Elementor theme
  ↓
Elementor + Elementor Pro
  ↓
HTML iniziale renderizzato dal server
  ↓
JavaScript client-side per interazioni, carousel, menu, popup e tracking
```

Non è una SPA React/Next/Vue.

Non sono stati rilevati: `_next/`; `__NEXT_DATA__`; Nuxt; Vite; React come framework
applicativo; Webpack come struttura principale del sito.

## 2. SSR / rendering

### Evidenza

La richiesta HTTP della home restituisce direttamente HTML completo con: titolo;
testo; menu; contenuto SEO; immagini; CTA; markup Elementor.

Il browser non deve costruire l'intera pagina recuperando dati da un'API prima di
mostrare il contenuto.

### Conclusione

```text
server-side rendered WordPress
+ progressive enhancement JavaScript
+ CSS e widget Elementor
```

Favorevole a: SEO; pagine informative; contenuto pubblico; aggiornamenti editoriali;
link condivisibili; crawler e archivi.

Non significa però che ogni funzione sia server-side: menu, slider, popup, form e
alcuni widget sono gestiti dal browser.

## 3. Stack osservato

### Server e CMS

- server dichiarato: Apache
- WordPress: `7.1` secondo il meta generator
- REST API WordPress attiva
- oEmbed WordPress attivo
- sitemap WordPress pubblica
- tema: `Hello Elementor 3.5.1`

### Page builder

- Elementor: `4.2.4`
- Elementor Pro: `4.2.3`
- CSS Elementor generato per singole pagine (`post-5.css`, `post-8.css`, ecc.)
- font locali Elementor: Lato, Jost, Roboto
- widget osservati: menu, posts, gallery, carousel, icons, popup, sticky, animation, swiper

### Plugin osservabili

Dagli asset e dalle namespace REST pubbliche risultano:

- Cookie Law Info / CookieYes
- Elementor / Elementor Pro
- Essential Addons for Elementor Lite `6.8.3`
- WP Rocket `3.23.3.3`
- SEOPress
- Redirection
- Wordfence / Wordfence Login Security
- Ninja Forms
- HandL UTM Grabber
- Tracking Code Manager
- Google Analytics / Google Tag Manager
- YouTube embed

Questa è una rilevazione esterna basata su asset e API: non è un inventario certo dei
plugin installati, perché alcuni possono essere inattivi, mascherati o non caricati
sulla home.

## 4. Caching e performance

Il sito espone il meta generator di WP Rocket con feature tra cui: delay JavaScript;
defer JavaScript; preconnect; optimization/cache; preload links; ottimizzazione desktop.

```text
Cache-Control: max-age=0
```

Questo non basta per concludere se la pagina sia o non sia servita da cache
applicativa o reverse proxy. Il server dichiarato è Apache e non è stato osservato un
header evidente che attribuisca il traffico a Cloudflare.

> **WP Rocket è presente; l'efficacia della cache reale, il backend PHP, il database
> e l'hosting non sono determinabili completamente dalla scansione pubblica.**

## 5. Architettura dei contenuti

### Quantità osservabile via REST API

- circa 153 pagine
- circa 206 articoli
- circa 855 media

I numeri dipendono dall'istante della scansione e dai contenuti pubblicati.

### Tipi di contenuto

```text
post · page · attachment · nav_menu_item · wp_block · wp_template
wp_template_part · wp_global_styles · wp_navigation · wp_font_family
wp_font_face · elementor_library · elementor_snippet
```

Non sono stati osservati custom post type verticali pubblici dedicati a: moduli;
ruoli; casi cliente; norme; versioni; eventi; webinar; settori.

Questo non significa che tali concetti non esistano. Significa che, dal modello
pubblico osservabile, sono principalmente rappresentati come pagine, articoli, media
e template.

## 6. API e superfici pubbliche

Sono pubblicamente raggiungibili:

```text
/wp-json/
/wp-json/wp/v2/pages
/wp-json/wp/v2/posts
/wp-json/wp/v2/media
/wp-json/oembed/1.0/embed
/wp-sitemap.xml
/robots.txt
```

La risposta `/wp-json/` espone numerosi namespace, tra cui:

```text
wp/v2 · oembed/1.0 · elementor/v1 · elementor-pro/v1 · elementor-ai/v1
wp-rocket/v1 · seopress/v1 · redirection/v1 · wordfence/v1
ninja-forms-* · mcp · wp-abilities/v1
```

Non si assume che tutte le route siano accessibili senza autenticazione o che siano
utilizzabili come API di integrazione. La loro presenza è però un segnale
architetturale: il sito dispone di una superficie machine-readable ampia.

## 7. Content architecture: cosa funziona

Lo stack è adatto a: pubblicare rapidamente pagine e articoli; gestire una redazione
non tecnica; creare landing page; incorporare video e documenti; creare pagine per
ruoli e settori; mantenere SEO e sitemap; costruire CTA e form; pubblicare
aggiornamenti frequenti.

È coerente con un sito di prodotto verticale che deve comunicare: funzionalità; casi
cliente; aggiornamenti normativi; webinar; versioni; demo.

## 8. Limiti strutturali per Open Nexus

### 8.1 Pagina come contenitore

La rappresentazione pubblica è prevalentemente `pagina / articolo / media`.

Non è visibile un modello semantico nativo in cui:

```text
norma ↔ obbligo ↔ ruolo ↔ modulo ↔ caso cliente ↔ versione ↔ CTA
```

Questo non è un giudizio negativo su WordPress. È il normale confine di un CMS
page-oriented.

### 8.2 Duplicazione

Quando lo stesso concetto deve vivere in: una pagina; un articolo; un PDF; un webinar;
una FAQ; una release note; una pagina caso cliente — il CMS non garantisce
automaticamente che le relazioni semantiche e le fonti restino sincronizzate.

### 8.3 Versioning semantico

WordPress conserva revisioni delle pagine, ma non necessariamente il significato di
dominio: quale norma ha prodotto una modifica; quali pagine dipendono da essa; quali
workflow sono impattati; quale claim è diventato obsoleto; quale caso cliente dimostra
una funzione.

### 8.4 Rendering non è conoscenza

```text
Elementor   → come appare
Open Nexus  → cosa significa, da dove proviene, come si riusa
```

## 9. Connessione con Open Nexus

La connessione più credibile è un **headless knowledge layer / semantic overlay**,
non una sostituzione immediata di WordPress.

```text
WordPress + Elementor  → pubblicazione e branding esistenti
Open Nexus             → modello semantico · fonti · relazioni · versioni
                         workflow editoriale · viste generate
```

### A. Import read-only

Acquisire pagine e articoli via REST; estrarre entità e relazioni; collegare fonti e
date; costruire una mappa navigabile; non modificare WordPress.

### B. Content intelligence interna

Indicizzare contenuti e documenti; fornire ricerca con citazioni; trovare pagine
potenzialmente obsolete; rilevare duplicazioni; proporre collegamenti mancanti;
produrre briefing per la redazione.

### C. Generazione di viste

Dallo stesso modello: pagina per produttori; pagina per trasportatori; pagina per
consulenti; hub RENTRI; scheda modulo; caso cliente correlato; percorso verso la demo.

### D. Workflow editoriale governato

```text
fonte / release / norma
  → estrazione → proposta modifica → elenco pagine impattate
  → revisione → pubblicazione WordPress → audit e versione
```

La pubblicazione automatica dovrebbe essere successiva all'approvazione umana.

## 10. Stack per una prima implementazione

**Ingestion:** WordPress REST API; sitemap; media/documenti; PDF e slide; feed degli
articoli; eventuali export.

**Normalizzazione:** estrazione testo; deduplicazione; riconoscimento di moduli,
ruoli, norme, versioni, casi e CTA; collegamento pagina–fonte–data; classificazione
con confidenza.

```text
Foundation
  → ApplicationBundle → PageData → validazione → runtime → renderer

X Prometeo Knowledge
  → ontologia contenuti → workflow editoriale → viste per ruolo
    → policy di pubblicazione
```

**Output iniziale:** mappa della conoscenza del sito; assistente read-only con
citazioni; elenco duplicazioni e contenuti obsoleti; pagina esperienza per ruolo;
report delle pagine impattate da una nuova normativa o release.

## 11. Informazioni non determinabili dalla scansione pubblica

```text
provider hosting · versione PHP · database e versione MySQL/MariaDB
configurazione reale di cache · CDN effettivamente usata
ambienti staging e produzione · workflow redazionale interno · CRM
software di marketing automation · integrazione reale con Prometeo gestionale
eventuali API private · dati di traffico e conversione
uptime e metriche Core Web Vitals reali
```

Questi elementi richiedono accesso autorizzato o conversazione con il gestore.

## 12. Valutazione tecnica

| Dimensione | Risultato |
|---|---|
| Rendering iniziale | WordPress SSR / HTML server-rendered |
| CMS | WordPress |
| Builder | Elementor + Elementor Pro |
| Tema | Hello Elementor |
| Frontend SPA | non rilevato |
| API pubblica | WordPress REST API attiva |
| Sitemap | attiva |
| Contenuti | 153 pagine, 206 post, 855 media osservati |
| Modello semantico verticale pubblico | non rilevato |
| Cache plugin | WP Rocket rilevato |
| Hosting | Apache osservato; provider non determinato |
| Open Nexus opportunity | semantic overlay e content intelligence |

## 13. Conclusione

Il sito non è tecnicamente un'applicazione Open Nexus: è un WordPress server-rendered
con Elementor, costruito per pubblicare e promuovere un prodotto verticale.

Proprio per questo è un buon candidato per una sonda non invasiva:

> **Open Nexus può aggiungere un modello semantico, una source authority e workflow
> editoriali governati senza sostituire WordPress, Elementor o il sistema gestionale
> Prometeo.**

```text
WordPress esistente → acquisizione REST → conoscenza strutturata
→ relazioni e fonti → esperienza per ruolo → assistente read-only
→ proposta di aggiornamento con approvazione
```

---

*Documento sorgente. Analisi derivata e correzioni in `29-PROMETEO-ANALISI.md`,
D-068 (impressione giusta, motivo sbagliato), D-069 (namespace `mcp`, ingestione
commodity, ontologia come moat).*
