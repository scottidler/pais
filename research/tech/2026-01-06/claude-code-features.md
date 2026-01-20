# Claude Code Features: How I Use Every Feature

**Source:** https://blog.sshh.io/p/how-i-use-every-claude-code-feature
**Author:** Shrivu Shankar
**Date Researched:** 2026-01-06

---

## SUMMARY

Shrivu Shankar shares pragmatic strategies for maximizing Claude Code productivity across hobby and professional contexts, emphasizing minimal configuration and agent autonomy.

---

## IDEAS

- Start your CLAUDE.md file small and document only what Claude consistently gets wrong in practice.
- Avoid embedding entire documentation files; instead pitch the agent on when to reference external docs.
- Provide alternatives rather than prohibitive constraints so the agent has viable paths to follow always.
- Simple well-designed CLIs reduce documentation burden and serve as a forcing function for clean design.
- Professional monorepo CLAUDE.md reaches 13KB with strict curation for tools used by thirty percent engineers.
- Use `/clear` plus `/catchup` as default workflow to reset state then read changed files.
- For complex tasks use Document and Clear pattern where agent dumps progress to markdown first.
- Avoid `/compact` command because automatic compaction is opaque error-prone and not well optimized overall.
- Baseline context usage in large monorepos consumes approximately twenty thousand tokens before development begins.
- Maintain minimal custom slash commands to avoid forcing engineers to learn magic command lists.
- Excessive slash command proliferation creates friction and fails the goal of seamless development workflows.
- Master-Clone architecture places all context in CLAUDE.md letting main agent spawn autonomous task clones.
- Preserve holistic reasoning while managing token efficiency through self-delegation rather than rigid subagents.
- Block-at-submit hooks validate state at commit time while avoiding mid-plan blocking that frustrates agents.
- Block-at-write hooks confuse or frustrate the agent by interrupting planning flow with deterministic validation.
- Built-in planning mode is essential for significant feature work in both hobby and professional projects.
- Custom planning tools aligned with internal design standards improve professional team development workflows significantly.
- Skills represent the formal productization of environment scripting replacing ad-hoc MCP configurations cleanly.
- Migrate stateless tools like Jira AWS and GitHub from MCP to simple CLIs for better maintenance.
- Reserve MCP for complex stateful environments like Playwright that genuinely benefit from persistent connections.
- Effective MCP design provides high-level gateway tools rather than mirroring low-level REST API endpoints.
- Claude Code SDK enables parallel bash scripting for large refactors across many files simultaneously.
- Build internal chat tools for non-technical users using the SDK to democratize agent capabilities.
- Use SDK for rapid agent prototyping before deployment to production systems and user-facing applications.
- GitHub Actions integration enables operationalized agent workflows triggered from Slack Jira or monitoring alerts.
- Session logs support meta-analysis for continuous improvement creating feedback loops for better CLAUDE.md files.
- Judge the tool by the final PR quality and not by how it gets there during development.
- HTTP proxy inspection extended timeouts and permission auditing improve enterprise Claude Code deployments significantly.

---

## INSIGHTS

- Minimal CLAUDE.md files that grow from failures outperform comprehensive upfront documentation that becomes stale.
- Agent autonomy through Master-Clone architecture beats rigid subagent gatekeeping for preserving holistic reasoning capabilities.
- Blocking validation at submit time maintains agent flow while blocking at write time causes confusion.
- Skills productize environment scripting cleanly while MCP should be reserved for genuinely stateful operations.
- Context management through clear-catchup patterns beats opaque automatic compaction for predictable agent behavior.
- High-level gateway MCP tools outperform REST API mirrors by matching how agents actually reason.
- Session log meta-analysis creates improvement feedback loops connecting bugs to better CLAUDE.md and CLIs.
- Success metrics should focus on merged PR quality not intermediate interaction styles with the agent.
- Simple CLIs reduce documentation burden while serving as forcing functions for cleaner system design.
- Custom slash commands fail when they force engineers to learn documented magic command lists.

---

## QUOTES

- "Your CLAUDE.md should start small, documenting based on what Claude is getting wrong." — Shrivu Shankar
- "The moment you force an engineer to learn a new, documented-somewhere list of essential magic commands just to get work done, you've failed." — Shrivu Shankar
- "Automatic compaction is opaque, error-prone, and not well-optimized." — Shrivu Shankar
- "Block-at-write hooks confuse or even frustrate the agent." — Shrivu Shankar
- "Skills represent the formal productization of environment scripting." — Shrivu Shankar
- "Judge the tool by the final PR and not how it gets there." — Shrivu Shankar
- "Bugs → Improved CLAUDE.md / CLIs → Better Agent." — Shrivu Shankar

---

## HABITS

- Start CLAUDE.md files minimal and grow them only based on observed failures during actual development.
- Use `/clear` plus `/catchup` as the default workflow pattern for resetting context between tasks.
- Document progress to markdown before clearing session state when working on complex multi-step tasks.
- Maintain only minimal custom slash commands to reduce cognitive load on engineering team members.
- Reserve MCP for stateful environments and migrate stateless integrations to simple CLI tools instead.
- Review session logs regularly to identify patterns for improving CLAUDE.md files and CLI tools.
- Focus evaluation on merged PR quality rather than intermediate interaction styles during development sessions.

---

## FACTS

- Professional monorepo CLAUDE.md files can reach 13KB when curated for widely-used engineering tools only.
- Baseline context in large monorepos consumes approximately 20k tokens (10%) before development work begins.
- Strict curation means documenting only tools used by thirty percent or more of engineers.
- GitHub Actions can trigger Claude Code workflows from Slack Jira or monitoring alert systems.
- Claude Code SDK supports three primary use cases: parallel scripting, internal chat, and rapid prototyping.

---

## REFERENCES

- Claude Code CLI and SDK
- CLAUDE.md configuration file format
- `/clear`, `/catchup`, `/compact`, `/pr` slash commands
- MCP (Model Context Protocol)
- Playwright for stateful browser automation
- GitHub Actions for CI/CD automation
- Jira, AWS, GitHub integrations
- settings.json configuration file

---

## ONE-SENTENCE TAKEAWAY

Start CLAUDE.md minimal, let agents self-delegate via Master-Clone, and judge success by merged PR quality.

---

## RECOMMENDATIONS

- Begin with a minimal CLAUDE.md and expand it only when you observe Claude making repeated mistakes.
- Use Master-Clone architecture over rigid subagents to preserve holistic reasoning while managing token limits.
- Implement block-at-submit hooks for validation and avoid block-at-write hooks that interrupt agent planning.
- Migrate stateless tool integrations from MCP to simple CLIs for better maintainability and clarity.
- Reserve MCP specifically for complex stateful environments like Playwright that need persistent connections.
- Design MCP tools as high-level gateways rather than mirrors of low-level REST API endpoints.
- Use `/clear` plus `/catchup` as your default workflow instead of relying on automatic compaction.
- Document agent progress to markdown before clearing session state during complex multi-step development tasks.
- Keep custom slash commands minimal to avoid forcing engineers to learn documented magic command lists.
- Review session logs regularly to create feedback loops improving CLAUDE.md files and supporting CLIs.
- Use Claude Code SDK for parallel bash scripting when refactoring across many files simultaneously.
- Build internal chat tools with SDK to give non-technical users access to agent capabilities.
- Leverage GitHub Actions integration to trigger agent workflows from Slack Jira or monitoring alerts.
- Focus success metrics on final merged PR quality rather than how the agent behaves during development.
- Configure HTTP proxy inspection and extended timeouts for better enterprise Claude Code deployments.
