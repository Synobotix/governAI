from typing import List, Dict, Any


# =========================================================
# 1. IR BUILDER
# =========================================================

def build_ir(persona: str, overlays: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build intermediate representation (IR) from persona + overlays.
    """

    rules = []
    constraints = []
    output_format = []

    for overlay in overlays:
        if not isinstance(overlay, dict):
            continue

        rules.extend(overlay.get("rules", []))
        constraints.extend(overlay.get("constraints", []))
        output_format.extend(overlay.get("output", []))

    return {
        "persona": persona,
        "rules": rules,
        "constraints": constraints,
        "output_format": output_format,
    }


# =========================================================
# 2. IR NORMALIZATION
# =========================================================

def normalize_ir(ir: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean IR: remove duplicates, normalize empty fields.
    """

    def dedupe(lst):
        seen = set()
        out = []
        for x in lst:
            if x and x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return {
        "persona": ir.get("persona", ""),
        "rules": dedupe(ir.get("rules", [])),
        "constraints": dedupe(ir.get("constraints", [])),
        "output_format": dedupe(ir.get("output_format", [])),
    }


# =========================================================
# 3. FLATTEN TO OPENCODE PROMPT
# =========================================================

SKILL_DESCRIPTIONS = {
    "diagnostics": "Structured diagnostic method: facts → hypotheses → validation → root cause.",
    "hypothesis-driven": "Multi-hypothesis reasoning: generate, rank, evaluate, and update competing explanations.",
    "strict-mode": "Epistemic rigor: separate facts from assumptions, state uncertainty, refuse overconfidence.",
    "structured-analysis": "Stage-based analysis: frame → decompose → analyze → synthesize → conclude.",
}


def flatten_to_opencode_prompt(
    ir: Dict[str, Any],
    task_rules: List[str] | None = None,
    overlay_names: List[str] | None = None,
) -> str:
    """
    Convert IR → OpenCode system prompt string.
    """

    sections = []

    # Persona
    sections.append("SYSTEM PERSONA:")
    sections.append(ir["persona"].strip())

    # Rules
    if ir["rules"]:
        sections.append("=== RULES ===")
        sections.append("\n".join(ir["rules"]))

    # Constraints
    if ir["constraints"]:
        sections.append("=== CONSTRAINTS ===")
        sections.append("\n".join(ir["constraints"]))

    # Task behavior
    if task_rules:
        sections.append("=== TASK BEHAVIOR ===")
        sections.append("\n".join(task_rules))

    # Output format
    if ir["output_format"]:
        sections.append("=== OUTPUT FORMAT ===")
        sections.append("\n\n---\n\n".join(ir["output_format"]))

    # Available skills (overlays as skills)
    if overlay_names:
        skill_lines = []
        for name in overlay_names:
            desc = SKILL_DESCRIPTIONS.get(name, name.replace("-", " ").title())
            skill_lines.append(f"- {name}: {desc}")
        sections.append("=== AVAILABLE SKILLS ===")
        sections.append("You have access to the following overlay skills. "
                        "Use them by loading the corresponding skill file "
                        "from `.opencode/skills/overlays/<name>/SKILL.md`:")
        sections.append("\n".join(skill_lines))

    return "\n\n".join(sections).strip()

# =========================================================
# 4. OVERLAY COMPILER
# =========================================================

def compile_overlay(raw_text: str) -> Dict[str, Any]:
    """
    Parse overlay markdown → structured dict.

    Rules and Constraints are returned as lists of bullet items.
    Output Behavior is returned as a list containing one string
    (the full section body including headings and prose).
    """

    def extract_items(section: str) -> List[str]:
        marker = f"## {section}"
        if marker not in raw_text:
            return []

        block = raw_text.split(marker)[1]
        block = block.split("\n##")[0]

        lines = []
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("- "):
                lines.append(line[2:].strip())

        return lines

    def extract_body(section: str) -> str:
        marker = f"## {section}"
        if marker not in raw_text:
            return ""

        import re

        block = raw_text.split(marker, 1)[1]
        # split only on L2 headings (## ), not L3/L4 (### / ####)
        parts = re.split(r"\n## (?![#])", block, maxsplit=1)
        block = parts[0]

        lines = []
        for line in block.splitlines():
            stripped = line.strip()
            if stripped == "---":
                continue
            lines.append(line)

        return "\n".join(lines).strip()

    body = extract_body("Output Behavior")
    return {
        "rules": extract_items("Rules"),
        "constraints": extract_items("Constraints"),
        "output": [body] if body else [],
    }