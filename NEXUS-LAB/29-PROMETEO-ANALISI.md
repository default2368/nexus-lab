# Analisi della scansione PrometeoRifiuti — il soggetto mancante

**Data:** 2026-09-15
**Fonte:** `25-SCANSIONE-PROMETEO-RIFIUTI.md` (ricevuta; NX-87 chiuso)
**Contesto:** `28-PROMETEO-RENTRI.md`, D-053 → D-059

---

## 0. Cosa la scansione stabilisce

PrometeoRifiuti è un **gestionale verticale esistente e consolidato**:

```text
vendor        Informatica EDP
copertura     registri carico/scarico · formulari e XFIR · MUD · RENTRI
              autorizzazioni e scadenze · giacenze · contratti · pianificazione
              DDT e rapportini · fatturazione · magazzino MPS/EOW
              dashboard · integrazione contabilità
              gestione di produttori, trasportatori, destinatari, intermediari,
              consulenti e associazioni
scala         2.000+ installazioni · 3.000+ aziende (dichiarazione del fornitore)
prezzo        da €125/utente/mese (catalogo Capterra, NESSUNA recensione mostrata
              → dato di listino, non verifica commerciale)
```

Questo chiude **K4** in modo diverso da come era stato impostato in `28-...` § 3.2:

```text
pavimento open source     ASSENTE (confermato)
pavimento COMMERCIALE     PRESENTE, FORTE, INCUMBENT
                          3.000 aziende, dominio, dati, workflow, canale, supporto
```

**Non è un mercato vuoto. È un mercato con un incumbent verticale maturo.**

---

## 1. Cinque cose che la scansione azzecca

Vanno dette, perché sono disciplina rara:

### 1.1 "Prometeo ha già una Foundation verticale" (§ 4)

E la conclusione corretta:

> *"Open Nexus non dovrebbe sostituirlo né ricostruire un gestionale rifiuti generico.
> La connessione più plausibile è un semantic/evidence layer sopra un sistema
> operativo già esistente."*

È la **posizione di Aiera** identificata in `12-MERCATO-CONOSCENZA.md`: layer di
accesso, conoscenza ed evidenza sopra sistemi e contenuti altrui. Arrivarci
indipendentemente, su un dominio diverso, è una conferma del metodo.

### 1.2 § 7.5 Potere dell'incumbent

```text
Prometeo possiede: dominio · dati · workflow · conoscenza regolatoria
                   canale clienti · supporto
"Open Nexus non dovrebbe entrare come concorrente frontale senza un
 vantaggio molto specifico."
```

Onestà che manca nella maggior parte delle analisi di questo tipo.

### 1.3 § 7.4 L'integrazione NON è verificata

> *"non è stata verificata un'API pubblica generale di Prometeo... Quindi non va
> assunto che l'integrazione sia tecnicamente o commercialmente disponibile."*

È il blocco operativo principale ed è dichiarato invece che nascosto.

### 1.4 § 8 Percorso 1 — overlay read-only

```text
export CSV / PDF / dati autorizzati → normalizzazione → query con evidenze
→ dashboard / dossier / alert
```

Nessuna modifica al transazionale, rischio contenuto, dimostrazione rapida. È
l'ingresso corretto e non richiede l'accordo con Informatica EDP.

### 1.5 § 19 Il test architetturale

> *"La sonda deve stressare Foundation, non costringerla a diventare Prometeo."*

Con la regola di promozione: *una capacità entra nel core solo se serve anche a una
seconda applicazione nominata.* È D-040 applicato correttamente, senza che il
documento ci avesse letto.

---

## 2. Il buco: il soggetto non è deciso

La scansione lo **sa** e lo dichiara in § 12 e § 16, ma poi produce comunque
opportunità per entrambi i soggetti senza scegliere.

```text
§ 12.A  utenti di PrometeoRifiuti
        produttori · trasportatori · destinatari · intermediari · consulenti · associazioni
        → Opportunità A–E (§ 5), MVP Waste Evidence Assistant (§ 9)

§ 12.B  gestori del sito e della comunicazione Prometeo
        → § 13 bisogni ipotizzati, § 15 Prometeo Knowledge Experience

§ 16    "il potenziale cliente potrebbe essere Informatica EDP,
         non l'utente finale di Prometeo"
```

