# Persona, tre Authority, e il vero modello di costo di X

**Data:** 2026-09-10
**Origine:** brainstorming — definizione della persona e del perimetro di X

---

## 1. Il cambio di persona

Dichiarazione dell'utente:

> *"non voglio che l'utente sposti rettangoli, voglio che un manager, un responsabile
> finanziario, un broker, esplori il mercato guidato dalla nostra X, che osserva,
> monitora, registra, propone modelli."*

### 1.1 Cosa cambia

```text
PRIMA (implicito)                  DOPO (dichiarato)
─────────────────────────────────────────────────────────────────
builder / developer                decision-maker
costruisce applicazioni            esplora un dominio
drag & drop, componenti            osservazione guidata
output: un'app da manutenere       output: comprensione + modelli proposti
ToolJet, Appsmith, Retool          nessuno, nel perimetro osservato
```

### 1.2 Perché è la mossa giusta

Esce completamente dal mercato affollato. ToolJet, Appsmith, Retool, Budibase
competono su *"chi fa costruire internal tools più in fretta"*. Quella gara ha già
vincitori con 40k star e SOC 2.

*"Un responsabile finanziario che esplora il mercato guidato da X"* non ha
concorrenti diretti nel set analizzato:

```text
ToolJet     costruisce tool per chi gestisce dati      ≠ guidare chi decide
Instruqt    insegna a sviluppatori tramite lab         ≠ guidare chi decide
Trustable   genera applicazioni con AI locale          ≠ guidare chi decide
```

Il più vicino è Instruqt, ma Instruqt è **didattica per sviluppatori**. Qui si parla
di **supporto alla decisione per ruoli non tecnici**. Sono mercati diversi con
budget diversi — e quello dei ruoli non tecnici è più grande.

### 1.3 Il prezzo della scelta: due prodotti, non uno

Un manager, un CFO o un broker **non installa una CLI**, **non usa Claude Code**,
**non configura MCP**. Quindi:

```text
TIER BUILDER          nexus-mcp · porta il proprio modello · RIGA 4 · costo zero
                      chi: sviluppatori, integratori, chi costruisce experience

TIER DECISION-MAKER   X in-app · il Brain paga i token · RIGA 2 · costo ricorrente
                      chi: manager, CFO, broker, ruoli non tecnici
```

**Conseguenza onesta:** il pivot di persona **riporta la riga 2 al centro**.
Non la elimina. Questo in parte rivaluta l'obiezione dell'utente sul costo —
ma pone un vincolo nuovo e più severo, vedi § 2.

---

## 2. La trappola nel verbo "osserva"

> *"X, che osserva, monitora, registra, propone modelli."*

Quattro verbi. Tre sono gratuiti, uno no. E quello che non lo è è il più pericoloso
proprio perché sembra il più innocuo.

### 2.1 Il profilo di costo dell'osservazione continua

```text
Generazione su richiesta    costo ∝ numero di richieste utente
                            se nessuno chiede, non spendi

Osservazione continua       costo ∝ TEMPO
                            monitora = gira sempre, anche di notte,
                            anche quando nessuno guarda
```

**"Monitora" è riga 2 con gli steroidi.** Non è costo per-request, è costo
per-orologio. Un sistema che osserva il mercato per un broker osserva il mercato
anche alle tre di notte.

Se l'osservazione passa da un LLM, il costo non è più lineare negli utenti: è
lineare nel **tempo × fonti monitorate**. È il modello di costo peggiore possibile
per un progetto singolo.

### 2.2 La soluzione — ed è già nel tuo split

```text
FOUNDATION OSSERVA       deterministico, gratis, continuo
  estrazione token (la CLI lo fa già)
  parsing, normalizzazione, hashing
  registrazione, serie storiche, delta
  soglie, regole, trigger

        ↓  solo quando c'è qualcosa che merita interpretazione

X INTERPRETA             AI, metered, a domanda o su evento
  propone modelli
  spiega un'anomalia
  genera una knowledge experience
```

**Foundation osserva, X interpreta.** È la stessa proposizione di
*"Foundation produce, Execution esegue"*, applicata al costo invece che al rendering.

Regola operativa:

```text
Un LLM non deve MAI essere nel percorso di osservazione continua.
Un LLM entra solo su:
  · domanda esplicita dell'utente
  · evento/soglia superata (trigger deterministico)
  · batch schedulato con tetto di spesa
```

Questo trasforma un costo per-orologio in un costo per-evento, che è bounded.
E il trigger è deterministico, quindi è Foundation, quindi è gratis.

### 2.3 Perché è anche un vantaggio competitivo

Un clone che mette un LLM sull'osservazione continua ha un costo strutturale che
non può rimuovere senza riscrivere il prodotto. Tu, se imposti la regola adesso,
hai osservazione **illimitata e gratuita** e interpretazione **meterizzata**.

È esattamente l'asimmetria che cercavi.

---

## 3. Le tre Authority

