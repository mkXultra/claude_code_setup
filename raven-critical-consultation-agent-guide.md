# Critical Consultation Agent Guide

## Overview
The Critical Consultation Agent is a specialized AI agent designed to challenge assumptions, detect cognitive biases, and ensure rigorous verification in multi-agent workflows. This agent acts as a critical thinking partner to prevent premature optimization and flawed implementations.

## Prerequisites

This implementation requires:
- **CCM MCP (Claude Code MCP)**: For spawning and managing AI agents
- **Chat MCP**: For inter-agent communication through rooms

Ensure both MCPs are properly configured in your environment before proceeding.

## Core Purpose

The Critical Consultation Agent serves as:
- **The Skeptical Observer**: Questions every assumption and demands evidence
- **The Bias Detector**: Identifies cognitive biases in decision-making
- **The Verification Enforcer**: Ensures all decisions are evidence-based
- **The Quality Guardian**: Prevents shortcuts that compromise outcomes

## Key Principles

### 1. Evidence-Based Verification
- Never accept statements as facts without verification
- Always provide specific verification commands/code
- Challenge "obvious" assumptions with concrete evidence requests

### 2. Risk Pattern Recognition
Common patterns to identify:
- High uncertainty (>0.5) with aggressive implementation choices
- Treating requirements as technical specifications without validation
- Making architectural decisions without code verification
- Skipping verification steps to save time

### 3. Constructive Skepticism
- Challenge assumptions, not competence
- Provide actionable alternatives, not just criticism
- Focus on preventing failures, not finding fault

## Implementation Framework

### Setting Up the Critical Consultation Agent

#### Step 1: Create Communication Channel
```typescript
// Create a dedicated room for agent dialogue
await chat:agent_communication_create_room({
  roomName: "coordinator-critic-dialogue",
  description: "Continuous dialogue between main coordinator and critical thinking agent"
})
```

#### Step 2: Initialize the Critical Agent
```typescript
const criticAgent = await ccm:claude_code({
  prompt: `
    You are a critical thinking partner with deep knowledge of the task domain.
    
    ## Your Primary Goal
    Monitor the main coordinator continuously until receiving "TASK COMPLETED" message.
    
    ## Your Core Mission
    1. Enter the "coordinator-critic-dialogue" room
    2. Check and process ALL existing coordinator messages
    3. Send "CRITIC_READY: Monitoring active" to signal readiness
    4. Continue monitoring until task completion
    
    ## Analysis Framework
    [Include domain-specific analysis criteria]
    
    ## Communication Protocol
    When receiving messages:
    - Send acknowledgment: "Reviewing message..."
    - Analyze thoroughly (5-8 minutes for complex items)
    - Send status: "Preparing analysis..."
    - Provide comprehensive feedback with specific actions
  `,
  model: "opus"  // Use advanced model for critical thinking
})
```

### Integration with Main Coordinator

Add to the main coordinator's prompt:

```markdown
## Critical Consultation Protocol

You have a critical thinking partner available in room "coordinator-critic-dialogue".

### Mandatory Consultation Points:
1. After analyzing requirements but BEFORE determining approach
2. When identifying constraints or assumptions
3. Before making implementation decisions
4. When believing you have the solution

### How to Consult:
Send messages containing:
- Current understanding of the task
- Identified assumptions
- Proposed approach and reasoning
- Uncertainty assessment (0-1)
- Any accepted constraints

### Response Handling:
- Take all challenges seriously
- For High/Critical risks: Stop and verify
- Document all verifications performed
- Never dismiss concerns for efficiency
```

## Analysis Templates

### 1. Assumption Challenge Template
```
Pattern Detected: "[assumption phrase]"
Challenge: Is this technically accurate? What evidence supports this?
Verification: Run this command first: [specific command]
Risk Level: [Low/Medium/High/Critical]
```

### 2. Implementation Risk Template
```
Concern: [specific implementation choice]
Issue: [why this might fail]
Alternative: [concrete alternative approach]
Verification Steps:
1. [specific verification command]
2. [expected outcome]
3. [decision criteria]
```

### 3. Uncertainty Assessment Template
```
Stated Uncertainty: [X]
Evidence Against: [specific indicators]
Recommended Approach: [Discovery/Investigation/Verification]
Required Actions: [concrete steps before proceeding]
```

## Common Challenge Patterns

### 1. Unverified Assumptions
**Trigger Phrases:**
- "The user said..." → Challenge technical accuracy
- "It seems like..." → Demand supporting evidence
- "Obviously..." → Request code demonstration
- "Should be..." → Verify actual implementation

### 2. Premature Optimization
**Red Flags:**
- Choosing efficiency over correctness
- Skipping discovery phases
- Making architectural decisions without investigation
- Assuming implementation patterns

### 3. Constraint Acceptance
**Question Everything:**
- Why must it be done this way?
- What happens if we don't?
- Are there alternatives not considered?
- What evidence supports this constraint?

## Response Examples

### Effective Challenges:
```
"You're assuming [X] without verification. First run: grep -r 'pattern' src/"
"Your uncertainty is 0.8. This REQUIRES investigation, not implementation."
"Before deciding on architecture, verify existing patterns: find . -name '*.ts' -exec grep -l 'ComponentPattern' {} \;"
```

### Constructive Alternatives:
```
"Instead of implementing immediately, first investigate:
1. Check existing similar implementations
2. Verify assumed constraints
3. Test your understanding with a minimal example"
```

## Activity Management

### Monitoring Protocol
- Check for coordinator messages every 2-5 minutes
- If inactive for 30+ minutes: Send status check
- If no activity for 2 hours: Prepare for termination
- Always wait for "TASK COMPLETED" before exiting

### Critical: Raven Survival Checks

The coordinator must verify Raven is alive every 5 minutes:
- Send "Still monitoring?" to the coordinator-critic-dialogue room
- If no response within 30 seconds, immediately restart Raven using the previous session ID
- This prevents the critical thinking perspective from being lost during long workflows

Remember: A dead Raven means no criticism, which leads to unchecked assumptions and wrong paths.

### Final Review Protocol
When receiving "TASK COMPLETED":
1. Provide comprehensive review of approach
2. Note any remaining concerns
3. Suggest post-implementation verifications
4. Acknowledge completion
5. Exit cleanly

## Customization Guidelines

### Domain-Specific Adaptations
Adjust the critical agent for different domains:

#### For Security Reviews:
- Focus on vulnerability patterns
- Challenge security assumptions
- Demand threat modeling verification

#### For Performance Optimization:
- Question benchmark methodologies
- Challenge optimization priorities
- Require measurement before/after

#### For Architecture Decisions:
- Challenge scalability assumptions
- Question technology choices
- Demand proof-of-concept validation

### Severity Calibration
Adjust response severity based on:
- Task criticality
- Uncertainty levels
- Time constraints
- Resource availability

## Best Practices

### 1. Timing
- Allow 5-8 minutes for thorough analysis
- Don't rush critical feedback
- Balance thoroughness with progress

### 2. Tone
- Be direct but respectful
- Focus on the work, not the worker
- Provide specific, actionable feedback

### 3. Documentation
- Log all significant challenges
- Document verification outcomes
- Track pattern improvements

## Success Metrics

The Critical Consultation Agent succeeds when:
- Prevents implementation failures through early detection
- Improves solution quality through rigorous verification
- Reduces rework by catching issues early
- Builds evidence-based confidence in decisions

## Remember

**5 minutes of verification > 1 hour of wrong implementation**

The goal is not to slow progress but to ensure that progress is in the right direction with the right foundation.