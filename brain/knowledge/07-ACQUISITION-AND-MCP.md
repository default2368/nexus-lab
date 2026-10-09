# 07 — ACQUISITION AND MCP

**Scopo:** implementare il primo tratto eseguibile del ciclo:

```text
Foundation acquisisce
→ X interpreta
→ Foundation valida, registra e renderizza
```

**Non è:** un crawler distribuito, un browser agent, un sostituto di Playwright o
un motore RAG.

**Dipende da:**

- `05-EVALUATION.md`
- `06-STORAGE-AND-VALIDATION.md`
- contratto JSON del record di acquisizione e del claim
- X-FOUNDATION: Settings/configurazione, Provider/esecuzione, Module/orchestrazione,
  Route/contratto

---

## 0. P0 sicurezza — prima dello scraping

Il tool MCP attuale:

```text
check_remote_health(url)
```

accetta un URL arbitrario e lo recupera dal server. Se non applica controlli forti,
è una superficie **SSRF**.

Un chiamante potrebbe tentare:

```text
http://127.0.0.1
http://localhost
http://169.254.169.254                 metadata cloud
http://[::1]
http://10.x.x.x / 172.16-31.x.x / 192.168.x.x
endpoint interni Fly / Redis / servizi privati
redirect pubblico → destinazione privata
DNS pubblico che cambia IP dopo il controllo
```

### Regole non negoziabili

```text
· solo http e https
· credenziali nell'URL vietate (`user:password@host`)
· risoluzione DNS prima della connessione
· rifiuto di loopback, private, link-local, multicast, reserved e metadata IP,
  sia IPv4 sia IPv6
· stessa verifica su OGNI redirect
· massimo redirect, timeout, dimensione body e content type
· nessun header Authorization/Cookie fornito dall'utente
· user-agent identificativo
· rate limit per principal e dominio
· log di target, IP risolto, redirect, byte e stato
· protezione dal DNS rebinding: connettere all'IP validato e verificare host/SNI,
  oppure rieseguire il controllo immediatamente prima di ogni connessione
```

**Prima azione:** disabilitare `check_remote_health` in produzione oppure farlo
passare dallo stesso `PublicTargetPolicy` usato dal futuro connettore.

---

## 1. Il perimetro del primo incremento

### Incluso

```text
· acquisizione di UNA risorsa pubblica HTTP/HTTPS
· HTML già presente nella risposta iniziale
· header, redirect, status, content type, size, hash
· estrazione deterministica di testo e metadata
· scoperta limitata: robots.txt, sitemap.xml, llms.txt, WordPress REST root
· record di acquisizione nativo
· validazione deterministica
· esposizione via MCP
```

### Escluso

```text
· login e cookie
· form submission
· crawling completo
· esecuzione JavaScript / headless browser
· proxy rotation o evasione anti-bot
· siti privati o intranet
· upload di documenti sensibili
· interpretazione LLM dentro il fetcher
· scrittura su CMS remoto
```

Se una pagina richiede JavaScript, il record dichiara:

```text
rendering_mode: client_required
status: unsupported_in_v0
```

Non attiva Playwright di nascosto.

---

## 2. Librerie Python

Usare il minimo indispensabile e tenere ogni libreria dietro un adapter.

```text
HTTP                 httpx.AsyncClient
URL e IP policy      urllib.parse + ipaddress + socket/async resolver
HTML parser          la libreria basic già esistente, incapsulata
                     dietro `HtmlExtractor`
                     candidato successivo: selectolax (veloce)
article extraction   opzionale, solo dopo misura: trafilatura
XML / sitemap        defusedxml o parser XML standard con protezioni
robots.txt           urllib.robotparser
hash                 hashlib.sha256
contracts            Pydantic già naturale in FastAPI
storage iniziale     JSONL + filesystem personale/persistente
```

**Non introdurre subito:** BeautifulSoup + lxml + selectolax + trafilatura insieme.
Una implementazione, un adapter, test comparativi prima di cambiare.

**Playwright è fallback futuro**, non dipendenza base. Aumenta molto immagine Docker,
RAM, tempi di startup e superficie di sicurezza.

---

## 3. Modello del record di acquisizione

Campi derivati dall'azione. Nessun LLM.

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, AnyUrl, Field


class RedirectHop(BaseModel):
    source: str
    target: str
    status_code: int
    resolved_ip: str


