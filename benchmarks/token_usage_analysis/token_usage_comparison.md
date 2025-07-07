# Claude Code Model Token Usage Comparison Results

## Experiment Overview
We executed Claude Code with the same prompt using three models (Opus, Sonnet, and Haiku) to compare token usage and costs.

### Prompt Used
```
You are an excellent programmer. Please perform the following tasks:

1. Implement a simple Fibonacci sequence calculation function in Python
2. Write unit tests for that function
3. Explain the efficiency of the implementation

The implementation should meet the following requirements:
- Function name should be `fibonacci`
- Return the nth Fibonacci number (0th is 0, 1st is 1)
- Raise ValueError for negative input
- Use memoization for efficient implementation
```

## Experiment Results

### Token Usage Comparison

| Model | Input Tokens | Cache Creation | Cache Read | Output Tokens | Total Cost |
|-------|--------------|----------------|------------|---------------|------------|
| **Opus** | 76 | 6,491 | 181,898 | 2,445 | **$0.582** |
| **Sonnet** | 76 | 19,605 | 176,531 | 3,328 | **$0.179** |
| **Haiku** | 34 | 17,269 | 81,647 | 1,354 | **$0.029** |

### Performance Comparison

| Model | Execution Time | Result | Number of Turns |
|-------|----------------|--------|-----------------|
| **Opus** | 76 seconds | Success | 26 |
| **Sonnet** | 86 seconds | Success | 24 |
| **Haiku** | 27 seconds | Success | 16 |

## Analysis Results

### 1. Cost Efficiency
- **Cheapest**: Haiku ($0.029)
- **Middle**: Sonnet ($0.179) - About 6x Haiku
- **Most Expensive**: Opus ($0.582) - About 20x Haiku

### 2. Processing Speed
- **Fastest**: Haiku (27 seconds)
- **Middle**: Opus (76 seconds)
- **Slowest**: Sonnet (86 seconds)

### 3. Output Detail Level
- **Sonnet**: 3,328 tokens (most detailed)
- **Opus**: 2,445 tokens
- **Haiku**: 1,354 tokens (most compact)

### 4. Number of Turns (Interactions)
- **Opus**: 26 turns (most)
- **Sonnet**: 24 turns
- **Haiku**: 16 turns (least)

### 5. Notable Points
- Haiku's input token count is lower than the other two models (34 vs 76)
  - Possible differences in tokenizer or system prompts between models
- All models successfully completed the task
- Opus used the most turns, taking a more careful approach

## Conclusion

### Model Selection Guidelines

1. **Cost-focused**: Haiku
   - Most affordable ($0.029)
   - Fastest (27 seconds)
   - Optimal for simple tasks

2. **Balance of Quality and Cost**: Sonnet
   - Moderate cost ($0.179)
   - Most detailed output
   - Recommended for production use

3. **Highest Quality / Complex Tasks**: Opus
   - Most expensive ($0.582)
   - Most turns for careful implementation
   - Recommended for complex system design or research

### CCM MCP Advantages
- Detailed cost information available via `get_claude_result`
- Enables appropriate model selection based on project budget
- Allows comparison of different model characteristics with the same prompt