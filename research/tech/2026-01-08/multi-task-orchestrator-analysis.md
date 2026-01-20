# Multi-Task AI Orchestrator: Design Analysis

> Comparing your multi-task orchestrator RFC against Gas Town and KAI/PAI.

**Date:** 2026-01-08
**Sources:**
- [Welcome to Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) - Steve Yegge, January 2026
- [Building a Personal AI Infrastructure](https://danielmiessler.com/blog/personal-ai-infrastructure) - Daniel Miessler
- ~/multi-task-ai-orchestrator.md - Local RFC

---

## Executive Summary

The multi-task orchestrator RFC proposes a Rust-based daemon that manages concurrent AI agent tasks within a single process. This fills a gap in the current landscape: **disciplined multi-task execution**.

The core thesis is correct: "The agentic loop is simple; multi-task coordination is where the real complexity and value lies."

---

## Landscape Positioning

```
                Single-Task          Multi-Task
              ┌─────────────────┬─────────────────┐
              │                 │                 │
   Chaotic    │    Cursor/      │   Gas Town      │
              │    Aider        │                 │
              │                 │                 │
              ├─────────────────┼─────────────────┤
              │                 │                 │
   Disciplined│   KAI/PAI       │   PAIS          │
              │   Claude Code   │   Orchestrator  │
              │                 │                 │
              └─────────────────┴─────────────────┘
```

The RFC targets the bottom-right quadrant—disciplined multi-task—which no existing tool occupies.

---

## Detailed Comparison

### Architecture

| Aspect | Gas Town | KAI/PAI | PAIS Orchestrator |
|--------|----------|---------|-------------------|
| **Multi-task** | Yes (20-30 agents) | No (inherits CC limit) | Yes (N tasks) |
| **Process model** | tmux + N processes | 1 process | 1 daemon + async tasks |
| **Coordination** | Chaos + git | None needed | Explicit locks + scheduler |
| **Crash recovery** | Git-backed (Beads) | transcript_path | SQLite + filesystem |
| **Engineering rigor** | "Never seen the code" | Well-documented | RFC-driven, typed |
| **Resource safety** | "Can wreck your shit" | Hooks/permissions | Lock manager + policies |
| **Language** | Go (225k lines) | TypeScript/Bun | Rust |

### Task/Agent Models

| System | Model | Persistence |
|--------|-------|-------------|
| **Gas Town** | Role-based (Overseer, Mayor, Polecats, Refinery, Witness) | Git-backed molecules |
| **KAI/PAI** | Personality-based (Engineer, Architect, Researcher, etc.) | File-based history |
| **PAIS Orchestrator** | State-machine tasks (Queued, Running, WaitingForUser, Blocked, etc.) | SQLite + filesystem |

### Process Models Compared

**Gas Town:**
```
┌──────────────────────────────────────────────┐
│                    tmux                       │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│  │ CC #1  │ │ CC #2  │ │ CC #3  │ │ CC #N  │ │
│  │ pane 1 │ │ pane 2 │ │ pane 3 │ │ pane N │ │
│  └────────┘ └────────┘ └────────┘ └────────┘ │
│       │          │          │          │     │
│       └──────────┴──────────┴──────────┘     │
│                      │                        │
│               Beads (git)                     │
└──────────────────────────────────────────────┘
```
- N separate Claude Code processes
- Coordination via git (Beads)
- Visual monitoring (watch panes)
- Merge conflicts at scale

**PAIS Orchestrator:**
```
┌──────────────────────────────────────────────┐
│              PAIS Daemon (single process)     │
│                                              │
│  ┌─────────────────────────────────────────┐ │
│  │            Task Manager                  │ │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │ │
│  │  │Task 1│ │Task 2│ │Task 3│ │Task N│   │ │
│  │  │tokio │ │tokio │ │tokio │ │tokio │   │ │
│  │  └──────┘ └──────┘ └──────┘ └──────┘   │ │
│  └─────────────────────────────────────────┘ │
│                      │                        │
│  ┌─────────────────────────────────────────┐ │
│  │ Shared: LLM Client, Lock Manager,       │ │
│  │         Knowledge Store, Event Bus      │ │
│  └─────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```
- Single process, N tokio tasks
- Shared rate limiting and knowledge
- Explicit resource locking
- Lower overhead, better coordination

---

## Strengths of the RFC Design

### 1. Daemon Model

Gas Town spawns separate processes (tmux panes). The RFC uses tokio tasks in a single daemon. Benefits:

- **Shared LLM rate limiting** - One rate limiter, not N competing ones
- **Shared knowledge store** - Learnings available instantly to all tasks
- **Lower overhead** - Tokio tasks are ~KB, not ~100MB per process
- **Coordinated resource locking** - Deadlock-free lock acquisition

### 2. Explicit Task States

The `TaskStatus` enum is more nuanced than Gas Town's implicit state:

```rust
pub enum TaskStatus {
    Queued,
    Running { phase: RunningPhase, started_at: DateTime<Utc> },
    WaitingForUser { prompt: String, options: Option<Vec<String>> },
    Blocked { resource: ResourceId, reason: String },
    Completed { summary: String, completed_at: DateTime<Utc> },
    Failed { error: String, recoverable: bool, failed_at: DateTime<Utc> },
    Paused,
    Cancelled,
}
```

This enables:
- Clear visibility into task progress
- Automatic recovery decisions
- Proper scheduling

### 3. Resource Locking with Deadlock Prevention

Gas Town's Beads has merge conflict problems. The RFC's sorted-acquire pattern prevents deadlocks:

```rust
// Sort resources to prevent deadlock
let mut sorted: Vec<_> = resources.iter().collect();
sorted.sort();

for resource in sorted {
    self.acquire_one(resource, mode, task_id).await?;
}
```

### 4. Git Worktrees

The right solution for multi-task git coordination:

```rust
pub async fn setup_workspace(
    &self,
    repo_path: &Path,
    task_id: TaskId,
) -> Result<PathBuf> {
    let worktree_path = repo_path
        .parent()
        .unwrap()
        .join(format!(".worktrees/{}", task_id));

    Command::new("git")
        .args(["worktree", "add", worktree_path.to_str().unwrap()])
        .current_dir(repo_path)
        .output()
        .await?;

    Ok(worktree_path)
}
```

Gas Town struggles with git coordination. This solves it cleanly.

### 5. Attach/Detach Semantics

Like tmux, but for AI tasks:

```bash
pais task attach <id>   # Interactive mode
pais task detach        # Ctrl+D, task continues
pais task send <id> "message"  # Send without attaching
```

Neither Gas Town nor KAI has this as a first-class concept.

---

## What to Steal from Gas Town

### 1. The Witness Concept

Gas Town has a "Witness" agent that monitors other agents and unsticks them when they drift. The RFC's scheduler doesn't have this.

**Recommendation:** Add a background monitoring task:

```rust
pub struct Witness {
    /// Detect tasks burning tokens without progress
    async fn detect_drift(&self, task: &Task) -> Option<DriftReport>;

    /// Intervene on stuck tasks
    async fn unstick(&self, task_id: TaskId, strategy: UnstickStrategy);
}
```

### 2. Named Agent Roles

The RFC's tasks are anonymous. Gas Town's Mayor/Polecats/Refinery/Witness roles create clearer mental models.

**Recommendation:** Consider role templates:

```rust
pub enum TaskRole {
    /// One-off worker task
    Worker,
    /// Long-running coordinator
    Coordinator,
    /// Background monitor
    Witness,
    /// Handles merges and conflicts
    Refiner,
}
```

### 3. Git-Backed State Benefits

Beads' everything-is-git approach has advantages the RFC's SQLite+filesystem doesn't:

- Built-in versioning (git log shows task history)
- Easy debugging (git diff between checkpoints)
- Natural branching for task isolation
- Conflict detection built-in

**Recommendation:** Consider hybrid—SQLite for queries, git for conversation history.

---

## What to Steal from KAI/PAI

### 1. Learning Extraction Patterns

KAI's `hasLearningIndicators()` function:

```typescript
function hasLearningIndicators(text: string): boolean {
  const indicators = [
    'problem', 'solved', 'discovered', 'fixed', 'learned', 'realized',
    'figured out', 'root cause', 'debugging', 'issue was', 'turned out',
    'mistake', 'error', 'bug', 'solution'
  ];
  const lowerText = text.toLowerCase();
  const matches = indicators.filter(i => lowerText.includes(i));
  return matches.length >= 2;  // Need 2+ indicators
}
```

The RFC mentions a knowledge store but doesn't detail extraction.

### 2. Routing Accuracy Measurement

KAI claims ~95-98% routing accuracy. The RFC should measure:

- Task completion rate
- User intervention rate
- Cost per successful task
- Drift detection accuracy

### 3. Security Layers

KAI has 4 defense layers. The RFC's `SecurityPolicy` struct is a start:

```rust
pub struct SecurityPolicy {
    dangerous_commands: Vec<Regex>,
    protected_paths: Vec<PathBuf>,
    allowed_hosts: Vec<String>,
    max_cost_per_task: f64,
    max_concurrent_tasks: usize,
}
```

**Recommendation:** Add explicit layers:
1. Pre-tool validation (current)
2. Sandboxed execution
3. Post-tool audit
4. Anomaly detection

---

## Critical Design Questions

### Answered

| Question | Recommendation | Rationale |
|----------|---------------|-----------|
| Daemon vs on-demand? | **Daemon** | Cross-task intelligence requires shared state |
| SQLite vs KV store? | **SQLite** | Queries like "all tasks touching this file" |
| Git worktrees vs stashing? | **Worktrees** | Stashing is a nightmare with N tasks |
| Sub-tasks? | **Yes, bounded** | 2-3 levels max, like Gas Town's Polecats |

### Still Open

1. **Layer on Claude Code or replace?**
   - Pro CC: Battle-tested tools, existing permissions, automatic updates
   - Pro replace: Full control, no Node dependency, cleaner architecture
   - **Lean:** Layer on CC initially, fork tools if needed

2. **How smart should learning extraction be?**
   - Simple: Keyword matching (fast, deterministic)
   - Smart: LLM-powered extraction (expensive, better quality)
   - **Lean:** Start simple, upgrade if quality insufficient

3. **Notification strategy?**
   - Terminal bell for attached users
   - Desktop notification for detached
   - Consider: webhook for remote monitoring

---

## Implementation Priority

### Phase 1: MVP (Validate Core Thesis)

Focus: Prove multi-task coordination works

```
[ ] Single-task agent loop (copy from reference impls)
[ ] Task manager with concurrent execution
[ ] Basic CLI: new, list, attach, detach
[ ] SQLite persistence
```

**Success metric:** Run 3 tasks concurrently without conflicts

### Phase 2: Coordination (Differentiator)

Focus: Resource safety Gas Town lacks

```
[ ] Lock manager with deadlock prevention
[ ] Git worktree coordination
[ ] Event bus for cross-task communication
[ ] User input routing
```

**Success metric:** 10 tasks in same repo, zero conflicts

### Phase 3: Intelligence (KAI Parity)

Focus: Cross-task learning

```
[ ] Knowledge store implementation
[ ] Learning extraction (keyword-based)
[ ] Context injection from knowledge
[ ] Witness (drift detection)
```

**Success metric:** Task B uses learning from Task A without explicit sharing

### Phase 4: Polish

```
[ ] Streaming responses
[ ] TUI dashboard
[ ] Cost tracking
[ ] Comprehensive security policy
```

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Tokio complexity | Medium | High | Start simple, add concurrency incrementally |
| LLM rate limits | High | Medium | Shared rate limiter, request queuing |
| Git worktree edge cases | Medium | Medium | Fallback to single-task mode |
| Context explosion (N tasks) | High | High | Aggressive summarization, token budgets |
| Daemon stability | Medium | High | Watchdog, automatic restart, checkpointing |

---

## Conclusion

The RFC fills a genuine gap: disciplined multi-task AI orchestration. It takes:

- **From Gas Town:** Multi-task ambition, git-backed thinking
- **From KAI/PAI:** Discipline, learning systems, security posture
- **Original:** Daemon model, explicit locking, attach/detach semantics

The Rust implementation is well-suited—tokio for concurrency, SQLite for persistence, strong typing for correctness.

**Recommendation:** Ship Phase 1 in 2-3 weeks. Validate the thesis before investing in advanced features. The core innovation is task coordination, not another agentic loop.

---

## References

- [Gas Town vs KAI/PAI Comparison](./gas-town-vs-kai-pai/2026-01-08.md) - Related research
- [Multi-Task AI Orchestrator RFC](~/multi-task-ai-orchestrator.md) - Source document
- [Welcome to Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) - Steve Yegge
- [Hacker News Discussion](https://news.ycombinator.com/item?id=46458936) - Community reception
- [PAI Deep Dive](https://www.youtube.com/watch?v=Le0DLrn7ta0) - Daniel Miessler
