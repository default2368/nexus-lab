# Quantizzazione della collaborazione Prometeo — tempo, denaro, proiezione

**Data:** 2026-09-16
**Registro:** interno
**Domanda corretta:** non "quanto vale un prodotto per Y" (Y è indefinita), ma
**"quanto costa puntare l'MVP esistente su un'ipotesi di collaborazione con
Prometeo, e cosa può tornare"**.

---

## 0. Cosa la correzione "Y = ?" invalida, e cosa no

```text
RESTA VALIDO (intelligence di mercato, indipendente da Y)
  · gli assi di pricing osservati: volume · frequenza · connettori · seat ·
    governance · profondità storica
  · il premio di verticale 7–70× misurato su listini pubblici
  · i tre livelli di ricavo per testa (traffico $0,03 · prosumer $33 · B2B $189–391)
  · il filtro di sostituibilità (sotto 1× se un LLM generalista fa l'80%)
  · il fatto che la governance sia un asse di prezzo (GoMarble)
  · la banda $11k–50k ARR come RIFERIMENTO di mercato

NON È VALIDO (proiezione su di noi)
  · qualunque stima di NOSTRO ricavo
  · la scelta del payer
  · il pricing del nostro prodotto
  · NX-65 usato come obiettivo invece che come paragone
```

**Regola:** la scansione dice cosa paga il mercato. Non dice cosa incasseremmo noi.
Confondere le due è l'errore, ed è lo stesso tipo di errore di "il sito è statico":
dato buono, conclusione non supportata.

---

## 1. Cosa significa "collaborazione", e le forme possibili

```text
(a) TECHNOLOGY PARTNERSHIP   licenziano/incorporano Open Nexus, noi diamo il motore
(b) PILOT CONGIUNTO          costruiamo il layer sui loro contenuti, loro danno
                             accesso + dominio
(c) RESELLER / WHITE-LABEL   lo vendono alle loro 3.000 aziende
(d) DESIGN PARTNER           sono il primo utente, si costruisce insieme
(e) ACQUISIZIONE / INVESTIMENTO  improbabile allo stato
```

**Realistico oggi: (b), con possibile evoluzione a (c).**

Ma attenzione: **non sappiamo se esista una controparte.** NX-91 è aperto. Se A. non
è dentro né accanto a Informatica EDP, allora (b) non ha interlocutore e l'ipotesi
diventa "costruire per i nodi del network", che è un altro progetto.

**Tutto ciò che segue è condizionato alla risposta di NX-91.**

---

## 2. Tempo

### 2.1 Scomposizione del pilot

```text
COMPONENTE                                    stima lavoro   dipende da
──────────────────────────────────────────────────────────────────────────
Connettore WordPress (REST + sitemap)         2–4 giorni     niente
  ingestione, normalizzazione, content_sha
Ontologia di dominio                          20–40 ore      A. o un esperto
  norma ↔ obbligo ↔ ruolo ↔ modulo ↔                         di dominio
  caso cliente ↔ versione ↔ CTA
Grafo di dipendenza norma → contenuto,        2–4 settimane  ontologia
  versionato nel tempo (NX-99 / BRAIN-006)
Pipeline di classificazione ed estrazione     1 settimana    ontologia
  (classe 0, reduction)
Vista editoriale come experience              1–2 settimane  grafo + C-01
Vista probatoria come experience              1–2 settimane  grafo + versioning
Governance: approvazione, catena di           1–2 settimane  C-08 parziale
  evidenza, audit
──────────────────────────────────────────────────────────────────────────
TOTALE LAVORO                                 ~8–14 settimane di lavoro concentrato
```

### 2.2 Il moltiplicatore che nessuno mette nei piani

```text
hai un impiego a tempo pieno.

8–14 settimane di lavoro concentrato
  = 320–560 ore
  = a 10 ore/settimana reali (sere + weekend, con gli imprevisti)
  = 32–56 settimane di CALENDARIO
  = 8–13 mesi
```

**Questo è il numero vero, ed è quello che di solito uccide i pilot.** Non la
complessità tecnica: il calendario.

Mitigazioni possibili:

```text
· tagliare la vista probatoria nel pilot, tenerla per la fase 2   → −2 settimane
· usare l'ontologia minima (norma → contenuto, senza obblighi)    → −1 settimana
· partire da 20 pagine invece di 153 + 206 + 855                  → −3 giorni
· NON tagliare la governance: è il differenziatore
```

