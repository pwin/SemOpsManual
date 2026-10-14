// Chapter 8 §8.2: a mistake of kind. Since 0.15.0 a datatype property's range
// is a datatype, made with datatype('xsd:string'), not a bare string. The type
// checker refuses this file; run without it, the DSL throws an internal TypeError.
import { ontology, defclass, defdatatypeproperty } from 'ontology-suite/dsl';

ontology('https://acme.example.org/ns/', 'acme');
const Employee = defclass('Employee');
defdatatypeproperty('hasEmployeeId', { domain: Employee, range: 'xsd:string' });
