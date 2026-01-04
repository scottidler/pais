---
name: gx
description: Multi-repo Git operations - bulk changes, PRs, and cleanup across many repositories
allowed-tools: Bash(gx:*), Bash(gh:*)
tier: 1
triggers:
  - multi-repo
  - bulk change
  - mass update
  - N repos
  - many repos
  - across repos
  - gx
---

# GX

CLI for git operations across multiple repositories simultaneously.

## Syntax Discovery

**ALWAYS run `--help` to discover exact syntax before using any command:**

```bash
gx --help                    # List all commands
gx <command> --help          # Command options (e.g., gx create --help)
gx <command> <action> --help # Action options (e.g., gx create sub --help)
```

The help output includes working EXAMPLES - use those as templates.

## Core Concept: Progressive Filtering

GX operations follow a funnel pattern - start broad, narrow down:

```
All repos in cwd
    ↓ -p pattern      (filter repos by name)
    ↓ --files         (filter files within repos)
    ↓ sub/regex       (filter by content match)
    ↓ --commit        (actually make changes)
    ↓ --pr            (create PRs)
```

**Omit later stages to preview what would be affected.**

## Worked Example: Find and Replace Across Repos

**Goal:** Update Python version from 3.11 to 3.12 in Dockerfiles across philo repos.

### Step 1: Filter by repo pattern

```bash
$ gx create -p philo -p philo-fe
Matched repositories:
  tatari-tv/philo
  tatari-tv/philo-fe

  2📦 | 2🔍
```

✓ Found 2 repos matching the pattern.

### Step 2: Filter by files

```bash
$ gx create -p philo -p philo-fe -f Dockerfile
Matched repositories:
  tatari-tv/philo
    Dockerfile
  tatari-tv/philo-fe
    Dockerfile

  2📄 | 2📦 | 2🔍
```

✓ Both repos have Dockerfiles.

### Step 3: Add substitution pattern (dry-run)

```bash
$ gx create -p philo -p philo-fe -f Dockerfile sub python:3.11 python:3.12
GX-2026-01-03T20-30-52 ------- ✏️ tatari-tv/philo
GX-2026-01-03T20-30-52 ------- ➖ tatari-tv/philo-fe

📊 2 repositories processed:
   ✏️  1 would change
   ➖ 1 no matches
   📄 1 files affected

🔍 Pattern Analysis:
   📄 Files scanned: 2
   ✅ Files changed: 1
   ❌ Files with no matches: 1
```

✓ Output shows only philo has the pattern - philo-fe doesn't match.

### Step 4: Execute changes (add --commit)

```bash
$ gx create -p philo -f Dockerfile sub python:3.11 python:3.12 --commit
```

### Step 5: Create PRs (add --pr)

```bash
$ gx create -p philo -f Dockerfile sub python:3.11 python:3.12 --commit --pr
```

### Step 6: Review and merge

```bash
$ gx review ls GX-2026-01-03T20-30-52     # List PRs
$ gx review approve GX-2026-01-03T20-30-52 # Approve and merge
```

### Step 7: Cleanup

```bash
$ gx cleanup GX-2026-01-03T20-30-52       # Delete branches
```

---

**Key insight:** Build up queries incrementally. Each step's output guides the next refinement. Don't jump straight to `--commit` - preview first!

## Quick Reference

### Discovery Commands (no changes)

```bash
gx create -p PATTERN                        # Which repos match?
gx create -p PATTERN -f FILE                # Which have this file?
gx create -p PATTERN -f FILE sub OLD NEW    # Which files have OLD?
```

### Execution Commands (makes changes)

```bash
gx create ... --commit                      # Apply changes locally
gx create ... --commit --pr                 # Apply + create PRs
gx create ... --commit --pr=draft           # Apply + create draft PRs
```

### Post-Change Commands

```bash
gx review ls <change-id>       # List PRs for a change
gx review approve <change-id>  # Approve and merge
gx cleanup <change-id>         # Clean up branches after merge
gx cleanup --list              # Show what needs cleanup
```

## Commands Overview

| Command | Purpose |
|---------|---------|
| `status` | Show git status across repos |
| `checkout` | Checkout branches across repos |
| `clone` | Clone org repos |
| `create` | Make changes, create PRs |
| `review` | Manage PRs (list, approve, delete) |
| `cleanup` | Clean up branches after merge |
| `rollback` | Recover from interrupted operations |

Run `gx <command> --help` for each command's options and examples.

## Key Concepts

- **Change IDs**: Auto-generated like `GX-2026-01-03T12-30-00`. All branches/PRs for one operation share the same ID.
- **Dry-run by default**: Without `--commit`, changes are previewed only.
- **Pattern Analysis**: Output shows files scanned, changed, and unmatched.

## Requirements

- `git` >= 2.30
- `gh` CLI (authenticated)
