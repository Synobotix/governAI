#!/usr/bin/env python3
"""
Sync overlays from sources/overlays/ → .opencode/skills/overlays/<name>/SKILL.md.

Reads each overlay markdown file, wraps it in a skill structure
(frontmatter + Role + Instructions + Triggers), and writes it
as a valid SKILL.md in the skills directory.

Usage:
    python3 scripts/sync_overlays_to_skills.py
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OVERLAYS_SRC = ROOT / "sources" / "overlays"
SKILLS_DST = ROOT / ".opencode" / "skills" / "overlays"

BRIEF_DESCRIPTIONS = {
    "diagnostics": "Apply diagnostic reasoning — start from facts, generate multiple hypotheses, distinguish symptoms from causes, propose validation steps before conclusions. Use when the user asks for troubleshooting, root cause analysis, debugging, or investigating failures.",
    "hypothesis-driven": "Apply hypothesis-driven reasoning — generate multiple explanations, rank by plausibility, avoid premature convergence, and update hypotheses as new evidence arrives. Use when the user needs structured exploration of competing explanations.",
    "strict-mode": "Apply strict reasoning — explicitly separate facts from assumptions, state uncertainty, mark inferences as hypotheses, refuse unsupported certainty. Use when precision, rigor, and explicit evidence boundaries are required.",
    "structured-analysis": "Apply structured analysis — decompose problems into explicit stages, maintain consistent reasoning structure, separate problem understanding from solution generation. Use when the user needs methodical, stage-by-stage problem solving.",
}

TRIGGERS_BY_SECTION = {
    "diagnostics": [
        "Investigating a bug, crash, or failure",
        "Performing root cause analysis",
        "Debugging a complex system",
        "Asking for diagnostic steps",
        "Troubleshooting an unknown issue",
    ],
    "hypothesis-driven": [
        "Exploring multiple possible explanations",
        "Investigating an ambiguous problem",
        "Evaluating competing theories or interpretations",
        "Asking for probabilistic or weighted reasoning",
        "Dealing with incomplete or noisy information",
    ],
    "strict-mode": [
        "Asking for rigorous analysis",
        "Requiring high precision and evidence-based answers",
        "Evaluating risks or critical decisions",
        "Working in safety-critical or high-stakes domains",
        "Requesting analysis of incomplete or uncertain data",
    ],
    "structured-analysis": [
        "Solving a complex or multi-faceted problem",
        "Asking for a methodical, step-by-step approach",
        "Requiring clear separation of analysis phases",
        "Working on architecture, design, or planning tasks",
        "Needing traceable reasoning from problem to solution",
    ],
}


def extract_sections(text: str) -> dict:
    sections = {}
    current = None
    buffer = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+)", line)
        if m:
            if current:
                sections[current] = "\n".join(buffer).strip()
            current = m.group(1).strip()
            buffer = []
        else:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer).strip()
    return sections


def build_description(name: str) -> str:
    return BRIEF_DESCRIPTIONS.get(
        name,
        f"Apply {name.replace('-', ' ')} behavior to the current task."
    )


def build_triggers(name: str) -> list:
    return TRIGGERS_BY_SECTION.get(name, [
        f"The task involves {name.replace('-', ' ')}"
    ])


def build_skill(name: str, body: str) -> str:
    description = build_description(name)
    triggers = build_triggers(name)

    sections = extract_sections(body)
    has_rules = "Rules" in sections
    has_constraints = "Constraints" in sections
    has_output = "Output Behavior" in sections
    has_identity = "Identity" in sections
    has_intent = "Intent" in sections

    lines = ["---",
             f"name: {name}",
             f"description: {description}",
             "---",
             "",
             "# Role",
             "",
             f"You are the **{name}** overlay.",
             "",
             "---",
             "",
             "## Instructions",
             ""]

    if has_identity:
        lines.append("### Identity")
        lines.append("")
        lines.append(sections["Identity"].strip())
        lines.append("")

    if has_intent:
        lines.append("### Intent")
        lines.append("")
        lines.append(sections["Intent"].strip())
        lines.append("")

    if has_rules:
        lines.append("### Rules")
        lines.append("")
        for rline in sections["Rules"].splitlines():
            lines.append(rline)
        lines.append("")

    if has_constraints:
        lines.append("### Constraints")
        lines.append("")
        for cline in sections["Constraints"].splitlines():
            lines.append(cline)
        lines.append("")

    if has_output:
        lines.append("### Output Behavior")
        lines.append("")
        for oline in sections["Output Behavior"].splitlines():
            if oline.strip() == "---":
                continue
            lines.append(oline)
        lines.append("")

    lines.append("---")
    lines.append("## Triggers")
    lines.append("")
    lines.append("This skill is relevant when the user is:")
    for t in triggers:
        lines.append(f"- {t}")

    return "\n".join(lines)


def sync():
    if not OVERLAYS_SRC.exists():
        print(f"✖ Overlays source not found: {OVERLAYS_SRC}")
        return 1

    SKILLS_DST.mkdir(parents=True, exist_ok=True)

    for overlay_file in sorted(OVERLAYS_SRC.glob("*.md")):
        name = overlay_file.stem
        body = overlay_file.read_text(encoding="utf-8")

        skill_dir = SKILLS_DST / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_path = skill_dir / "SKILL.md"

        skill_content = build_skill(name, body)
        skill_path.write_text(skill_content, encoding="utf-8")
        print(f"✔ {name} → {skill_path}")

    print(f"\n✔ Synced {len(list(OVERLAYS_SRC.glob('*.md')))} overlays to skills")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(sync())
