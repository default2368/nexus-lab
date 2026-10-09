# NX-59 · Tokenizzazione locale dei dati sensibili prima dell'LLM

**Data:** 2026-09-13
**Proposta dell'utente:**

> *"tutti i dati sensibili restano in locale come localStorage. Un layer intermedio
> provvede un codice di occultamento (dovremmo fare un algoritmo) e sincronizza il
> dato con il locale. All'LLM arrivano codici alfanumerici incomprensibili. Costo 0 —
> e pensare che ci sono società che realizzano intero hw e sistemi proprietari per
> LLM locali per proteggere la privacy."*

**Verdetto:** l'idea è corretta, ha un nome consolidato, costa poco e **converge con
la reduction pipeline già progettata**. Ha quattro punti di rottura, di cui uno legale
e uno architetturale. Non va costruita da zero.

---

## 1. Ha un nome, e il fatto che esista è una buona notizia

```text
tokenizzazione / pseudonimizzazione      il termine generale
PII redaction / prompt sanitization      nel contesto LLM
de-identification                        in ambito sanitario/legale
format-preserving encryption (FPE)       se serve reversibilità crittografica
                                         NIST SP 800-38G, algoritmi FF1 e FF3-1
```

Esiste implementazione open source matura:

```text
Microsoft Presidio    MIT license, Python + Docker
                      detection + anonymization di PII
                      registry di recognizer estendibile con recognizer custom
                      fa ESATTAMENTE il "layer intermedio" della proposta
```

**Regola: non scrivere l'algoritmo. Incapsula Presidio e aggiungi i recognizer di
dominio.** Un algoritmo di anonimizzazione scritto da soli è il classico caso in cui
l'errore non si vede: funziona sui tuoi test e fallisce sui dati reali.

Sul punto "società che fanno hardware": esistono ed è un mercato reale — appliance
locali, GPU on-prem, secure enclave, e l'high end è attestazione hardware del tipo
Apple Private Cloud Compute. Trustable/Nuvolaris sta esattamente lì (NuvolarIA
appliance, Private AI, Sovereign AI). Ma **risolvono una minaccia diversa**: vedi § 5.

---

## 2. La convergenza: è la reduction pipeline applicata alla privacy

Questa è la parte più interessante, ed è tua.

```text
COSTO       sorgente grezza  → riduzione       → pochi token all'LLM      450×
PRIVACY     dato sensibile   → tokenizzazione  → codici all'LLM           esposizione ~0
```

**Stessa forma. Stesso posto. Stessa classe.**

```text
entrambe sono:  deterministiche
                locali
                classe 0 (zero token, zero costo marginale)
                prima del confine LLM
                reversibili solo in locale
```

E **si compongono**, nello stesso stadio:

```text
sorgente
  ↓
CONNECTOR          fetch, content_sha, change detection          NX-27
  ↓
REDUCE             estrazione, scoring, riduzione                C-07
  ↓
SANITIZE           tokenizzazione PII                            NX-59  ← nuovo
  ↓
LLM                vede solo token e score                       classe 1
  ↓
DETOKENIZE         riassociazione in locale, mai in transito
  ↓
EXPERIENCE         PageData con riferimenti, non con valori
```

Un solo confine, tre trasformazioni deterministiche. È l'architettura giusta ed è
coerente con tutto il resto: **il confine LLM è l'unico punto dove il dato lascia il
dispositivo, e a quel punto è già ridotto e già tokenizzato.**

---

## 3. Dove si rompe — i quattro punti

### 3.1 Il trade-off fondamentale: strutturale vs semantico

```text
LLM riceve: PERSON_1 ha acquistato ASSET_7 per AMOUNT_3 il DATE_2

PUÒ fare     ragionare sulle RELAZIONI: pattern, sequenze, anomalie strutturali,
             classificazione, coerenza, confronti, aggregazioni
NON PUÒ      giudicare il CONTENUTO: "questa clausola contrattuale è rischiosa?",
             "questa frase è diffamatoria?", "questo referto è coerente?"
```

**Non è un limite del tuo algoritmo: è information-theoretic.** Se il valore
semantico sta nel contenuto, e il contenuto è ciò che nascondi, il valore è nascosto.

Conseguenza di progettazione, ed è la cosa da decidere prima di scrivere codice:

> Per ogni caso d'uso va dichiarato se il compito è **STRUTTURALE** o **SEMANTICO**.
> I compiti strutturali vanno in tokenizzazione. I compiti semantici o restano in
> locale senza LLM, o richiedono un modello locale, o richiedono consenso esplicito.

Non esiste una terza via. Chiunque prometta "AI su dati sensibili senza esporli" per
compiti semantici sta mentendo o sta usando hardware locale.

### 3.2 Re-identificazione

Mascherare i nomi non basta: **la combinazione di attributi identifica**.

