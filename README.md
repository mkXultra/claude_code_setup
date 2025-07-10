# Claude Code Multi-Agent Collaboration Setup

This repository contains workflows and scripts for enabling multiple AI agents to work together collaboratively using Claude Code's MCP (Model Context Protocol) feature.

## Overview

With this setup, you can orchestrate multiple Claude Code instances that:
- Work on different aspects of a task in parallel
- Share discoveries through a chat room
- Review each other's work
- Automatically iterate until quality standards are met

## Key Features

- **Multi-Agent Bug Fix Workflow**: Automated investigation → implementation → review → fix cycles
- **Multi-Agent Investigation Workflow**: Parallel investigation of complex systems with specialized agents
- **Cost Optimization**: 85%+ token cost reduction through prompt caching
- **Quality Assurance**: Automated code review with iterative improvements

## Quick Start

### 1. Clone this repository
```bash
git clone https://github.com/mkXultra/claude_code_setup
cd claude_code_setup
```

### 2. Link to your project
In your working project directory:
```bash
ln -s /path/to/claude_code_setup guide
```

### 3. Install MCP components
From your project root:
```bash
./guide/mcp_add.sh
```

This installs:
- **Chat MCP**: For agent communication
- **CCM (Claude Code Manager)**: For spawning and managing multiple Claude instances
- **Playwright MCP**: For browser automation (optional)

### 4. Verify installation
In Claude Code:
```
/mcp
```
You should see `chat`, `ccm`, and `playwright` listed.

### 5. Use a workflow

**For workflows with Chat MCP (recommended for better performance):**
```
# Bug fixing with real-time coordination
@guide/multi-agent-bug-fix-workflow-v2.md Please fix [bug description]

# Advanced bug fixing with confidence scoring (highest accuracy)
@guide/multi-agent-bug-fix-workflow-v3.md Please fix [bug description]

# Feature implementation with TDD and chat
@guide/multi-agent-feature-implementation-workflow-v2.md Please implement [feature]

# Investigation with parallel agents
@guide/multi-agent-investigation-workflow.md Please investigate [topic]
```

**For traditional workflows (file-based coordination):**
```
# Original bug fix workflow
@guide/multi-agent-bug-fix-workflow.md Please fix [bug description]

# Original TDD feature implementation
@guide/multi-agent-feature-implementation-workflow.md Please implement [feature]
```

## Available Workflows

### Workflows with Chat MCP (Real-time Coordination)

These workflows use chat rooms for agent communication, providing real-time coordination and reduced wait times:

#### 1. Multi-Agent Investigation Workflow
- **Files**: `multi-agent-investigation-workflow.md` (English), `multi-agent-investigation-workflow_jp.md` (Japanese)
- **Features**: Parallel investigation with 4-6 specialized agents, real-time progress updates
- **Chat**: Agents report findings and coordinate through shared chat room

#### 2. Multi-Agent Bug Fix Workflow v2
- **File**: `multi-agent-bug-fix-workflow-v2.md` (English)
- **Features**: Enhanced version with chat-based coordination
- **Benefits**: 30-50% time reduction, dynamic issue resolution, real-time progress

#### 3. Multi-Agent Bug Fix Workflow v3 (Advanced)
- **File**: `multi-agent-bug-fix-workflow-v3.md` (English)
- **Features**: Replication-first approach with confidence scoring
- **Benefits**: Bug verification, user approval checkpoints, pattern learning, 80%+ fix success rate
- **Key Innovation**: Replicates bug before fixing, shows confidence levels, learns from history

#### 4. Multi-Agent Feature Implementation Workflow v2 (TDD)
- **File**: `multi-agent-feature-implementation-workflow-v2.md` (English)
- **Features**: TDD cycles coordinated through chat
- **Benefits**: 40-60% time reduction, event-driven Red-Green-Refactor cycles

#### 5. Article Creation Workflow v5 MCP
- **File**: `article-creation-workflow-v5-mcp.md`
- **Features**: Multi-phase article creation with chat coordination

#### 6. Lightweight 3-Agent Refactoring Workflow
- **File**: `lightweight-3-agent-refactoring-workflow.md`
- **Features**: Efficient refactoring with progress visualization

