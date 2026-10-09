# Stato di salute di Nexus Lab — non di Open Nexus

**Data:** 2026-09-12
**Perché questo documento esiste:** `16-FOUNDATION-HEALTH.md` misura **Open Nexus**,
l'artefatto. Questo misura **Nexus Lab**, l'ente che produce artefatti. Sono due
griglie diverse e danno due numeri diversi.

**Occasione:** feedback esterno (PM/architetto) sul documento 16, che l'utente
definisce *"un po' più hype"*. Qui si prende ciò che il feedback aggiunge, si estende
il suo concetto migliore, e si nomina ciò che non può vedere.

---

## 1. Cosa il feedback esterno aggiunge davvero

Tre contributi veri, che il documento 16 non conteneva.

### 1.1 La comparazione sul problema

```text
Molti progetti:  contratti fragili → design assente → refactor impossibili
Open Nexus:       governance del design sofisticata → collo di bottiglia
                 spostato sui contratti applicativi
```

Il documento 16 diceva "c'è un'asimmetria". Il feedback dice **in che direzione sta
l'asimmetria rispetto al fallimento tipico**, che è l'informazione utile. Un problema
di enforcement dei contratti in un sistema che ha già governance del design è un
problema di rifinitura. Lo stesso problema in un sistema senza governance è
strutturale. Voto confermato, diagnosi meglio posizionata.

### 1.2 "Queste non sono feature. Sono anticorpi."

La frase migliore del feedback. Exception registry, scadenze, `reason` obbligatorie,
tracciabilità delle decisioni: non sono funzionalità, è **sistema immunitario**.

Vale la pena estenderla, perché un sistema immunitario ha due malattie specifiche e
**entrambe sono già visibili nel repo**.

### 1.3 "Un'app tollera `as any`. Una Foundation no."

Diagnosi corretta e più netta della mia. Il documento 16 classificava `as any` come
odore. Il feedback lo riclassifica come **residuo di pensiero-da-app dentro una
piattaforma**. Non è sciatteria: è l'abitudine di quando il sistema era un'app,
sopravvissuta al cambio di natura.

Questo cambia la correzione: non si tratta di "mettere i tipi giusti", si tratta di
decidere che **il punto di scrittura di un contratto è un confine di piattaforma**.
NX-38 non è cleanup, è cambiamento di statuto.

---

## 2. Le due malattie autoimmuni — già nel repo

Un sistema immunitario attacca ciò che riconosce come estraneo. Fallisce in due modi,
e Open Nexus li presenta entrambi.

### 2.1 Autoimmunità: l'anticorpo attacca il tessuto nuovo

```text
tests/contracts/artifact-consumption-closure.test.ts
  garantisce che APPLICATION_TYPE_PROJECTION sia pari all'output di BundleCollector
  → oggi protegge dal drift                                   ✅
  → a 0.7.0, un bundle autorato da AI/Importer aggiunge un appId
  → la projection manuale non lo contiene
  → il test FALLISCE
  → il test blocca l'authoring                                ❌
```

**L'anticorpo attacca il tessuto nuovo.** È NX-11, ed è già a backlog — ma vale la
pena nominarlo per quello che è: non un debito tecnico, è **il primo caso di
governance che diventa ostruzione**. Ce ne saranno altri, perché ogni test di parità
su una materializzazione manuale ha questa proprietà.

Regola che ne discende:

> Ogni garanzia di parità su un artefatto **scritto a mano** è una garanzia che
> scade quando l'artefatto smette di essere scritto a mano.
> Va marcata come temporanea nel momento in cui si scrive, non scoperta dopo.

### 2.2 Siti privilegiati: dove il sistema immunitario non pattuglia

```text
EXCEPTIONS:
  legacy-frozen:webpage-template   expires: frozen
  legacy-frozen:pages              expires: frozen
    scope: [..., 'src/pages/build/', ...]     ← match a prefisso
```

Un'eccezione `frozen` è un sito che l'organismo ha deciso di non pattugliare.
Corretto per codice davvero morto. Ma:

```text
src/pages/build/ contiene [...component].astro = il punto d'ingresso di EXECUTION
inScope usa startsWith → tutto ciò che verrà aggiunto lì è esente per costruzione
```

**I siti privilegiati sono esattamente dove le infezioni attecchiscono**, perché
nessuno li guarda. E la scadenza sta nel doc ma non nel dato (NX-46), quindi nulla
impedisce a un'eccezione "temporanea" di diventare `frozen` per inerzia.

Regola:

> Un'eccezione senza scadenza machine-enforced non è un'eccezione.
> È una zona franca con una data di nascita e nessuna di morte.

### 2.3 Perché queste due cose vanno dette adesso

