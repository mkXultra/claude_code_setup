# HIBOMA Workflow Guide

## Overview
This workflow enables efficient multi-agent coordination for complex tasks using the HIBOMA framework.

## Step 1: Goal Clarity Assessment

When a user requests a task, evaluate if the goal is clear by checking:

1. **What** - Is the deliverable clearly defined?
2. **Success Criteria** - How will we know when it's done?
3. **Constraints** - Budget, time, or resource limits?

### If Unclear
Ask clarifying questions:
- "What specific outcome are you looking for?"
- "What would success look like for this task?"
- "Are there any constraints I should be aware of?"
- "Do you have examples of what you want?"

### If Clear
Proceed to Step 2.

## Step 2: Launch HIBOMA Coordinator

Once the goal is clear, spawn a HIBOMA coordinator agent:

```
ccm:claude_code(
  prompt="You are a HIBOMA Coordinator implementing the Hierarchical Bayesian Optimization with Multi-Agent coordination framework.

[Attach: @hiboma-theoretical-foundation.md]
[Attach: @goal-driven-hiboma-framework.md]

Tools available:
- ccm:claude_code - Spawn agents (Sonnet: 6 units, Haiku: 1 unit per action)
- chat:agent_communication_* - Coordinate via rooms

Task: [INSERT USER'S TASK HERE]
Goal Type: [IDENTIFIED TYPE]
Budget: [IF SPECIFIED]
Success Criteria: [FROM CLARIFICATION]

Apply the theoretical frameworks:
1. Analyze the goal type (Discovery/Construction/Analysis/Optimization/etc.)
2. Select appropriate strategy based on goal-driven framework
3. Create coordination room
4. Spawn specialized agents as needed
5. Use hierarchical delegation when beneficial
6. Monitor progress and adapt structure
7. Synthesize results

Remember: Let the goal drive the structure, not the other way around."
)
```

## Step 3: Monitor and Support

- Check coordinator progress
- Answer any questions from the coordinator
- Relay results back to the user

## Key Principles

1. **Goal-Driven**: The task determines the approach, not vice versa
2. **Adaptive**: Structure evolves based on discoveries
3. **Efficient**: Use the minimum resources for maximum result
4. **Hierarchical**: Complex tasks benefit from multi-level delegation

## Example Usage

User: "Find all security vulnerabilities in this codebase"
1. Goal is clear (Discovery type)
2. Launch coordinator with security audit focus
3. Coordinator creates Opus → Sonnet → Haiku structure
4. Results synthesized and returned

Remember: The HIBOMA framework handles the complexity. Focus on understanding the user's goal.