#### 7. HIBOMA Workflow Guide
- **File**: `hiboma-workflow-guide.md`
- **Features**: Hierarchical coordination with Luna-Raven dialogue

#### 8. Refactoring Workflow v5 Template
- **File**: `refactoring-workflow-v5-template.md`
- **Features**: Standardized refactoring with specialized chat rooms

### Workflows without Chat MCP (File-based Coordination)

These workflows use traditional file-based coordination and fixed wait times:

#### 1. Multi-Agent Bug Fix Workflow (Original)
- **Files**: `multi-agent-bug-fix-workflow.md` (English), `multi-agent-bug-fix-workflow_jp.md` (Japanese)
- **Features**: Investigation → Implementation → Review → Debug cycle
- **Coordination**: Through deliverable files and session management

#### 2. Multi-Agent Feature Implementation Workflow (TDD Original)
- **Files**: `multi-agent-feature-implementation-workflow.md` (English), `multi-agent-feature-implementation-workflow_jp.md` (Japanese)
- **Features**: Test-Driven Development with Red-Green-Refactor cycles
- **Coordination**: Through test files and implementation handoffs

## Example Results

### Bug Fix Example
- **Task**: Fix file locking directory creation bug
- **Time**: 15 minutes (vs hours manually)
- **Cost**: 85% reduction through caching
- **Quality**: Automated review caught edge cases

### Investigation Example
- **Task**: Permission system analysis
- **Time**: 20 minutes with 7 agents
- **Deliverables**: 5 comprehensive reports totaling 45KB
- **Coverage**: Complete system understanding

## Cost Optimization

The workflows use a "foundation session" strategy:
```json
{
  "cache_read_input_tokens": 390302,  // Reused tokens (cheap!)
  "input_tokens": 56                  // New tokens (expensive)
}
```
Result: 90%+ token cost savings

## Key Files in this Repository

### Installation & Setup
- `mcp_add.sh`: Installation script for MCP components
- `mcp_add_global.sh`: Global installation script
- `install_claude_commands.sh`: Claude commands setup

### Workflows with Chat MCP
- `multi-agent-bug-fix-workflow-v2.md`: Enhanced bug fixing with chat (English)
- `multi-agent-bug-fix-workflow-v3.md`: Advanced bug fixing with replication & confidence (English)
- `multi-agent-feature-implementation-workflow-v2.md`: Enhanced TDD implementation with chat (English)
- `multi-agent-investigation-workflow.md`: Investigation workflow with chat (English)
- `multi-agent-investigation-workflow_jp.md`: Investigation workflow with chat (Japanese)
- `article-creation-workflow-v5-mcp.md`: Article creation with chat
- `lightweight-3-agent-refactoring-workflow.md`: Lightweight refactoring with chat
- `hiboma-workflow-guide.md`: HIBOMA framework with chat
- `refactoring-workflow-v5-template.md`: Refactoring template with chat

### Workflows without Chat MCP
- `multi-agent-bug-fix-workflow.md`: Original bug fixing workflow (English)
- `multi-agent-bug-fix-workflow_jp.md`: Original bug fixing workflow (Japanese)
- `multi-agent-feature-implementation-workflow.md`: Original TDD workflow (English)
- `multi-agent-feature-implementation-workflow_jp.md`: Original TDD workflow (Japanese)

### Documentation & Guides
- `CLAUDE.md`: Claude Code guidance for this repository
- `chat-mcp-prompt-guide.md`: How to use Chat MCP effectively (English)
- `chat-mcp-prompt-guide_jp.md`: How to use Chat MCP effectively (Japanese)
- `claude-model-selector.md`: Model selection guidance
- `workflow-log-spec.md`: Logging specifications
- `coordinator-wait-strategies.md`: Coordination strategies

## Requirements

- Claude Code with MCP support
- Node.js (for npx commands)
- Active Claude API access

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your License Here]

## Acknowledgments

Built using:
- [Claude Code MCP](https://www.npmjs.com/package/@mkxultra/claude-code-mcp)
- [Agent Communication MCP](https://www.npmjs.com/package/agent-communication-mcp)
- [Playwright MCP](https://www.npmjs.com/package/@playwright/mcp)