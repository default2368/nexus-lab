#!/usr/bin/env bash
# Nexus Lab control-plane workspace resolver.
#
# This root script is intentionally a thin, dependency-free launcher. The P0
# contract uses JSON documents and Node's built-in JSON parser; no npm package
# or handwritten YAML parser is required.
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

if ! command -v node >/dev/null 2>&1; then
  printf '%s\n' '✗ Node.js is required for run-project.sh (JSON.parse, no external packages).' >&2
  exit 127
fi

export NEXUS_CONTROL_PLANE_ROOT="$SCRIPT_DIR"
exec node - "$@" <<'NODE'
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');

const CONTROL_PLANE_ROOT = path.resolve(process.env.NEXUS_CONTROL_PLANE_ROOT || process.cwd());
const DEFAULT_SPEC = path.join(CONTROL_PLANE_ROOT, 'nexus.spec.json');
const DEFAULT_LOCAL = path.join(CONTROL_PLANE_ROOT, '.nexus', 'workspace.local.json');
const DEFAULT_LOCK = path.join(CONTROL_PLANE_ROOT, '.nexus', 'workspace.lock.json');
const RUN_ROOT = path.join(CONTROL_PLANE_ROOT, 'workspaces');

const ID_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const TYPES = new Set(['app', 'library', 'scripts', 'documentation', 'rules', 'research', 'container']);
const RUNTIMES = new Set(['node', 'python', 'js', 'rust', 'go', 'shell', '-']);
const ROLES = new Set(['root', 'control-plane', 'primary', 'secondary', 'temp']);
const SPEC_SCHEMA = 'nexus-lab/workspace-spec/v1';
const LOCAL_SCHEMA = 'nexus-lab/workspace-local/v1';
const LOCK_SCHEMA = 'nexus-lab/workspace-lock/v1';
const RECEIPT_DIR = path.join(CONTROL_PLANE_ROOT, '.nexus', 'receipts');

class ContractError extends Error {}

function fail(message) {
  throw new ContractError(message);
}

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function assertObject(value, label) {
  if (!isObject(value)) fail(`${label} deve essere un oggetto JSON.`);
}

function readJson(file, label) {
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch (error) {
    fail(`${label} non leggibile: ${file}`);
  }
  try {
    return JSON.parse(text);
  } catch (error) {
    fail(`${label} non è JSON valido: ${file}`);
  }
}

function isSymlink(file) {
  try {
    return fs.lstatSync(file).isSymbolicLink();
  } catch (error) {
    return false;
  }
}

function ensureRegularFile(file, label) {
  let stat;
  try {
    stat = fs.lstatSync(file);
  } catch (error) {
    fail(`${label} non trovato: ${file}`);
  }
  if (!stat.isFile() || stat.isSymbolicLink()) fail(`${label} deve essere un file regolare: ${file}`);
}

function ensureDirectory(dir, label) {
  let stat;
  try {
    stat = fs.lstatSync(dir);
  } catch (error) {
    fail(`${label} non trovato: ${dir}`);
  }
  if (!stat.isDirectory() || stat.isSymbolicLink()) fail(`${label} deve essere una directory reale: ${dir}`);
}

function assertId(value, label) {
  if (typeof value !== 'string' || !ID_RE.test(value)) {
    fail(`${label} non è un ID kebab-case valido: ${String(value)}`);
  }
}

function assertRelativePath(value, label) {
  if (typeof value !== 'string' || value.length === 0 || value.includes('\0')) {
    fail(`${label} deve essere un path relativo non vuoto.`);
  }
  if (path.isAbsolute(value) || /^[A-Za-z]:[\\/]/.test(value)) {
    fail(`${label} non può essere assoluto: ${value}`);
  }
  const parts = value.replaceAll('\\', '/').split('/');
  if (parts.includes('..')) fail(`${label} contiene traversal: ${value}`);
}

function isWithin(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (relative !== '..' && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative));
}

function realPath(file, label) {
  let resolved;
  try {
    resolved = fs.realpathSync(file);
  } catch (error) {
    fail(`${label} non risolvibile: ${file}`);
  }
  return resolved;
}

function stableValue(value) {
  if (Array.isArray(value)) return value.map(stableValue);
  if (isObject(value)) {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stableValue(value[key])]));
  }
  return value;
}

