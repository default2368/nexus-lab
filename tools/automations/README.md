# Automations — marcia in più per 0.8.X / 0.9.X

**Obiettivo:** dare al cantiere Foundation una strumentazione che gira in Classe 0 (deterministica, gratis) e che alimenta il Brain come collector di procedure.

```
0.8.X cantiere = distribuzione, authority, asset, template
0.9.X cantiere = EntityRecord, Projection, Domain Pack
Brain collector = trasforma procedure documentate in Candidate Domain
```

## Struttura

```
tools/automations/
├── README.md                      questo file
├── f08-audit.py                   F08-001 audit authority + impatto ADR
├── check-physical-pages.py        F08-002 / F08-018 retirement ledger
├── check-page-contracts.py        F08-004 / F08-006 / F08-007 assi ortogonali + ID espliciti
├── check-asset-template.py        F08-010 / F08-011 / F08-011A asset locality + template resolution
├── brain-collector.py             Brain collector of procedures → CandidateDomainSpec
├── sufficiency-evaluator.py       DA-02 valutatore sufficiency per 09-DOMAIN-ACQUISITION
└── collect-epistemic-records.py   NEXUS-LAB/*.md → brain/records/*.jsonl (NX-56)
```

## Principio

Ogni script:

- è Classe 0, nessun LLM
- produce `COMMAND-LEDGER.md` + output JSONL/MD versionabile
- non modifica sorgenti, solo report
- rispetta `Runtime never observes repository directly` — legge file, non importa runtime
- segue `05-EVALUATION.md`: ogni affermazione con comando/file di evidenza

## Uso

```bash
# Audit 0.8.X completo
python3 tools/automations/f08-audit.py --repo /path/to/open-nexus-foundation --output /tmp/f08-audit

# Brain collector: da procedura a candidate domain
python3 tools/automations/brain-collector.py --input NEXUS-LAB/SORGENTI/25-SCANSIONE-PROMETEO-RIFIUTI.md --output /tmp/candidate-prometeo.yaml

# Sufficiency per G. o A.
python3 tools/automations/sufficiency-evaluator.py --input uploads/03-opennexus-verticale-rifiuti.txt --output /tmp/sufficiency.json

# Epistemic records da NEXUS-LAB (NX-56)
python3 tools/automations/collect-epistemic-records.py --input NEXUS-LAB --output brain/records/nexus-lab/
```

## Integrazione Brain

I tool atomici esposti via MCP (07-ACQUISITION-AND-MCP.md):

```
acquire_public_url
discover_public_surface
validate_claim_record
collect_procedure → candidate_domain
evaluate_sufficiency
```

Il Brain non scrive mai direttamente su canonical Domain Pack. Propone CandidateDomainSpec.

```
Expert knowledge + Documented sources + Observed workflow
        ↓ Brain interpretation
Candidate Domain Definition (OBSERVED/INFERRED/PROPOSED/UNKNOWN/CONFLICTING)
        ↓ Expert correction
Validated AuthoringSpec / Domain Pack
```

## KPI 0.8.X automatizzati

| KPI | Script |
|-----|--------|
| KPI-08-01 protected kernel modificati | f08-audit.py |
| KPI-08-02 physical pages non gestite | check-physical-pages.py |
| KPI-08-03 registrazioni duplicate | check-page-contracts.py |
| KPI-08-04 pagine senza ID esplicito | check-page-contracts.py |
| KPI-08-05 broken references | check-page-contracts.py |
| KPI-08-06 remote asset dependencies | check-asset-template.py |
| KPI-08-07 template non dichiarati | check-asset-template.py |
| KPI-08-08 repository observations | f08-audit.py |
| KPI-08-09 clean-room validation | check-asset-template.py (future) |

## 0.9.X

- `brain-collector.py` → produce CandidateDomainSpec con sufficiency level
- `sufficiency-evaluator.py` → valuta 14 dimensioni (Purpose, Actors, Objects, Workflow, States, Decisions, Evidence, Relationships, Operations, Access, Exceptions, Examples, Provenance, Sensitivity)
