#!/usr/bin/env bash
#
# push-session.sh — aggiorna il branch remoto della sessione rispetto al locale
# PROGETTO: open-nexus-lab
# Ubicazione: $ROOT/tools/git/push-session.sh
#
# Modalità:
#   ./push-session.sh           dry-run: mostra cosa farebbe
#   ./push-session.sh --apply   esegue il push
#   ./push-session.sh status    sola diagnostica locale vs remoto
#   ./push-session.sh help
#
# Vincoli:
#   - Non pusha mai su master/main
#   - Non forza mai (no --force, no --force-with-lease)
#   - Richiede worktree clean
#   - Divergenza locale/remoto → BLOCKED_BRANCH_DIVERGED
#   - Remoto avanti → BLOCKED_REMOTE_AHEAD (non è compito di questo script)
#
set -euo pipefail

# ============================================================
# ROOT — derivata dalla posizione dello script
# ============================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ============================================================
# CONFIG
# ============================================================
REMOTE="origin"
PROTECTED_BRANCHES=("master" "main")

# ============================================================
# COLORI
# ============================================================
if [[ -t 1 ]]; then
  BOLD=$'\033[1m'; DIM=$'\033[2m'; RESET=$'\033[0m'
  RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; CYAN=$'\033[36m'
else
  BOLD=""; DIM=""; RESET=""; RED=""; GREEN=""; YELLOW=""; CYAN=""
fi

hr()    { printf '%s\n' "${DIM}──────────────────────────────────────────────────${RESET}"; }
title() { printf '\n%s%s%s\n' "${BOLD}${CYAN}" "$1" "${RESET}"; hr; }
ok()    { printf '  %s✓%s %s\n' "${GREEN}" "${RESET}" "$1"; }
warn()  { printf '  %s!%s %s\n' "${YELLOW}" "${RESET}" "$1"; }
err()   { printf '  %s✗%s %s\n' "${RED}" "${RESET}" "$1" >&2; }
say()   { printf '%s\n' "$1"; }
dim()   { printf '%s%s%s\n' "${DIM}" "$1" "${RESET}"; }

stop() {
  printf '\n%sSTATUS = %s%s\n' "${BOLD}${RED}" "$1" "${RESET}" >&2
  exit 1
}

# ============================================================
# PREFLIGHT
# ============================================================
preflight() {
  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    err "Non sei in un repository git."
    stop "BLOCKED_NOT_A_REPO"
  fi

  local top
  top="$(git rev-parse --show-toplevel)"
  if [[ "$top" != "$WORKSPACE_ROOT" ]]; then
    err "Root inattesa: $top"
    err "Attesa:        $WORKSPACE_ROOT"
    err "Lo script deve essere eseguito dalla propria root di workspace."
    stop "BLOCKED_UNEXPECTED_ROOT"
  fi

  if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
    err "Remote '$REMOTE' non configurato."
    stop "BLOCKED_NO_REMOTE"
  fi
}

# ============================================================
# RACCOLTA STATO
# ============================================================
collect_state() {
  BRANCH="$(git branch --show-current)"
  HEAD="$(git rev-parse HEAD)"
  REMOTE_URL="$(git remote get-url "$REMOTE")"

  if [[ -z "$(git status --porcelain)" ]]; then
    WORKTREE="clean"
  else
    WORKTREE="dirty"
  fi

  local stash_count
  stash_count="$(git stash list | wc -l | tr -d ' ')"
  if (( stash_count == 0 )); then
    STASH="empty"
  else
    STASH="present ($stash_count)"
  fi
}

# ============================================================
# DIAGNOSTICA
# ============================================================
show_state() {
  title "Stato locale"
  say "  root:    $WORKSPACE_ROOT"
  say "  remote:  $REMOTE  ($REMOTE_URL)"
  say "  branch:  $BRANCH"
  say "  HEAD:    $HEAD"
  say "  status:  $WORKTREE"
  say "  stash:   $STASH"
}

# ============================================================
# CONFRONTO CON REMOTO
# ============================================================
compare_remote() {
  title "Confronto con $REMOTE/$BRANCH"

  if ! git ls-remote --exit-code "$REMOTE" "refs/heads/$BRANCH" >/dev/null 2>&1; then
    warn "Branch remoto '$REMOTE/$BRANCH' non esiste."
    REMOTE_EXISTS="no"
    AHEAD=0
    BEHIND=0
    return 0
  fi

  REMOTE_EXISTS="yes"
  git fetch "$REMOTE" "$BRANCH" >/dev/null 2>&1 || true

  local remote_head
  remote_head="$(git rev-parse "$REMOTE/$BRANCH")"

  read -r AHEAD BEHIND < <(git rev-list --left-right --count "$BRANCH...$REMOTE/$BRANCH")

  say "  locale:  $HEAD"
  say "  remoto:  $remote_head"
  say "  ahead:   $AHEAD   behind: $BEHIND"
}

