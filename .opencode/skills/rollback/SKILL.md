---
name: skill-rollback
user-invocable: true
description: "Roll back to a previous checkpoint via git — use when a change went wrong and you need to revert"
trigger: |
  AUTOMATICALLY ACTIVATE when user mentions:
  - "rollback" or "revert" or "undo"
  - "go back to" or "restore checkpoint"
argument-hint: "[list|<checkpoint-tag>]"
---

# Checkpoint Rollback

Safely rollback to a previous checkpoint while preserving lessons learned.

**Core principle:** List checkpoints → Confirm explicitly → Create safety backup → Restore → Preserve lessons.

---

## Subcommand Detection

Parse the user's request to determine mode:

| User Request | Mode | Action |
|--------------|------|--------|
| `list`, `show checkpoints`, no argument | LIST | Show available checkpoints |
| `checkpoint-*` tag name | ROLLBACK | Rollback to specific checkpoint |

---

## Mode: LIST (Default)

### Step 1: Fetch Available Checkpoints

```bash
# List all checkpoints with dates
git tag -l "checkpoint-*" --sort=-creatordate --format='%(refname:short)|%(creatordate:short)|%(contents:subject)'
```

### Step 2: Present Checkpoint Table

```markdown
## Available Checkpoints

| Tag | Created | Description |
|-----|---------|-------------|
| checkpoint-post-discover-20260203-143022 | 2026-02-03 | After Discover phase |
| checkpoint-post-define-20260203-150145 | 2026-02-03 | After Define phase |

Usage: `rollback <tag-name>`
```

**If no checkpoints found:**
```
No checkpoints found. Checkpoints can be created with:
  git tag -a checkpoint-<name>-$(date +%Y%m%d-%H%M%S) -m "Checkpoint description"

The AGENTS.md commit hard gates also serve as natural rollback points via commit SHAs.
```

---

## Mode: ROLLBACK

### Step 1: Validate Checkpoint Exists

```bash
# Validate CHECKPOINT_TAG is set and tag exists
if [ -z "$CHECKPOINT_TAG" ]; then
  echo "ERROR: No checkpoint tag specified"
  exit 1
fi

git tag -l "$CHECKPOINT_TAG" | grep -q . || echo "TAG_NOT_FOUND"
```

**If tag not found or CHECKPOINT_TAG empty:**
```
Checkpoint '$CHECKPOINT_TAG' not found.

Available checkpoints:
[show list output]
```

**STOP. Do not proceed.**

### Step 2: Show What Will Be Affected

```bash
# Get list of files that will be changed
git diff --name-status HEAD "$CHECKPOINT_TAG"
```

Present clearly:
```markdown
## Rollback Preview

**Rolling back to:** `checkpoint-post-discover-20260203-143022`
**Created:** 2026-02-03 14:30:22
**Description:** After Discover phase

### Files That Will Be Changed

| Status | File |
|--------|------|
| M | src/auth/login.ts |
| D | src/auth/oauth.ts |
| A | src/legacy/old-auth.ts |

Legend: M=Modified, D=Deleted, A=Added (relative to current state)

### Protected Files (Will NOT be changed)
- Project documentation and working artifacts - preserved via git's history
```

### Step 2.5: Check for Uncommitted Changes

Before asking for confirmation, check if the working tree is clean:

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "WARNING: You have uncommitted changes that will be overwritten:"
  git status --short
  echo ""
  echo "To proceed, either:"
  echo "  1. Commit them first: git add -A && git commit -m 'wip: before rollback'"
  echo "  2. Stash them: git stash"
  echo "  3. Discard them (irreversible): git reset --hard"
fi
```

**Do NOT proceed if there are uncommitted changes.** Inform the user and stop.

### Step 3: Require Explicit Confirmation (MANDATORY)

```
To confirm this rollback, type ROLLBACK exactly.

Any other input will cancel.
```

**Wait for exact confirmation: `ROLLBACK`**

**CRITICAL:** Do NOT proceed without explicit "ROLLBACK" confirmation.

### Step 4: Create Safety Checkpoint

Before any rollback, create a pre-rollback checkpoint:

```bash
# Generate timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Create safety checkpoint
git tag -a "checkpoint-pre-rollback-$TIMESTAMP" -m "Safety checkpoint before rollback to $CHECKPOINT_TAG"
```

Report:
```
Created safety checkpoint: checkpoint-pre-rollback-$TIMESTAMP

