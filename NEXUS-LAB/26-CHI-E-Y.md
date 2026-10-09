# Chi è Y — e perché la nonna non ha capito

**Data:** 2026-09-14
**Origine:** *"persona deve cominciare a non essere ME"* · *"chi è Y?"* ·
*"ieri chiacchierata con parente sviluppatore... ma che fa questo sw? devi poterlo
spiegare a tua nonna"*

---

## 1. Il dato più importante del messaggio non è la nonna

È che la domanda l'ha fatta **uno sviluppatore**.

```text
"ma che fa questo sw?"
```

Non l'ha chiesta un utente confuso. L'ha chiesta un tecnico, in una conversazione,
e non ha ricevuto una risposta che gli restasse.

Questo cambia la diagnosi. Non è un problema di semplificazione per i non tecnici:
è che **non esiste una frase che dica cosa fa il prodotto**. Se esistesse, uno
sviluppatore la capirebbe al primo colpo — è il suo mestiere.

### 1.1 Perché non esiste

Tutte le formulazioni che abbiamo usato in 25 documenti descrivono il **meccanismo**:

```text
"Foundation produce, Execution esegue"
"PageData is the language of knowledge experiences"
"indeterminismo che diventa determinismo"
"contracts over free-form code"
"Infrastructure must be reusable; Domain must be replaceable"
```

Sono corrette, sono tue, e sono tutte risposte a *"come funziona?"*.
Nessuna risponde a *"cosa fa per qualcuno?"*.

### 1.2 Il test dei benchmark

Come rispondono gli altri alla stessa domanda, dalle loro home page:

```text
ToolJet      "Build internal tools: admin panels, dashboards, operational apps"
Trustable    "Build apps with local AI on your PC"
Instruqt     "Hands-on labs that drive product adoption"
AlphaSense   "Find insights across 500M business documents"
Visualping   "Get alerted when a webpage changes"
Particl      "See what your retail competitors are doing"
text-to-SQL  "Query your database in plain English"
Open Nexus    —
```

La forma è sempre la stessa:

```text
VERBO + OGGETTO + BENEFICIARIO
```

