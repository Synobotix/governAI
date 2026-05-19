import re


def extract_sections(md: str):
    """
    Extract structured sections from persona/overlay markdown.
    """

    sections = {}

    current = None
    buffer = []

    for line in md.splitlines():
        match = re.match(r"^##\s+(.*)", line)

        if match:
            if current:
                sections[current] = "\n".join(buffer).strip()
                buffer = []

            current = match.group(1).strip().lower()
            continue

        if current:
            buffer.append(line)

    if current:
        sections[current] = "\n".join(buffer).strip()

    return sections


def extract_rules(md: str):
    sections = extract_sections(md)
    return sections.get("rules", "")


def extract_constraints(md: str):
    sections = extract_sections(md)
    return sections.get("constraints", "")


def extract_output_behavior(md: str):
    sections = extract_sections(md)
    return sections.get("output behavior", "")