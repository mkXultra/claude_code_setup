# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Multi-Agent AI Orchestration Framework that enables multiple Claude Code instances to collaborate on complex software development tasks. The framework uses MCP (Model Context Protocol) for inter-agent communication and implements sophisticated workflows for bug fixing, investigation, and feature implementation.

## Recent Enhancements (v2 Workflows)

### Chat MCP Integration
- **Real-time Coordination**: Agents communicate through chat rooms instead of fixed wait times
- **Event-driven Execution**: Workflows respond to chat messages ([COMPLETED], [HANDOFF], etc.)
- **Performance Gains**: 30-60% time reduction compared to traditional workflows

### Enhanced Workflows Now Available
1. **`multi-agent-bug-fix-workflow-v2.md`**: Bug fixing with chat coordination
2. **`multi-agent-feature-implementation-workflow-v2.md`**: TDD with real-time Red-Green-Refactor cycles

### Bilingual Support
All documentation now available in English and Japanese (files with `_jp` suffix)

## Key Commands

### Installation and Setup
```bash
# Install MCP components (from project directory after linking this repo)
./guide/mcp_add.sh

# Install MCP components globally
./guide/mcp_add_global.sh  

# Install Claude commands (creates symlinks in ~/.claude/commands)
./guide/install_claude_commands.sh

# Verify MCP installation
/mcp  # Should show chat, ccm, and playwright
```

### Testing
```bash
# Run benchmark tests
cd benchmarks/token_usage_analysis
python test_fibonacci.py
```

## Architecture

### Core Components

1. **MCP Integration**
   - `chat`: Agent communication via `agent-communication-mcp`
   - `ccm`: Claude Code Manager via `@mkxultra/claude-code-mcp`
   - Communication happens through a shared chat room

2. **Agent Types**
   - **Investigation Agent** (Opus): Analyzes problems and proposes solutions
   - **Implementation Agent** (Sonnet): Executes code changes
   - **Review Agent** (Opus): Performs code review
   - **Debug Agent** (Sonnet): Troubleshoots failures
   - **Specialist Agents**: Dynamic spawning for specific expertise areas

3. **Workflow Patterns**
   - **Bug Fix**: Investigation → Implementation → Review → Fix cycles
   - **Bug Fix v2 (Chat)**: Real-time coordination, dynamic debugging, 30-50% faster
   - **Investigation**: Parallel multi-agent analysis → Integration
   - **Feature Implementation (TDD)**: Design → Red → Green → Refactor cycles
   - **Feature Implementation v2 (Chat)**: Event-driven TDD, 40-60% faster
   - **Refactoring**: Analysis → Change → Verification cycles
   - **Article Creation**: Multi-phase content generation with chat tracking

### Key Directories
- `/`: Workflow markdown files and documentation
- `/benchmarks/`: Performance testing and token usage analysis
  - `token_usage_analysis/`: Model comparison results and methodology
- `/commands/`: Claude Code custom commands
  - `co-sleep.md`: Intelligent wait strategies
  - `create-commit-msg-staged.md`: Commit message generation

## Working with Workflows

### Workflow Categories

#### Chat-Enhanced Workflows (Recommended)
These workflows use real-time chat coordination for improved efficiency:
- `multi-agent-bug-fix-workflow-v2.md` - Bug fixing with 30-50% time reduction
- `multi-agent-feature-implementation-workflow-v2.md` - TDD implementation with event-driven cycles
- `multi-agent-investigation-workflow.md` - Parallel investigation with chat updates
- `article-creation-workflow-v5-mcp.md` - Article creation with progress tracking
- `lightweight-3-agent-refactoring-workflow.md` - Efficient refactoring
- `hiboma-workflow-guide.md` - Hierarchical coordination framework
- `refactoring-workflow-v5-template.md` - Template-based refactoring

#### Traditional Workflows (File-based)
These use file-based coordination with fixed wait times:
- `multi-agent-bug-fix-workflow.md` - Original bug fix workflow
- `multi-agent-feature-implementation-workflow.md` - Original TDD workflow

