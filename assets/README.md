# Brand assets

| File | Size | Use |
|---|---|---|
| `semantechs-logo.png` | 1024×1024 | Archival original |
| `semantechs-logo-320.png` | 320×320 | Every in-page header in this manual |

**Source:** <https://semantechs.co.uk/turtle-editor-viewer-new/assets/semantechsLogo-C3PGK8jf.jpeg>

Note that the source URL ends in `.jpeg` and is served as `Content-Type:
image/jpeg`, but the bytes are a PNG (1024×1024, 8-bit RGBA). It is stored here
with the correct `.png` extension.

Use the 320 px variant in pages — it is around a tenth of the file size and no
page in this manual displays the mark above 160 px.

## Palette

Sampled directly from the mark. Full rationale, usage rules and the Mermaid
`classDef` block in [Appendix A](../docs/diagram-style.md).

| Role | Stroke | Fill | Sampled from |
|---|---|---|---|
| Authoring / human work | `#FD5B1C` | `#FFE6DA` | turtle shell, upper field |
| Automation / CI gates | `#02B7D4` | `#D9F4FA` | the SPARQL hook |
| Data and ingestion | `#7CBA07` | `#ECF7D5` | turtle body |
| Operations / runtime | `#0CB88E` | `#D9F5EC` | lower-right field |
| Governance / decision | `#FE8902` | `#FFF0D6` | owl plumage |
| Not covered by tooling | `#8A93A0` | `#F1F3F5` | — (deliberately grey) |
| Text and edges | `#14243A` | — | outline ink |

Grey is reserved: it means "SemOps asks for this and the toolchain does not
provide it". Never use it decoratively.
