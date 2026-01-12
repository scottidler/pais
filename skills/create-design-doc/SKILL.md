---
name: create-design-doc
description: Create high-quality design documents using Jeffrey Emanuel's Rule of Five methodology. USE WHEN the user wants to create a design doc, technical specification, RFC, or architecture document for a feature or system.
---

# Create Design Document

Create comprehensive, high-quality design documents by applying **Jeffrey Emanuel's Rule of Five** — the principle that AI agents produce dramatically better output when forced to review their own work 4-5 times until convergence.

> **Reference:** See `~/.config/pais/research/tech/rule-of-five/2026-01-10.md` for the full research on this methodology.

## When to Use This Skill

- Creating a design document for a new feature
- Writing a technical specification or RFC
- Documenting architecture decisions
- Planning a significant refactor or system change
- Any document that requires high quality and careful thought

## The Rule of Five Methodology

### Core Principle

**"When in doubt, have the agent review its own work 5 times."**

The output converges after 4-5 iterations. Only at that point can you begin to trust the output.

### Review Pass Structure

Each review pass focuses on different aspects, mixing "in-the-small" (details) with "in-the-large" (architecture):

| Pass | Focus Area | Questions to Ask |
|------|------------|------------------|
| 1 | **Completeness** | Are all sections filled? Missing requirements? Gaps in the design? |
| 2 | **Correctness** | Are there logical errors? Wrong assumptions? Technical inaccuracies? |
| 3 | **Edge Cases** | What could go wrong? Error handling? Failure modes? Security issues? |
| 4 | **Architecture** | Does this fit the larger system? Scalability? Dependencies? Trade-offs? |
| 5 | **Clarity** | Is it understandable? Could someone implement from this? Ambiguous sections? |

### Guidelines by Task Size

| Task Size | Recommended Passes |
|-----------|-------------------|
| Small features | 2-3 passes |
| Medium features | 3-4 passes |
| Large/complex features | 4-5 passes |
| Critical systems | 5 passes (full) |

## Design Document Process

### Phase 1: Information Gathering

Before writing, gather context:

1. **Understand the problem**
   - What problem are we solving?
   - Who are the users/stakeholders?
   - What are the constraints?

2. **Explore the codebase**
   - What existing code is relevant?
   - What patterns does the codebase use?
   - What are the integration points?

3. **Research if needed**
   - Are there industry-standard approaches?
   - What have others done?
   - Are there relevant libraries or tools?

### Phase 2: Initial Draft

Create the first draft using the template below.

### Phase 3: Iterative Review (Rule of Five)

For each review pass:

1. **Announce the review focus** (e.g., "Review Pass 2: Checking for correctness...")
2. **Systematically examine** each section through that lens
3. **Make improvements** inline
4. **Document changes made** at the end of the pass
5. **Assess convergence** — if no significant changes in 2 consecutive passes, document is ready

### Phase 4: Final Output

Present the converged design document with a summary of the review process.

## Design Document Template

```markdown
# Design Document: [Feature Name]

**Author:** [Name]
**Date:** [YYYY-MM-DD]
**Status:** Draft | In Review | Approved
**Review Passes:** [X/5]

## Summary

[2-3 sentence overview of what this design accomplishes]

## Problem Statement

### Background
[Context and history leading to this design]

### Problem
[Clear statement of the problem being solved]

### Goals
- [Goal 1]
- [Goal 2]

### Non-Goals
- [Explicitly out of scope item 1]
- [Explicitly out of scope item 2]

## Proposed Solution

### Overview
[High-level description of the solution]

### Architecture
[System architecture, components, and their interactions]

### Data Model
[Data structures, schemas, or models involved]

### API Design
[Interfaces, endpoints, or function signatures]

### Implementation Plan
[Phased approach or steps to implement]

## Alternatives Considered

### Alternative 1: [Name]
- **Description:** [What this approach would look like]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Why not chosen:** [Reasoning]

### Alternative 2: [Name]
[Same structure]

## Technical Considerations

### Dependencies
[What this depends on, internal and external]

### Performance
[Expected performance characteristics, benchmarks if relevant]

### Security
[Security implications and mitigations]

### Testing Strategy
[How this will be tested]

### Rollout Plan
[How this will be deployed/released]

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [How to address] |

## Open Questions

- [ ] [Question 1 that needs resolution]
- [ ] [Question 2]

## References

- [Link to relevant docs, PRs, or resources]
```

## Example Review Process

```
=== REVIEW PASS 1: COMPLETENESS ===
Checking all sections are filled...
- Summary: OK
- Problem Statement: Missing non-goals section
- Proposed Solution: API Design section is empty
- Alternatives: Only one alternative listed, should have 2+
- Risks: Table is incomplete

Changes made:
- Added non-goals section with 3 items
- Drafted initial API design
- Added second alternative approach
- Completed risk table with 4 entries

=== REVIEW PASS 2: CORRECTNESS ===
Checking for logical errors and technical accuracy...
- Found incorrect assumption about database constraint
- API endpoint naming doesn't follow existing conventions
- Implementation plan has dependency ordering issue

Changes made:
- Corrected database constraint description
- Renamed endpoints to match /api/v2/* pattern
- Reordered implementation steps

=== REVIEW PASS 3: EDGE CASES ===
[...continues...]

=== REVIEW PASS 4: ARCHITECTURE ===
[...continues...]

=== REVIEW PASS 5: CLARITY ===
Checking readability and implementability...
- No significant changes needed
- Document has converged

FINAL STATUS: Document complete after 5 passes
```

## Output Storage

Save design documents to the project's `docs/` directory or a dedicated location:

```
docs/design/
├── YYYY-MM-DD-feature-name.md
└── ...
```

Or for user-specified locations.

## Tips for Better Design Docs

1. **Start with the problem, not the solution** — ensure the problem is well-understood before proposing fixes
2. **Be explicit about non-goals** — prevents scope creep and misunderstanding
3. **Always include alternatives** — shows you've considered options
4. **Make it implementable** — someone should be able to code from this
5. **Keep it updated** — design docs are living documents
6. **Trust the process** — the Rule of Five works; don't skip reviews
7. **NEVER include time/effort estimates** — no "1-2 days", "2 weeks", etc. Focus on WHAT needs to be done, not guessing HOW LONG. Time estimates are unreliable and misleading.

## Related Skills

- `/rust-cli-coder` — for implementing Rust CLIs from designs
- `/python-coder` — for implementing Python code from designs
- `/tech-researcher` — for researching approaches before designing
