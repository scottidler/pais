# Rust Crates for Mermaid & Excalidraw Diagram Generation

**Research Date:** 2026-01-05

## Executive Summary

### Mermaid: Clear Winner - `aquamarine`
For **Mermaid diagram generation**, there is a clear winner: **aquamarine** (544 stars, 532K downloads/month). It's well-maintained, widely adopted, and the de facto standard for embedding Mermaid diagrams in Rust documentation.

### Excalidraw: No Clear Winner - Emerging Space
For **Excalidraw generation**, the ecosystem is immature. **excalidraw-dsl** (16 stars) shows the most promise as a general-purpose DSL, but it's not yet published on crates.io. **excalidocker-rs** (129 stars) is production-ready but domain-specific (docker-compose only).

---

## Mermaid Crates - Detailed Analysis

### 1. aquamarine (RECOMMENDED)

| Metric | Value |
|--------|-------|
| GitHub Stars | 544 |
| Downloads/month | ~532,000 |
| Dependents | 1,212 crates (74 direct) |
| Latest Version | 0.6.0 (Oct 2024) |
| License | MIT |
| Lib.rs Rank | #22 in Visualization |

**What it does:** Procedural macro that embeds Mermaid.js diagrams directly into rustdoc documentation.

**Key Features:**
- Integrates with `#[doc]` attributes via `#[aquamarine]` proc macro
- Automatic dark/light theme detection
- Custom theming support via Mermaid's `%init%` attribute
- Can load diagrams from external `.mmd` files via `include_mmd!`
- Requires rustc 1.38.0+

