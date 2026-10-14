// Chapter 8 §8.2 / Chapter 14 §14.4: the usage the package README suggests,
// build().quads handed to n3's Writer, without a cast. Under strict TypeScript with
// @types/n3 installed, the bundled Quad type is not assignable to n3's.
import { ontology, defclass, build } from 'ontology-suite/dsl';
import { Writer } from 'n3';

ontology('https://acme.example.org/ns/', 'acme');
defclass('Employee');
const { quads, prefixes } = build();
new Writer({ prefixes }).addQuads(quads);
