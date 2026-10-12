# Nota tecnica opzionale per F. — 2 pagine max — solo se richiesta

**Denominazioni provvisorie — non consegnare automaticamente**
Puoi dire: "Ho anche due pagine più tecniche, se mai ti interessassero."

---

## Piattaforma

Infrastruttura per produrre e verificare applicazioni di conoscenza in modo riproducibile, con contratti, gate e provenienza. Base tecnica chiusa per distribuzione: contratti pubblici, discovery su artefatti, renderer minificato, interfaccia a riga di comando. Parte remota mai distribuita: compilatore, validatore, registro versionato, telemetria che compone.

Disponibile: infrastruttura e contratti, artefatti distribuibili, provenienza e controlli, esperienza su più applicazioni.

## Motore documentale

Acquisizione con preservazione byte/hash, estrazione struttura (intestazioni, liste, tabelle), record e relazioni, claim con fonte e metadati epistemici (osservato/inferito/proposto/sconosciuto/limite). Classe 0 deterministica, costo zero, senza lettura diretta repository da runtime.

In sviluppo: acquisizione documenti, risposta con fonti e metadati, interfaccia di ispezione, dossier sintetico per G.

## Interfaccia

Applicazione per navigare dossier, ispezionare evidenze, vedere gap e conflitti, correggere modello. Risposta epistemica con fonti, metadati, traccia di valutazione. Modalità conversazionale ed epistemica separate.

## Strumenti operativi

Workspace esportabile con contesto progetto, manifest, lock, snapshot Git. Receipt di verifica immutabile per esecuzione (identità repository, commit, stato worktree, comando, risultato, scope). Report di divergenza. Modello di lettura ricostruibile derivato da receipt.

Da validare: uso reale, committente e sostenibilità, tempi di adozione, secondo dominio.

## Contratti e roadmap tecnica

- Foundation 0.8.2: chiusura sicurezza/convergenza superfici/release — P0 critical path
- Assistant: normalizzatore risposta /evaluate, console diagnostica, upload Markdown verso API acquisizione — P1 parallel
- Brain: conformità buste claim, traccia valutazione, acquisizione Markdown M1 con gate dimensione/tipo, SHA-256, blob evidenza grezza, osservazione sorgente, ricevuta acquisizione — P1 parallel
- CLI: contratti contesto progetto, manifest workspace, snapshot Git, ricevuta verifica, ricevuta handoff — P2 contract/design lane, implementation conditional
- G. pilot: North Star — riconoscimento/correzione dossier
- Ecosystem governance: parked, non blocking — separate authority YES, new repository REVIEW_REQUIRED

## Come è stata preparata questa nota

Questa nota è stata redatta con il supporto di strumenti di intelligenza artificiale a partire dal materiale prodotto durante lo sviluppo: decisioni, test, report, problemi, correzioni e confronti. L'AI ha aiutato a collegare e sintetizzare questi contenuti; le fonti, le distinzioni fra fatto e proposta e la forma finale restano sottoposte a revisione umana. È un piccolo esempio dello stesso metodo proposto dal progetto: utilizzare ciò che è già documentato senza perderne origine, contesto e limiti.

---

*Nota tecnica — dettagli implementativi non rilevanti per valutazione progettuale — denominazioni interne provvisorie — 2 pagine max*