**Usage Example:**
```rust
#[cfg_attr(doc, aquamarine::aquamarine)]
/// ```mermaid
/// graph LR
///     A --> B
/// ```
pub fn my_function() {}
```

**Notable Users:** google/autocxx, teloxide

**Verdict:** Production-ready, well-maintained, industry standard.

---

### 2. simple-mermaid (Alternative)

| Metric | Value |
|--------|-------|
| GitHub Stars | 22 |
| Downloads/month | ~202,000 |
| Dependents | 445 crates (15 direct) |
| Latest Version | 0.2.0 (Dec 2024) |
| License | MIT |
| Dependencies | Zero |

**What it does:** Declarative macro for including Mermaid diagrams in rustdoc from external files.

**Key Differentiators from aquamarine:**
- Zero dependencies (faster compile times)
- Designed for external `.mmd` files as primary workflow
- No limitations on multiple external diagrams per doc block
- Simpler implementation (declarative vs procedural macro)

**When to choose over aquamarine:**
- You prefer keeping diagrams in external files
- You want minimal dependencies
- Compile time is a concern

**Verdict:** Solid alternative, especially for external-file workflows.

---

### 3. mdbook-mermaid (For mdBook only)

| Metric | Value |
|--------|-------|
| GitHub Stars | 426 |
| Downloads/month | ~11,400 |
| Latest Version | 0.17.0 (Nov 2025) |
| License | MPL-2.0 |

**What it does:** mdBook preprocessor that renders Mermaid code blocks as diagrams.

**Use case:** Only for mdBook documentation projects, not for rustdoc or general-purpose diagram generation.

**Verdict:** Best choice if using mdBook; not applicable otherwise.

---

### 4. mermaid-rs (Low maturity)

| Metric | Value |
|--------|-------|
| GitHub Stars | 6 |
| Downloads/month | Low (ranked #931) |
| Latest Version | 0.1.1 (Oct 2024) |
| License | MIT |

**What it does:** Rust bindings that render Mermaid to SVG via embedded Chromium.

**Concerns:**
- Requires Chromium runtime (2.5MB download, heavy dependency)
- Only 78 lines of Rust code
- Very low adoption
- Last commit Oct 2024

**Verdict:** Not recommended. Heavy dependency for minimal functionality.

---

### 5. rust_mermaid (Experimental)

| Metric | Value |
|--------|-------|
| GitHub Stars | 5 |
| Latest Version | 0.1.1 |

**What it does:** Generate Mermaid diagrams from Rust and save as images.

**Verdict:** Too immature for production use.

---

## Excalidraw Crates - Detailed Analysis

### 1. excalidraw-dsl (Most Promising - Not Yet Published)

| Metric | Value |
|--------|-------|
| GitHub Stars | 16 |
| crates.io | NOT PUBLISHED |
| Latest Commits | Jul 2025 (active ML features) |
| License | MIT |

**What it does:** A full DSL for generating Excalidraw diagrams from text.

**Key Features:**
- Text-based diagram syntax
- Multiple layout algorithms (Dagre, Force, ELK)
- Component types and theming
- Containers and groups
- Live preview web server
- CLI tool (`edsl`)

**DSL Example:**
```
start "Hello"
world "World"
start -> world
```

**Current Status:**
- Actively developed (commits through Jul 2025)
- Adding ML-based layout features
- NOT yet on crates.io - must install from source

**Verdict:** Most feature-rich option, but requires source installation. Watch for crates.io publication.

---

### 2. excalidocker-rs (Domain-Specific)

| Metric | Value |
|--------|-------|
| GitHub Stars | 129 |
| Docker Pulls | Available on Docker Hub |
| Latest Version | 0.1.8 (Jul 2023) |
| License | MIT |

**What it does:** Converts docker-compose.yaml files into Excalidraw diagrams.

**Key Features:**
- Works with local and remote docker-compose files (via GitHub URLs)
- Customizable layouts (vertical, horizontal, stepped)
- Configurable colors, fonts, styles
- Available via brew, Docker, and binary releases

**Limitations:**
- Only works with docker-compose files
- Not a general-purpose diagram generator
- Last release Jul 2023 (potentially stale)

**Verdict:** Production-ready for its specific use case. Not general-purpose.

---

### 3. Other Excalidraw Projects (Not Recommended)

| Project | Stars | Status |
|---------|-------|--------|
| excalidraw-client | 7 | Desktop wrapper, not generator |
| excalidraw-wasm | 7 | Excalidraw clone in Rust, not generator |
| excalidraw-rs | 2 | Abandoned |

---

## Recommendations

### For Mermaid Diagrams

**Primary Choice: `aquamarine`**
```toml
[dependencies]
aquamarine = "0.6"
```

Use aquamarine if you:
- Want rustdoc integration
- Need proven, production-ready solution
- Want community support

**Alternative: `simple-mermaid`**
```toml
[dependencies]
simple-mermaid = "0.2"
```

Use simple-mermaid if you:
- Keep diagrams in external files
- Want zero dependencies
- Care about compile times

### For Excalidraw Diagrams

**No clear winner currently.**

| Use Case | Recommendation |
|----------|----------------|
| Docker-compose visualization | excalidocker-rs |
| General-purpose DSL | excalidraw-dsl (from source) |
| Programmatic generation | Build your own using Excalidraw's JSON format |

**If you need general Excalidraw generation today:**
1. Clone tyrchen/excalidraw-dsl and use from source
2. OR generate Excalidraw JSON directly (it's well-documented format)
3. OR use excalidocker-rs code as a reference implementation

---

## Links

### Mermaid
- [aquamarine](https://github.com/mersinvald/aquamarine) | [crates.io](https://crates.io/crates/aquamarine) | [docs.rs](https://docs.rs/aquamarine)
- [simple-mermaid](https://github.com/glueball/simple-mermaid) | [crates.io](https://crates.io/crates/simple-mermaid)
- [mdbook-mermaid](https://github.com/badboy/mdbook-mermaid) | [crates.io](https://crates.io/crates/mdbook-mermaid)

### Excalidraw
- [excalidraw-dsl](https://github.com/tyrchen/excalidraw-dsl) (not on crates.io)
- [excalidocker-rs](https://github.com/etolbakov/excalidocker-rs) | [Docker Hub](https://hub.docker.com/r/etolbakov/excalidocker)
