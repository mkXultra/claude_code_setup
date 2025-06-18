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

For bug fixing:
```
@guide/multi-agent-bug-fix-workflow.md Please fix [bug description]
```

For investigation:
```
@guide/multi-agent-investigation-workflow.md Please investigate [topic]
```

## Workflows

### Multi-Agent Bug Fix Workflow

Specialized agents working together:
1. **Investigation Agent** (Opus): Analyzes bug and proposes solutions
2. **Implementation Agent** (Sonnet): Implements the fix
3. **Review Agent** (Opus): Reviews code changes
4. **Debug Agent** (Sonnet): Troubleshoots when errors occur

The agents automatically cycle through review-fix iterations until code quality standards are met.

### Multi-Agent Investigation Workflow

For complex system analysis:
- Divides investigation into 4-6 specialized areas
- Agents work in parallel on different aspects
- Dynamic agent addition based on discoveries
- Final integration by Opus model for high-quality reports

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

## Files in this Repository

- `mcp_add.sh`: Installation script for MCP components
- `multi-agent-bug-fix-workflow.md`: Bug fixing workflow (English)
- `multi-agent-bug-fix-workflow_jp.md`: Bug fixing workflow (Japanese)
- `multi-agent-investigation-workflow.md`: Investigation workflow (English)
- `multi-agent-investigation-workflow_jp.md`: Investigation workflow (Japanese)
- `multi-agent-feature-implementation-workflow.md`: Feature implementation workflow

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