function stableJson(value) {
  return `${JSON.stringify(stableValue(value))}\n`;
}

function sha256(value) {
  return crypto.createHash('sha256').update(typeof value === 'string' ? value : stableJson(value), 'utf8').digest('hex');
}

function sanitizeRemote(remote) {
  if (remote === null || remote === undefined || remote === '') return null;
  if (typeof remote !== 'string') fail('git.remote deve essere una stringa.');
  let value = remote.trim();
  if (!value) return null;

  if (/^[A-Za-z0-9.-]+(?::[0-9]+)?\/.+/.test(value) && !value.includes('://')) {
    return value.replaceAll('\\\\', '/');
  }

  const scp = value.match(/^(?:[^@/]+@)?([^:/]+):(.+)$/);
  if (scp && !value.includes('://')) return `${scp[1]}/${scp[2]}`.replace(/\/+/g, '/');

  try {
    const parsed = new URL(value);
    if (!parsed.hostname) fail(`remote non valido: ${remote}`);
    return `${parsed.hostname}${parsed.port ? `:${parsed.port}` : ''}${parsed.pathname}`.replace(/\/+/g, '/');
  } catch (error) {
    fail(`remote non valido: ${remote}`);
  }
}

function safeGit(projectRoot, args) {
  try {
    return execFileSync('git', ['-C', projectRoot, ...args], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
      timeout: 5000,
      maxBuffer: 1024 * 1024,
    }).trim();
  } catch (error) {
    return null;
  }
}

function gitSnapshot(projectRoot) {
  const topLevel = safeGit(projectRoot, ['rev-parse', '--show-toplevel']);
  if (!topLevel) return null;
  return {
    root: realPath(topLevel, 'Git root'),
    head: safeGit(projectRoot, ['rev-parse', 'HEAD']),
    remote: sanitizeRemote(safeGit(projectRoot, ['remote', 'get-url', 'origin'])),
  };
}

function validateSpec(spec) {
  assertObject(spec, 'Spec');
  if (spec.schemaVersion !== SPEC_SCHEMA) fail(`schemaVersion spec non supportata: ${String(spec.schemaVersion)}`);
  assertId(spec.workspaceId, 'workspaceId');
  if (!Array.isArray(spec.projects) || spec.projects.length === 0) fail('La spec deve contenere almeno un project.');

  const ids = new Set();
  for (const project of spec.projects) {
    assertObject(project, 'project');
    assertId(project.id, 'project.id');
    if (ids.has(project.id)) fail(`project.id duplicato: ${project.id}`);
    ids.add(project.id);
    if (typeof project.name !== 'string' || project.name.length === 0) fail(`name mancante per ${project.id}`);
    assertRelativePath(project.path, `path di ${project.id}`);
    if (!TYPES.has(project.type)) fail(`type non supportato per ${project.id}: ${project.type}`);
    if (!RUNTIMES.has(project.runtime)) fail(`runtime non supportato per ${project.id}: ${project.runtime}`);
    if (!ROLES.has(project.role)) fail(`role non supportato per ${project.id}: ${project.role}`);
    if (project.git !== null && project.git !== undefined) {
      assertObject(project.git, `git di ${project.id}`);
      sanitizeRemote(project.git.remote);
    }
  }

  const allowedPlanIds = spec.allowedPlanIds || [];
  if (!Array.isArray(allowedPlanIds)) fail('allowedPlanIds deve essere un array.');
  for (const planId of allowedPlanIds) assertId(planId, 'allowedPlanIds[]');
  if (new Set(allowedPlanIds).size !== allowedPlanIds.length) fail('allowedPlanIds contiene duplicati.');
}

function readLocal(localFile) {
  if (!fs.existsSync(localFile)) {
    return { schemaVersion: LOCAL_SCHEMA, programWorkspaceRoot: CONTROL_PLANE_ROOT, projectPaths: {} };
  }
  ensureRegularFile(localFile, 'Binding locale');
  const local = readJson(localFile, 'Binding locale');
  assertObject(local, 'Binding locale');
  if (local.schemaVersion !== LOCAL_SCHEMA) fail(`schemaVersion local non supportata: ${String(local.schemaVersion)}`);
  if (local.programWorkspaceRoot !== undefined && typeof local.programWorkspaceRoot !== 'string') {
    fail('programWorkspaceRoot locale deve essere una stringa.');
  }
  if (local.projectPaths !== undefined && !isObject(local.projectPaths)) fail('projectPaths locale deve essere un oggetto.');
  return {
    schemaVersion: LOCAL_SCHEMA,
    programWorkspaceRoot: local.programWorkspaceRoot || CONTROL_PLANE_ROOT,
    projectPaths: local.projectPaths || {},
  };
}