Perché la governance è il risultato migliore della sessione, e i sistemi di governance
non falliscono per assenza — falliscono per **eccesso di fiducia in se stessi**.
Hai costruito gli anticorpi in tre settimane e funzionano. Il rischio non è che
smettano di funzionare: è che smettano di essere messi in discussione.

---

## 3. Griglia di salute di Nexus Lab

Dimensioni diverse da quelle di Open Nexus. Un artefatto si misura su boundary e
contratti; un ente si misura su capacità.

| # | Capacità | Voto | Evidenza |
|---|---|---|---|
| 1 | **Produrre** | **A** | 5 stratificazioni, 0.4.x → 0.7.0, refactor invasivo senza regressioni |
| 2 | **Misurarsi** | **A−** | 21 test authority, parity test, style checker con baseline pubblicata (554/33). Manca: strumentazione costo (NX-24), stato suite globale |
| 3 | **Scegliere dove** | **D** | NX-30 aperto. Nessun verticale. Nessuna conversazione con un utente a verbale. Persona dichiarata da due giorni e già in contraddizione con `audience` |
| 4 | **Distribuire** | **D+** | NX-01, NX-01b, NX-14 tutti aperti. Le config degli strumenti puntano ancora a un model ID ritirato dal 10 settembre |
| 5 | **Sostenere** | **B** | Struttura di costo capita (450× dalla reduction, classi 0–4), ma non strumentata. `< 10 €/mese` è oggi una disciplina, non una struttura |
| 6 | **Apprendere dall'esterno** | **B+** | Quattro benchmark analizzati in una sessione, un incidente di provider intercettato. Ma è tutta ricerca a tavolino: zero conversazioni |
| 7 | **Riprodursi** | **n/a** | Correttamente sequenziato: NX-33 bloccato da NX-31. Non è un'assenza, è un ordine |

**Sintesi Nexus Lab: C+ / B−**
**Sintesi Open Nexus: B+ / A−**

### 3.1 La frase che esce dalla differenza

> **L'artefatto è più sano dell'ente che lo produce.**

È la condizione normale di un fondatore tecnico singolo, ed è la condizione che uccide
i progetti — non il codice. Il codice sta benissimo. Quello che non esiste ancora è
la capacità di scegliere **dove** il codice va a finire.

Confronto con i benchmark, che rende la cosa concreta:

```text
AlphaSense   architettura irrilevante · contenuto 500M · $350M
Hebbia       RAG naive falliva 84% · forward-deployed engineers · 250 clienti
Rogo         35.000 professionisti · single-tenant · SOC2/ISO27001
Aiera        contract layer + MCP sopra contenuti altrui

Open Nexus    architettura eccellente · contenuto 0 · clienti 0
```

Loro hanno la colonna 2 e 3 piene e la colonna 1 vuota. Tu hai la colonna 1 piena e
le altre due vuote. **Nessuno dei due profili è sufficiente**, ma il tuo è quello che
si riempie più lentamente se non ci lavori esplicitamente — perché la colonna 1 si
riempie scrivendo codice, che è ciò che sai fare, e le altre due si riempiono
parlando con estranei, che è ciò che non hai ancora fatto.

---

## 4. La divergenza sul backlog

Il feedback propone:

```text
P0  NX-38   elimina bypass del contratto (as any)
P0  NX-39   restringe i tipi al contratto reale
P1  NX-42   completa il modello audience
P1  NX-11   generazione materializzazione
P2  expiry nelle eccezioni
P2  scope src/pages/build/
```

Concordo su tutti e sei, e promuovo NX-38/39 a P0 come proposto. Ma:

```text
sono sei voci INTERNE. Tutte.

assenti:  NX-30  il verticale                     (P0 strategico)
          NX-45  PageData ammette escape hatch?   (decide la forma del gate)
          NX-14  nexus-mcp                        (unica struttura di costo
                                                   sopravvissibile a scala)
```

Non è un errore del feedback: è la **natura** di un feedback da PM su un report di
salute interna. Un PM ottimizza per il backlog eseguibile, e l'eseguibile è sempre
interno. NX-30 non è eseguibile domani: richiede di parlare con qualcuno.

**È esattamente la trappola che ho nominato due volte nella sessione**, e il fatto
che un feedback competente e ben intenzionato ci caschi dentro naturalmente è la
prova che la trappola è strutturale, non disciplinare. Non si evita essendo più
attenti. Si evita avendo una voce di backlog che non può essere eseguita da soli.

---

## 5. Il contrappeso onesto alla validazione

Il feedback conclude:

> *"la struttura mentale che hai costruito sta iniziando a produrre evidenze
> misurabili di coerenza architetturale."*

Vero, misurato, e meritato. Ma va detto anche il resto:

> **Coerenza interna non è valore.** Un sistema può essere perfettamente coerente e
> perfettamente inutile.

