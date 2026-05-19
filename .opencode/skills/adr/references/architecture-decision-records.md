# Architecture Decision Records (ADR) Reference

## Definitions

| Term | Definition |
|------|-----------|
| **ADR** (Architecture Decision Record) | A document that captures an important architectural decision, its context, and its consequences |
| **AD** (Architecture Decision) | A software design choice that addresses a significant requirement |
| **ADL** (Architecture Decision Log) | The collection of all ADRs created and maintained for a project |
| **ASR** (Architecturally-Significant Requirement) | A requirement that has a measurable effect on a software system's architecture |
| **AKM** (Architecture Knowledge Management) | The discipline of capturing, sharing, and using architectural knowledge |

## File Name Conventions

ADR files should follow these conventions:

- Numeric ID prefix for unambiguous referencing: `NNNN-` (e.g. `0001-choose-database.md`)
- Present tense imperative verb phrase
- Lowercase with dashes
- Markdown extension (`.md`)

Examples:

```
0001-choose-database.md
0002-format-timestamps.md
0003-manage-passwords.md
```

## ADR File Structure

### YAML Front Matter

Each ADR should start with a YAML front matter block recording metadata:

```yaml
---
title: Choose Database Technology
date: 2026-05-12
status: Proposed
authors: [Jane Doe, John Smith]
supersedes: null
superseded-by: null
---
```

### Status Values

The `status` field follows the lifecycle:

- `Proposed` — drafted, under review
- `Accepted` — approved and actionable
- `Deprecated` — no longer recommended
- `Superseded` — replaced by another ADR (recorded in `superseded-by`)

## Writing Good ADRs

### Context Section

- Explain your organization's situation and business priorities
- Include rationale based on team skills, composition, constraints
- Include pros and cons in terms that align with actual needs and goals

### Consequences Section

- Explain what follows from the decision (effects, outcomes, follow-ups)
- Note any subsequent ADRs triggered by this decision
- Include after-action review processes (e.g. review the ADR one month later)

### Good ADR Characteristics

- **Rationale** — Explain the reasons for the decision, not just the decision itself
- **Specific** — One ADR per decision, not multiple decisions bundled
- **Timestamped** — Identify when each item was written (costs, schedules, scaling may change)
- **Immutable** — Do not alter existing information; amend with new info or supersede with a new ADR

### Superseding

When a decision replaces or invalidates a previous ADR, create a new ADR that explicitly references the superseded one via the `supersedes` field.

## When to Create an ADR

See the ADR skill definition (`.opencode/skills/adr/SKILL.md`) for the full list of conditions. In short: an ADR is warranted for durable decisions affecting invariants, boundaries, contracts, schemas, trust, migration, or architecture policy.

## Project Conventions

ADRs for this project live in `docs/governance/adr/`. The template is at `docs/governance/adr/_template.md`. The index is at `docs/governance/adr/index.md`.

## Available Templates

| Template | Style | Best For |
|----------|-------|----------|
| Michael Nygard | Simple, popular | Most teams starting out |
| Jeff Tyree & Art Akerman | More sophisticated | Enterprise with formal processes |
| Alexandrian Pattern | Context-focused | Complex decisions needing rich context |
| Business Case | MBA-oriented (costs, SWOT) | Decisions requiring business justification |
| MADR (Markdown ADR) | Simple + elaborate versions | Teams wanting options and pros/cons |
| Planguage | QA-oriented | Quality-critical decisions |

## Teamwork

### Advice

- Use the name **"decisions"** over "ADRs" — teams contribute more when the term is accessible
- Prefer **mutability with timestamps** over strict immutability in practice
- Focus on the **"why"** — decision records are for thinking smarter, not forced paperwork

### Key Questions

| Question | Purpose |
|----------|---------|
| Who can create an ADR? | Defines authorship scope |
| What justifies raising an ADR? | Sets the bar for when to document |
| What justifies skipping an ADR? | Identifies when a decision is too small/risky/temporary |
| What is the ADR lifecycle? | Defines states: Proposed → Accepted → Deprecated → Superseded |
| Who approves/reviews? | Identifies roles: author, reviewer, approver, maintainer |
| How does governance interact? | Consensus, conflict resolution, escalation paths |

## ADR Lifecycle

```
Proposed → Accepted → Deprecated → Superseded
```

Each state transition should be recorded with a timestamp in the ADR file. The `status` field in the YAML front matter reflects the current state.

## Fitness Functions

Fitness functions are automated checks that verify decisions are maintained over time.

- A decision record **documents** the decision; a fitness function **assures** it
- Fitness functions run on every commit/build via CI

### Examples

**ArchUnit (Java)** — check architecture rules using plain JUnit:

```java
@Test
public void services_should_only_be_accessed_by_controllers() {
    JavaClasses classes = new ClassFileImporter().importPackages("com.myapp");
    ArchRule rule = classes().that().areAnnotatedWith(Service.class)
        .should().onlyBeAccessed()
        .byClassesThat().areAnnotatedWith(Controller.class);
    rule.check(classes);
}
```

**ArchUnitTS (TypeScript)** — check architecture rules in Jest/Vitest:

```typescript
test('domain layer should not depend on infrastructure', () => {
    const rule = new ArchRule()
        .layer('domain').shouldNotDependOn('infrastructure');
    rule.check(imports);
});
```

**AI-augmented fitness function** — use an LLM to verify decision alignment:

```
This is a fitness function to evaluate if our work uses all our decisions.
Our decisions are here: {url}
Our work to evaluate is here: {url}
Explain any errors, problems, gaps, weaknesses. Be direct. Be decisive.
```

### Decision Guardrails

Tools like [Decision Guardian](https://github.com/DecispherHQ/decision-guardian) surface relevant ADRs on pull requests when a developer modifies code that a decision covers. Works with any CI system and as a pre-commit hook.

## Related Concepts

- **[arc42](https://arc42.org/)** — A template for documenting software architectures, including ADRs plus guidance on goals, constraints, contexts, quality, and risks
- **[C4 Model](https://c4model.com/)** — A hierarchical approach to software architecture diagramming (context, container, component, code)

## Resources

- [Documenting architecture decisions — Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)
- [Markdown Architectural Decision Records (MADR)](https://adr.github.io/madr/)
- [ADR GitHub organization](https://adr.github.io/)
- [ThoughtWorks Technology Radar: Lightweight ADRs](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- [AWS Prescriptive Guidance: ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [Red Hat: Why you should use ADRs](https://www.redhat.com/architect/architecture-decision-records)
- [Fundamentals of Software Architecture — Mark Richards & Neal Ford](https://www.amazon.com/Fundamentals-Software-Architecture-Engineering-Approach-ebook/dp/B0849MPK73)
- [Building Evolutionary Architectures — Neal Ford et al.](https://www.amazon.com/Building-Evolutionary-Architectures-Neal-Ford-ebook/dp/B0BN4T1P27)
