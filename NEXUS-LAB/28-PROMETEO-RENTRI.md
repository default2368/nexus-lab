# Y-2 / Prometeo / RENTRI — valutazione

**Data:** 2026-09-15
**Fonte:** `26-NEXUS-PROMETEO-BRAIN-NETWORK.txt` (prodotto in altra sessione), che
rimanda a `25-SCANSIONE-PROMETEO-RIFIUTI.md` **non disponibile in questo workspace**.
**Persona:** A., avvocato. Segnale: *"guarda questi siamo noi, vedi se riscontri
bisogni."*

**Nota di numerazione:** il file allegato è "26-" nella sequenza dell'altra sessione.
In questo workspace `26-` è già `26-CHI-E-Y.md`. Da riconciliare al merge.

---

## 0. Perché questo è il dato più importante della sessione

D-047 aveva stabilito un **criterio** per NX-30:

> il verticale giusto è dove rendere conto è un **obbligo**, non una scelta.
> PA · giustizia · sanità · finanza regolamentata · appalti · sicurezza.

Prometeo / tracciabilità rifiuti / RENTRI è **letteralmente quel criterio realizzato**:

```text
· registro elettronico nazionale → l'obbligo DI RENDERE CONTO è il prodotto
· catena di responsabilità a più soggetti, ciascuno con obblighi propri
· sanzioni amministrative e penali → l'evidenza non è un lusso
· fonti normative che cambiano → serve versioning e dipendenza
· avvocato coinvolto → il dominio è giuridico, non tecnico
```

Non è un'istanza fra le altre. È la prima che **soddisfa K1 al massimo grado**, e
K1 era il criterio su cui tutte le altre candidate cadevano.

E c'è un secondo fatto, che conta più del primo:

> **A. ha iniziato lui.** Non è outreach. È una persona che ha mostrato il proprio
> mondo e ha chiesto "vedi se riscontri bisogni".

È il primo segnale **inbound** della sessione. K8 passa da pianificato a accaduto.

---

## 1. Cosa il documento azzecca — credito esplicito

Cinque cose, e sono le stesse a cui siamo arrivati indipendentemente:

### 1.1 `dato ≠ interpretazione ≠ decisione` (§ 4)

