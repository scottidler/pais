# Jeffrey Emanuel's Rule of Five for Agentic LLM

## SUMMARY

Jeffrey Emanuel's Rule of Five requires AI agents to review their work five times with varying focus areas until convergence, transforming untrusted first-draft outputs into production-quality artifacts.

---

## The Rule of Five - Core Principle

**"When in doubt, have the agent review its own work 5 times."**

Jeffrey Emanuel discovered this powerful and unintuitive rule through extensive experimentation with agentic coding workflows. He found that he gets the best designs, the best plans, and the best implementations by forcing agents to review their proposals (and then their work) 4-5 times, at which point it **converges**.

### Convergence Defined

After 4-5 iterations, the agent will say something like "I think this is about as good as we can make it." This convergence point is critical:

> "At that point it has converged. And that, folks, is the first point at which you can begin to moderately trust the output the agent has produced. If you always take the first thing it generates, with no review at all, you're bound to be disappointed."
> — Steve Yegge

---

## The Five Passes Documented

| Pass | Type | Description |
|------|------|-------------|
| **Pass 1** | Generation | Initial task completion - the agent produces the first output |
| **Pass 2** | 1st Code Review | Standard review finding "all the usual stuff" - bugs, issues, improvements |
| **Pass 3** | 2nd Code Review | Deeper review - "even on the second review it will often find things it missed in the first review" |
| **Pass 4** | 3rd Code Review | Broader/existential review - "where you start asking it existential questions about whether you're doing the Right Thing throughout the project" |
| **Pass 5** | 4th Code Review | Final convergence pass - agent confirms "this is about as good as we can make it" |

### Critical Insight on Pass 4 (3rd Review)

> "It definitely feels weird to ask for the 3rd code review, which is the agent's 4th pass over the code, counting the generation step. But the 3rd review, especially during the Design phase, is where you start asking it existential questions about whether you're doing the Right Thing throughout the project."
> — Steve Yegge describing Jeffrey Emanuel's methodology

---

## Review Focus Areas

Each review should vary in scope. You need a **mixture** of:

### In-the-Small Reviews
- Looking for bad code at the implementation level
- Bugs, errors, silly mistakes
- Security issues, inefficiencies
- Conformance to coding standards

### In-the-Large Reviews
- Looking for bad architecture and design decisions
- Questioning whether you're solving the right problem
- Evaluating overall approach and structure
- "Existential questions" about project direction

### Varying Scope Pattern

> "Each review should be slightly broader and more outlandish than the previous one, or you can do it the opposite order. But you need a mixture of in-the-small and in-the-large reviews. You're having it look for bad code (or designs), but also bad architecture."
> — Jeffrey Emanuel (via Steve Yegge)

---

## Guidelines for Application

### Task Size Rules
| Task Size | Minimum Passes |
|-----------|----------------|
| Small tasks | 2-3 passes |
| Big tasks | 4-5 passes |
| Unfamiliar territory | Err toward more passes |

### Where to Apply
The Rule of Five applies at **every step** in the process:
- **5 passes over the implementation plan** → results in far better issues and dependencies
- **5 passes over the implementation** → code + 4 reviews

### When Unfamiliar
> "If you're not super familiar with the language, the stack, or the domain, then you should err on the side of more reviews."

---

## Jeffrey Emanuel's Actual Prompts

Based on his public posts, here are the specific prompts Jeffrey Emanuel uses:

### Prompt 1: Exploration & Fresh Eyes Review

> "I want you to sort of randomly explore the code files in this project, choosing code files to deeply investigate and understand and trace their functionality and execution flows through the related code files which they import or which they are imported by. Once you understand the purpose of the code in the larger context of the workflows, I want you to do a super careful, methodical, and critical check with 'fresh eyes' to find any obvious bugs, problems, errors, issues, silly mistakes, etc. and then systematically and meticulously and intelligently correct them."

### Prompt 2: Self-Review After Changes

> "Great, now I want you to carefully read over all of the new code you just wrote and other existing code you just modified with 'fresh eyes' looking super carefully for any obvious bugs, errors, problems, issues, confusion, etc. Carefully fix anything you uncover. Use ultrathink."

### Prompt 3: Weakest Parts Assessment (In-the-Large)

