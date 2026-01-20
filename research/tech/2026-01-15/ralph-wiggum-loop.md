# Ralph Wiggum Loop Research - 2026-01-15

## Overview

The Ralph Wiggum technique is an autonomous AI development loop created by Geoffrey Huntley. In its purest form, it's a simple bash while loop that repeatedly feeds Claude Code a prompt file until completion.

## The REAL Ralph Wiggum (Original Bash Script)

### Simplest Form

```bash
while :; do cat PROMPT.md | claude ; done
```

### With Permissions Skip (for true autonomy)

```bash
while true; do
    cat PROMPT.md | claude -p \
        --dangerously-skip-permissions \
        --model opus \
        --verbose
    git push origin $(git branch --show-current)
done
```

## Key Philosophy

- "Ralph is a Bash loop" — Geoffrey Huntley
- "Deterministically bad in an undeterministic world"
- Forces Claude to confront its own failures without a safety net
- Each iteration sees modified files and git history from previous runs

## Recommended Project Structure

```
project-root/
├── loop.sh                    # The orchestration script
├── PROMPT.md                  # Main instructions (or split into plan/build)
├── PROMPT_plan.md            # Planning mode instructions (optional)
├── PROMPT_build.md           # Building mode instructions (optional)
├── AGENTS.md                 # Operational how-to guide
├── IMPLEMENTATION_PLAN.md    # Task list (generated/updated by Ralph)
├── specs/                    # Requirements (one per feature/JTBD topic)
└── src/                      # Implementation code
```

## Advanced Loop Script (loop.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration
MAX_ITERATIONS=${MAX_ITERATIONS:-50}
PROMPT_FILE=${PROMPT_FILE:-PROMPT.md}
MODEL=${MODEL:-sonnet}

iteration=0

while true; do
    ((iteration++))
    echo "=== Iteration $iteration of $MAX_ITERATIONS ==="

    if [[ $iteration -gt $MAX_ITERATIONS ]]; then
        echo "Max iterations reached. Exiting."
        exit 0
    fi

    # Run Claude with the prompt
    cat "$PROMPT_FILE" | claude -p \
        --dangerously-skip-permissions \
        --model "$MODEL" \
        --verbose

    # Optional: push changes after each iteration
    # git push origin $(git branch --show-current) 2>/dev/null || true

    # Optional: sleep between iterations
    sleep 2
done
```

## PROMPT.md Structure (Example)

```markdown
# Project: [Your Project Name]

## Context
You are an autonomous AI developer working on [project description].

## Current State
- Read IMPLEMENTATION_PLAN.md for the current task list
- Check git log for recent changes
- Review any failing tests

## Your Task
1. Identify the highest priority incomplete task from IMPLEMENTATION_PLAN.md
2. Investigate the codebase before making changes
3. Implement the solution
4. Run tests to verify
5. If tests pass, commit with a meaningful message
6. Update IMPLEMENTATION_PLAN.md marking the task complete

## Success Criteria
[Define what "done" looks like]

## Constraints
- Only work on ONE task per iteration
- Always run tests before committing
- Update the plan file after each task
```

## Safety Considerations

1. **Always set max iterations** - Prevent runaway API costs
2. **Use sandboxed environments** - VMs, containers, or disposable cloud instances
3. **Monitor API usage** - 50-iteration loops can cost $50-100+
4. **Have escape hatches** - Ctrl+C, git reset --hard

## Sources

- https://ghuntley.com/ralph/
- https://github.com/ghuntley/how-to-ralph-wiggum
- https://paddo.dev/blog/ralph-wiggum-autonomous-loops/
- https://www.humanlayer.dev/blog/brief-history-of-ralph
- https://github.com/frankbria/ralph-claude-code
