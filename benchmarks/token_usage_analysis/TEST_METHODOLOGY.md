# Token Usage Comparison Test Methodology

## Overview
This document describes the method used to compare token usage across different models (Opus, Sonnet, Haiku) using Claude Code via CCM MCP.

## Test Environment
- **Execution Environment**: Claude Code with CCM MCP
- **Test Date**: 2025-06-21
- **Models Used**:
  - claude-opus-4-20250514
  - claude-3-5-sonnet
  - claude-3-5-haiku-20241022

## Test Procedure

### 1. Preparation
1. Create working directories
   ```bash
   mkdir -p opus_test sonnet_test haiku_test
   ```

2. Create common prompt file (`test_prompt.txt`)
   - Contains Fibonacci sequence implementation task
   - Includes requirements for memoization, error handling, and unit tests

### 2. Execution with Each Model

#### Opus Execution
```bash
mcp__ccm__claude_code(
  workFolder="/path/to/opus_test",
  model="opus",
  prompt_file="/path/to/test_prompt.txt"
)
```

#### Sonnet Execution
```bash
mcp__ccm__claude_code(
  workFolder="/path/to/sonnet_test",
  model="sonnet",
  prompt_file="/path/to/test_prompt.txt"
)
```

#### Haiku Execution
```bash
mcp__ccm__claude_code(
  workFolder="/path/to/haiku_test",
  model="claude-3-5-haiku-20241022",
  prompt_file="/path/to/test_prompt.txt"
)
```

### 3. Result Retrieval
Retrieve results using each process PID:
```bash
mcp__ccm__get_claude_result(pid=<process_id>)
```

### 4. Measured Items
- **Input tokens**
- **Cache creation tokens**
- **Cache read tokens**
- **Output tokens**
- **Total cost (USD)**
- **Execution time**
- **Number of turns**

## Important Notes

### Avoiding File Name Conflicts
Using separate working directories for each model prevents conflicts with generated files (`fibonacci.py`, `test_fibonacci.py`).

### Execution Timing
- Each model execution started in parallel
- Results retrieved after appropriate wait time (30-60 seconds)

### Token Count Differences
Confirmed that Haiku model's input token count is lower than other models (34 vs 76). This may be due to differences in internal tokenizer or system prompts.

## Checking Implementation Files

Implementation results for each model can be found at:
- `implementations/opus/fibonacci.py` - Opus implementation
- `implementations/sonnet/fibonacci.py` - Sonnet implementation
- `implementations/haiku/fibonacci.py` - Haiku implementation

Test code is similarly saved in each directory.

## Utilizing Results
- Model selection based on project budget
- Appropriate model selection based on task complexity
- Cost-performance optimization