L'utente introduce *"una policy ferrea di graphic authority"*. Non è un dettaglio
grafico: è il terzo membro di una famiglia che nel recap ufficiale era già
parzialmente visibile.

```text
┌────────────────────────────────────────────────────────────────────┐
│ 1. IDENTIFIER AUTHORITY                                            │
│    chi decide l'identità di una pagina/app?                        │
│    stato: F-01 aperto — Registry ID ≠ Bundle-derived ID            │
│    causa: BundleCollector → title slugging                         │
│    → ADR-008, input per 0.7.0                                      │
├────────────────────────────────────────────────────────────────────┤
│ 2. PAGE SOURCE AUTHORITY                                           │
│    chi decide il contenuto di una pagina?                          │
│    stato: debito — "logical ownership validato,                    │
│    Page Source Authority non formalized"                           │
│    → aggravato da D-013: projection hardcodata = bundle non        │
│      più source authority                                          │
├────────────────────────────────────────────────────────────────────┤
│ 3. GRAPHIC AUTHORITY                          ← NUOVA              │
│    chi decide come una pagina appare?                              │
│    stato: proposta dall'utente, da formalizzare                    │
└────────────────────────────────────────────────────────────────────┘
```

### 3.1 Definizione proposta di Graphic Authority

> **Graphic Authority è la policy che stabilisce che la presentazione visiva è
> governata da un contratto, non da chi genera il contenuto.**

Conseguenza diretta: quando X arricchisce una pagina — con osservazioni, estrazioni,
modelli proposti — **non può inventare linguaggio visivo nuovo**. Deve esprimersi
dentro la Graphic Authority vigente.

### 3.2 Perché è la mossa corretta

È la stessa proposizione di ToolJet applicata al visivo:

```text
ToolJet   "agents build against real contracts rather than emitting free-form code"
Nexus     "X enriches pages against Graphic Authority rather than inventing layout"
```

Ed è coerente con decisioni già congelate:

- **D-002** — PageData è il linguaggio, i renderer cambiano. Graphic Authority è
  ciò che impedisce a un renderer di diventare il luogo dove si nasconde la conoscenza.
- **D-005** — page semantics select the renderer, application identity does not.
- **D-007** — infrastructure reusable, domain replaceable.

Senza Graphic Authority, "arricchire le pagine tramite i nostri modelli di
osservazione" produce deriva visiva: ogni arricchimento inventa un modo nuovo di
mostrare, e in sei mesi hai quaranta stili. **La deriva grafica è il drift applicato
alla UI** — e ha lo stesso costo: nessuna singola modifica è grave, l'accumulo
rende il sistema illeggibile.

### 3.3 Cosa deve contenere (da formalizzare)

```text
· token di design vincolanti (colore, spazio, tipografia) — non temi
· inventario chiuso di blocchi componibili
· regole di densità informativa per tipo di contenuto
· politica di accessibilità (contrasto, non solo colore — cfr. Trustable § 3.4)
· versione: graphicAuthority: vN nel bundle
· gate VALIDATE che rifiuta blocchi fuori inventario
```

Il gate è NX-03. **Graphic Authority senza gate è una linea guida, non un contratto.**
Con il gate diventa enforcement, e l'enforcement è quello che tiene quando X genera
da sola.

---

## 4. Local-first con ping Redis

Dichiarazione dell'utente:

> *"se redis manda un ping l'applicazione si sincronizza, altrimenti resta in locale."*

### 4.1 Il pattern

```text
Redis raggiungibile, ping ricevuto
   → l'applicazione si sincronizza → server authority

Redis non raggiungibile / nessun ping
   → l'applicazione resta in locale → local authority
```

È **local-first con sincronizzazione su segnale**, e ha tre proprietà utili:

```text
1. degradazione elegante   il server giù non blocca l'utente
2. costo                   lo stato locale non costa nulla a servire
3. authority esplicita     chi comanda è definito dal raggiungibilità
```

### 4.2 Risolve due debiti aperti

Questo pattern è la risposta a voci che stavano nel backlog da prima:

```text
AF-003 — Server Session Recovery
  "Timeout / fallback / availability Redis"
  → il ping È il meccanismo di availability detection
  → il fallback È "resta in locale"
  → AF-003 non richiede infra nuova, richiede di formalizzare questo pattern

AF-004 — Client Session Reconciliation
  "Più producer scrivono userStore; definire authority e freshness"
  → authority: locale quando offline, server quando il ping arriva
  → freshness: il ping È il segnale di invalidazione
  → AF-004 si chiude definendo il ping come evento di revalidazione
```

**Nota di coerenza col recap ufficiale:** lì si dice che non esistono
`BroadcastChannel` né storage listener, e che il comportamento multi-tab osservato è
condivisione server-side su nuova request. Il pattern qui proposto è **diverso**:
non è sync cross-tab, è sync local↔server. Non contraddice il recap, aggiunge un
livello. Va dichiarato esplicitamente per non creare confusione con
`Cross-tab Auth Synchronization` (P2, "solo se requisito di prodotto").

