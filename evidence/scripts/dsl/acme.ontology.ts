// Chapter 8 §8.2: the Acme fixture's core, written with the ontology-suite DSL,
// deliberate contradiction included. Run with tsx; writes Turtle to argv[2].
//
//   node node_modules/tsx/dist/cli.mjs scripts/dsl/acme.ontology.ts work/C08_10/acme.ttl
import { ontology, defontology, defclass, defobjectproperty,
         defdatatypeproperty, datatype, build } from 'ontology-suite/dsl';
import { Writer } from 'n3';
import { writeFileSync } from 'node:fs';

ontology('https://acme.example.org/ns/', 'acme');
defontology('https://acme.example.org/ns/1.0.0', { label: 'Acme Robotics org chart' });

const Department = defclass('Department', { label: [{ value: 'Department', language: 'en' }] });
const Employee   = defclass('Employee',   { label: [{ value: 'Employee',   language: 'en' }] });
defclass('Engineer', { subClassOf: [Employee] });

// The fixture's contradiction, written as code.
defclass('Contractor', { subClassOf: [Employee], disjointWith: [Employee] });

defobjectproperty('worksIn', { domain: Employee, range: Department });
defdatatypeproperty('hasEmployeeId', { domain: Employee, range: datatype('xsd:string') });

const { quads, prefixes } = build();
const w = new Writer({ prefixes });
// No cast: from 0.16.1 the bundled Quad type is n3's (C08.16). Up to 0.16.0
// this line needed `quads as any` to compile, though it ran.
w.addQuads(quads);
w.end((_e: unknown, ttl: string) => writeFileSync(process.argv[2], ttl));