Versione minima credibile: **~5–7 settimane di lavoro = 5–8 mesi di calendario.**

### 2.3 Cosa c'è già e non va rifatto

```text
renderer per knowledge experience    LIVE su openfav.vercel.app     C-01 ✓
governance della presentazione       check-style-authority.mjs      C-03 ✓
proiezione semantica                 resolveStatusTone              C-04 ✓
sessione e policy                    0.6.3-A/B                      C-06 ~
produzione artefatti                 bundle-collector + manifest    C-05 ~
riduzione deterministica             CLI estrazione token           C-07 ~
```

**L'MVP di tutto rispetto esiste.** Non si costruisce la piattaforma: si costruisce
un connettore, un'ontologia e due viste.

---

## 3. Denaro

### 3.1 Costi di avvio

```text
verifica legale posizione dipendente pubblico (NX-86)   €200–500
  → NON è opzionale. È il prerequisito.
eventuale costituzione di soggetto giuridico            €1.000–3.000
  → solo se la collaborazione diventa contrattuale
  → in Italia: notaio + commercialista + primo anno
eventuale assicurazione RC professionale                €300–800/anno
  → se si maneggiano dati di clienti in dominio sanzionatorio
──────────────────────────────────────────────────────────────
minimo per partire                                      €200–500
se diventa contrattuale                                 €1.500–4.000
```

### 3.2 Costi ricorrenti

```text
LLM (deepseek-flash con reduction pipeline)      €2–20/mese
Infrastruttura (Fly + Vercel esistenti)          €0–5/mese
Storage (SQLite / volume esistente)              €0–2/mese
Dominio + email                                  ~€2/mese
──────────────────────────────────────────────────────────────
totale                                           €5–30/mese
```

Conferma `08-COST-CULTURE` § 7.4: sotto €30/mese. Il vincolo non è il denaro.

### 3.3 Il vero costo

```text
denaro        €200–500 per partire, < €30/mese
tempo         5–8 mesi di calendario per la versione minima
OPPORTUNITÀ   cosa non fai in quei 5–8 mesi
```

L'ultima riga è quella che va quantificata. In 5–8 mesi potresti:

```text
P5  analisi di mercato come servizio    → primo ricavo in 4–8 settimane
P4  servizi sopra Foundation            → primo ricavo in 2–4 settimane
NX-56 pubblicazione + test del frame    → 1–2 settimane
```

**Il costo del pilot Prometeo non è €300. È il mancato primo ricavo.**

---

## 4. Proiezione — tre scenari

Stime, marcate come tali. Nessuna è una previsione.

### 4.1 Scenario A — la collaborazione funziona

```text
condizioni    A. è collegato a Prometeo · NX-86 risolto · accettano un pilot
esito         fee di pilot €5–20k una-tantum
              poi licenza o revenue share
proiezione    se anche solo il 5% delle 3.000 aziende prende un modulo
              aggiuntivo a €50/mese → 150 × €50 = €7.500/mese
tempo         12–24 mesi
probabilità   [INFERITO] bassa-media. Non sappiamo chi sia A., se Prometeo
              abbia interesse, e se preferirebbero costruirlo da soli.
```

### 4.2 Scenario B — riferimento riutilizzabile

```text
condizioni    il pilot si fa, ma non scala con Prometeo
esito         un layer verticale funzionante in un dominio regolamentato
              → vendibile ad altri nodi: consulenti ambientali, associazioni,
                studi legali che assistono operatori rifiuti
proiezione    30–50 studi/consulenti × €150–400/mese = €4.500–20.000/mese
tempo         18–30 mesi
probabilità   [INFERITO] media. Richiede vendita B2B, che non hai mai fatto.
```

### 4.3 Scenario C — non decolla

```text
condizioni    A. era curioso, o Prometeo lo fa da solo, o NX-86 blocca
esito         5–8 mesi spesi, nessun ricavo
              MA: il grafo di dipendenza versionato entra in Foundation
                  (NX-99, regola del due soddisfatta)
                  un riferimento verticale nel portfolio
                  M-06 parzialmente attivato
                  una relazione con un avvocato di dominio
tempo         —
probabilità   [INFERITO] la più alta dei tre
```