La sessione ha prodotto il controesempio: AlphaSense, Hebbia e Rogo non hanno una
coerenza architetturale che valga la pena nominare, e hanno 250 istituzioni clienti.
La coerenza è la tua lingua madre — ed è anche la tua zona di comfort, il che è
lo stesso problema detto in modo gentile.

Il rischio non è che tu smetta di essere rigoroso. Il rischio è che **il rigore
diventi il sostituto del contatto col mercato**, perché il rigore è misurabile,
leggibile e auto-validante, mentre il contatto col mercato non è nessuna delle tre.

Un indicatore concreto: questa sessione ha prodotto sedici documenti e zero
conversazioni con un potenziale utente. Il rapporto va invertito, non bilanciato.

---

## 6. "Un sistema che ti risponde"

La parte più profonda del feedback:

> *"Quando eri da solo con idea → ipotesi → intuizione, non avevi modo di sapere se
> avevi ragione. Adesso hai test, authority, contract, artifact closure, review
> indipendenti. Quindi quando fai un refactor enorme e non succede nulla, non è più
> una sensazione. È un dato."*

È corretto, e questa sessione ne è la dimostrazione — ma in una direzione che il
feedback non nota.

```text
Quattro ipotesi formulate dall'assistente:
  1. AF-001 come prerequisito commerciale      → falsificata dai file
  2. Graphic Authority come novità             → esisteva già, decomposta meglio
  3. "scommetto sul primo caso" su Q-005       → grep cercava nomi, non valori
  4. D-027 "valore senza fonte dichiarativa"   → fonte documentata e testata

Quattro su quattro smentite dall'evidenza.
```

**Un sistema che ti dà sempre ragione non è un sistema che ti risponde.**
Il tuo ha risposto smentendo un revisore esterno quattro volte di fila, e il
revisore ha dovuto correggersi ogni volta. È la proprietà più rara che un sistema
possa avere, ed è la stessa proprietà che fa sì che un refactor invasivo non produca
regressioni: **la realtà interna vince sull'opinione esterna.**

Vale per il codice e vale per i feedback — incluso questo documento, incluso il
feedback che l'ha provocato, inclusi i miei sedici file. La regola di verifica è la
stessa di `03-WORKFLOW.md`: ogni affermazione su cosa esiste cita il comando che
l'ha prodotta.

---

## 7. Priorità a livello Lab

Non coincidono con le priorità a livello artefatto, ed è normale.

```text
LIVELLO OPENNEXUS (artefatto)          LIVELLO NEXUS LAB (ente)
──────────────────────────────────────────────────────────────────────
P0  NX-38 via as any                   P0  NX-30 il verticale
P0  NX-39 tipi stretti                     → l'unica voce che non puoi
P1  NX-42 audience                             eseguire da solo
P1  NX-11 materializzazione generata   P0  NX-25 bonifica config model ID
P2  NX-46 expiry nel dato                  → il provider ha ritirato un ID
P2  NX-47 scope src/pages/build              e i tuoi strumenti non lo sanno
                                       P1  NX-14 nexus-mcp
                                           → unica struttura di costo
                                             sopravvissibile a scala
                                       P1  NX-45 escape hatch in PageData
                                           → decide la forma del gate
```

Le due colonne vanno eseguite **in parallelo**, non in sequenza. La colonna sinistra
è ciò che sai fare e ti dà evidenze. La colonna destra è ciò che non hai ancora fatto
e ti dà un mercato.

Se devi sceglierne una sola oggi: **NX-25**, perché è un incidente attivo — le config
puntano a un modello ritirato dal 10 settembre e il fallback silenzioso del provider
è il caso peggiore.

Se devi sceglierne una sola questa settimana: **NX-30**, perché è l'unica che cambia
il significato di tutte le altre.

---

## 8. Chiusura

Il feedback dice che sei passato da *"qual è la tesi?"* a *"la tesi è abbastanza
forte da sopravvivere a un refactor violento?"*.

È vero, ed è un passaggio reale. Ma c'è una terza domanda, e nessuna delle due
riguarda il codice:

```text
1. Qual è la tesi?                                    → risposta: c'è
2. La tesi sopravvive a un refactor violento?         → risposta: sì, cinque volte
3. A chi serve la tesi, e chi paga?                   → risposta: non ancora
```

Le prime due le hai chiuse. La terza è NX-30, non richiede una riga di codice, ed è
l'unica che determina se le prime due valgono qualcosa.

**Open Nexus è sano. Nexus Lab non è ancora un ente che sa scegliere.**
Si costruisce, e si costruisce più in fretta di quanto tu abbia costruito Foundation
— perché non richiede architettura, richiede conversazioni.

---

*Ultimo aggiornamento: 2026-09-12*