class AcquisitionRecord(BaseModel):
    acquisition_id: str
    source_ref: str
    normalized_url: str
    final_url: str | None = None

    collection_action: Literal["http_fetch"] = "http_fetch"
    collector_id: str
    collector_version: str
    collected_at: datetime

    status: Literal[
        "success",
        "not_modified",
        "rejected_by_policy",
        "unsupported_content",
        "unsupported_in_v0",
        "timeout",
        "http_error",
        "network_error",
    ]

    http_status: int | None = None
    content_type: str | None = None
    content_length: int | None = None
    resolved_ip: str | None = None
    rendering_mode: Literal[
        "server_rendered",
        "client_required",
        "not_applicable",
        "unknown",
    ] = "unknown"

    redirects: list[RedirectHop] = Field(default_factory=list)
    response_headers: dict[str, str] = Field(default_factory=dict)

    content_sha256: str | None = None
    raw_artifact_ref: str | None = None
    extracted_text_ref: str | None = None
    error_code: str | None = None
    error_detail: str | None = None
```

**Nota privacy:** `response_headers` usa allowlist. Non registrare `Set-Cookie`,
`Authorization` o header potenzialmente sensibili.

### Gate minimo

```text
· `collected_at` derivato dal tool
· `collector_id/version` presenti
· source_ref e normalized_url coerenti
· success → http_status, content_type, hash e artifact_ref obbligatori
· rejected_by_policy → resolved_ip o reason obbligatorio
· redirect chain completa e validata
· hash ricalcolabile dall'artefatto
```

---

## 4. Moduli

```text
app/
├── config/
│   └── settings.py
├── acquisition/
│   ├── contracts.py       AcquisitionRecord, policy/result types
│   ├── policy.py          PublicTargetPolicy (SSRF)
│   ├── fetcher.py         HttpFetcher
│   ├── extractor.py       HtmlExtractor adapter
│   ├── discovery.py       robots/sitemap/llms/wp-json
│   ├── store.py           JSONL + artifact store
│   └── service.py         orchestrazione deterministica
├── claims/
│   ├── contracts.py
│   └── validate.py
├── llm/
│   └── providers/...
├── modules/
│   ├── explain.py
│   └── web_scan.py        orchestrazione Brain, non HTTP raw
├── mcp/
│   ├── server.py
│   └── tools/
│       ├── acquisition.py
│       └── claims.py
└── routes/
```

### Regola delle dipendenze

```text
acquisition/    NON importa llm/
claims/validate NON importa llm/
mcp/tools      chiama service, non fetcher direttamente
modules/       orchestra service + provider
routes/        espone contratti, non decide provider o business model
```

Questa è la regola X-FOUNDATION applicata al codice.

---

## 5. Tool MCP v0

Rimuovere dalla lista di produzione i tool dimostrativi non pertinenti:

```text
calculate_operation
format_text
get_weather (simulato)
```

Possono restare in profilo `development`, ma non devono inquinare il catalogo di
produzione né la scelta tool dell'agente.

### 5.1 `acquire_public_url`

Input:

```json
{
  "url": "https://example.com/page",
  "max_bytes": 2000000,
  "use_conditional_headers": true
}
```

Output: `AcquisitionRecord` + riferimenti agli artefatti. Non ritorna due megabyte di
HTML dentro il contesto MCP.

### 5.2 `discover_public_surface`

Esegue un massimo di richieste predefinito:

```text
/robots.txt
/sitemap.xml
/llms.txt
/wp-json/                 solo se WordPress rilevato o richiesto
```

Output:

```text
risorse trovate · status · content type · hash · acquisition_id
```

Non esegue crawl dei link.

### 5.3 `get_acquisition_record`

Input: `acquisition_id`.
Output: record, metadata ed excerpt limitato/paginato.

### 5.4 `validate_claim_record`

Gate classe 0 del contratto claim.

Output:

```text
valid: true | false
errors: [{rule_id, field, message}]
warnings: []
```

### 5.5 `get_server_info`

Resta. Deve esporre:

```text
server version
protocol version
AI state: disabled | healthy | degraded
provider catalog checked_at
acquisition policy version
claim schema version
```

---

## 6. Non esporre ancora `scan_site`

Un tool monolitico:

```text
scan_site(url) → report completo
```

sembra comodo ma nasconde:

```text
· quali fetch sono avvenuti
· quale record appartiene a quale azione
· dove è entrato l'LLM
· quale passaggio è fallito
· quanto è costato
```

La motion completa può esistere nel modulo `web_scan`, ma deve comporre tool e record
atomici. Il report è un artefatto, non l'output grezzo di una tool call.

Prima:

```text
acquire → validate acquisition → extract → capture claims
→ validate claims → interpret → build artifact
```

Solo dopo test end-to-end si può esporre un tool di alto livello che conservi tutti
gli ID intermedi.

---

## 7. Autenticazione e autorizzazione MCP

Il server Streamable HTTP non deve essere un endpoint pubblico anonimo.

```text
Authorization: Bearer <AUTH_API_KEY o PAT>
```

Separazioni:

```text
AUTH_API_KEY          autorizza chi chiama il server
DEEPSEEK_API_KEY      autorizza il server verso il provider
NEXUS_PAT             futuro: principal, scope, quota e workspace
```

Mai usare la chiave provider come chiave del server.

Scope futuri:

```text
acquisition:read
acquisition:create
claims:validate
brain:interpret
artifacts:build
```

Rate limit separati per scope. `acquisition:create` ha limiti per dominio e byte.

---

## 8. Configurazione X-FOUNDATION

Il documento X-FOUNDATION è corretto nel separare configurazione, esecuzione,
orchestrazione e contratti. C'è però una precisazione.

```text
Settings PUÒ caricare il valore `AI_ENGINE`.
Settings NON interpreta cosa quel valore comporta.
```

Quindi:

```text
settings.py      carica e valida stringhe/tipi
runtime policy   decide il comportamento di disabled/optional/required
provider config  configura il provider già scelto
routing policy   sceglie quale provider/model alias usare per classe di costo
```

`DEEPSEEK_MODEL` unico è sufficiente oggi, ma non va usato come routing globale
quando esisteranno `default` e `gate`. La scelta per classe appartiene alla policy,
non alle settings.

### Config minima iniziale

```text
ENVIRONMENT
AI_ENGINE
AUTH_API_KEY
DEEPSEEK_API_KEY
DEEPSEEK_BASE_URL
DEEPSEEK_MODEL
DEEPSEEK_TIMEOUT_SECONDS
ACQUISITION_MAX_BYTES
ACQUISITION_TIMEOUT_SECONDS
ACQUISITION_USER_AGENT
ARTIFACT_STORE_PATH
RECORD_STORE_PATH
```

Nessun `USE_SCRAPER`, `ENABLE_MCP_SCAN`, `USE_PLAYWRIGHT` finché non esiste davvero
un percorso alternativo.

---

## 9. Commit sequence

```text
PR 1 — sicurezza e contratti
  · PublicTargetPolicy
  · AcquisitionRecord
  · test SSRF
  · check_remote_health disabilitato o policy-enforced

