# Google AntiGravity Agent Instructions (AGENTS.md)

This document contains the global rules of engagement, architectural constraints, and tool protocols for all autonomous agents operating within the **OpenFav** project.

---

## 🤖 ROLES & RESPONSIBILITIES

### 1. The Planner Agent
* **Objective:** Map out structural and architectural changes before any code is touched.
* **MCP Protocol:** 
  * You MUST use `codebase-memory-mcp` as your primary search tool.
  * Use `search_graph` to find routes or controller entry points.
  * Use `trace_path` to map dependencies (Fan-In/Fan-Out) and avoid breaking changes.
  * NEVER suggest modifying core runtime files unless the user explicitly bypasses the safety locks.

### 2. The Coder Agent
* **Objective:** Implement code modifications, create virtual templates, and resolve route controllers.
* **MCP Protocol:** 
  * Do NOT read entire files. Use `get_code_snippet` to retrieve only the required functions or classes to keep your context window lean.
  * Follow established TypeScript typings and Next.js/Astro conventions.
  * Respect the immutability of core files.

### 3. The Verifier Agent
* **Objective:** Execute tests, log behaviors, and verify that the requirements of the PRD are met.
* **MCP Protocol:**
  * Use `index_status` to ensure the database graph is updated after code changes.
  * Run project test suites to verify there are no baseline contract regressions.

---

## ⚠️ STRICT CODEBASE INVARIANTS (IMMUTABLE FILES)

Unless the user gives explicit, high-priority consent, ALL agents are strictly forbidden from modifying or writing to:
* `PageController`
* `normalizeToPageData`
* `ApplicationDefinition`
* `ApplicationContext`
* `BundleCollector`
* `DiscoveryService` / `DiscoveryServiceV2`

---

## 🛡️ AUTHENTICATION & REDIRECT SECURE LIFECYCLE (PRD 0.6.3-A-R1)

When handling login, session, or auth flows, you must enforce the following security specs:
1. **Redirects:** Every redirect path (the `next` parameter) must pass through the `validateInternalReturnPath(next)` function to protect against Open Redirect vulnerabilities.
2. **Path Sanitization:** The return path must start with `/`, but must not start with `//` or `/\` (no protocol-relative URL bypasses).
3. **Fallbacks:** Standard standalone login (without a `next` query parameter) must fallback to `/build/auth/welcome`.
4. **No Hardcoded Destinations:** Never hardcode platform dashboard URLs (like `core-admin/dashboard` or `Operations`) in auth components (such as `success.ts` or `signin.ts`). Use dynamic lookup or fallback.

---

## 📊 MCP TOOL CONVENTIONS

* Always verify that the `codebase-memory-mcp` server is alive (`index_status`) before executing workspace-wide search queries.
* Prefer `search_graph` over `search_code` (text search) for finding defined symbols (functions, classes, schemas).
