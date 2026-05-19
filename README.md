<a id="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Synobotix/governAI">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">GovernAI</h3>

  <p align="center">
    Central governance system for AI configurations, defining structured standards for agent behavior, personas, and operational overlays. It enables controlled composition, versioning, and validation of AI contexts across projects. Designed to enforce consistency, traceability, and reproducibility of AI-driven systems while supporting scalable experimentation and reliable deployment workflows.
    <br />
    <a href="https://github.com/Synobotix/governAI"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Synobotix/governAI">View Demo</a>
    &middot;
    <a href="https://github.com/Synobotix/governAI/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Synobotix/governAI/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#how-it-works">How It Works</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#quick-start">Quick Start</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#docs">Docs</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

Central repository for governing and structuring AI agent configurations across multiple domains. It defines a composable system of personas, behavioral overlays, project contexts, and runtime profiles to ensure consistent, traceable, and reproducible AI behavior. The goal is to move from ad-hoc prompt engineering to a formalized governance layer for AI systems, where every configuration is versioned, auditable, and testable.

The repository acts as a single source of truth for AI behavior design, enabling modular assembly of agent capabilities depending on task requirements. It supports separation of concerns between role definition (persona), domain constraints (project context), and behavioral modifiers (overlays), allowing fine-grained control over agent output characteristics. It is designed for scalability and experimentation: configurations can be composed, compared, evaluated, and iterated with full reproducibility. This enables structured benchmarking of AI behaviors and systematic improvement over time.

Ultimately, this system aims to provide an infrastructure-level approach to AI governance, ensuring reliability, consistency, and clarity in complex AI-driven workflows.

The compilation pipeline:

```
                    ┌─ scripts/validate_catalog.py (schema + source check)
                    │
sources/personas/  ─┤
                    ├─ catalog/index.yaml ── scripts/compile.py ── dist/opencode.json
sources/overlays/  ─┤
                    │
                    └─ scripts/sync_overlays_to_skills.py → .opencode/skills/overlays/
```

**Key principles:**
- **Separation of concerns** — persona (cognitive baseline) vs overlays (behavioral modifiers) vs config (composition)
- **Determinism** — same input always produces the same output
- **Runtime targeting** — currently compiles to OpenCode JSON

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

The compilation pipeline is written in Python. No external dependencies beyond PyYAML.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## How It Works

1. **Define** a persona (`sources/personas/<name>.md`) — stable cognitive baseline
2. **Stack** overlays (`sources/overlays/<name>.md`) — behavioral modifiers
3. **Register** in `catalog/index.yaml` — persona + overlays + model + tools + targets
4. **Validate** — `scripts/validate_catalog.py` checks schema and source references
5. **Sync** overlays to skills — `scripts/sync_overlays_to_skills.py`
6. **Compile** — `scripts/compile.py` merges everything into a single system prompt, adds available skills

### Capabilities

| | |
|---|---|---|
| Persona + overlay compilation | Deterministic, reproducible builds |
| Primary / subagent modes | Task delegation with permission + budget |
| Model-agnostic | Set any model ID in catalog |
| Prompt sections | System Persona, Rules, Constraints, Task Behavior, Output Format, Available Skills |
| Catalog validation | Schema + source reference checks via `validate_catalog.py` |
| Overlay-to-skill sync | Automatic sync to `.opencode/skills/overlays/` |

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

### Prerequisites

- Python 3.10+
- PyYAML (`pip install pyyaml`)

### Quick Start

```bash
pip install pyyaml
python3 scripts/validate_catalog.py           # validate catalog
python3 scripts/sync_overlays_to_skills.py   # sync overlays to skills
python3 scripts/compile.py                   # → dist/opencode.json
```

See the [Getting Started guide](docs/guides/getting-started.md) for a full walkthrough.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

### Define a persona

Create `sources/personas/<name>.md` with sections: Identity, Cognitive Profile, Communication Style, Default Reasoning Behavior.

### Define overlays

Create `sources/overlays/<name>.md` with sections: Rules, Constraints, Output Behavior. Rules and Constraints use bullet lists (`- item`); Output Behavior captures the full section body (headings + prose).

### Register in catalog

Edit `catalog/index.yaml` to compose persona + overlays into a config entry.

### Validate, sync, and build

```bash
python3 scripts/validate_catalog.py          # check catalog
python3 scripts/sync_overlays_to_skills.py   # sync overlays → skills
python3 scripts/compile.py                   # build
opencode --agent <agent-id>                  # run
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Docs

- [Getting Started](docs/guides/getting-started.md)
- [Terminology](docs/overview/terminology.md)
- [Build Pipeline](docs/engineering/build-system/build-pipeline.md)
- [Catalog Specification](docs/governance/catalog-spec.md)
- [Persona Specification](docs/engineering/config-system/personas.md)
- [Overlay Specification](docs/engineering/config-system/overlays.md)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT license. See [`LICENSE`](./LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Project Link: [governAI](https://github.com/Synobotix/governAI)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[contributors-shield]: https://img.shields.io/github/contributors/Synobotix/governAI.svg?style=for-the-badge
[contributors-url]: https://github.com/Synobotix/governAI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Synobotix/governAI.svg?style=for-the-badge
[forks-url]: https://github.com/Synobotix/governAI/network/members
[stars-shield]: https://img.shields.io/github/stars/Synobotix/governAI.svg?style=for-the-badge
[stars-url]: https://github.com/Synobotix/governAI/stargazers
[issues-shield]: https://img.shields.io/github/issues/Synobotix/governAI.svg?style=for-the-badge
[issues-url]: https://github.com/Synobotix/governAI/issues
[license-shield]: https://img.shields.io/github/license/Synobotix/governAI.svg?style=for-the-badge
[license-url]: https://github.com/Synobotix/governAI/blob/master/LICENSE.txt
