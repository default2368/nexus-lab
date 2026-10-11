#!/usr/bin/env bash
#
# run-project.sh — Nexus-Lab workspace manager
#
# Root script del workspace. Legge nexus.spec.yaml, scrive .nexus/workspace.yaml.
# La CLI consuma solo il manifest. Lo spec definisce la forma.
#
# Verbi:
#   setup      guidato da nexus.spec.yaml (mandatory + path)
#   add        scan dir + append al manifest
#   scan       sola lettura, mostra candidati
#   validate   coerenza spec ↔ manifest, path esistono
#   show       mostra manifest
#   init       bootstrap libero senza spec (legacy)
#   help       questo messaggio
#
set -euo pipefail

# ---------- config ----------
DEFAULT_MANIFEST_NAME=".nexus/workspace.yaml"
DEFAULT_SPEC_NAME="nexus.spec.yaml"
SCHEMA_VERSION="workspace-manifest/0.2"

# ---------- colori ----------
if [[ -t 1 ]]; then
  BOLD=$'\033[1m'; DIM=$'\033[2m'; RESET=$'\033[0m'
  RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; CYAN=$'\033[36m'
else
  BOLD=""; DIM=""; RESET=""; RED=""; GREEN=""; YELLOW=""; CYAN=""
fi

say()   { printf '%s\n' "$1"; }
dim()   { printf '%s%s%s\n' "$DIM" "$1" "$RESET"; }
ok()    { printf '%s✓%s %s\n' "$GREEN" "$RESET" "$1"; }
warn()  { printf '%s!%s %s\n' "$YELLOW" "$RESET" "$1"; }
err()   { printf '%s✗%s %s\n' "$RED" "$RESET" "$1" >&2; }
title() { printf '\n%s%s%s\n' "${BOLD}${CYAN}" "$1" "${RESET}"; }

ask() {
  local prompt="$1" default="${2:-}" reply
  if [[ -n "$default" ]]; then
    printf '%s%s%s [%s%s%s]: ' "$BOLD" "$prompt" "$RESET" "$DIM" "$default" "$RESET" >&2
  else
    printf '%s%s%s: ' "$BOLD" "$prompt" "$RESET" >&2
  fi
  read -r reply || true
  printf '%s' "${reply:-$default}"
}

confirm() {
  local prompt="$1" reply
  printf '%s%s%s [s/N]: ' "$BOLD" "$prompt" "$RESET" >&2
  read -r reply || true
  [[ "$reply" =~ ^[sSyY]$ ]]
}

abs_path() { ( cd "$1" && pwd ); }

# ---------- git ----------
detect_git() {
  local p="$1"
  if git -C "$p" rev-parse --git-dir >/dev/null 2>&1; then
    local remote
    remote="$(git -C "$p" remote get-url origin 2>/dev/null || true)"
    printf '%s' "${remote:-}"
  fi
}

# ---------- type / runtime guess ----------
guess_type() {
  case "$(basename "$1")" in
    *documentation*|docs)     echo "documentation" ;;
    *scripts*|*tools*)        echo "scripts" ;;
    *research*)               echo "research" ;;
    *rules*|*governance*)     echo "rules" ;;
    foundation|frontend|backend|cli|insight|startup) echo "app" ;;
    *)                        echo "unknown" ;;
  esac
}

guess_runtime() {
  local p="$1"
  [[ -f "$p/package.json" ]]     && { echo "node"; return; }
  [[ -f "$p/pyproject.toml" ]]   && { echo "python"; return; }
  [[ -f "$p/requirements.txt" ]] && { echo "python"; return; }
  [[ -f "$p/Cargo.toml" ]]       && { echo "rust"; return; }
  [[ -f "$p/go.mod" ]]           && { echo "go"; return; }
  echo "-"
}