PR 2 — acquisizione deterministica
  · HttpFetcher
  · HtmlExtractor adapter sulla libreria esistente
  · JSONL/artifact store
  · test con server locale controllato

PR 3 — MCP tools atomici
  · acquire_public_url
  · discover_public_surface
  · get_acquisition_record
  · auth + rate limit
  · rimozione tool demo dal profilo production

PR 4 — claim gate
  · claim schema
  · validate_claim_record
  · primo claim Emergent nativo

PR 5 — primo ciclo completo
  · un record acquisito
  · un claim interpretato
  · gate
  · matrice generata
  · PageData
  · renderer
```

Ogni PR è revertibile e produce un artefatto verificabile.

---

## 10. Definition of Done v0

```text
□ check_remote_health non può raggiungere IP privati, loopback, metadata o redirect
  verso destinazioni vietate
□ server parte e serve tool deterministici con AI_ENGINE=disabled
□ nessun tool acquisition importa un provider LLM
□ ogni fetch produce AcquisitionRecord prima di qualunque interpretazione
□ HTML raw non viene inserito interamente nel contesto MCP
□ record JSONL e artifact hash sono coerenti
□ claim Emergent registrato nativamente, non ricostruito
□ gate automatico blocca record incompleti
□ Brain segnala ma non blocca
□ umano può ratificare
□ matrice è generata, non mantenuta a mano
□ snapshot contiene record_set_sha e versioni di ruleset/template
□ costo e model_id risolto sono loggati per ogni chiamata LLM
```

---

## 11. Primo obiettivo

Non "scraper funzionante" e non "MCP con tanti tool".

> **Un claim Emergent acquisito nativamente, validato, proiettato in matrice e
> renderizzato senza ricostruire la provenance dopo.**

Quello è il primo artefatto maturo del ciclo Foundation → X → Foundation.

---

*Redatto il 2026-09-19. Il perimetro è volutamente stretto: una risorsa pubblica,
nessun JavaScript, nessun dato privato, nessun crawler.*