È D-048 (l'AI entra in scena una volta sola) e la separazione
`observed / inferred / recommended` di `03-WORKFLOW.md`, arrivate da un'altra
direzione. Convergenza indipendente = la separazione è giusta.

### 1.2 "Una risorsa Brain non è necessariamente un modello AI" (§ 2)

```text
regola deterministica · parser · query · algoritmo · prompt governato ·
sequenza di agenti · workflow umano · combinazione
```

È la **reduction pipeline** e la classe 0 di `08-COST-CULTURE`, formulate senza
averle lette. E infatti gli esempi BRAIN-002 (confronta scadenza con autorizzazione)
e BRAIN-003 (rileva incongruenze registro/formulario) sono **deterministici**:
classe 0, costo zero, alta frequenza. Esattamente il profilo che permette il
pricing per-check (§ 12.3).

### 1.3 Il workflow contract con "quando si arresta" (§ 3)

È **L-1**, la lacuna che avevo segnalato nel metodo Sonda: nessun criterio di
arresto. Qui c'è, e c'è anche `chi approva`, `quale evidenza conserva`, `cosa
succede se la fonte è incompleta o contraddittoria`. Lacuna chiusa.

### 1.4 La disciplina su A. (§ 7, § 10)

```text
"è un segnale utile, ma non è ancora validazione commerciale"
"non assumere che l'apertura di A equivalga a budget"
"non usare dati o materiali riservati senza autorizzazione"
"non trasformare interpretazioni legali in risposte automatiche"
```

Questo è il tipo di onestà che mancava nelle scansioni precedenti. Va preservato.

### 1.5 "Il network va costruito dopo un primo workflow verticale funzionante" (§ 5)

Corretto, ed è la frase che tiene in piedi tutto il resto.

---

## 2. Dove il documento outruns se stesso

C'è una contraddizione interna di struttura, non di contenuto.

```text
§ 1   "non solo sito, non solo contenuto, non solo chatbot...
       ma un ECOSISTEMA FUNZIONALE CONDIVISO"
§ 6   "perché può giustificare uno SPIN-OFF" — con 8 condizioni
§ 11  tesi: "costruire un ECOSISTEMA di capacità Brain, workflow e
       interpretazioni verificabili... network di soggetti"

§ 9   "non partire dal network completo" — pilot su una materia delimitata
§ 10  "non promuovere Brain capability nel core prima di una seconda applicazione"
```

**§ 9 e § 10 sono giusti. § 1, § 6 e § 11 sono la stessa malattia di sempre in abiti
nuovi**: l'architettura che cresce prima dell'evidenza.

Il percorso reale è:

```text
1 pilot su una materia      → § 9, corretto
2 secondo caso d'uso        → regola del due (D-040)
3 solo allora: ecosistema   → § 1
4 solo allora: spin-off     → § 6
```

Il documento li elenca tutti e quattro allo stesso livello di dettaglio, il che li
rende psicologicamente equivalenti. Non lo sono.

**Decisione da prendere esplicitamente:** si adotta § 9 come piano e si archiviano
§ 1/6/11 come scenario condizionato al successo di § 9. Altrimenti fra tre mesi si
starà progettando il network invece di fare il pilot.

Nota: "spin-off" implica un soggetto giuridico. Vedi § 5 — per un dipendente
pubblico non è una parola neutra.

---

## 3. La matrice, rieseguita

```text
                          K1   K2   K3   K4    K5   K6   K7   K8
──────────────────────────────────────────────────────────────────
Y-1 volontario             ~   ✗✗   ✗    ✗✗    ✗    ✗✗   ✗    ✓✓
E  analisi con evidenza    ✓   ✓    ✓✓   ✓     ✓    ✓✓   ✓✓   ~
D  dev validation          ✓   ~    ✓✓   ✗     ~    ✓✓   ~    ✓✓
Y-2 Prometeo/RENTRI        ✓✓  ✓✓   ✓✓   ✓?    ✓✓   ~    ✗    ✓
──────────────────────────────────────────────────────────────────
```

### 3.1 Le celle che contano

**K1 ✓✓** — l'obbligo di rendere conto è letterale, con sanzioni. Massimo grado
raggiungibile. Nessuna delle altre candidate ci arriva.

**K2 ✓✓** — un LLM generalista **non può** fare compliance RENTRI: non ha il
registro, non ha le autorizzazioni del cliente, non può produrre evidenza
legalmente difendibile, e se sbaglia ci sono sanzioni. È il caso in cui il filtro
di sostituibilità è superato al massimo grado.

**K3 ✓✓** — fonti normative che cambiano, scadenze, formulari, registri: osservazione
continua **deterministica** (BRAIN-002/003 sono regole, non AI). È il profilo
perfetto per il pricing per-check a costo marginale zero.

**K5 ✓✓** — massimamente verticale, regolamentato, specifico italiano. Il premio
7–70× si applica integralmente.

**K6 ~** — il pilot di § 9 richiede C-01 (live), C-04 (verificata), C-07 (parziale),
C-08 (parziale). **Non richiede C-09 né C-11**, che sono le teoriche.
È la differenza decisiva con Y-1:

```text
Y-1     richiede C-09 authoring agentico + C-11 distribuzione firmata
        = le DUE capacità meno verificate dell'inventario
Y-2     richiede C-01 + C-04 + C-07 + C-08
        = tutte verificate o parziali, nessuna teorica
```

Restano da costruire: i connettori per fonti normative e registri (NX-27/28) e
BRAIN-006 (aggiornare le viste dipendenti da una norma modificata), che richiede un
grafo di dipendenza fra contenuti e non è banale.

**K8 ✓** — A. esiste e ha già aperto. Manca il contenuto della conversazione: le
dieci domande di § 8 non sono ancora state fatte.

**K4 ✓?** — **l'unica cella non verificata, ed è quella che può ribaltare tutto.**

### 3.2 K4: la verifica mancante

```text
pavimento OPEN SOURCE      quasi certamente assente
                           → nessun progetto open source fa compliance RENTRI
                           → richiede dominio giuridico italiano

pavimento COMMERCIALE      quasi certamente PRESENTE e affollato
                           → il passaggio a RENTRI ha generato un'ondata di
                             prodotti; i gestionali rifiuti esistono da decenni
                           → DA VERIFICARE, non da assumere
```

**La domanda giusta non è "esiste un pavimento open source" ma:**

> cosa fanno i gestionali rifiuti esistenti che Open Nexus non farebbe, e cosa
> NON fanno che Open Nexus farebbe?

L'ipotesi del documento (§ 6 punto 7, "integrazioni con sistemi transazionali") è
che Open Nexus stia **sopra** i sistemi transazionali, non al loro posto. È la
posizione di Aiera: layer di conoscenza, interpretazione ed evidenza sopra contenuti
e sistemi altrui.

Se è così, K4 diventa ✓ e non c'è conflitto con gli incumbent — c'è integrazione.
Se invece il pilot dovesse sostituire un gestionale, K4 crolla e il progetto è morto
prima di iniziare.

**Questa è la prima cosa da verificare, prima di parlare con A. di qualunque cosa.**

---

## 4. Le tre domande da aggiungere alle dieci di § 8

Le dieci domande del documento sono buone e vanno fatte così come sono. Ne aggiungerei
tre, tutte su K4 e sul payer:

```text
11. Quale software usate OGGI per registri, formulari e RENTRI?
    Cosa vi costa, e cosa vi fa arrabbiare di quello che usate?
    → è la domanda K4. Se la risposta è "niente, Excel", il pavimento è zero
      e l'opportunità è enorme. Se è un nome di gestionale, va studiato.

12. Quando una norma cambia, chi se ne accorge, quanto tempo ci mette,
    e cosa succede a chi non se ne accorge?
    → è la domanda sulla frequenza e sul costo dell'errore.
      Da qui esce il pricing.

13. Chi firma il preventivo per una cosa del genere, e quale cifra
    non richiede una riunione?
    → è la domanda sul payer reale. A. è avvocato: è lui il compratore,
      è il suo cliente, o è l'associazione?
```

La 13 è quella che il documento evita, ed è comprensibile — ma è l'unica che
trasforma un segnale in un'opportunità.

---

## 5. La cosa seria: il tuo impiego

Va detta chiaramente, perché con questo verticale smette di essere una nota a piè
di pagina.

```text
lavori presso un'amministrazione pubblica
stai valutando un prodotto di COMPLIANCE in un dominio regolamentato
il dominio coinvolge autorità, obblighi, sanzioni, prova documentale
e i documenti strategici SONO ANCORA sul tenant del tuo datore di lavoro
```

Tre piani distinti, tutti da verificare con un legale (non con me):

```text
1. INCOMPATIBILITÀ / AUTORIZZAZIONI
   attività extra-istituzionali dei dipendenti pubblici: obblighi di
   comunicazione e autorizzazione. "Spin-off" (§ 6) è una parola che
   implica un soggetto giuridico e va maneggiata con un professionista.

2. PROPRIETÀ DEL MATERIALE
   NX-50 è ancora aperto. Strategia di un prodotto commerciale salvata su
   account istituzionale = ambiguità che vuoi risolvere PRIMA di avere
   qualcosa che vale.

3. CONFLITTO PERCEPITO
   anche se formalmente pulito, un prodotto di compliance venduto a soggetti
   regolamentati da un dipendente pubblico genera una domanda scomoda.
   Meglio averci pensato prima che dover rispondere dopo.
```

**NX-50 era "urgente" quando era solo una questione di ordine. Adesso è un
prerequisito.** Non si parla con A. di un progetto commerciale con i documenti del
progetto sul cloud del Ministero.

---

## 6. Cosa cambia nel backlog

```text
NX-30   HA UNA CANDIDATA FORTE. Non è più "il verticale si deduce dalle sonde":
        c'è un verticale con K1 ✓✓, K2 ✓✓, K3 ✓✓, K5 ✓✓ e una persona che ha
        aperto la conversazione. Resta da verificare K4.

NX-49   la prima istanza candidata diventa il Vertical Brain & Evidence Pilot
        di § 9, non E (analisi di mercato) e non Y-1.
        E resta utile come capacità interna e come NX-56 (pubblicazione).
        Y-1 resta utile come NX-79 (audit delle authority).

NX-84   NUOVO P0 — verifica K4: censimento dei gestionali rifiuti / RENTRI
        esistenti. Cosa fanno, cosa non fanno, cosa costano.
        PRIMA di qualunque conversazione di prodotto con A.

NX-85   NUOVO P0 — colloquio con A. sulle 13 domande (§ 8 del documento + § 4 qui).
        Obiettivo: bisogni e payer, NON presentare Open Nexus.
        Il documento lo dice già: "non presentare subito Open Nexus come soluzione".

NX-86   NUOVO P0 — NX-50 elevato a prerequisito: bonifica tenant + verifica
        incompatibilità con un legale, prima di NX-85.

NX-87   NUOVO P1 — richiedere `25-SCANSIONE-PROMETEO-RIFIUTI.md` al workspace.
        Manca il contesto che ha prodotto il documento.

NX-88   NUOVO P2 — BRAIN-006 (aggiornare le viste dipendenti da una norma
        modificata) richiede un grafo di dipendenza fra contenuti.
        È l'unica capacità del pilot non coperta da C-01..C-08.
```

---

## 7. La frase per questo verticale

NX-73 chiedeva due livelli. Per Prometeo:

```text
LIVELLO X (motore)
  "Rende verificabile ciò che altrimenti sarebbe solo un'opinione."

LIVELLO ISTANZA (per A. e per il suo mondo)
  "Quando cambia una norma, ti dice cosa cambia per te, da dove viene,
   e cosa devi fare — con la fonte attaccata."
```

Test della nonna: *"ti dice cosa devi fare quando cambia la legge, e ti fa vedere
dove l'ha scritto."* Regge.

Test di sostituibilità: un LLM generalista può dirti cosa dice una norma. Non può
 dirti **cosa cambia per te**, perché non ha il tuo registro, le tue autorizzazioni,
le tue scadenze. E non può produrre una traccia che un avvocato firmerebbe.

---

## 8. Verdetto

```text
Y-2 / Prometeo è la candidata più forte mai apparsa nella sessione,
su ogni criterio tranne K7 (nessun prototipo) e K4 (non verificato).

Non è ancora un'opportunità: è un segnale inbound con un dominio ad altissima
compatibilità architetturale.

La sequenza corretta è:
  1. NX-86  bonifica tenant + verifica legale          ← prerequisito, non negoziabile
  2. NX-84  censimento incumbent (K4)                  ← può ribaltare tutto
  3. NX-85  colloquio con A., 13 domande, niente pitch
  4. solo dopo: pilot § 9 su una materia delimitata

Non prima. E § 1/6/11 del documento (ecosistema, network, spin-off) vanno
archiviati come scenario condizionato, non come piano.
```

---

*Ultimo aggiornamento: 2026-09-15*
