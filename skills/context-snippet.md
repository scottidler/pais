## Available Skills

| Skill | Description | Triggers |
|-------|-------------|----------|
| **aka** | High-performance shell alias manager. Use when managing s... | alia, aliase, expansion, managing, optimizing, querying, shell, startup |
| **cidr** | CIDR calculator for network calculations. Use when workin... | addresse, network, range, subnet, working |
| **clone** | Smart git clone with org-specific SSH keys, versioning, a... | git |
| **core** | Core operating principles and preferences. Always loaded ... | - |
| **dashify** | Normalize filenames by lowercasing and replacing spaces/u... | cleaning, file, name |
| **ls-git-repos** | Recursively find all local git repositories. Use to disco... | git |
| **ls-github-repos** | List all repositories under a GitHub organization or user... | - |
| **ls-owners** | Analyze CODEOWNERS files and detect unowned code paths. U... | - |
| **ls-stale-branches** | Find remote branches that haven't been updated in N days.... | - |
| **ls-stale-prs** | Find open PRs that haven't been updated in N days. Use fo... | - |
| **otto** | Otto task runner for builds and CI. Use when running test... | build, make, mention, otto, pipeline, runner, running, task, test |
| **python-coder** | Write Python code using Scott's conventions. Use when cre... | code, creating, package, project, python, reviewing, script |
| **reposlug** | Extract owner/repo slug from a git remote. Use for script... | git |
| **rkvr** | Safe file deletion with archiving and recovery. Use rmrf ... | - |
| **rust-coder** | Write Rust code using Scott's conventions. USE WHEN creat... | cargo, cli, code, creating, librarie, mention, reviewing, rust, tool |
| **whitespace** | Remove trailing whitespace from files. Use as a linting s... | - |

## Workflow Routing

Some skills have specific workflows for common tasks:

### rust-coder

| Intent | Workflow |
|--------|----------|
| new CLI project | `workflows/new-cli.md` |
| create new CLI | `workflows/new-cli.md` |
| scaffold CLI | `workflows/new-cli.md` |

When a request matches a workflow intent:
1. Read the workflow file from `/home/saidler/.config/pais/skills/[skill-name]/[workflow-path]`
2. Follow the step-by-step instructions in the workflow

## Routing Instructions

When a user request matches a skill's triggers:
1. Read the full SKILL.md file from `/home/saidler/.config/pais/skills/[skill-name]/SKILL.md`
2. Follow the skill's instructions and conventions
3. No need to ask for permission - the skill is pre-approved