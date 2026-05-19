# C4 Diagram Review Checklist

Adapted from the [C4 model review checklist](https://c4model.com/diagrams/checklist).

## Notation

Sévérité :
- **[REQUIRED]** = doit être satisfait pour valider le diagramme
- **[RECOMMENDED]** = fortement conseillé, sauf justification
- **[OPTIONAL]** = bonne pratique, peut être ignoré

Types de diagramme :
- ALL = tous les types
- CTX = system context
- CONT = container
- COMP = component
- CODE = code
- LAND = system landscape
- DYN = dynamic
- DEPL = deployment

## General

- [REQUIRED] [ALL] **Title** — Does the diagram have a clear title?
- [REQUIRED] [ALL] **Diagram type** — Is the diagram type obvious from the title or notation?
- [REQUIRED] [ALL] **Scope** — Is the scope of the diagram clearly understood?
- [REQUIRED] [ALL] **Legend** — Does the diagram have a key or legend explaining notation?
- [REQUIRED] [ALL] **Correct level** — Does the diagram stay at a single C4 level without mixing levels?
- [RECOMMENDED] [ALL] **Version** — Does the diagram include a version, date, or last-updated timestamp?

## Elements

- [REQUIRED] [ALL] **Names** — Does every element have a meaningful name?
- [REQUIRED] [ALL] **Abstraction** — Is every element's type clear and appropriate for its role (e.g. no databases as Person, no components as Container)?
- [REQUIRED] [ALL] **Description** — Is it clear what each element does?
- [RECOMMENDED] [CONT, COMP, DEPL] **Technology** — Are technology choices shown for each element?
- [RECOMMENDED] [ALL] **Acronyms** — Are all acronyms and abbreviations explained?
- [OPTIONAL] [ALL] **Colors** — Is every color meaningful and explained?
- [OPTIONAL] [ALL] **Shapes** — Is every shape meaningful and explained?
- [OPTIONAL] [ALL] **Icons** — Is every icon meaningful and explained?
- [OPTIONAL] [ALL] **Border styles** — Are border styles (solid, dashed) meaningful and explained?
- [OPTIONAL] [ALL] **Element sizes** — Are element sizes meaningful (small vs large boxes)?

## Boundaries

- [REQUIRED] [CTX, CONT, LAND] **Ownership** — Are internal elements clearly separated from external ones (System vs System_Ext)?
- [REQUIRED] [CTX, CONT, LAND] **Boundary labels** — Does every boundary have a descriptive label?
- [RECOMMENDED] [CONT, COMP] **Nested boundaries** — Are nested boundaries logically structured and non-overlapping?
- [REQUIRED] [CTX, CONT, LAND] **External people** — Are external people clearly marked (Person_Ext when outside the enterprise)?

## Relationships

- [REQUIRED] [ALL] **Labels** — Does every line have a label describing the intent of the relationship?
- [REQUIRED] [ALL] **Direction** — Does the description match the relationship direction?
- [RECOMMENDED] [CONT, COMP, DYN] **Protocol** — Where applicable, is the communication protocol shown?
- [RECOMMENDED] [ALL] **Acronyms** — Are all acronyms and abbreviations on relationships explained?
- [OPTIONAL] [ALL] **Colors** — Are relationship colors meaningful and explained?
- [OPTIONAL] [ALL] **Arrow heads** — Is every arrow head meaningful and explained?
- [OPTIONAL] [ALL] **Line styles** — Are line styles (solid, dashed) meaningful and explained?
- [OPTIONAL] [DYN] **Sequence** — Are relationship numbers present and sequential?

## Code-Specific

- [REQUIRED] [CODE] **Single component scope** — Does the diagram cover exactly one component?
- [REQUIRED] [CODE] **Element selection** — Are only the elements needed to tell the story shown (not every getter/setter)?
- [REQUIRED] [CODE] **All references defined** — Is every type referenced in a relationship defined in the diagram (no dangling references)?
- [RECOMMENDED] [CODE] **Stereotypes** — Are UML stereotypes used to clarify element roles (e.g. `<<Service>>`, `<<Entity>>`, `<<Repository>>`)?
- [RECOMMENDED] [CODE] **Design patterns** — Are key design patterns annotated where applicable?
- [RECOMMENDED] [CODE] **Legend relevance** — Is the legend (if any) appropriate for class-level notation, not carrying C4-level stereotypes?
- [OPTIONAL] [CODE] **Generation preference** — Is the diagram generated from code rather than hand-maintained?

## Usage

Add this checklist to architecture reviews, PR review checklists, or documentation validation gates.

Cross-reference from reference files when validating a specific diagram type:
- [system-context.md](./references/system-context.md)
- [container.md](./references/container.md)
- [component.md](./references/component.md)
- [code.md](./references/code.md)