**Sono due prodotti diversi, con payer diversi, cicli di vendita diversi e rischi
diversi.** La scansione li contiene entrambi e non decide, perché non sa chi è A.

### 2.1 L'ambiguità sta in quattro parole

> *"guarda questi siamo noi"*

```text
se A. è dentro/accanto a Informatica EDP
   → "siamo noi" = il vendor
   → il prodotto è il § 13-15: layer editoriale e di conoscenza
   → il payer è il vendor
   → ciclo B2B lungo, ma il bisogno è fuori dalla competenza core dell'incumbent

se A. è un consulente / associazione / avvocato che USA o assiste chi usa
   → "siamo noi" = gli utenti
   → il prodotto è il § 9: Waste Evidence Assistant
   → il payer è lo studio / l'associazione / l'azienda
   → ciclo più corto, ma il bisogno è DENTRO la competenza core dell'incumbent

se A. è un avvocato che assiste aziende in contenzioso ambientale
   → "siamo noi" = chi deve difendersi o provare
   → il prodotto è un terzo, che la scansione non nomina: vedi § 4
   → il payer è lo studio legale o l'assicurazione
```

**Non si procede oltre senza questa risposta.** Ed è una domanda da una riga, non
da un'intervista.

---

## 3. Il secondo buco: due opportunità sono già dell'incumbent

La scansione descrive in § 2.1 cosa fa Prometeo:

> *"Prometeo comunica il valore attraverso **alert su autorizzazioni scadute, limiti
> di giacenza e incongruenze**, oltre alla compilazione dei documenti e il dialogo
> con RENTRI."*

E in § 5 propone come **Opportunità A**:

```text
quali formulari sono incompleti?
quali autorizzazioni scadono nei prossimi 30 giorni?      ← Prometeo lo fa
quali rifiuti sono prossimi al limite di giacenza?         ← Prometeo lo fa
quali movimenti non hanno corrispondenza?                  ← Prometeo lo fa
quali dati MUD sembrano incoerenti?
```

Stessa cosa per **Opportunità E**:

> *"Prometeo già produce webinar e documentazione su RENTRI."* (§ 5.E)

**Quindi le due opportunità presentate come più coerenti sono già coperte
dall'incumbent.** La scansione lo dice in § 2.1 e non lo collega a § 5. Non è un
errore di raccolta: è un mancato collegamento.

Conseguenza:

```text
Opportunità A   controllo documentale, scadenze, incongruenze   → COPERTA
Opportunità E   knowledge layer RENTRI, formazione              → COPERTA
Opportunità B   dossier di audit con fonti                      → PARZIALMENTE
Opportunità C   network consulenti/associazioni multi-azienda   → DA VERIFICARE
Opportunità D   analisi circolarità e costi                     → PARZIALMENTE (dashboard)
§ 13-15         layer editoriale del sito/vendor                → SCOPERTA
```

---

## 4. L'apertura reale: ciò che un gestionale non può fare per costruzione

Un gestionale transazionale memorizza **lo stato corrente**. Registra il movimento,
la scadenza, il formulario, l'autorizzazione. Lo fa bene, ed è il suo mestiere.

Quello che strutturalmente **non** fa:

### 4.1 Ricostruzione probatoria versionata

```text
in un contenzioso o in una sanzione la domanda non è
  "qual è lo stato attuale?"
ma
  "qual era lo stato AL MOMENTO DEL FATTO, secondo la norma ALLORA vigente,
   e con quali prove documentali?"
```

Serve:

```text
· la versione della norma applicabile in quella data
· lo stato del registro in quella data
· chi ha fatto cosa, quando, con quale autorizzazione allora valida
· la catena documentale completa e non alterabile
· la distinzione fra dato osservato, inferenza e conclusione
```

È **forense**, non gestionale. E richiede esattamente tre cose che Open Nexus ha e un
gestionale non ha motivo di avere:

```text
Source Authority      ogni affermazione risale a fonte, data, versione
versioning            la norma di allora, non quella di oggi
evidence citation     la traccia che un avvocato può firmare
```

La scansione ci arriva senza nominarla, in § 4.1:

```text
affermazione → evento/documento → fonte → data → versione → stato di validazione
```

**Quella catena è il prodotto.** E A. è un avvocato: è l'unica persona del network
per cui quella catena è il lavoro, non un optional.