### 4.3 Effetto sul costo

Conferma la risposta dell'utente: **sì, il local-first cambia il discorso sui costi.**

```text
serving       locale/statico           costo marginale ~zero
sessione      locale con revalidazione nessuna chiamata Redis per request
AI            solo su evento/domanda   vedi § 2.2
```

Il costo residuo concentrato resta uno solo: **l'interpretazione AI**. Che è
esattamente ciò che va meterizzato.

### 4.4 Attenzione

Il local-first introduce un problema che va progettato, non scoperto:

```text
conflitto   due producer scrivono lo stesso stato, offline
perdita     quanto stato locale si può perdere se non sincronizza mai?
sicurezza   dati sensibili persistiti in localStorage? per un broker/CFO
            è materiale regolamentare
TTL         lo stato locale scade?
```

Il punto sicurezza è serio per la persona dichiarata: un responsabile finanziario
che esplora il mercato lascia tracce locali. Va deciso **prima**, non dopo.

---

## 5. Connettività: copiare l'interfaccia, non la libreria

L'utente propone di copiare da ToolJet la *"connettività con provider e db"*.

### 5.1 Cosa ha ToolJet

```text
90+ data source / 100+ integrazioni
directory plugins/ nel repo
ToolJet CLI (@tooljet/cli) per creare plugin
marketplace/
```

### 5.2 Cosa NON copiare

Costruire 90 connettori è lavoro da team per anni. È il loro fossato, non il tuo,
e provarci ti dissangua prima di arrivare al prodotto.

### 5.3 Cosa copiare

```text
L'INTERFACCIA del plugin, non la libreria dei plugin.
```

E per la persona dichiarata i connettori che contano sono **pochi e profondi**:

```text
priorità 1   feed di mercato / dati finanziari
priorità 2   sorgenti documentali interne (PDF, fogli, export ERP)
priorità 3   API REST generiche + GraphQL (copre l'80% del resto)
priorità 4   PostgreSQL / ToolJet-DB-like (già presente: redis console, catalog)
```

Regola: **narrow and deep**, non wide and shallow. Un broker non ha bisogno di
Airtable. Ha bisogno che il suo feed sia affidabile, puntuale e verificabile.

### 5.4 Vincolo architetturale

Un connettore è un **provider di dati**, non Runtime. Stesso principio di
`EnvironmentProvider` in P-004 e dei provider in DiscoveryService:

```text
il connettore produce dati normalizzati
il bundle li dichiara
il Runtime non osserva il connettore, osserva l'artefatto
```

Se un connettore finisce nel request path del Runtime, si ricrea AF-001 in un altro
punto. **Da mettere esplicitamente fra i simboli da non toccare nella spec.**

---

## 6. Sintesi

```text
PERSONA        decision-maker non tecnico (manager, CFO, broker)
               → due tier: Builder (MCP, riga 4) + Decision-maker (X, riga 2)

COSTO          Foundation OSSERVA (deterministico, gratis, continuo)
               X INTERPRETA (AI, metered, su evento o domanda)
               → mai un LLM nel percorso di osservazione continua

CONTRATTI      Identifier Authority (F-01, aperto)
               Page Source Authority (debito, aggravato da D-013)
               Graphic Authority (nuova, da formalizzare + gate)

RESILIENZA     local-first con ping Redis come segnale di sincronizzazione
               → chiude AF-003 e AF-004 senza infra nuova
               → attenzione a conflitti, TTL e dati locali sensibili

CONNETTIVITÀ   copiare l'interfaccia plugin, non la libreria
               pochi connettori, profondi, nel dominio della persona
               mai nel request path del Runtime
```

---

## 7. Nuove voci di backlog

| ID | Azione | Pri | Layer |
|---|---|---|---|
| NX-18 | Formalizzare Graphic Authority + gate in VALIDATE | **P0** | X |
| NX-19 | Regola "nessun LLM nell'osservazione continua": trigger deterministici + batch con tetto | **P0** | X/Brain |
| NX-20 | Local-first con ping Redis → chiude AF-003 e AF-004 | P1 | Execution |
| NX-21 | Interfaccia plugin per connettori (non libreria) | P1 | X |
| NX-22 | Definizione dei due tier Builder / Decision-maker | **P0** | Prodotto |
| NX-23 | Policy dati locali sensibili per persona finanziaria (TTL, cifratura, consenso) | P1 | Legale/Sicurezza |

Nessuna tocca `PageController`, `normalizeToPageData`, `ApplicationDefinition`,
`ApplicationContext`, `BundleCollector`, `DiscoveryService` o `PageData`.
**Tutte in zona sicura.** NX-20 tocca la sessione client, che è già territorio
AF-004, non Runtime contract.

---

*Ultimo aggiornamento: 2026-09-10*