```text
"donna, 47 anni, giudice, Savona, due figli"
→ il nome è mascherato, la persona è unica
```

Il risultato classico sull'87% della popolazione USA identificabile da
CAP + data di nascita + sesso vale ancora, e peggiora con corpus piccoli.

**Per il verticale che hai dichiarato — PA, giustizia, conoscenza civica — questo è
il punto critico.** Un atto giudiziario è intrinsecamente identificante: le parti, il
tribunale, la data, il tipo di procedimento. Tokenizzare i nomi e lasciare il
contesto non anonimizza niente.

Mitigazione parziale: generalizzare anche gli attributi (età → fascia, data →
trimestre, luogo → regione). Ma ogni generalizzazione riduce l'utilità, e si torna al
punto 3.1.

### 3.3 Il testo libero

```text
NER masking funziona su:  nomi, date, importi, codici fiscali, IBAN, email, telefoni
NER masking fallisce su:  il testo libero, che è dove il PII vive davvero

"l'imputato ha incontrato il sindaco al bar Rossi"
 → maschera "Rossi", restano "sindaco", "bar", "imputato"
 → in una città piccola la frase resta identificante
```

Ha precision/recall: o lasci passare PII (falso negativo) o mascheri troppo e
distruggi il senso (falso positivo). Non si risolve con un algoritmo migliore, si
gestisce dichiarando il livello di confidenza richiesto per dominio.

### 3.4 `localStorage` è il posto sbagliato per la mappa

Questo è il punto architetturale, ed è correggibile.

```text
localStorage:
  ✗ non cifrato
  ✗ leggibile da qualunque XSS sulla pagina
  ✗ leggibile da qualunque estensione del browser
  ✗ leggibile da chiunque abbia accesso fisico
  ✗ condiviso per tutta l'origin
  ✗ senza scadenza
  ✗ sopravvive al logout
```

E la mappa di tokenizzazione è **l'unico asset che trasforma codici in dati sensibili**.
Chi ha la mappa ha tutto. Metterla in `localStorage` è come cifrare una cassaforte e
lasciare la chiave appesa allo sportello.

Alternative, in ordine di costo:

```text
IndexedDB + WebCrypto (AES-GCM)     chiave derivata da passphrase, mai persistita
                                    → ragionevole, costo zero, resta nel browser
OPFS (Origin Private File System)   meglio per volumi, stessa logica
file locale cifrato via CLI         se c'è un companion locale, è la soluzione migliore
secure enclave / keychain           se disponibile, per la chiave
```

Regola: **la chiave non va mai persistita accanto ai dati.** Derivata da passphrase a
ogni sessione, o custodita dal sistema operativo.

---

## 4. Il punto legale — e per il tuo verticale è quello decisivo

```text
GDPR Art. 4(5)   la PSEUDONIMIZZAZIONE è trattamento di dati personali
GDPR Recital 26  solo i dati ANONIMI escono dal perimetro
                 anonimato = "nessun mezzo ragionevolmente utilizzabile"
                             per re-identificare
```

**Se tu conservi la mappa, è pseudonimizzazione, non anonimizzazione.**

Conseguenze:

```text
· i token inviati a un provider LLM restano dati personali
· serve comunque base giuridica
· se il provider è extra-UE, resta un trasferimento internazionale
  → servono garanzie (SCC, adeguatezza)
· la tokenizzazione RIDUCE il rischio, non elimina l'obbligo
· per un ente pubblico italiano il DPO valuterà il trasferimento,
  non la tecnica
```

Questo non invalida l'idea — la ridimensiona. La formulazione corretta è:

```text
SBAGLIATO   "i dati sensibili non lasciano il dispositivo"
            → falso se la mappa permette di ricostruirli e il provider riceve token

CORRETTO    "il contenuto sensibile non lascia il dispositivo;
             all'LLM arrivano pseudonimi non re-identificabili
             senza la mappa locale"
            → vero, difendibile, e comunque un miglioramento sostanziale
```

La seconda formulazione è vendibile. La prima no, e se la scrivi in un documento
commerciale per la PA ti torna indietro in gara.

---

## 5. Perché l'hardware esiste comunque

Le appliance locali non risolvono la stessa minaccia.

```text
TOKENIZZAZIONE    protegge il CONTENUTO dal provider
                  il provider vede comunque: metadati, timing, volume,
                  struttura della richiesta, e i token

MODELLO LOCALE    elimina il TRASFERIMENTO
                  niente esce, quindi niente metadati, niente timing,
                  niente dipendenza da un terzo
```

Per un hedge fund la tokenizzazione basta. Per una procura, un ospedale o un
ministero **il trasferimento stesso è il problema**, e nessun token lo risolve.

Ed è esattamente perché Trustable/Nuvolaris vende appliance e non algoritmi: il loro
cliente compra l'eliminazione del trasferimento, non la riduzione del contenuto.