Nessuno menziona l'architettura. Nessuno. Nemmeno ToolJet, che ha un'architettura
notevole, e nemmeno Hebbia, che ha una tesi tecnica forte ("il RAG naive fallisce
sull'84% delle query complesse") — quella la dicono agli investitori, non in home.

### 1.3 I due problemi sono uno solo

```text
"la persona non deve essere ME"          → non so chi è Y
"devi poterlo spiegare a tua nonna"      → non ho la frase

sono lo STESSO problema:
senza una frase di risultato, l'unica persona che riesci a immaginare
mentre usa il prodotto sei tu.
```

La persona torna a essere "ME" **perché il prodotto è descritto come meccanismo**.
Un meccanismo lo capisce solo chi l'ha costruito. Un risultato lo capisce chiunque
abbia quel risultato da ottenere.

---

## 2. La Y proposta, e perché non tiene

Proposta dell'utente:

> *"un utente di dominio, una persona che sa fare un prompt e ha tutti gli strumenti
> base di lavoro"*

### 2.1 È definita da cosa SA FARE, non da cosa DEVE FARE

```text
"utente di dominio"              → competenza
"sa fare un prompt"              → competenza
"ha gli strumenti base"          → dotazione
```

Tre attributi, zero bisogni. È la descrizione di un **segmento demografico**, non di
una persona con un problema. Non è falsificabile e non è trovabile: non esiste un
elenco di "persone che sanno fare un prompt".

Confronto con una definizione utilizzabile:

```text
"chi passa N ore a settimana a raccogliere informazioni da fonti sparse
 per produrre un report, una decisione o una pratica che qualcun altro
 dovrà approvare"
```

Questa ha un numero (N ore), un'attività osservabile, e un punto dove si può
chiedere a qualcuno "sei tu?".

### 2.2 E c'è una trappola precisa

`NX-64`, il filtro di sostituibilità, dalla scansione di ieri:

> *se un utente può ottenere l'80% del risultato incollando testo in un LLM
> generalista, il multiplo è sotto 1×.*

**"Una persona che sa fare un prompt" è esattamente la persona che può ottenere
l'80% del risultato da ChatGPT.** È il cliente meno probabile, non il più probabile.

La scansione lo mostra: `AI research/homework engine`, 1M views, 96% di margine,
multiplo **0,94×**. Utenti che sanno chiedere, prodotto che non trattiene.

### 2.3 La Y che esce dai tuoi stessi dati

Chi paga, nei listini che hai raccolto?

```text
GoMarble     fa pagare di più read-WRITE con approvazione e AUDIT TRAIL
Particl      250–1.000 $/mese: benchmarking e profondità storica
Visualping   140 $/mese sul piano Business: 20K check, API, integrazioni
text-to-SQL  238 abbonati a 209 $: elimina una competenza, ma su dati aziendali
```

Cosa hanno in comune? **Il compratore deve giustificare il risultato a qualcun altro.**

```text
Y = LA PERSONA CHE DEVE RENDERE CONTO

  · il compliance officer che deve produrre una traccia verificabile
  · l'analista che deve difendere una conclusione davanti a un comitato
  · il giornalista che deve citare la fonte
  · chi fa due diligence e non può permettersi di sbagliare
  · il funzionario pubblico che deve rispondere a un consiglio o a un controllo
```

**La responsabilità è ciò che rende l'evidenza non opzionale.** E un LLM generalista
ti dà una risposta senza responsabilità: non ha fonte, non ha versione, non ha
traccia, non risponde a nessuno.

Questo chiude il cerchio con tre cose già stabilite:

```text
M-04 / § 8.3   il differenziatore è la traccia di evidenza, non l'analisi
M-06           il verticale normativo: la responsabilità è un fatto regolamentare
NX-69          la governance venduta come tier: audit trail = piano superiore
```

E spiega perché il tuo istinto su PA/giustizia era giusto: **sono i settori dove
rendere conto non è una scelta, è un obbligo.**

---

## 3. La frase

### 3.1 Per la nonna

```text
"Fa le ricerche al posto tuo, e si ricorda dove ha trovato ogni cosa."
```

Test: contiene il differenziatore (*si ricorda dove*) senza una parola tecnica.
Una nonna capisce. Uno sviluppatore capisce al primo colpo.

### 3.2 Per il parente sviluppatore

```text
"Quando devi mettere insieme informazioni sparse in cento posti, e poi devi
 spiegare a qualcuno perché sei arrivato a quella conclusione: raccoglie,
 tiene le fonti, e ti dà la risposta con la prova attaccata."
```

### 3.3 Per il listino

```text
VERBO        raccoglie, confronta, tiene traccia
OGGETTO      fonti eterogenee su un dominio
BENEFICIARIO chi deve rendere conto di una conclusione
```

### 3.4 Cosa NON è la frase

```text
non è "piattaforma per knowledge experience"
non è "framework con contratti e invarianti"
non è "Foundation produce, Execution esegue"
```

Quelle restano vere, e restano per gli ADR, per gli investitori tecnici e per te.
Ma non sono la risposta a "che fa questo sw?".

---

## 4. "Quando entra in scena l'AI?" — la risposta è tua, ed è giusta

> *"meno lo fa, più la base è solida e può superare tempeste."*

Confermato, e c'è un test che lo rende operativo:

```text
TOGLI L'AI. Il prodotto produce ancora qualcosa di utile?

  SÌ  → l'AI è al posto giusto: interpreta ciò che la base ha già raccolto
  NO  → l'AI È la base, e la base è fragile
```

Per Open Nexus, senza AI restano:

```text
· il corpus raccolto e versionato
· le fonti e la loro tracciabilità
· la classificazione e il confronto
· la change detection
· l'esperienza navigabile
```

**È già un prodotto.** L'AI aggiunge l'interpretazione sopra.

Quindi la polarità è corretta, ed è il motivo per cui il sistema supera le tempeste:

```text
l'AI può essere sbagliata      → il corpus resta giusto
l'AI può essere indisponibile  → il corpus resta servibile
l'AI può diventare cara        → il corpus resta gratuito
l'AI può essere ritirata       → è già successo il 10 settembre, e il corpus
  (model ID cambiato)            non se n'è accorto
```

È D-017 (degradation budget) applicato all'AI stessa. E la riduzione del § 4 di
`08-COST-CULTURE` non è solo un risparmio: è ciò che rende l'AI **opzionale**.

Regola da scrivere:

> **L'AI entra in scena una volta sola: nell'interpretazione.**
> Tutto ciò che sta prima (raccolta, riduzione, classificazione, rilevamento)
> e tutto ciò che sta dopo (rendering, navigazione, pubblicazione) è deterministico.
> Se l'AI entra in un altro punto, va motivato per iscritto.

---

## 5. Sul "naufrago nel mare delle startup"

L'immagine è tua e va presa sul serio, perché contiene la diagnosi.

```text
il naufrago    sta in acqua, il flusso decide dove va
il navigante   ha una rotta, il flusso è una variabile da compensare
```

Cosa distingue i due? Non la forza. **La strumentazione e una destinazione.**

Stato attuale, onesto:

```text
strumentazione   ECCELLENTE   25 documenti · 73 voci · 67 decisioni
                              metodo di falsificazione funzionante
                              inventario di capacità con evidenza
                              scansione di mercato con numeri
destinazione     ASSENTE      NX-30 aperto, Y non definita fino a oggi,
                              nessuna frase di risultato
```

**Hai una strumentazione da traversata oceanica e nessuna destinazione a catalogo.**
Non è un naufragio: è una barca ottima ferma in rada. Che è una condizione diversa,
e si risolve in modo diverso — non costruendo più strumentazione.

E il rischio specifico, che va nominato perché è già successo due volte in questa
sessione: costruire la strumentazione è piacevole, produce evidenze, e dà la
sensazione di avanzare. La destinazione no: la destinazione produce solo domande
senza risposta finché qualcuno non risponde.

---

## 6. Cosa cambia

```text
NX-73  NUOVO P0 — la frase. Verbo + oggetto + beneficiario.
       Candidata in § 3. Va testata su 5 persone, non scelta a tavolino.
       Se il parente sviluppatore non la ripete dopo un giorno, non funziona.

NX-22  RICALENDRIZZATO — i due tier non erano "Builder / Decision-maker".
       Sono "chi costruisce" e "CHI DEVE RENDERE CONTO". Il secondo è Y.

NX-30  HA UN CRITERIO — il verticale giusto è dove rendere conto è un obbligo,
       non una scelta. PA, giustizia, sanità, finanza regolamentata,
       appalti, sicurezza. Non è più una domanda aperta: è un filtro.

NX-64  CONFERMATO E RAFFORZATO — "sa fare un prompt" è il cliente meno probabile,
       perché può già farsi l'80% da solo.

NX-49  la sonda va valutata contro Y, non contro l'utente generico.
       Job-seeker: il candidato NON deve rendere conto a nessuno.
       Il career service / outplacement SÌ (deve giustificare il placement).
       → conferma empirica del targeting B2B trovato nella scansione.
```

---

## 7. Il test da fare, che costa zero

La frase di § 3.1 va detta a cinque persone, di cui almeno tre non tecniche, e va
chiesto **il giorno dopo**: *"ti ricordi cosa fa quel software di cui ti ho parlato?"*

```text
se ripetono "fa le ricerche e si ricorda dove ha trovato le cose"
   → la frase funziona
se ripetono "una roba con l'AI"
   → non funziona, e nessun ADR la salverà
```

È il test più economico dell'intero backlog ed è l'unico che misura la cosa di cui
parliamo da due giorni. Ed è anche la prima **conversazione** — cioè la voce che
manca da D-039 in poi.

Non serve un cliente. Serve una persona che ti ascolti e poi si ricordi.

---

*Ultimo aggiornamento: 2026-09-14*
