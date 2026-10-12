# F08-001 Impact Matrix — Authority Audit
Generated: 2026-10-09T19:09:16.463048
Repo: /home/user/nexus-lab

## Protected Kernel Check

| Symbol | Found | Risk |
|---|---|---|
| PageController | CLEAN | OK |
| normalizeToPageData | CLEAN | OK |
| ApplicationDefinition | CLEAN | OK |
| ApplicationContext | CLEAN | OK |
| BundleCollector | CLEAN | OK |
| DiscoveryService | CLEAN | OK |
| DiscoveryServiceV2 | CLEAN | OK |
| PageData | CLEAN | OK |

## Authority Claims Verification

| Claim | Command | Evidence | Status |
|---|---|---|---|
| ADR files | `find docs -type f -iname 'ADR-*' 2>/dev/...` | — | NOT_FOUND |
| createApplicationDefinition | `git grep -n "createApplicationDefinition...` | NEXUS-LAB/01-DECISION-LOG.md:1313:createApplicationDefinition('simple', 'Simple' | EVIDENCE |
| ApplicationDefinition | `git grep -n "ApplicationDefinition" 2>/d...` | AGENTS.md:37:* `ApplicationDefinition` | EVIDENCE |
| ApplicationBundle | `git grep -n "ApplicationBundle" 2>/dev/n...` | NEXUS-LAB/00-INDICE.md:94:  ApplicationBundle → BundleCollector → Build Artifact | EVIDENCE |
| PageMeta | `git grep -n "PageMeta" 2>/dev/null | hea...` | documentation/prompts/PROMPT-FOUNDATION-DEFAULTS-LIVENESS-HANDOFF.md:50:Page / P | EVIDENCE |
| WebPageTemplate | `git grep -n "WebPageTemplate" 2>/dev/nul...` | NEXUS-LAB/01-DECISION-LOG.md:30:Non significa che ogni UI debba usare `WebPageTe | EVIDENCE |
| PAGES_REGISTRY | `git grep -n "PAGES_REGISTRY" 2>/dev/null...` | NEXUS-LAB/35-RISPOSTA-TRASPARENZA-CODIFICATA.md:47:**[OSSERVATO]** `f08-audit.py | EVIDENCE |
| virtualProvider | `git grep -n "virtualProvider\|virtual-pr...` | NEXUS-LAB/35-RISPOSTA-TRASPARENZA-CODIFICATA.md:47:**[OSSERVATO]** `f08-audit.py | EVIDENCE |
| access policies | `git grep -n "PUBLIC\|PROTECTED\|LANDING\...` | NEXUS-LAB/01-DECISION-LOG.md:2976:· `open-nexus/assistant` esiste già (PROTECTED | EVIDENCE |
| physical pages | `git grep -n "physical/main/chat\|physica...` | NEXUS-LAB/01-DECISION-LOG.md:2976:· `open-nexus/assistant` esiste già (PROTECTED | EVIDENCE |
| assistant/discovery | `git grep -n "simple/assistant\|core-admi...` | documentation/prompts/PROMPT-SURF-082-003-STALE-REFERENCE-CONVERGENCE.md:69:  ca | EVIDENCE |

## Physical Routes Classification

| Route | Classification | Owner | Action |
|---|---|---|---|
| physical/main/chat | LEGACY_APPLICATION | simple/assistant | RETIRE |
| physical/main/home-pages | LEGACY_APPLICATION | core-admin/discovery-pages | RETIRE |
| physical/debug/status | INFRASTRUCTURE | Operations | PRESERVE |
| physical/debug/debug-theme | DEBUG | TemplateLab | MOVE |
| physical/debug/debug-auth | DEBUG | Auth | RETIRE |