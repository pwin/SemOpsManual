// Chapter 8 §8.2: the inline inverse, new in the DSL at 0.16.0. "A part of some
// Car" written without minting a named inverse property, as MDL-001 recommends.
// Run with tsx; writes Turtle to argv[2].
import { ontology, defclass, defobjectproperty, some, inverse, build } from 'ontology-suite/dsl';
import { Writer } from 'n3';
import { writeFileSync } from 'node:fs';

ontology('https://example.org/cars/', 'car');
const Car = defclass('Car');
const hasPart = defobjectproperty('hasPart');
defclass('CarPart', { subClassOf: [some(inverse(hasPart), Car)] });

const { quads, prefixes } = build();
const w = new Writer({ prefixes });
w.addQuads(quads as any);   // the bundled Quad type and @types/n3 disagree (C08.16)
w.end((_e: unknown, ttl: string) => writeFileSync(process.argv[2], ttl));