### 4.2 Layer cross-sistema

Un'azienda reale ha Prometeo **e** fogli di calcolo **e** email **e** magari un altro
gestionale per la contabilità. Un vendor unifica il proprio sistema; non ha interesse
a unificare anche ciò che sta fuori. Un overlay che legge export da qualunque fonte e
produce una vista unica con evidenza **non è nel mestiere dell'incumbent**.

È il Percorso 1 (§ 8) visto dal lato giusto: non "versione leggera in attesa di
integrazione", ma **la cosa che solo un terzo può fare**.

### 4.3 Il layer editoriale (§ 13-15)

Se A. è lato vendor, questa è l'apertura: un gestionale non è bravo a governare
contenuto normativo che cambia e va ripubblicato in dieci formati. Non è il suo
mestiere, e non lo diventerà.

---

## 5. Matrice aggiornata

```text
                          K1   K2   K3   K4    K5   K6   K7   K8
Y-2 generico (28-...)      ✓✓  ✓✓   ✓✓   ✓?    ✓✓   ~    ✗    ✓
Y-2 con K4 verificato      ✓✓  ✓✓   ✓✓   ✗     ✓✓   ~    ✗    ✓
                                       ↑
                              incumbent forte: A ed E sono coperte

Y-2 come layer forense     ✓✓  ✓✓   ~    ✓     ✓✓   ~    ✗    ✓
  (§ 4.1)                            ↑     ↑
                        frequenza episodica  nessun incumbent fa
                        (contenziosi)        ricostruzione probatoria versionata

Y-2 come layer editoriale  ~   ✓    ✓    ✓     ✓    ~    ✗    ✓?
  (§ 4.3, se A. è vendor)  ↑
                    K1 più debole: il team marketing non "rende conto"
                    come un responsabile ambientale
```

**La riga che tiene K1 ✓✓ e guadagna K4 ✓ è il layer forense (§ 4.1).**

---

## 6. La domanda da fare, ed è una sola

Prima delle diciotto domande della scansione (§ 18) e prima delle dieci del documento
Prometeo (§ 8), ne serve una:

> **"Quando dici 'siamo noi', intendi chi fa il software, chi lo usa, o chi assiste
> chi lo usa?"**

Una riga. Determina quale dei tre prodotti esiste.

E la seconda, subito dopo, se la risposta è "avvocato / assistenza":

> **"Quante volte ti è capitato di dover ricostruire cosa era vero in una certa data,
> secondo la norma di allora, e quanto ti è costato?"**

Se la risposta è "spesso" e "molto", § 4.1 è un prodotto. Se è "raramente", il layer
forense è un'idea elegante senza domanda.

---

## 7. Cosa NON fare

```text
· non presentare Open Nexus a Informatica EDP come concorrente del gestionale
· non assumere che esista un'API (§ 7.4)
· non proporre Opportunità A o E: sono già coperte (§ 3)
· non partire dal network (§ 7.6, e la scansione lo dice già)
· non accettare dati reali senza autorizzazione scritta
· non produrre interpretazioni normative automatiche (§ 7.1)
· non costruire niente prima della risposta di § 6
```

E, sopra tutto: **NX-86 prima di qualunque contatto commerciale.** Con un incumbent
identificato e un potenziale rapporto con il suo vendor o i suoi clienti, la
posizione di dipendente pubblico va chiarita con un legale prima, non dopo.

---

## 8. Backlog

```text
NX-87  CHIUSO — documento ricevuto.
NX-84  AGGIORNATO — K4 verificato: incumbent forte, non mercato vuoto.
       A ed E coperte. Restano da verificare: B (dossier), C (multi-azienda),
       D (circolarità), e l'esistenza di un'API.
NX-91  NUOVO P0 — la domanda di § 6: chi è A. rispetto a Prometeo?
       Una riga. Precede tutto, incluse le 18 domande di § 18.
NX-92  NUOVO P1 — layer forense versionato (§ 4.1) come ipotesi principale
       se A. è lato legale/assistenza. Da validare con la seconda domanda di § 6.
NX-93  NUOVO P2 — verificare se Prometeo gestisce già la vista multi-azienda
       per consulenti e associazioni (Opportunità C). Se sì, anche C è coperta.
```

---

*Ultimo aggiornamento: 2026-09-15*
