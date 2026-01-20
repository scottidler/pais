# Jeffrey Emanuel's "Rule of Five"

**Research Date:** 2026-01-10

## Summary

The **Rule of Five** is an agentic coding principle discovered by Jeffrey Emanuel stating: **"When in doubt, have the agent review its own work 5 times."**

The core insight is that AI coding agents produce dramatically better output when forced to iteratively review their own work 4-5 times, at which point the output "converges" and the agent will declare it's as good as it can get.

## Who is Jeffrey Emanuel?

- **Founder & CEO** of Lumera Network
- **Creator** of the Agentic Coding Tooling Flywheel - a self-reinforcing ecosystem of 7 interconnected tools
- **GitHub:** [@Dicklesworthstone](https://github.com/Dicklesworthstone)
- **30+ open-source projects** with 10K+ GitHub stars
- Key projects: MCP Agent Mail, Beads Viewer, CASS Memory System, and more

## The Rule of Five - How It Works

### The Core Principle

Force AI agents to review their proposals (designs, plans, implementations) **4-5 times**, at which point the output converges. It typically takes 4-5 iterations before the agent will say something like "I think this is about as good as we can make it."

### The Process

1. **Have the agent do a task** (design, plan, or implement)
2. **Conduct a series of focused reviews** with these characteristics:
   - Each review should be slightly broader and more outlandish than the previous (or vice versa)
   - Mix "in-the-small" reviews (code quality, edge cases) with "in-the-large" reviews (architecture, design)
   - Look for both bad code/designs AND bad architecture

### Practical Guidelines

| Task Size | Recommended Passes |
|-----------|-------------------|
| Small tasks | 2-3 passes |
| Big tasks | 4-5 passes |

### Where to Apply

- **5 passes over implementation plans** - results in better issues and dependencies
- **5 passes over implementation** - code + 4 reviews
- Apply at every step in the process

## Why It Works

Claude (the AI) claims this process matches their own **breadth-first cognition model**:
1. They solve problems first in very broad strokes
2. They almost always need more passes for proofreading, refining, and polishing
3. Much like humans do

## Validation

Steve Yegge tested this approach:

> "I tried it, and sure enough, it does take 4-5 iterations, just as Jeffrey described, before the agent will say something like, 'I think this is about as good as we can make it.' At that point it has converged. And that, folks, is the first point at which you can begin to moderately trust the output the agent has produced."

## Trade-offs

**Costs:**
- Slower execution
- More expensive (more API calls/tokens)

**Benefits:**
- Higher quality output
- Likely less expensive than rework from skipping review steps
- More trustworthy results
- Better designs, plans, and implementations

## Related Concepts

Emanuel also discovered that combining **MCP Agent Mail** with **Beads** creates an ad-hoc "agent village" where agents naturally collaborate, divide up work, and farm it out.

## Key Resources

### GitHub Repositories

| Repository | Stars | Description |
|------------|-------|-------------|
| [agentic_coding_flywheel_setup](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup) | 662 | Transforms a fresh VPS into a fully-armed agentic coding environment |
| [beads_viewer](https://github.com/Dicklesworthstone/beads_viewer) | 858 | View beads (task management for coding agents) |
| [claude_code_agent_farm](https://github.com/Dicklesworthstone/claude_code_agent_farm) | 619 | Multi-agent Claude Code orchestration |
| [cass_memory_system](https://github.com/Dicklesworthstone/cass_memory_system) | 151 | Persistent agent memory framework |

### Articles

- [Six New Tips for Better Coding With Agents](https://steve-yegge.medium.com/six-new-tips-for-better-coding-with-agents-d4e9c86e42a9) - Steve Yegge, Dec 2025
- [Jeffrey Emanuel's Projects](https://jeffreyemanuel.com/projects) - Personal portfolio

## Recommendations

1. **Start with 2-3 review passes** on small tasks to build intuition
2. **Use 4-5 passes** for anything complex or high-stakes
3. **Vary review focus** - mix detailed code reviews with high-level architecture reviews
4. **Don't skip reviews** - the cost of rework likely exceeds the cost of reviews
5. **Trust output only after convergence** - when the agent says it can't improve further