# ============================================================
# GATE
# ============================================================
gate_protected_branch() {
  local p
  for p in "${PROTECTED_BRANCHES[@]}"; do
    if [[ "$BRANCH" == "$p" ]]; then
      err "Branch protetto: $BRANCH"
      err "Questo script pusha solo branch di sessione."
      stop "BLOCKED_PROTECTED_BRANCH"
    fi
  done
}

gate_worktree() {
  if [[ "$WORKTREE" != "clean" ]]; then
    err "Worktree non pulito — commit o stash prima di pushare."
    git status --short | sed 's/^/    /'
    stop "BLOCKED_DIRTY_WORKTREE"
  fi
}

gate_divergence() {
  if (( AHEAD > 0 && BEHIND > 0 )); then
    err "Branch divergenti (ahead=$AHEAD, behind=$BEHIND)."
    err "Richiede owner decision: pull --rebase? merge? reset?"
    stop "BLOCKED_BRANCH_DIVERGED"
  fi
  if (( AHEAD == 0 && BEHIND > 0 )); then
    err "Remoto avanti di $BEHIND commit."
    err "Questo script non pulla. Serve 'git pull --ff-only' — decisione separata."
    stop "BLOCKED_REMOTE_AHEAD"
  fi
}

# ============================================================
# AZIONE
# ============================================================
do_push() {
  title "Push"
  if [[ "$REMOTE_EXISTS" == "no" ]]; then
    say "  creo branch remoto: $REMOTE/$BRANCH"
    if [[ "$APPLY" == "yes" ]]; then
      git push -u "$REMOTE" "$BRANCH"
    else
      dim "  (dry-run) git push -u $REMOTE $BRANCH"
    fi
  else
    say "  push: $BRANCH → $REMOTE/$BRANCH  ($AHEAD commit)"
    if [[ "$APPLY" == "yes" ]]; then
      git push "$REMOTE" "$BRANCH"
    else
      dim "  (dry-run) git push $REMOTE $BRANCH"
    fi
  fi
}

do_nothing() {
  title "Esito"
  ok "Niente da fare: locale e remoto sono allineati."
}

# ============================================================
# COMANDI
# ============================================================
cmd_status() {
  preflight
  collect_state
  show_state
  compare_remote
  say ""
}

cmd_run() {
  APPLY="${1:-no}"

  preflight
  collect_state
  show_state
  gate_protected_branch
  gate_worktree
  compare_remote
  gate_divergence

  if [[ "$REMOTE_EXISTS" == "no" ]] || (( AHEAD > 0 )); then
    do_push
  else
    do_nothing
  fi

  say ""
  if [[ "$APPLY" == "yes" ]]; then
    printf '%sSTATUS = %s%s\n' "${BOLD}${GREEN}" "PUSH_OK" "${RESET}"
  else
    printf '%sSTATUS = %s%s\n' "${BOLD}${YELLOW}" "DRY_RUN" "${RESET}"
    dim "  (rilancia con --apply per eseguire)"
  fi
}

cmd_help() {
  cat <<EOF
${BOLD}push-session.sh${RESET} — aggiorna il branch remoto della sessione rispetto al locale
PROGETTO: open-nexus-lab

${BOLD}USO${RESET}
  ./push-session.sh           dry-run (mostra cosa farebbe)
  ./push-session.sh --apply   esegue il push
  ./push-session.sh status    sola diagnostica locale vs remoto
  ./push-session.sh help

${BOLD}ROOT (derivata)${RESET}
  script:         $SCRIPT_DIR
  workspace root: $WORKSPACE_ROOT
  remote:         $REMOTE

${BOLD}REGOLE${RESET}
  - non pusha su ${PROTECTED_BRANCHES[*]}
  - richiede worktree clean
  - divergenza locale/remoto → BLOCKED_BRANCH_DIVERGED
  - remoto avanti           → BLOCKED_REMOTE_AHEAD
  - no force, no rebase, no reset

${BOLD}STATI${RESET}
  DRY_RUN
  PUSH_OK
  BLOCKED_NOT_A_REPO
  BLOCKED_UNEXPECTED_ROOT
  BLOCKED_NO_REMOTE
  BLOCKED_PROTECTED_BRANCH
  BLOCKED_DIRTY_WORKTREE
  BLOCKED_BRANCH_DIVERGED
  BLOCKED_REMOTE_AHEAD
EOF
}

# ============================================================
# ENTRYPOINT
# ============================================================
case "${1:-}" in
  ""|--dry-run)   cmd_run no ;;
  --apply)        cmd_run yes ;;
  status)         cmd_status ;;
  help|-h|--help) cmd_help ;;
  *) err "comando sconosciuto: $1"; cmd_help; exit 1 ;;
esac