#!/usr/bin/env node
// Design Enforcement — Style Authority checker (0.7.0.2, ADR-0012/PRD-0013).
//
// Rule: visual values must flow through Design Authority (semantic tokens)
// or Primitive Authority. Raw palette classes / hex / rgb/rgba are violations
// unless covered by the Exception Registry below.
//
// Categories (docs/design/STYLE-INVENTORY.md):
//   A compliant · B/D violations (error) · C/E allowed exceptions (with key)
//
// Usage:
//   node scripts/design/check-style-authority.mjs            # report
//   node scripts/design/check-style-authority.mjs --json     # machine-readable
//   node scripts/design/check-style-authority.mjs --ci       # exit 1 on error

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const ROOT = process.cwd();
const SRC = join(ROOT, 'src');
const EXTENSIONS = new Set(['.tsx', '.ts', '.astro', '.css']);
const SKIP_DIRS = new Set(['node_modules', 'dist', '.astro']);

// ---------------------------------------------------------------------------
// Exception Registry (mirrors docs/design/exception-registry.md)
// category: external-brand | decorative-effect | legacy-frozen | presentation-candidate
// ---------------------------------------------------------------------------
export const EXCEPTIONS = [
  {
    key: 'external-brand:operations',
    category: 'external-brand',
    scope: ['src/react/dashboards/operations'],
    reason: 'Operations surface brand identity — becomes operationsAccent in presentation.manifest (0.7.0.3)',
  },
  {
    key: 'decorative-effect:overlays',
    category: 'decorative-effect',
    scope: ['src/components/ui/skeleton', 'src/react/components/common/GlassOverlay'],
    reason: 'Gloss/overlay rgba values with no semantic equivalent',
  },
  {
    key: 'external-brand:google',
    category: 'external-brand',
    scope: ['src/react/components/auth/AuthPage.tsx'],
    reason: 'Official Google brand colors (sign-in button) — no semantic equivalent by design',
  },
  {
    key: 'legacy-frozen:webpage-template',
    category: 'legacy-frozen',
    scope: ['src/react/templates/WebPageTemplate'],
    reason: 'Non-evolutive legacy template, excluded from Boy-Scout migration',
  },
  {
    key: 'legacy-frozen:pages',
    category: 'legacy-frozen',
    scope: ['src/pages/indexV0.astro', 'src/pages/indexV1.astro', 'src/pages/index.astro', 'src/pages/debug/', 'src/pages/build/', 'src/pages/landing.astro'],
    reason: 'Frozen landing/debug/legacy pages — not evolutive surfaces',
  },
];

// Semantic color roots permitted by the Design Authority (globals.css / tailwind.config).
// Raw palette roots (Tailwind defaults) are treated as Category B/D violations.
export const RAW_PALETTE_ROOTS = [
  'slate', 'gray', 'zinc', 'neutral', 'stone', 'red', 'orange', 'amber',
  'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan', 'sky', 'blue',
  'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose',
];

const PALETTE_CLASS_RE = new RegExp(
  String.raw`\b(?:bg|text|border|ring|from|to|via|fill|stroke|decoration|divide|outline|accent|caret|placeholder)-(${RAW_PALETTE_ROOTS.join('|')})-\d{2,3}(?:\/\d{1,3})?\b`,
  'g',
);
const ARBITRARY_HEX_CLASS_RE = /\b(?:bg|text|border|ring|from|to|via|fill|stroke)-\[(#(?:[0-9a-fA-F]{3,8}))\]/g;
const HEX_RE = /#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b/g;
const RGB_RE = /\brgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}/g;

function* walk(dir) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const st = statSync(full);
    if (st.isDirectory()) {
      if (!SKIP_DIRS.has(entry)) yield* walk(full);
    } else if (EXTENSIONS.has(entry.slice(entry.lastIndexOf('.')))) {
      yield full;
    }
  }
}
function inScope(relPath, scope) {
  return scope.some((s) => relPath.startsWith(s));
}

export function exceptionFor(relPath) {
  for (const ex of EXCEPTIONS) {
    if (inScope(relPath, ex.scope)) return ex;
  }
  return null;
}

/** Classify one file's source → list of findings. Pure; used by tests. */
export function classifySource(source, relPath) {
  const findings = [];
  const push = (kind, value, index, detail) => {
    const ex = exceptionFor(relPath);
    findings.push({
      kind, value, detail,
      line: source.slice(0, index).split('\n').length,
      file: relPath,
      status: ex ? 'allowed-exception' : 'error',
      exception: ex ? ex.key : null,
    });
  };
  for (const m of source.matchAll(PALETTE_CLASS_RE)) push('palette-class', m[0], m.index, m[1]);
  for (const m of source.matchAll(ARBITRARY_HEX_CLASS_RE)) push('arbitrary-hex', m[0], m.index, m[1]);
  for (const m of source.matchAll(HEX_RE)) {
    if (source.slice(Math.max(0, m.index - 2), m.index) === '-[') continue; // already captured as arbitrary class
    push('hex', m[0], m.index, null);
  }
  for (const m of source.matchAll(RGB_RE)) push('rgb', m[0], m.index, null);
  return findings;
}

export function scan() {
  const all = [];
  for (const file of walk(SRC)) {
    const rel = relative(ROOT, file).split(sep).join('/');
    const source = readFileSync(file, 'utf8');
    all.push(...classifySource(source, rel));
  }
  return all;
}

function report(findings, json) {
  const errors = findings.filter((f) => f.status === 'error');
  const allowed = findings.filter((f) => f.status === 'allowed-exception');
  if (json) {
    console.log(JSON.stringify({ total: findings.length, errors: errors.length, allowed: allowed.length, findings }, null, 2));
    return errors.length;
  }
  const byFile = new Map();
  for (const f of findings) {
    if (!byFile.has(f.file)) byFile.set(f.file, []);
    byFile.get(f.file).push(f);
  }
  console.log(`\nStyle Authority report — ${findings.length} findings (${errors.length} errors, ${allowed.length} allowed exceptions)\n`);
  for (const [file, items] of [...byFile.entries()].sort()) {
    const errs = items.filter((i) => i.status === 'error').length;
    console.log(`${errs ? '✗' : '○'} ${file}  (${errs} errors)`);
    for (const i of items.slice(0, 8)) {
      console.log(`   L${i.line}  [${i.status}]  ${i.kind}  ${i.value}${i.exception ? `  ← ${i.exception}` : ''}`);
    }
    if (items.length > 8) console.log(`   … +${items.length - 8} more`);
  }
  console.log('');
  return errors.length;
}

const isMain = process.argv[1] && process.argv[1].endsWith('check-style-authority.mjs');
if (isMain) {
  const errors = report(scan(), process.argv.includes('--json'));
  if (process.argv.includes('--ci') && errors > 0) process.exit(1);
}
