// Chapter 7 §7.1: the editor and CI on one sh:datatype constraint.
//
//   node scripts/datatype_gap.mjs data/datatypes
//
// Until 0.3.9 the engine checked the lexical form of only some datatypes, and
// let seven through by name: "not-a-year"^^xsd:gYear satisfied
// sh:datatype xsd:gYear. The extension's 0.18.0 release bundles shacl-wasm-node
// 0.3.8; a fresh install of the suite resolves shacl 0.3.9. This validates the
// same data through both builds (0.3.8 is installed under an npm alias) and
// names the focus node of each result.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const require = createRequire(import.meta.url);
const dir = process.argv[2];
const shapes = readFileSync(join(dir, 'shapes.ttl'), 'utf8');
const data = readFileSync(join(dir, 'data.ttl'), 'utf8');

for (const name of ['shacl-wasm-node-0.3.8', 'shacl-wasm-node']) {
  const { Validator } = require(name);
  const { version } = require(`${name}/package.json`);
  const report = Validator.fromTurtle(shapes).validateTurtle(data, null, 'none');
  const focus = report.results.map((r) => String(r.focusNode ?? r.focus ?? '?').replace('https://example.org/', 'ex:'));
  console.log(`shacl-wasm-node ${version}  conforms=${report.conforms}  results=${report.results.length}  focus=${focus.join(',') || '-'}`);
}
