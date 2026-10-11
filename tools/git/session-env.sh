#!/usr/bin/env bash
#
# session-env.sh — deriva ed esporta le variabili di sessione Arena
# PROGETTO: open-nexus-lab
# Ubicazione: $ROOT/tools/git/session-env.sh
#
# Uso:
#   source tools/git/session-env.sh
#   echo "$ARENA_SESSION_ID"
#
# Oppure per aggiornare il record persistito:
#   source tools/git/session-env.sh --persist
#
# Sicuro da source-are: non esce mai, non uccide la shell, non fa set -e.
#

# NOTA: questo file è pensato per essere "sourced", non eseguito.
#       Se eseguito direttamente, stampa le variabili e termina.

# ============================================================
# ROOT — derivata dalla posizione dello script
# ============================================================
if [[ -n "${BASH_SOURCE[0]:-}" ]]; then
  _SESSION_ENV_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  _SESSION_ENV_DIR="$(pwd)"
fi
_SESSION_ENV_ROOT="$(cd "$_SESSION_ENV_DIR/../.." && pwd)"

# ============================================================
# RILEVAZIONE BRANCH
# ============================================================
SESSION_BRANCH="$(git -C "$_SESSION_ENV_ROOT" branch --show-current 2>/dev/null || true)"

# ============================================================
# DERIVAZIONE VARIABILI ARENA
# ============================================================
# Pattern atteso: arena/<sessionId>-<projectId>
#   es: arena/27d91f45-nexus-lab
#       ARENA_SESSION_ID      = 27d91f45
#       ARENA_SESSION_PROJECT = nexus-lab

if [[ "$SESSION_BRANCH" =~ ^arena/([a-f0-9]+)-(.+)$ ]]; then
  ARENA_SESSION_ID="${BASH_REMATCH[1]}"
  ARENA_SESSION_PROJECT="${BASH_REMATCH[2]}"
  ARENA_SESSION_BRANCH="$SESSION_BRANCH"
  ARENA_SESSION_KIND="arena"
else
  ARENA_SESSION_ID=""
  ARENA_SESSION_PROJECT=""
  ARENA_SESSION_BRANCH="$SESSION_BRANCH"
  ARENA_SESSION_KIND="non-arena"
fi

ARENA_SESSION_ROOT="$_SESSION_ENV_ROOT"

# Esporta per i sottoprocessi
export ARENA_SESSION_ID
export ARENA_SESSION_PROJECT
export ARENA_SESSION_BRANCH
export ARENA_SESSION_KIND
export ARENA_SESSION_ROOT

# ============================================================
# PERSISTENZA OPZIONALE
# ============================================================
#   source tools/git/session-env.sh --persist
#   scrive .nexus/session.json (non versionato)
#
_persist_session() {
  [[ "$ARENA_SESSION_KIND" != "arena" ]] && return 0

  local dir="$ARENA_SESSION_ROOT/.nexus"
  mkdir -p "$dir"

  local file="$dir/session.json"
  local now
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  # preserva openedAt se già presente per la stessa sessione
  local opened_at="$now"
  if [[ -f "$file" ]]; then
    local existing_id
    existing_id="$(node -e "try{const j=require('$file');process.stdout.write(j.sessionId||'')}catch(e){}" 2>/dev/null || true)"
    local existing_open
    existing_open="$(node -e "try{const j=require('$file');process.stdout.write(j.openedAt||'')}catch(e){}" 2>/dev/null || true)"
    if [[ "$existing_id" == "$ARENA_SESSION_ID" && -n "$existing_open" ]]; then
      opened_at="$existing_open"
    fi
  fi

  cat > "$file" <<JSON
{
  "schemaVersion": "nexus-lab/session/v1",
  "sessionId": "$ARENA_SESSION_ID",
  "projectId": "$ARENA_SESSION_PROJECT",
  "branchRef": "$ARENA_SESSION_BRANCH",
  "workspaceRoot": "$ARENA_SESSION_ROOT",
  "openedAt": "$opened_at",
  "recordedAt": "$now"
}
JSON

  ARENA_SESSION_RECORD="$file"
  export ARENA_SESSION_RECORD
}

# ============================================================
# OUTPUT (solo se eseguito, non se sourced)
# ============================================================
_session_env_print() {
  printf 'ARENA_SESSION_ID      = %s\n' "${ARENA_SESSION_ID:-<none>}"
  printf 'ARENA_SESSION_PROJECT = %s\n' "${ARENA_SESSION_PROJECT:-<none>}"
  printf 'ARENA_SESSION_BRANCH  = %s\n' "${ARENA_SESSION_BRANCH:-<none>}"
  printf 'ARENA_SESSION_KIND    = %s\n' "${ARENA_SESSION_KIND:-<none>}"
  printf 'ARENA_SESSION_ROOT    = %s\n' "${ARENA_SESSION_ROOT:-<none>}"
  [[ -n "${ARENA_SESSION_RECORD:-}" ]] && \
    printf 'ARENA_SESSION_RECORD  = %s\n' "$ARENA_SESSION_RECORD"
}

# ============================================================
# FLAG --persist (accettato sia in sourcing sia in esecuzione)
# ============================================================
for _arg in "${@:-}"; do
  case "$_arg" in
    --persist) _persist_session ;;
    --print)   _session_env_print ;;
  esac
done
unset _arg

# Se eseguito direttamente (non sourced), stampa e termina
if [[ "${BASH_SOURCE[0]:-}" == "${0:-}" ]]; then
  _session_env_print
fi

# Pulizia namespace temporaneo (le variabili ARENA_* restano)
unset _SESSION_ENV_DIR
unset _SESSION_ENV_ROOT