function resolveBinding(local) {
  const programRootCandidate = path.isAbsolute(local.programWorkspaceRoot)
    ? local.programWorkspaceRoot
    : path.resolve(CONTROL_PLANE_ROOT, local.programWorkspaceRoot);
  const programRoot = realPath(programRootCandidate, 'PROGRAM_WORKSPACE_ROOT');
  const controlPlaneRoot = realPath(CONTROL_PLANE_ROOT, 'CONTROL_PLANE_ROOT');
  if (!isWithin(programRoot, controlPlaneRoot)) {
    fail('CONTROL_PLANE_ROOT deve essere dentro PROGRAM_WORKSPACE_ROOT.');
  }
  return { programRoot, controlPlaneRoot };
}

function resolveWorkspace(spec, local) {
  validateSpec(spec);
  const { programRoot, controlPlaneRoot } = resolveBinding(local);
  const projectPaths = local.projectPaths || {};
  const projects = spec.projects.map((project) => {
    const override = Object.prototype.hasOwnProperty.call(projectPaths, project.id)
      ? projectPaths[project.id]
      : project.path;
    if (typeof override !== 'string' || override.length === 0) fail(`path locale non valido per ${project.id}`);
    const projectCandidate = path.isAbsolute(override) ? override : path.resolve(programRoot, override);
    const resolvedPath = realPath(projectCandidate, `project ${project.id}`);
    if (!isWithin(programRoot, resolvedPath)) fail(`project ${project.id} esce da PROGRAM_WORKSPACE_ROOT.`);
    return {
      id: project.id,
      name: project.name,
      path: project.path,
      resolvedPath,
      type: project.type,
      runtime: project.runtime,
      role: project.role,
      git: project.git ? { remote: sanitizeRemote(project.git.remote) } : null,
      gitSnapshot: gitSnapshot(resolvedPath),
    };
  });

  const controlPlaneProject = projects.find((project) => project.role === 'control-plane');
  if (!controlPlaneProject) fail('La spec deve dichiarare un project role=control-plane.');
  if (realPath(controlPlaneProject.resolvedPath, 'control-plane project') !== controlPlaneRoot) {
    fail('Il project role=control-plane deve puntare a CONTROL_PLANE_ROOT.');
  }

  const semantic = {
    schemaVersion: LOCK_SCHEMA,
    workspaceId: spec.workspaceId,
    programWorkspaceRoot: programRoot,
    controlPlaneRoot,
    runWorkspacesRoot: RUN_ROOT,
    allowedPlanIds: [...(spec.allowedPlanIds || [])].sort(),
    projects: projects.sort((a, b) => a.id.localeCompare(b.id)),
  };
  const specDigest = sha256(spec);
  const bindingDigest = sha256({
    schemaVersion: local.schemaVersion,
    programWorkspaceRoot: programRoot,
    projectPaths: Object.fromEntries(Object.keys(projectPaths).sort().map((key) => [key, projectPaths[key]])),
  });
  const resolutionDigest = sha256(semantic);
  return {
    ...semantic,
    digests: { specDigest, bindingDigest, resolutionDigest },
    metadata: { generatedAt: new Date().toISOString() },
  };
}

function atomicWriteJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  const temporary = `${file}.tmp-${process.pid}-${crypto.randomBytes(6).toString('hex')}`;
  const fd = fs.openSync(temporary, 'wx', 0o600);
  try {
    fs.writeFileSync(fd, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
    fs.fsyncSync(fd);
  } finally {
    fs.closeSync(fd);
  }
  fs.renameSync(temporary, file);
}

function parseOptions(args) {
  const options = {};
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (!arg.startsWith('--')) fail(`Opzione sconosciuta: ${arg}`);
    const key = arg.slice(2);
    const value = args[index + 1];
    if (!value || value.startsWith('--')) fail(`Valore mancante per --${key}`);
    options[key] = value;
    index += 1;
  }
  return options;
}

