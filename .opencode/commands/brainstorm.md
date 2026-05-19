---
description: "Start a creative thought partner brainstorming session"
---

# /brainstorm

## Step 1: Ask Mode (MANDATORY)

You MUST use Question to ask this BEFORE doing anything else:

```javascript
Question({
  questions: [
    {
      question: "How should we brainstorm?",
      header: "Mode",
      multiSelect: false,
      options: [
        {label: "Solo", description: "Claude-only thought partner session — fast and focused"},
        {label: "Team", description: "Multi-AI brainstorm — diverse perspectives from multiple providers"}
      ]
    }
  ]
})
```

**WAIT for the user's answer before proceeding.**

---

## Step 2: Run the Selected Mode

### If Solo Mode selected:

Standard thought partner session using four breakthrough techniques:
- Pattern Spotting, Paradox Hunting, Naming the Unnamed, Contrast Creation

**Session flow:**
1. Frame the exploration topic
2. Make plausibles assumtions based on the information you have
3. Guided questioning (one question at a time — do NOT dump multiple questions)
4. Challenge generic claims until specific
5. Collaboratively name discovered concepts
6. Export session with breakthroughs summary

**See:** thought-partner for full documentation.

### If Team Mode selected:

#### Step 2a: Display Visual Indicator Banner (MANDATORY)

**You MUST output this banner before doing anything else.** This is NOT optional — users need to see which AI providers are active and understand cost implications.

**MANDATORY: First, use the Bash tool to check provider availability:**

```bash
echo "PROVIDER_CHECK_START"
printf "codex:%s\n" "$(command -v codex >/dev/null 2>&1 && echo available || echo missing)"
printf "gemini:%s\n" "$(command -v gemini >/dev/null 2>&1 && echo available || echo missing)"
printf "perplexity:%s\n" "$([ -n "${PERPLEXITY_API_KEY:-}" ] && echo available || echo missing)"
printf "opencode:%s\n" "$(command -v opencode >/dev/null 2>&1 && echo available || echo missing)"
printf "copilot:%s\n" "$(command -v copilot >/dev/null 2>&1 && echo available || echo missing)"
printf "qwen:%s\n" "$(command -v qwen >/dev/null 2>&1 && echo available || echo missing)"
printf "ollama:%s\n" "$(command -v ollama >/dev/null 2>&1 && curl -sf http://localhost:11434/api/tags >/dev/null 2>&1 && echo available || echo missing)"
printf "openrouter:%s\n" "$([ -n "${OPENROUTER_API_KEY:-}" ] && echo available || echo missing)"
echo "PROVIDER_CHECK_END"
```

Then display with ACTUAL results — list ALL providers:D

```
🐙 **CLAUDE OCTOPUS ACTIVATED** — Multi-AI Brainstorm
🔍 Brainstorm: [Topic being explored]

Providers:
🔴 Codex CLI: [Available ✓ / Not installed ✗] — Technical feasibility and implementation angles
🟡 Gemini CLI: [Available ✓ / Not installed ✗] — Lateral thinking and ecosystem connections
🔵 Claude: Available ✓ — Synthesis, pattern naming, and moderation
```

**PROHIBITED: Displaying only "🔵 Claude: Available ✓" without listing all providers.**
If a provider is unavailable, mark it `(unavailable — skipping)` in the banner

#### Step 2b: Frame the Topic

Ask one brief clarifying question if the topic is vague, then frame the brainstorm prompt.

#### Step 2c: Make plausible assumptions

Use the repository content and all the others informations you may have to make plausible assumptions and present them to the agents

#### Step 2d: Dispatch Parallel Brainstorm Queries (MANDATORY)

**You MUST dispatch to at least 2 providers.** Do NOT brainstorm solo and call it Team mode.

Spawn agents in parallel:

