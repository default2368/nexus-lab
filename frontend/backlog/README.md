# Frontend Operational Backlog

Questo backlog contiene **solo lavoro frontend eseguibile**.

Non contiene brainstorming, analisi di mercato, narrativa, decision log o roadmap
strategica. Quelli restano nel corpus Nexus Lab.

```text
NEXUS-LAB/*                   memoria strategica: perché, ipotesi, decisioni
frontend/backlog/BACKLOG.md   lavoro operativo: cosa facciamo adesso
ADR / test / commit           prova che il lavoro è stato chiuso
```

---

## Regole

### 1. Massimo tre elementi in corso

```text
IN_PROGRESS ≤ 3
P0 aperti   ≤ 2
```

Se entra un quarto elemento, uno dei tre deve tornare `READY`, diventare `BLOCKED` o
essere chiuso.

### 2. Una voce deve essere eseguibile

Ogni voce deve contenere:

```text
ID
release target
stato
priorità
problema osservato
una sola prossima azione
Definition of Done verificabile
fonte/provenienza
```

Se manca una prossima azione fisica, non è un task: resta nel corpus strategico.

### 3. Stati ammessi

```text
READY        può essere iniziato senza altre decisioni
IN_PROGRESS qualcuno ci sta lavorando
BLOCKED      dipende da una condizione esplicita
PARKED       valido, non nel percorso attuale
DONE         Definition of Done verificata
```

Niente “quasi fatto”, “in valutazione”, “importante”.

### 4. Priorità

```text
P0  blocca una release, un altro task o rende la demo ingannevole
P1  importante per la release target, non blocca il resto
P2  miglioramento pianificato
P3  idea valida, senza impegno
```

Un P0 deve dire **cosa blocca**.

### 5. Promozione dal corpus strategico

Una discussione entra qui soltanto quando:

```text
· il problema è osservato
· la decisione architetturale è presa o non necessaria
· la prossima azione è chiara
· la DoD si può verificare con test, comando o screenshot
```

Il campo `Fonte` conserva la provenienza (`ADR-*`, `NX-*`, screenshot, test), ma la
voce deve essere comprensibile senza aprire quei documenti.

### 6. Chiusura

Per chiudere una voce servono:

```text
· test/comando/screenshot previsto dalla DoD
· commit o PR
· eventuale ADR aggiornato
```

Dopo la chiusura la voce passa nella sezione `DONE` di `BACKLOG.md` con una riga.
Il dettaglio resta nel commit e nell’ADR, non viene duplicato.

### 7. Igiene

Quindici minuti a settimana:

```text
1. verificare i tre IN_PROGRESS
2. rimuovere i blocchi risolti
3. scegliere il prossimo READY
4. archiviare i DONE
5. nessun riordino generale della documentazione
```

Se la manutenzione richiede ore, il backlog ha fallito.