function pathsFromOptions(options) {
  return {
    spec: path.resolve(options.spec || DEFAULT_SPEC),
    local: path.resolve(options.local || DEFAULT_LOCAL),
    lock: path.resolve(options.lock || DEFAULT_LOCK),
  };
}

function loadResolution(options) {
  const locations = pathsFromOptions(options);
  ensureRegularFile(locations.spec, 'Spec');
  const spec = readJson(locations.spec, 'Spec');
  const local = readLocal(locations.local);
  const lock = resolveWorkspace(spec, local);
  return { locations, spec, local, lock };
}

function commandResolve(options) {
  const { locations, lock } = loadResolution(options);
  atomicWriteJson(locations.lock, lock);
  console.log(`resolved workspace=${lock.workspaceId}`);
  console.log(`specDigest=${lock.digests.specDigest}`);
  console.log(`bindingDigest=${lock.digests.bindingDigest}`);
  console.log(`resolutionDigest=${lock.digests.resolutionDigest}`);
  console.log(`lock=${locations.lock}`);
}

function commandValidate(options) {
  const { locations, lock } = loadResolution(options);
  if (fs.existsSync(locations.lock)) {
    const existing = readJson(locations.lock, 'Lock');
    if (!isObject(existing) || !isObject(existing.digests)) fail('Lock privo di digests.');
    for (const key of ['specDigest', 'bindingDigest', 'resolutionDigest']) {
      if (existing.digests[key] !== lock.digests[key]) fail(`Lock non aggiornato: ${key}`);
    }
  }
  console.log(`valid workspace=${lock.workspaceId}`);
  console.log(`projects=${lock.projects.length}`);
}

function commandShow(options) {
  const locations = pathsFromOptions(options);
  ensureRegularFile(locations.lock, 'Lock');
  const lock = readJson(locations.lock, 'Lock');
  console.log(JSON.stringify(lock, null, 2));
}

function runIdIsValid(runId) {
  return typeof runId === 'string' && /^run-[0-9TZ-]+-[a-f0-9]{12}$/.test(runId);
}

function ensureRunRoot() {
  if (fs.existsSync(RUN_ROOT)) ensureDirectory(RUN_ROOT, 'RUN_WORKSPACES_ROOT');
  else fs.mkdirSync(RUN_ROOT, { recursive: true, mode: 0o700 });
  const realRoot = realPath(RUN_ROOT, 'RUN_WORKSPACES_ROOT');
  if (realRoot !== path.resolve(RUN_ROOT)) fail('RUN_WORKSPACES_ROOT non può essere un symlink.');
}

function markerPath(runId) {
  if (!runIdIsValid(runId)) fail(`run ID non valido: ${runId}`);
  return path.join(RUN_ROOT, runId, '.nexus-run.json');
}

function readMarker(runId) {
  const marker = markerPath(runId);
  if (!fs.existsSync(RUN_ROOT)) fail(`RUN_WORKSPACES_ROOT non trovato: ${RUN_ROOT}`);
  ensureDirectory(RUN_ROOT, 'RUN_WORKSPACES_ROOT');
  const runDir = path.dirname(marker);
  ensureDirectory(runDir, 'run workspace');
  if (isSymlink(runDir)) fail('run workspace symlink non autorizzato.');
  ensureRegularFile(marker, 'Marker run');
  const value = readJson(marker, 'Marker run');
  if (value.runId !== runId) fail('run ID del marker non corrisponde.');
  return { marker, value, runDir };
}

function commandAllocate(options) {
  if (!options.plan) fail('Manca --plan.');
  assertId(options.plan, 'planId');
  const { lock } = loadResolution(options);
  if (!lock.allowedPlanIds.includes(options.plan)) {
    fail(`Piano non autorizzato dalla spec: ${options.plan}`);
  }
  ensureRunRoot();
  const timestamp = new Date().toISOString().replace(/[-:.]/g, '').replace(/Z$/, 'Z');
  const runId = `run-${timestamp}-${crypto.randomBytes(6).toString('hex')}`;
  const runDir = path.join(RUN_ROOT, runId);
  fs.mkdirSync(runDir, { recursive: false, mode: 0o700 });
  const marker = {
    schemaVersion: 'nexus-lab/run-marker/v1',
    runId,
    workspaceId: lock.workspaceId,
    planId: options.plan,
    planDigest: sha256({ planId: options.plan, source: 'spec-allowlist' }),
    lockDigest: lock.digests.resolutionDigest,
    status: 'ALLOCATED',
    createdAt: new Date().toISOString(),
  };
  atomicWriteJson(path.join(runDir, '.nexus-run.json'), marker);
  console.log(`allocated run=${runId}`);
}