**Ma** — e qui la tua intuizione sul costo è giusta — per una fascia enorme di casi
la tokenizzazione + **modello hostato in UE** copre il requisito a costo quasi zero
invece che a decine di migliaia di euro. Regolo.AI, che Trustable usa per Sovereign
AI, è esattamente quel pezzo.

Combinazione che ha senso, ed è la tua:

```text
dati sensibili in locale (cifrati, non localStorage nudo)
  ↓
riduzione + tokenizzazione deterministica in locale
  ↓
modello UE (Regolo.AI) o endpoint privato OpenAI-compatible
  ↓
artifacts compilati che servono anche senza nulla di questo (D-017)
```

Costo: un algoritmo incapsulato + un provider UE. Contro: un appliance.

---

## 6. Il claim di prodotto onesto

```text
CLAIM ECCESSIVO
  "AI su dati sensibili senza che escano dal dispositivo"
  → falso per compiti semantici, e falso giuridicamente se conservi la mappa

CLAIM DIFENDIBILE
  "Open Nexus esegue lavoro di conoscenza assistito da AI su corpus sensibili
   mantenendo il contenuto sul dispositivo: all'LLM arrivano pseudonimi e
   riduzioni deterministiche, per i compiti esprimibili su struttura e relazioni.
   I compiti che richiedono il contenuto restano locali, senza LLM
   o su modello locale/UE."
```

Più stretto, meno vendibile a prima lettura, e **sopravvive a un DPO**. Per il
verticale PA/giustizia è l'unica delle due che passa una gara.

---

## 7. Sequenza — importante

**Questa capacità non serve al pilota.**

```text
pilota (analisi di mercato)    oggetti PUBBLICI: siti, repo, doc, pricing
                               → zero dati sensibili → NX-59 non si applica

verticale civico / PA          atti, delibere, sentenze, dati personali
                               → NX-59 è PREREQUISITO, non optional
```

Quindi:

```text
1. il pilota procede senza NX-59                     (NX-56, NX-57)
2. NX-59 entra quando entra il verticale civico      (NX-30, NX-49)
3. non costruire NX-59 prima di aver scelto il verticale,
   perché il livello di mascheramento richiesto dipende dal dominio
```

Costruire adesso un algoritmo di anonimizzazione senza un dominio concreto produce
un componente che non protegge niente di specifico — il caso classico di sicurezza
generica che fallisce sul caso reale.

---

## 8. Cosa fare, se e quando

```text
1. incapsulare Microsoft Presidio (MIT), non scrivere un algoritmo
2. la mappa sta in IndexedDB + WebCrypto AES-GCM, chiave derivata da passphrase
   mai persistita. NON in localStorage.
3. dichiarare per ogni caso d'uso: STRUTTURALE o SEMANTICO
4. aggiungere recognizer di dominio (codice fiscale, IBAN, protocollo,
   numero di ruolo, RGA, riferimenti a procedimenti)
5. generalizzare anche gli attributi, non solo i nomi (età→fascia, data→trimestre)
6. loggare cosa è stato mascherato CON QUANTI CONFIDENCE, in locale
7. formulare il claim come in § 6, non come in § 6 riga 1
8. verificare con un DPO prima di scriverlo in un documento di gara
```

E una tensione da risolvere in progettazione:

```text
tokenizzazione STABILE (stesso input → stesso token)
  → necessaria per change detection (content_sha, NX-27)
    e per coerenza fra viste della stessa experience
  → ma abilita analisi di frequenza: se AMOUNT_3 ricorre 400 volte,
    il provider impara qualcosa

tokenizzazione per-sessione (sale)
  → nessun leakage di frequenza
  → ma rompe change detection e coerenza fra sessioni
```

Soluzione probabile: **stabile per entità, per-sessione per valori numerici**.
Va deciso per dominio, non in astratto.

---

## 9. Backlog

```text
NX-59  NUOVO P2 — tokenizzazione locale prima del confine LLM.
       PREREQUISITO del verticale civico/PA, NON del pilota.
       Non prima di NX-30: il livello di mascheramento dipende dal dominio.

NX-60  NUOVO P3 — verifica con DPO della formulazione del claim privacy,
       prima che compaia in qualunque documento pubblico o di gara.

AGGIORNAMENTO C-07 (21-CAPACITA-OPENNEXUS.md)
       la reduction pipeline ha un terzo stadio: SANITIZE, fra REDUCE e LLM.
       Stessa classe, stesso confine, stessa natura deterministica.
```

**Zona sicura:** NX-59 vive nel confine fra `modules/reduce/` e `modules/providers/`.
Non tocca Runtime, PageData né alcun simbolo vincolato. Va nel Brain.

---

*Ultimo aggiornamento: 2026-09-13*