# ---------- scan (condivisa) ----------
# Ritorna righe: name|path|type|runtime|remote
scan_dir() {
  local root="$1"
  [[ -d "$root" ]] || return 0
  local d base remote t r
  for d in "$root"/*/; do
    [[ -d "$d" ]] || continue
    base="$(basename "$d")"
    [[ "$base" == ".nexus" ]] && continue
    remote="$(detect_git "$d")"
    t="$(guess_type "$d")"
    r="$(guess_runtime "$d")"
    printf '%s|%s|%s|%s|%s\n' "$base" "$base" "$t" "$r" "${remote:--}"
  done
}

# ---------- manifest I/O ----------
# Struttura in memoria: righe "id|name|path|type|runtime|role|remote"
read_manifest_projects() {
  local m="$1"
  [[ -f "$m" ]] || return 0
  local in_projects=0
  local id="" name="" path="" type="" runtime="" role="" remote=""
  while IFS= read -r line; do
    if [[ "$line" =~ ^projects: ]]; then in_projects=1; continue; fi
    (( in_projects )) || continue

    if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]; then
      [[ -n "$id" ]] && printf '%s|%s|%s|%s|%s|%s|%s\n' "$id" "$name" "$path" "$type" "$runtime" "$role" "${remote:--}"
      id="${BASH_REMATCH[1]}"; name=""; path=""; type=""; runtime=""; role=""; remote=""
      continue
    fi
    [[ "$line" =~ ^[[:space:]]*name:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]    && name="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*path:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]    && path="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*type:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]    && type="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*runtime:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]] && runtime="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*role:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]    && role="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*remote:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]  && remote="${BASH_REMATCH[1]}"
  done < "$m"
  [[ -n "$id" ]] && printf '%s|%s|%s|%s|%s|%s|%s\n' "$id" "$name" "$path" "$type" "$runtime" "$role" "${remote:--}"
}

write_manifest() {
  local m="$1" root="$2" spec_path="$3"
  shift 3
  local projects=()
  (( $# )) && projects=("$@")
  local now; now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  mkdir -p "$(dirname "$m")"
  {
    echo "# nexus workspace manifest"
    echo "# generated by run-project.sh"
    echo "schemaVersion: \"$SCHEMA_VERSION\""
    echo "workspaceRoot: \"$root\""
    echo "generatedAt: \"$now\""
    [[ -n "$spec_path" ]] && echo "resolvedFrom: \"$spec_path\""
    echo "projects:"
    if (( ${#projects[@]} == 0 )); then
      echo "  []"
    else
      for p in ${projects[@]+"${projects[@]}"}; do
        IFS='|' read -r id name path type runtime role remote <<< "$p"
        echo "  - id: \"$id\""
        echo "    name: \"$name\""
        echo "    path: \"$path\""
        echo "    type: \"$type\""
        echo "    runtime: \"$runtime\""
        echo "    role: \"$role\""
        if [[ -z "$remote" || "$remote" == "-" ]]; then
          echo "    git: null"
        else
          echo "    git:"
          echo "      remote: \"$remote\""
        fi
      done
    fi
  } > "$m"
}

# ---------- spec I/O ----------
# Ritorna righe: id|name|type|runtime|role|pathDefault
read_spec_mandatory() {
  local s="$1"
  [[ -f "$s" ]] || return 0
  local in_mandatory=0
  local id="" name="" type="" runtime="" role="" pathDefault=""
  while IFS= read -r line; do
    if [[ "$line" =~ ^mandatory: ]]; then in_mandatory=1; continue; fi
    if (( in_mandatory )) && [[ "$line" =~ ^[a-zA-Z] ]]; then break; fi
    (( in_mandatory )) || continue

    if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]; then
      [[ -n "$id" ]] && printf '%s|%s|%s|%s|%s|%s\n' "$id" "$name" "$type" "$runtime" "$role" "$pathDefault"
      id="${BASH_REMATCH[1]}"; name=""; type=""; runtime=""; role=""; pathDefault=""
      continue
    fi
    [[ "$line" =~ ^[[:space:]]*name:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]        && name="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*type:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]        && type="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*runtime:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]     && runtime="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*role:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]]        && role="${BASH_REMATCH[1]}"
    [[ "$line" =~ ^[[:space:]]*pathDefault:[[:space:]]*\"?([^\"]*)\"?[[:space:]]*$ ]] && pathDefault="${BASH_REMATCH[1]}"
  done < "$s"
  [[ -n "$id" ]] && printf '%s|%s|%s|%s|%s|%s\n' "$id" "$name" "$type" "$runtime" "$role" "$pathDefault"
}

# ---------- setup ----------
cmd_setup() {
  local spec="$DEFAULT_SPEC_NAME"
  local manifest=""
  while (( $# )); do
    case "$1" in
      --spec)     spec="$2"; shift 2 ;;
      --manifest) manifest="$2"; shift 2 ;;
      -h|--help)  say "usage: run-project.sh setup [--spec nexus.spec.yaml] [--manifest .nexus/workspace.yaml]"; return 0 ;;
      *) err "flag sconosciuto: $1"; return 1 ;;
    esac
  done

  [[ -f "$spec" ]] || { err "Spec non trovato: $spec"; return 1; }

  title "Setup da spec: $spec"

  local root; root="$(ask "Workspace root" "$(pwd)")"
  [[ -d "$root" ]] || { err "Directory non esistente: $root"; return 1; }
  root="$(abs_path "$root")"
  [[ -z "$manifest" ]] && manifest="$root/$DEFAULT_MANIFEST_NAME"

  # leggi mandatory in array
  local mandatory_arr=()
  while IFS= read -r l; do
    [[ -n "$l" ]] && mandatory_arr+=("$l")
  done < <(read_spec_mandatory "$spec")

  (( ${#mandatory_arr[@]} == 0 )) && { err "Nessun mandatory nello spec"; return 1; }

  local projects=()
  title "Progetti obbligatori (spec)"
  for line in ${mandatory_arr[@]+"${mandatory_arr[@]}"}; do
    IFS='|' read -r id name type runtime role pathDefault <<< "$line"
    [[ -z "$id" ]] && continue
    say ""
    printf '  %s%s%s (%s / %s / %s)\n' "$BOLD" "$name" "$RESET" "$type" "$runtime" "$role"
    local p
    p="$(ask "  path" "$pathDefault")"
    local full="$root/$p"
    if [[ ! -d "$full" ]]; then
      warn "  path non esiste: $p"
      if ! confirm "  aggiungere comunque?"; then
        dim "  saltato: $id"; continue
      fi
    fi
    local remote=""
    [[ -d "$full" ]] && remote="$(detect_git "$full")"
    [[ -n "$remote" ]] && ok "  git: $remote" || dim "  git: (nessuno)"
    projects+=("$id|$name|$p|$type|$runtime|$role|${remote:--}")
  done

  # extra opzionali
  if confirm "Aggiungere progetti extra dalla scansione?"; then
    local scan_lines=()
    while IFS= read -r l; do
      [[ -n "$l" ]] && scan_lines+=("$l")
    done < <(scan_dir "$root")

    for line in ${scan_lines[@]+"${scan_lines[@]}"}; do
      IFS='|' read -r cname cpath ctype cruntime cremote <<< "$line"
      local exists=0
      for p in ${projects[@]+"${projects[@]}"}; do
        IFS='|' read -r _ _ pp _ _ _ _ <<< "$p"
        [[ "$pp" == "$cpath" ]] && { exists=1; break; }
      done
      (( exists )) && continue
      if confirm "  includere '$cname'?"; then
        local eid; eid="$(ask "    id" "$cname")"
        local etype; etype="$(ask "    type" "$ctype")"
        local eruntime; eruntime="$(ask "    runtime" "$cruntime")"
        local erole; erole="$(ask "    role" "secondary")"
        projects+=("$eid|$cname|$cpath|$etype|$eruntime|$erole|$cremote")
      fi
    done
  fi

  # check unicità id
  local seen=""
  for p in ${projects[@]+"${projects[@]}"}; do
    IFS='|' read -r pid _ <<< "$p"
    if [[ " $seen " == *" $pid "* ]]; then
      err "id duplicato: $pid"; return 1
    fi
    seen="$seen $pid"
  done

  write_manifest "$manifest" "$root" "$(basename "$spec")" ${projects[@]+"${projects[@]}"}
  ok "Manifest scritto: $manifest"

  title "Riepilogo"
  for p in ${projects[@]+"${projects[@]}"}; do
    IFS='|' read -r id name path type runtime role _ <<< "$p"
    printf '  %-14s %-26s %-14s %-8s %-8s %-10s\n' "$id" "$name" "$path" "$type" "$runtime" "$role"
  done
}

# ---------- scan ----------
cmd_scan() {
  local target="${1:-.}"
  [[ -d "$target" ]] || { err "Directory non esistente: $target"; return 1; }
  title "Scan: $target"
  local found=0
  while IFS='|' read -r name path type runtime remote; do
    found=$(( found + 1 ))
    printf '  %-26s %-14s %-8s %s\n' "$name" "$type" "$runtime" "$remote"
  done < <(scan_dir "$target")
  (( found == 0 )) && warn "Nessun progetto trovato."
  dim "  totale: $found"
}

# ---------- add ----------
cmd_add() {
  local target=""
  local manifest=""
  while (( $# )); do
    case "$1" in
      --manifest) manifest="$2"; shift 2 ;;
      -h|--help)  say "usage: run-project.sh add [DIR] [--manifest FILE]"; return 0 ;;
      *) target="$1"; shift ;;
    esac
  done

  if [[ -z "$manifest" ]]; then
    if [[ -f "$DEFAULT_MANIFEST_NAME" ]]; then
      manifest="$DEFAULT_MANIFEST_NAME"
    else
      err "Manifest non trovato. Usa --manifest PATH oppure esegui dalla root del workspace."
      return 1
    fi
  fi
  [[ -f "$manifest" ]] || { err "Manifest non trovato: $manifest"; return 1; }

  [[ -z "$target" ]] && target="."
  [[ -d "$target" ]] || { err "Directory non esistente: $target"; return 1; }

  title "Add da scan: $target"

  # leggi progetti esistenti
  local existing=()
  while IFS= read -r line; do existing+=("$line"); done < <(read_manifest_projects "$manifest")

  # materializza scan prima di qualsiasi interazione
  local scan_lines=()
  while IFS= read -r l; do
    [[ -n "$l" ]] && scan_lines+=("$l")
  done < <(scan_dir "$target")

  local added=0
  for line in ${scan_lines[@]+"${scan_lines[@]}"}; do
    IFS='|' read -r name path type runtime remote <<< "$line"

    local exists=0
    for p in ${existing[@]+"${existing[@]}"}; do
      IFS='|' read -r _ _ ep _ _ _ _ <<< "$p"
      [[ "$ep" == "$path" ]] && { exists=1; break; }
    done
    (( exists )) && { dim "  già presente: $name"; continue; }

    say ""
    printf '  %s%s%s\n' "$BOLD" "$name" "$RESET"
    printf '    type=%s  runtime=%s  remote=%s\n' "$type" "$runtime" "$remote"
    if confirm "  includere?"; then
      local eid; eid="$(ask "    id" "$name")"
      local etype; etype="$(ask "    type" "$type")"
      local eruntime; eruntime="$(ask "    runtime" "$runtime")"
      local erole; erole="$(ask "    role" "secondary")"

      local dup=0
      for p in ${existing[@]+"${existing[@]}"}; do
        IFS='|' read -r ep _ <<< "$p"
        [[ "$ep" == "$eid" ]] && dup=1
      done
      if (( dup )); then
        err "id duplicato: $eid"; continue
      fi

      existing+=("$eid|$name|$path|$etype|$eruntime|$erole|$remote")
      added=$(( added + 1 ))
      ok "  aggiunto: $eid"
    fi
  done

  if (( added == 0 )); then
    warn "Nessun progetto aggiunto."
    return 0
  fi

  # preserva root e spec dal manifest corrente
  local root spec
  root="$(grep -E '^workspaceRoot:' "$manifest" | sed -E 's/^workspaceRoot:[[:space:]]*"(.*)"$/\1/')"
  spec="$(grep -E '^resolvedFrom:' "$manifest" | sed -E 's/^resolvedFrom:[[:space:]]*"(.*)"$/\1/' || true)"

  write_manifest "$manifest" "$root" "$spec" ${existing[@]+"${existing[@]}"}
  ok "Manifest aggiornato ($added aggiunti): $manifest"
}

# ---------- validate ----------
cmd_validate() {
  local spec="$DEFAULT_SPEC_NAME"
  local manifest="$DEFAULT_MANIFEST_NAME"
  while (( $# )); do
    case "$1" in
      --spec)     spec="$2"; shift 2 ;;
      --manifest) manifest="$2"; shift 2 ;;
      *) break ;;
    esac
  done

  [[ -f "$manifest" ]] || { err "Manifest non trovato: $manifest"; return 1; }

  local root
  root="$(grep -E '^workspaceRoot:' "$manifest" | sed -E 's/^workspaceRoot:[[:space:]]*"(.*)"$/\1/')"

  title "Validate"
  local errors=0

  say ""
  dim "  [1] esistenza path"
  while IFS= read -r p; do
    IFS='|' read -r id _ path _ _ _ _ <<< "$p"
    if [[ -d "$root/$path" ]]; then
      ok "  $id → $path"
    else
      err "  $id → $path (mancante)"; errors=$(( errors + 1 ))
    fi
  done < <(read_manifest_projects "$manifest")

  if [[ -f "$spec" ]]; then
    say ""
    dim "  [2] mandatory dello spec presenti nel manifest"
    while IFS='|' read -r sid _ _ _ _ _; do
      [[ -z "$sid" ]] && continue
      local found=0
      while IFS= read -r p; do
        IFS='|' read -r id _ <<< "$p"
        [[ "$id" == "$sid" ]] && found=1
      done < <(read_manifest_projects "$manifest")
      if (( found )); then ok "  $sid"; else err "  $sid (mancante)"; errors=$(( errors + 1 )); fi
    done < <(read_spec_mandatory "$spec")
  else
    dim "  [2] spec non presente, skip"
  fi

  say ""
  dim "  [3] unicità id"
  local seen=""
  local dup_found=0
  while IFS= read -r p; do
    IFS='|' read -r id _ <<< "$p"
    if [[ " $seen " == *" $id "* ]]; then
      err "  id duplicato: $id"; errors=$(( errors + 1 )); dup_found=1
    fi
    seen="$seen $id"
  done < <(read_manifest_projects "$manifest")
  (( dup_found == 0 )) && ok "  tutti unici"

  say ""
  if (( errors == 0 )); then
    ok "Manifest valido."
  else
    err "Trovati $errors problemi."
    return 1
  fi
}

# ---------- show ----------
cmd_show() {
  local m="${1:-$DEFAULT_MANIFEST_NAME}"
  [[ -f "$m" ]] || { err "Manifest non trovato: $m"; return 1; }
  cat "$m"
}

# ---------- help ----------
cmd_help() {
  cat <<EOF
${BOLD}run-project.sh${RESET} — Nexus-Lab workspace manager

${BOLD}USO${RESET}
  run-project.sh setup [--spec FILE] [--manifest FILE]
      Guidato da nexus.spec.yaml. Chiede solo i path dei mandatory,
      poi opzionalmente scansiona e aggiunge extra.

  run-project.sh add [DIR] [--manifest FILE]
      Scansiona DIR (default: cwd) e appende i progetti scelti al manifest.

  run-project.sh scan [DIR]
      Sola lettura. Mostra i candidati in DIR.

  run-project.sh validate [--spec FILE] [--manifest FILE]
      Verifica: path esistono, mandatory presenti, id unici.

  run-project.sh show [FILE]
      Mostra il manifest.

  run-project.sh init
      Bootstrap libero senza spec (legacy).

  run-project.sh help

${BOLD}DEFAULT${RESET}
  Spec:     $DEFAULT_SPEC_NAME
  Manifest: $DEFAULT_MANIFEST_NAME

${BOLD}SCHEMA 0.2${RESET}
  project:
    id        chiave stabile (kebab-case)
    name      etichetta umana
    path      relativo a workspaceRoot
    type      app | library | scripts | documentation | rules | research | container
    runtime   node | python | js | rust | go | shell | -
    role      root | primary | secondary | temp
    git       null | { remote: <url> }
EOF
}

# ---------- legacy init ----------
cmd_init() {
  local root; root="$(ask "Workspace root" "$(pwd)")"
  [[ -d "$root" ]] || { err "Directory non esistente: $root"; return 1; }
  root="$(abs_path "$root")"
  local manifest="$root/$DEFAULT_MANIFEST_NAME"
  if [[ -e "$manifest" ]]; then
    warn "Manifest già esistente: $manifest"
    confirm "Sovrascrivere?" || { say "Annullato."; return 0; }
  fi

  # materializza scan prima di interazione
  local scan_lines=()
  while IFS= read -r l; do
    [[ -n "$l" ]] && scan_lines+=("$l")
  done < <(scan_dir "$root")

  local projects=()
  title "Scan top-level: $root"
  for line in ${scan_lines[@]+"${scan_lines[@]}"}; do
    IFS='|' read -r name path type runtime remote <<< "$line"
    if confirm "  includere '$name'?"; then
      local eid; eid="$(ask "    id" "$name")"
      local etype; etype="$(ask "    type" "$type")"
      local eruntime; eruntime="$(ask "    runtime" "$runtime")"
      local erole; erole="$(ask "    role" "secondary")"
      projects+=("$eid|$name|$path|$etype|$eruntime|$erole|$remote")
    fi
  done

  write_manifest "$manifest" "$root" "" ${projects[@]+"${projects[@]}"}
  ok "Manifest scritto: $manifest"
}

# ---------- entrypoint ----------
case "${1:-}" in
  setup)    shift; cmd_setup "$@" ;;
  add)      shift; cmd_add "$@" ;;
  scan)     shift; cmd_scan "$@" ;;
  validate) shift; cmd_validate "$@" ;;
  show)     shift; cmd_show "${1:-}" ;;
  init)     shift; cmd_init "$@" ;;
  help|-h|--help|"") cmd_help ;;
  *) err "Comando sconosciuto: $1"; cmd_help; exit 1 ;;
esac