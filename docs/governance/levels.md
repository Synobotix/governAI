# Change Levels

This document defines the default rigor level for repository work.

Its purpose is to ensure that:

- low-risk local changes do not pay structural-process cost
- bounded feature work gets the right amount of validation
- structural and sensitive changes are escalated before implementation
- `triage`, `planner`, and `preflight` use the same language

If uncertain between two levels, choose the higher level.

---

## L1 - Local low-risk change

### Typical examples

- doc-only change
- test-only change
- typo / wording / message fix
- highly localized bug fix
- internal non-structural code edit in one bounded area
- narrow implementation cleanup with no behavior or contract impact

### Required flow

```text
triage -> planner -> preflight -> coder -> review
```

### Optional downstream gates

- `qa` if behavior changed
- `doc` if user-facing or operator-facing documentation changed
- `release` only if the repository requires release tracking even for low-risk changes

### Constraints

All of the following should remain true:

- no architecture trigger
- no security trigger
- no public contract change
- no invariant surface touched
- no migration required
- no forbidden area touched
- no undefined blast radius
- no more than 3 files unless explicitly justified by planner

### Typical shape

L1 should stay:

- local
- reviewable
- easy to revert
- free of structural implications

If the change stops being clearly local, it is no longer L1.

---

## L2 - Standard bounded feature/change

### Typical examples

- normal feature inside existing module boundaries
- bug fix touching several files
- approved local refactor
- behavior change within existing contracts
- additive capability with bounded blast radius
- implementation extension that does not alter invariants or contract compatibility

### Required flow

```text
triage -> planner -> preflight -> coder -> qa -> review -> doc (if needed)
```

### Constraints

The following must hold:

- blast radius is bounded and understood
- no invariant change
- no schema/public contract break
- no migration required unless escalated to L3
- no unresolved trust-boundary ambiguity
- no structural redesign hidden inside "normal feature work"

### Typical shape

L2 is the default level for:

- real feature work
- real bug fixing
- bounded internal improvements

It may span multiple files and real behavior, but it still stays inside known system boundaries.

If the change starts to affect contracts, boundaries, schema, runtime semantics, or security-sensitive surfaces, it is no longer L2.

---

## L3 - Structural or sensitive change

### Typical examples

- module or package boundary change
- config contract change
- dependency introduction or meaningful dependency upgrade
- schema evolution
- file format change
- pipeline semantics change
- runtime orchestration change
- public API / CLI contract change
- migration-required change
- rollback-sensitive change
- security-sensitive feature
- trust boundary change
- blast radius unclear or cross-system

### Required flow

```text
governance if invariant/contract surface touched
-> triage
-> planner
-> architect or architect-security
-> adr
-> preflight
-> coder
-> doc
-> security (if needed)
-> qa
-> review
-> release
```

### Constraints

The following are mandatory when applicable:

- ADR required for invariant, structural, or contract-affecting decisions
- migration plan required when compatibility or persisted/public surfaces change
- rollback plan required when reversal is non-trivial or risk is elevated
- all required gates must be explicitly satisfied before preflight may PASS
- no implementation may start while boundary, contract, or trust-surface ambiguity remains unresolved

### Typical shape

L3 is used when the cost of misclassification is high.

This includes changes where:

- the system shape may change
- external or public expectations may change
- trust or security assumptions may change
- the repo needs durable decision records
- downstream consumers may be affected

If the request feels "too important to guess," it is L3.

---

## Escalation Rules

Escalate from L1 or L2 to L3 immediately if any of the following becomes true:

- a public contract is affected
- a schema, config, file format, or pipeline semantic changes
- a migration or rollback concern appears
- a forbidden area must be touched
- a trust boundary or security surface becomes relevant
- the blast radius becomes unclear
- planner can no longer keep the change bounded safely

When this happens:

- stop execution
- return to planner
- update `.agents/STATE.<slug>.md`
- trigger the required gates before coding continues

---

## Selection Rule

Use the lowest level that is still honest.

Do not classify low just to reduce process cost.

A wrong low classification is more expensive than a correct escalation.

