// Chapter 11 §11.1: what "conforms" means in the WebAssembly build.
//
//   node scripts/wasm_conforms.mjs data/shacl
//
// shacl-wasm-node 0.3.0 and 0.3.1 kept the old rule (only sh:Violation breaks
// conformance) after the CLI and Python bindings had moved to the specification's.
// 0.3.2 caught up. This validates a warnings-only graph through the package and
// prints the verdict.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const require = createRequire(import.meta.url);
const { Validator } = require('shacl-wasm-node');
const pkg = require('shacl-wasm-node/package.json');

const dir = process.argv[2];
const data = readFileSync(join(dir, 'data.ttl'), 'utf8');
for (const file of ['shapes-warning.ttl', 'shapes-violation.ttl']) {
  const v = Validator.fromTurtle(readFileSync(join(dir, file), 'utf8'));
  const report = v.validateTurtle(data, null, 'none');
  const severities = report.results.map((r) => String(r.severity ?? r.resultSeverity ?? '?'));
  console.log(`shacl-wasm-node ${pkg.version}  ${file.padEnd(22)} conforms=${report.conforms}  results=${report.results.length}  severities=${severities.join(',')}`);
}

// §11.7: rules through the same build, and a mode that does not exist.
const rules = Validator.fromTurtle(readFileSync(join(dir, '..', 'rules', 'triple.ttl'), 'utf8'));
const people = readFileSync(join(dir, '..', 'rules', 'people.ttl'), 'utf8');
for (const mode of ['none', 'rules', 'bogus']) {
  try {
    const r = rules.validateTurtle(people, null, mode);
    console.log(`inference=${mode.padEnd(6)} conforms=${r.conforms}  results=${r.results.length}`);
  } catch (e) {
    console.log(`inference=${mode.padEnd(6)} ERROR: ${e.message ?? e}`);
  }
}