> "Based on everything you've seen, what are the weakest/worst parts of the system? What is most needing of fresh ideas and innovative/creative/clever improvements?"

**Follow-up:**
> "OK, so now I need you to do exactly that! For each of those items, put on your thinking cap and come up with the very best, most creative, most clever, most sophisticated, yet pragmatic and workable ideas for how to improve, fix, and resolve the issues and problems!"

### Prompt 4: Peer Agent Review (Deep Analysis)

> "Ok can you now turn your attention to reviewing the code written by your fellow agents and checking for any issues, bugs, errors, problems, inefficiencies, security problems, reliability issues, etc. and carefully diagnose their underlying root causes using first-principle analysis and then fix or revise them if necessary? Don't restrict yourself to the latest commits, cast a wider net and go super deep! Use ultrathink."

### Prompt 5: Fix All Issues

> "OK, now fix ALL of them completely and correctly with extreme diligence and care!"

---

## Why the Rule of Five Works

### Claude's Own Explanation

> "Claude claims that this process matches their own cognition model, which is breadth-first: they solve each problem first in very broad strokes. And then they almost always need more passes for proofreading, refining, and polishing — much like humans do."
> — Steve Yegge

### The Human Parallel

Just as human writers need multiple drafts and editors need multiple passes, LLMs benefit from iterative refinement. The first output is a rough draft; convergence requires iteration.

---

## Automation: Ralph Loops as Evolution

Steve Yegge notes that Geoffrey Huntley's **Ralph loops** are "a brilliant automation of the discovery that LLMs can self-review to convergence" — which Jeffrey Emanuel was "also onto with his (weaker, manual) Rule of Five."

Ralph loops automate the iterative review process:
- Keep feeding an AI agent a task until the job is done
- "The criteria in the plan is deterministic, but evaluation is non-deterministic but converges through iteration"
- Backpressure rejects hallucinations without excessive slowdown

The Rule of Five is the manual methodology; Ralph loops are the automated implementation of the same insight.

---

## Practical Implementation Pattern

### For Design Phase
1. Generate initial design
2. First review: standard design review
3. Second review: deeper analysis, missed issues
4. Third review: **existential questions** - "Are we doing the Right Thing?"
5. Fourth review: convergence check - is it as good as it can be?

### For Implementation Phase
1. Generate initial code
2. First review: bugs, errors, style issues
3. Second review: deeper issues, things missed
4. Third review: architecture concerns, broader problems
5. Fourth review: convergence - "fresh eyes" final check

### For Plans/Specifications
1. Generate initial plan
2. Review for completeness
3. Review for dependencies and ordering
4. Review for feasibility and approach
5. Review for convergence

---

## Key Quotes

> "When in doubt, have the agent review its own work 5 times." — Jeffrey Emanuel

> "Jeffrey described a long, complex series of prompts for this process." — Steve Yegge

> "Even on the second review it will often find things it missed in the first review. But most people stop there, if they even ask at all." — Steve Yegge

> "The 3rd review, especially during the Design phase, is where you start asking it existential questions about whether you're doing the Right Thing." — Steve Yegge

> "With these canned prompts, you can easily keep 10+ agents busy and doing useful stuff for you all day." — Jeffrey Emanuel

---

## ONE-SENTENCE TAKEAWAY

Force AI agents to review their work five times with mixed micro and macro focus until convergence for trustworthy output.

---

## Sources

- [Six New Tips for Better Coding With Agents - Steve Yegge (Dec 2025)](https://steve-yegge.medium.com/six-new-tips-for-better-coding-with-agents-d4e9c86e42a9)
- [Jeffrey Emanuel's Canned Prompts - X/Twitter](https://x.com/doodlestein/status/1968402900394328284)
- [Agent Swarm Workflow - Jeffrey Emanuel](https://agent-skills.md/skills/Dicklesworthstone/agent_flywheel_clawdbot_skills_and_integrations/agent-swarm-workflow)
- [Jeffrey Emanuel's Website](https://jeffreyemanuel.com)
- [Jeffrey's Prompts](https://jeffreysprompts.com/)
- [Everything is a Ralph Loop - Geoffrey Huntley](https://ghuntley.com/loop/)