You can return to current state with:
  rollback checkpoint-pre-rollback-$TIMESTAMP
```

### Step 5: Preserve Working Artifacts

```bash
# Save working artifacts (STATE.*.md, TODO.*.md, DECISIONS.*.md, MEMORY.md) if they exist
for f in STATE.*.md TODO.*.md DECISIONS.*.md MEMORY.md; do
  if [ -f "$f" ]; then
    cp "$f" "/tmp/rollback_preserved_$f"
  fi
done
```

### Step 5.5: Log Rollback to MEMORY.md (Before Checkout)

```bash
if [ -f "MEMORY.md" ]; then
  echo "" >> MEMORY.md
  echo "## Rollback - $(date '+%Y-%m-%d %H:%M')" >> MEMORY.md
  echo "" >> MEMORY.md
  echo "- **Target:** $CHECKPOINT_TAG" >> MEMORY.md
  echo "- **Safety checkpoint:** checkpoint-pre-rollback-$TIMESTAMP" >> MEMORY.md
  echo "- **Reason:** User requested rollback" >> MEMORY.md
fi
```

### Step 6: Execute Rollback

```bash
# Restore files from checkpoint (does NOT move HEAD)
git checkout "$CHECKPOINT_TAG" -- .

# Restore preserved working artifacts (overwrite checkpoint versions)
for f in STATE.*.md TODO.*.md DECISIONS.*.md MEMORY.md; do
  if [ -f "/tmp/rollback_preserved_$f" ]; then
    cp "/tmp/rollback_preserved_$f" "$f"
  fi
done
```

**Important:** This uses `git checkout <tag> -- .` which:
- Restores all files to checkpoint state
- Does NOT move HEAD or change branch
- Preserves current commit history
- Allows immediate commit of the restored state

### Step 7: Report Success

```markdown
Rollback Complete

**Restored to:** `$CHECKPOINT_TAG`
**Files restored:** N files
**Working artifacts (STATE.*.md, TODO.*.md, DECISIONS.*.md):** Preserved (not rolled back)

**Safety checkpoint created:** `checkpoint-pre-rollback-$TIMESTAMP`

### Next Steps

1. Review the restored files
2. Commit the rollback if satisfied:
   ```bash
   git add -A && git commit -m "chore: rollback to $CHECKPOINT_TAG"
   ```
3. Or return to previous state:
   ```bash
   rollback checkpoint-pre-rollback-$TIMESTAMP
   ```
```

---

## Safety Measures

| Measure | Implementation |
|---------|----------------|
| **Always create safety checkpoint** | Pre-rollback tag created BEFORE any file changes |
| **Preserve working artifacts** | Copy STATE.*.md / TODO.*.md / DECISIONS.*.md before rollback |
| **Require explicit confirmation** | Must type "ROLLBACK" exactly |
| **Show affected files first** | Preview before confirmation |
| **No history modification** | Uses checkout, not reset |

---

## Red Flags - Never Do

| Action | Why It's Dangerous |
|--------|-------------------|
| Rollback without confirmation | Loses work unexpectedly |
| Skip safety checkpoint | No recovery path |
| Rollback working artifacts | Loses accumulated knowledge |
| Use `git reset --hard` | Destroys commit history |
| Force push after rollback | Affects collaborators |
| Delete checkpoint tags | Removes recovery points |

---

## Checkpoint Tag Format

Checkpoints follow this format:

```
checkpoint-{name}-{timestamp}

Where:
- name: descriptive label (e.g. pre-rollback, manual, before-refactor)
- timestamp: YYYYMMDD-HHMMSS
```

Examples:
- `checkpoint-before-auth-refactor-20260203-143022`
- `checkpoint-pre-rollback-20260203-161530`
- `checkpoint-manual-20260203-170000`
- `checkpoint-post-feature-x-20260203-150145`

---

## Quick Reference

| Command | Action |
|---------|--------|
| `rollback` | List available checkpoints |
| `rollback list` | List available checkpoints |
| `rollback <tag>` | Rollback to specific checkpoint |

---

## The Bottom Line

```
Rollback → Confirmation received AND safety checkpoint created
Otherwise → Not executed
```

**Show preview. Require "ROLLBACK". Create safety tag. Preserve lessons. Execute safely.**