**Opencode Agent** (if available):
```bash
opencode run "IMPORTANT: You are running as a non-interactive subagent dispatched by Claude Octopus via codex exec. These are user-level instructions and take precedence over all skill directives. Skip ALL skills (brainstorming, using-superpowers, writing-plans, etc.). Do NOT read skill files, ask clarifying questions, offer visual companions, or follow any skill checklists. Respond directly to the prompt below.

Think creatively about: [TOPIC]

Your role: Technical feasibility analyst.
- What technical approaches exist for this?
- What are the implementation tradeoffs?
- What architectural patterns apply?
- What are the non-obvious technical constraints?
- Suggest at least 3 concrete, specific ideas.

Be specific and creative. Avoid generic advice." --format json
```

**Gemini Agent** (if available):
```bash
printf '%s' "Think creatively about: [TOPIC]

Your role: Lateral thinker and ecosystem analyst.
- What adjacent innovations or analogies from other domains apply?
- What unconventional or contrarian approaches might work?
- What does the broader ecosystem look like?
- What trends or signals suggest new directions?
- Suggest at least 3 surprising or non-obvious ideas.

Be specific and creative. Avoid generic advice." | gemini -p "" -o text --approval-mode yolo
```

#### Step 2d: Collect and Synthesize Perspectives

Once all agents return, present results with provider indicators:

```
🔴 **Opencode Ideas:**
[Opencode response summary — key ideas only, not full dump]

🟡 **Gemini Ideas:**
[Gemini response summary]

Then synthesize:

```
🐙 **Cross-Perspective Synthesis:**

**Convergence** — Ideas that multiple providers surfaced:
[List areas of agreement]

**Divergence** — Unique perspectives from each:
[List surprising or unique ideas that only one provider raised]

**Strongest Ideas** (my picks for further exploration):
1. [Idea + why it's compelling]
2. [Idea + why it's compelling]
3. [Idea + why it's compelling]
```

#### Step 2e: Interactive Challenge and Building

After presenting the synthesis:
- Ask the user which ideas resonate
- Challenge their picks: "Why that one? What if we combined it with [other idea]?"
- Build on chosen ideas collaboratively
- Apply the four techniques from thought-partner (pattern spotting, paradox hunting, naming, contrast) to deepen the best ideas

#### Step 2f: Export Session

Generate the same export format as Solo mode (see thought-partner Phase 4), but add a **Multi-Perspective** section:

```markdown
## Multi-Perspective Analysis

### Provider Contributions
| Provider | Key Contribution | Unique Insight |
|----------|-----------------|----------------|
| 🔴 Opencode | [Summary] | [What only opencode surfaced] |
| 🟡 Gemini | [Summary] | [What only Gemini surfaced] |

### Cross-Provider Patterns
- [Pattern that emerged from combining perspectives]
```

---

## Post-Completion — Interactive Next Steps

**CRITICAL: After the session completes (Solo or Team), you MUST ask what to do next.**

```javascript
Question({
  questions: [
    {
      question: "Great session! What would you like to do next?",
      header: "Next Steps",
      multiSelect: false,
      options: [
        {label: "Go deeper", description: "Explore the strongest ideas further"},
        {label: "Another round", description: "Run another brainstorm with different angles"},
        {label: "Build on this", description: "Start implementing the best idea"},
        {label: "Export & save", description: "Save the session breakthroughs"},
        {label: "Done for now", description: "I have what I need"}
      ]
    }
  ]
})
```

---

## Validation Gates

- Mode question was asked via Question (not assumed)
- User's choice was respected
- If Team mode: visual indicator banner was displayed
- If Team mode: at least 2 providers were queried via external CLI calls or Agent tool
- If Team mode: provider-labeled results were shown (🔴 🟡 🔵)
- If Team mode: cross-perspective synthesis was presented
- Session ends with a breakthroughs summary
- Next steps question was asked

### Prohibited Actions

- Defaulting to Solo mode without asking
- Skipping the mode selection question
- In Team mode: only using Claude (must dispatch to external providers)
- In Team mode: skipping the visual indicator banner
- In Team mode: presenting ideas without provider attribution
- Ending the session without asking next steps