### Executing Workflows
Always reference workflows using the `@guide/` prefix:
```
# Recommended: Chat-enhanced workflows
@guide/multi-agent-bug-fix-workflow-v2.md Fix the authentication bug
@guide/multi-agent-feature-implementation-workflow-v2.md Implement user profile feature

# Traditional workflows
@guide/multi-agent-bug-fix-workflow.md Fix the authentication bug
@guide/multi-agent-investigation-workflow.md Investigate the permission system
```

### Workflow Deliverables
Workflows produce standardized deliverables:
- `bug-investigation-report.md`
- `code-review-report.md`
- `implementation-plan.md`
- `test-specification.md` (TDD workflows)
- Various specialist reports

### Chat Message Patterns
For chat-enabled workflows, use these standard formats:
```
[STARTED] Workflow initiated
[PROGRESS] Working on [task]
[COMPLETED] [Phase] complete, deliverable at [location]
[ISSUE] [Problem description]
[HANDOFF] Ready for [next agent]
[REQUEST] Need [assistance type]
[TDD-CYCLE] Starting cycle N: [description]
[RED] Tests failing as expected
[GREEN] Tests passing
[REFACTOR] Code improved, tests still passing
```

### Cost Optimization

#### Foundation Session Strategy
The framework uses "foundation sessions" for 85%+ token cost reduction:
- First agent loads full context (expensive)
- Subsequent agents reuse cached context (cheap)
- Always spawn agents from the coordinator session

#### Model Selection for Cost Efficiency
Based on benchmark analysis (`benchmarks/token_usage_analysis/`):
- **Haiku**: $0.029 per task - fastest (27s), best for simple tasks
- **Sonnet**: $0.179 per task - balanced, most detailed output
- **Opus**: $0.582 per task - highest quality, complex analysis

#### Time Savings with Chat Coordination
- Bug Fix v2: 30-50% reduction vs traditional
- Feature Implementation v2: 40-60% reduction
- Investigation: Up to 70% reduction with parallel agents

## Important Practices

### Agent Communication

#### Chat MCP Integration (for v2 workflows)
- Agents join chat rooms with standardized names: `bugfix-[timestamp]`, `tdd-feature-[timestamp]`
- Use natural language for chat instructions (see `chat-mcp-prompt-guide.md`)
- Standard message formats:
  ```
  [PROGRESS] Status update
  [COMPLETED] Task finished + location
  [ISSUE] Problem description
  [HANDOFF] Ready for next agent
  [REQUEST] Need assistance
  [RED/GREEN/REFACTOR] TDD cycle status
  ```
- Monitor chat every 15-30 seconds for real-time coordination
- No fixed wait times - purely event-driven

#### Traditional Communication
- Use `mcp__chat__post_message` for inter-agent communication
- Check chat history with `mcp__chat__list_messages`
- Wait for agent completion before proceeding

### Agent Management
- Spawn agents with appropriate models (Opus for analysis, Sonnet for implementation)
- Use `--prompt-caching` flag for cost efficiency
- Include `--resume $USER_DIR` for workspace consistency
- Monitor agent status with `mcp__ccm__get_all_instance_statuses`

### Error Handling
- Always check MCP availability before starting workflows
- Verify agent spawning success
- Use Debug Agent when errors occur
- Clean up deliverables before re-running workflows

### Language Support

#### Bilingual Documentation
Most documentation is available in both English and Japanese:
- Workflows: Add `_jp` suffix for Japanese versions
- Guides: `chat-mcp-prompt-guide.md` / `chat-mcp-prompt-guide_jp.md`
- Commands and benchmarks also have bilingual versions

#### Available Japanese Workflows
- `multi-agent-bug-fix-workflow_jp.md`
- `multi-agent-investigation-workflow_jp.md`
- `multi-agent-feature-implementation-workflow_jp.md`

## Critical Notes

1. **Never modify MCP configuration** - Use provided installation scripts
2. **Always use absolute paths** when working with files across agents
3. **Check existing deliverables** before starting workflows to avoid conflicts
4. **Prefer chat-enhanced workflows** - 30-60% time savings, better coordination
5. **Model selection matters** - Opus for quality, Sonnet for efficiency, Haiku for speed/cost
6. **Use coordinator wait strategies** - See `coordinator-wait-strategies.md` for optimal patterns
7. **Monitor chat for real-time coordination** - Event-driven is superior to polling