function commandStatus(options) {
  if (!options['run-id']) fail('Manca --run-id.');
  const { value } = readMarker(options['run-id']);
  console.log(JSON.stringify(value, null, 2));
}

function commandFinalize(options) {
  if (!options['run-id']) fail('Manca --run-id.');
  if (!options.receipt) fail('Manca --receipt.');
  const { value, runDir } = readMarker(options['run-id']);
  const receiptCandidate = path.isAbsolute(options.receipt)
    ? options.receipt
    : path.resolve(process.cwd(), options.receipt);
  ensureRegularFile(receiptCandidate, 'Receipt');
  const receipt = realPath(receiptCandidate, 'Receipt');
  if (!isWithin(realPath(runDir, 'run workspace'), receipt)) fail('La receipt deve stare dentro il run workspace.');
  const receiptValue = readJson(receipt, 'Receipt');
  assertObject(receiptValue, 'Receipt');
  if (receiptValue.runId !== options['run-id']) fail('runId della receipt non corrisponde.');
  fs.mkdirSync(RECEIPT_DIR, { recursive: true, mode: 0o700 });
  const finalReceipt = path.join(RECEIPT_DIR, `${options['run-id']}.json`);
  atomicWriteJson(finalReceipt, receiptValue);
  value.status = 'FINALIZED';
  value.receipt = path.relative(CONTROL_PLANE_ROOT, finalReceipt);
  atomicWriteJson(path.join(runDir, '.nexus-run.json'), value);
  console.log(`finalized run=${options['run-id']}`);
}

function commandClean(options) {
  if (!options['run-id']) fail('Manca --run-id.');
  const { value, runDir } = readMarker(options['run-id']);
  if (value.status !== 'FINALIZED') fail('Cleanup rifiutato: receipt non finalizzata.');
  const root = realPath(RUN_ROOT, 'RUN_WORKSPACES_ROOT');
  const resolvedRunDir = realPath(runDir, 'run workspace');
  if (!isWithin(root, resolvedRunDir) || resolvedRunDir === root) fail('Path run non autorizzato.');
  if (isSymlink(runDir)) fail('Cleanup rifiutato: run workspace symlink.');
  fs.rmSync(runDir, { recursive: true, force: false });
  console.log(`cleaned run=${options['run-id']}`);
}

function help() {
  console.log(`Nexus Lab control-plane workspace manager\n\n` +
`Usage\n` +
`  ./run-project.sh resolve [--spec FILE] [--local FILE] [--lock FILE]\n` +
`  ./run-project.sh validate [--spec FILE] [--local FILE] [--lock FILE]\n` +
`  ./run-project.sh show [--lock FILE]\n` +
`  ./run-project.sh run allocate --plan PLAN_ID [--spec FILE] [--local FILE] [--lock FILE]\n` +
`  ./run-project.sh run status --run-id RUN_ID\n` +
`  ./run-project.sh run finalize --run-id RUN_ID --receipt FILE\n` +
`  ./run-project.sh run clean --run-id RUN_ID\n`);
}

function main() {
  const args = process.argv.slice(2);
  const command = args.shift() || 'help';
  if (command === 'help' || command === '--help' || command === '-h') return help();
  if (command === 'resolve') return commandResolve(parseOptions(args));
  if (command === 'validate') return commandValidate(parseOptions(args));
  if (command === 'show') return commandShow(parseOptions(args));
  if (command !== 'run') fail(`Comando sconosciuto: ${command}`);
  const action = args.shift();
  const options = parseOptions(args);
  if (action === 'allocate') return commandAllocate(options);
  if (action === 'status') return commandStatus(options);
  if (action === 'finalize') return commandFinalize(options);
  if (action === 'clean') return commandClean(options);
  fail(`Azione run sconosciuta: ${String(action)}`);
}

try {
  main();
} catch (error) {
  if (error instanceof ContractError) {
    console.error(`✗ ${error.message}`);
    process.exitCode = 1;
  } else {
    console.error(`✗ ${error.message}`);
    process.exitCode = 1;
  }
}
NODE