**Lo scenario più probabile è quello senza ricavo.** Va detto, perché un piano che
non lo contempla non è un piano.

---

## 5. La questione delicata che hai nominato

> *"la delicata questione di quantizzazione di tempo/denaro/proiezione"*

La parte delicata non è nei numeri. È qui:

```text
più la nota di analisi è convincente,
più insegna a un incumbent con 3.000 clienti e un team di sviluppo
esattamente cosa gli manca e come chiuderlo.
```

Loro hanno: dominio, dati, workflow, canale, supporto, team. La scansione gli dice:
il vostro modello di contenuto è piatto, vi serve un grafo di dipendenza normativa
versionato. **È un'informazione che vale molto per chi ha i mezzi per usarla.**

### 5.1 Cosa si protegge e cosa si dà

```text
GIÀ DATO (nella nota)          · l'analisi del sito, pubblica e rifacibile
                                · l'osservazione sul modello di contenuto piatto
                                · le due viste concettuali
                                · l'ammissione che l'ingestione è commodity

DA NON DARE prima di accordo   · l'ontologia specifica
                                · il design del grafo di dipendenza
                                · il motore (Foundation non si spedisce: NX-01b)
                                · il metodo di riduzione e i numeri di costo
                                · i contratti interni

DA FIRMARE prima di costruire  · chi possiede l'ontologia prodotta insieme
                                · chi possiede il grafo
                                · diritto di riuso per altri clienti
                                · cosa succede se la collaborazione finisce
```

**Il punto critico è il diritto di riuso.** Se costruisci l'ontologia rifiuti per
loro senza clausola di riuso, hai regalato M-06 a un incumbent. Con la clausola,
hai un riferimento e un asset.

### 5.2 Leva negoziale, onestamente

```text
LORO HANNO       3.000 aziende · dominio · dati · canale · team · cassa
TU HAI           software funzionante e visibile · analisi di qualità ·
                 velocità · un motore che non devono costruire

SBILANCIATO. E va accettato invece di negoziato come se non lo fosse.
```

Conseguenza pratica: **non negoziare da pari.** Negoziare da fornitore specializzato
che porta una cosa che loro non hanno tempo di fare. È l'unica posizione credibile.

---

## 6. Raccomandazione

```text
1. NX-86 PRIMA. Non è prudenza: senza, ogni ora spesa sul pilot è a rischio.

2. NX-91 PRIMA. Una riga. Se A. non è collegato a Prometeo, tutto questo
   documento va riscritto perché la controparte non esiste.

3. NON iniziare il pilot prima di avere:
     · la risposta di NX-91
     · il parere legale
     · un accordo scritto minimo, anche di una pagina, su proprietà e riuso

4. IN PARALLELO, P5 o P4. Non come alternativa: come finanziamento e come
   prova che sai consegnare a un cliente. Arrivano a ricavo in 4–8 settimane
   e non dipendono da nessuno.

5. SE 1–3 si risolvono: pilot minimo (§ 2.2, 5–7 settimane di lavoro),
   con clausola di riuso, e con la vista probatoria rimandata alla fase 2.
```

### 6.1 La versione in una riga

> **Il pilot Prometeo costa 5–8 mesi di calendario e ~€300, e ha come esito più
> probabile nessun ricavo ma un asset architetturale e una relazione.**
>
> **Vale la pena se e solo se: (a) la tua posizione è chiarita, (b) sai chi è la
> controparte, (c) il riuso è scritto.**
>
> **Senza quelle tre, è il modo più affascinante di perdere otto mesi.**

---

## 7. Il numero che riassume

```text
costo monetario        trascurabile   < €300 + < €30/mese
costo di calendario    dominante      5–8 mesi
costo opportunità      reale          il primo ricavo che non arriva
valore in caso di fallimento   non zero   NX-99 entra in Foundation,
                                          M-06 parziale, relazione, riferimento
valore in caso di successo     alto       M-06 pieno + canale + ricavo
```

È un'opzione con **costo monetario basso, costo temporale alto, e valore residuo
non nullo**. Il che la rende difendibile — a patto di non pagarla due volte
aspettando di chiarire NX-86 e NX-91.

---

*Nota interna. Stime marcate. Nessuna proiezione qui è una previsione.*
