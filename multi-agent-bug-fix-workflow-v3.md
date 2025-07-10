# Multi-Agent Bug Fix Workflow v3 (with Bug Replication, Verification & Confidence Scoring)

## Overview

This document describes an advanced workflow for accurately fixing bugs through systematic replication, confidence-based decision making, and verification, coordinating multiple specialized agents using Claude Code MCP (`mcp__ccm__claude_code`) with real-time chat communication.

**Target Audience**: This document serves as a guide for Claude Code to execute multi-agent bug fixes with replication-first approach, confidence scoring, and chat-based coordination.

**Key Enhancements**: 
- **Bug Replication Phase**: Ensures accurate understanding before fixing
- **Confidence Scoring**: Transparent confidence levels at each phase
- **User Checkpoints**: Validates approach at critical decision points
- **Automated Verification**: Compares before/after states
- **Regression Prevention**: Creates tests to prevent reoccurrence
- **Bug Pattern Learning**: Leverages historical bug data

## Workflow Components

### 1. Bug Classifier Agent
- **Role**: Classify bug type and determine replication strategy
- **Model**: Haiku (for speed)
- **Deliverable**: Bug classification and routing strategy
- **Chat Name**: ClassifierAgent
- **NEW**: Routes bugs to appropriate specialists

### 2. Bug Replication Agent
- **Role**: Replicate the reported bug and capture evidence
- **Model**: Sonnet (for efficiency)
- **Deliverables**: 
  - `bug-replication-report.md`
  - Evidence files (screenshots/test results)
  - Confidence score
- **Chat Name**: ReplicationAgent

### 3. Investigation Agent
- **Role**: Investigate bug causes with confidence assessment
- **Model**: Opus
- **Deliverables**: 
  - `bug-investigation-report.md`
  - Fix confidence score
  - Solution proposal
- **Chat Name**: InvestigationAgent

### 4. Implementation Agent
- **Role**: Implement fixes based on approved investigation
- **Model**: Sonnet
- **Deliverable**: Actual code fixes
- **Chat Name**: ImplementationAgent

### 5. Verification Agent
- **Role**: Verify bug is fixed by re-running replication steps
- **Model**: Sonnet
- **Deliverables**: 
  - `bug-verification-report.md`
  - Comparison evidence
  - Verification confidence
- **Chat Name**: VerificationAgent

### 6. Review Agent
- **Role**: Code review of implemented fixes
- **Model**: Opus
- **Deliverable**: `code-review-report.md`
- **Chat Name**: ReviewAgent

### 7. Regression Test Agent
- **Role**: Create tests to prevent bug reoccurrence
- **Model**: Sonnet
- **Deliverable**: Regression test code
- **Chat Name**: RegressionAgent

### 8. Bug History Agent
- **Role**: Update bug patterns database
- **Model**: Haiku
- **Deliverable**: Updated bug history
- **Chat Name**: HistoryAgent
- **NEW**: Learns from each bug fix

### 9. Debug Agent
- **Role**: Troubleshooting when issues occur
- **Model**: Sonnet
- **Launch Condition**: Only when errors occur
- **Chat Name**: DebugAgent

### 10. Coordinator (Main Agent)
- **Role**: Monitor chat room, coordinate agents, handle user interactions, track confidence
- **Chat Name**: Coordinator

## Bug Classification System

### Bug Types and Routing

```yaml
bug_types:
  visual:
    description: "CSS, layout, rendering issues"
    primary_tool: "playwright"
    evidence: "screenshots, computed styles"
    
  functional:
    description: "Logic errors, incorrect behavior"
    primary_tool: "test-script"
    evidence: "input/output comparison"
    
  performance:
    description: "Slow operations, timeouts"
    primary_tool: "profiler"
    evidence: "timing data, resource usage"
    
  data:
    description: "Incorrect data handling, corruption"
    primary_tool: "data-validator"
    evidence: "data snapshots, transformations"
    
  integration:
    description: "API, service communication issues"
    primary_tool: "api-tester"
    evidence: "request/response logs"
    
  security:
    description: "Vulnerabilities, access issues"
    primary_tool: "security-scanner"
    evidence: "vulnerability reports"
```

## Evidence Collection Templates

### Frontend Evidence Template
```json
{
  "bugId": "BUG-2024-XXX",
  "timestamp": "ISO-8601",
  "classification": {
    "type": "visual|functional|performance",
    "confidence": 0.95,
    "subtype": "specific-category"
  },
  "environment": {
    "url": "https://...",
    "browser": "Chrome 120",
    "viewport": {"width": 1920, "height": 1080},
    "userAgent": "..."
  },
  "replication": {
    "steps": [
      {"action": "navigate", "target": "url", "result": "success"},
      {"action": "click", "target": "#submit", "result": "no-response"}
    ],
    "screenshots": {
      "before": "./evidence/screenshots/before-fix.png",
      "after": "./evidence/screenshots/after-fix.png",
      "diff": "./evidence/screenshots/diff.png"
    }
  },
  "console": {
    "errors": ["TypeError: Cannot read property..."],
    "warnings": [],
    "logs": []
  }
}
```

### Backend Evidence Template
```json
{
  "bugId": "BUG-2024-XXX",
  "timestamp": "ISO-8601",
  "classification": {
    "type": "functional|data|integration",
    "confidence": 0.85,
    "subtype": "api-error"
  },
  "test": {
    "script": "./evidence/test-scripts/reproduce-bug.js",
    "input": {"request": "data"},
    "expectedOutput": {"status": 200, "data": "..."},
    "actualOutput": {"status": 500, "error": "..."},
    "executionTime": 1234
  },
  "logs": {
    "error": ["Stack trace..."],
    "debug": ["Processing steps..."]
  },
  "database": {
    "before": "./evidence/snapshots/db-before.json",
    "after": "./evidence/snapshots/db-after.json"
  }
}
```

## Confidence Scoring System

### Confidence Calculation Factors

```python
def calculate_confidence(factors):
    """
    Calculate confidence score based on multiple factors
    Returns: float between 0.0 and 1.0
    """
    weights = {
        'replication_clarity': 0.25,      # How clearly bug was reproduced
        'root_cause_certainty': 0.30,     # How certain about root cause
        'fix_complexity': 0.20,           # Inverse of fix complexity
        'similar_bugs_success': 0.15,     # Success rate of similar fixes
        'test_coverage': 0.10             # Existing test coverage
    }
    
    score = sum(factors[key] * weights[key] for key in weights)
    return round(score, 2)
```

### Confidence Thresholds

- **High Confidence (>= 0.80)**: Proceed automatically with user notification
- **Medium Confidence (0.60-0.79)**: Request user approval with explanation
- **Low Confidence (< 0.60)**: Recommend additional investigation

## Detailed Workflow

### Phase 0: Setup and Initialization

```bash
# Create directory structure
mkdir -p ./backup/bugfix-v3
mkdir -p ./evidence/{screenshots,test-scripts,logs,snapshots}
mkdir -p ./bug-history

# Initialize bug tracking
BUG_ID="BUG-$(date +%Y%m%d-%H%M%S)"
echo "{\"bugId\": \"$BUG_ID\", \"status\": \"initiated\"}" > ./bug-history/$BUG_ID.json

# Backup existing files
for file in bug-*.md; do
  [ -f "$file" ] && mv "$file" "./backup/bugfix-v3/${file%.md}_$(date +%Y%m%d_%H%M%S).md"
done
```

**Chat Room Setup with Enhanced Messages**:
```bash
ROOM_NAME="bugfix-v3-$BUG_ID"

# Enhanced message format with confidence
[CLASSIFICATION] Bug type: [type], Confidence: [score]
[REPLICATION] Status: [status], Confidence: [score]
[INVESTIGATION] Root cause found, Confidence: [score]
[APPROVAL] User approval requested for [action]
[CONFIDENCE] Overall fix confidence: [score]
```

### Phase 1: Bug Classification and Strategy

#### Step 1.1: Launch Bug Classifier
```
mcp__ccm__claude_code:
  model: "haiku"
  prompt: |
    You are the Bug Classifier. Analyze this bug report:
    "[user's bug description]"
    
    1. Join chat "$ROOM_NAME" as "ClassifierAgent"
    2. Classify bug type based on description
    3. Determine confidence in classification (0-1)
    4. Select appropriate replication strategy
    5. Check bug-history/ for similar past bugs
    6. Report: "[CLASSIFICATION] Type: [type], Confidence: [score], Strategy: [approach]"
    7. Create initial bug-history/$BUG_ID.json with classification
```

### Phase 2: Bug Replication with Evidence

#### Step 2.1: Launch Replication Agent with Routing

Based on classification, use specialized replication approach:

```
mcp__ccm__claude_code:
  model: "sonnet"
  prompt: |
    You are the Bug Replication Agent. Your classification: $BUG_TYPE
    
    Join chat "$ROOM_NAME" as "ReplicationAgent"
    Report: "[PROGRESS] Starting $BUG_TYPE bug replication"
    
    Based on bug type, execute appropriate strategy:
    ${REPLICATION_STRATEGY_TEMPLATE}
    
    Calculate replication confidence based on:
    - Consistency of reproduction (weight: 0.4)
    - Clarity of evidence (weight: 0.3)
    - Match to user description (weight: 0.3)
    
    Create bug-replication-report.md with confidence score
    Report: "[REPLICATION] Complete, Confidence: [score]"
```

**Visual Bug Replication**:
```javascript
// Playwright strategy for visual bugs
await page.goto(url);
await page.waitForLoadState('networkidle');

// Capture multiple states
const evidence = {
  clean: await page.screenshot({fullPage: true}),
  hover: await page.hover(selector) && await page.screenshot(),
  active: await page.click(selector) && await page.screenshot(),
  computed: await page.evaluate(() => getComputedStyle(element))
};

// Calculate visual diff
const diffConfidence = await compareVisualStates(evidence);
```

### Phase 2.2: User Confirmation Checkpoint #1

**Enhanced confirmation with confidence display**:

```
Bug Replication Complete - Confirmation Required

Bug ID: $BUG_ID
Type: $BUG_TYPE (Classification Confidence: 85%)

I've replicated the following behavior with 92% confidence:

[Display evidence based on type]
- Screenshots: [before-fix.png]
- Steps taken: [numbered list]
- Observed behavior: [description]

Replication Confidence Factors:
✓ Consistent reproduction: 95%
✓ Clear evidence captured: 90%
✓ Matches your description: 90%

Is this the bug you're experiencing? (yes/no/clarify)
```

### Phase 3: Investigation with Confidence Assessment

#### Step 3.1: Launch Investigation with Historical Context

```
mcp__ccm__claude_code:
  model: "opus"
  prompt: |
    You are the Investigation Agent. Investigate the confirmed bug:
    
    1. Join chat "$ROOM_NAME" as "InvestigationAgent"
    2. Load similar bugs from bug-history/
    3. Analyze code paths from replication evidence
    4. Identify root cause with certainty assessment
    
    Calculate investigation confidence:
    - Root cause certainty (0-1)
    - Similar bug patterns (0-1)
    - Code complexity factor (0-1)
    - Test coverage in area (0-1)
    
    Report: "[INVESTIGATION] Root cause identified, Confidence: [score]"
```

### Phase 3.2: User Confirmation Checkpoint #2 (Investigation Confidence)

**NEW CHECKPOINT - Present solution confidence before implementation**:

```
Investigation Complete - Solution Approval Required

Root Cause Analysis:
The bug is caused by [detailed explanation of root cause]

Proposed Solution:
[Summary of the fix approach]

Fix Confidence: 80%

Confidence Breakdown:
✓ Root cause certainty: 85%
✓ Similar bugs fixed successfully: 8/10 (80%)
✓ Solution complexity: Simple (90%)
✓ Test coverage in area: 65%

Historical Context:
- Similar bug BUG-2024-001 fixed with same approach (success)
- Related issue BUG-2024-045 required 2 attempts

My confidence that this fix will fully resolve the issue is 80%.

Would you like me to proceed with this solution? (yes/no/discuss)

Options:
- 'yes' - Proceed with implementation
- 'no' - Investigate alternative approaches  
- 'discuss' - Ask questions about the solution
```

**Handle Low Confidence Scenarios**:
```
If confidence < 60%:
  "My confidence in this solution is only 45%. I recommend:
   1. Additional investigation in [areas]
   2. Consulting [specific documentation]
   3. Running diagnostic [tests]
   
   Would you like me to perform additional investigation? (yes/no)"
```

### Phase 4: Implementation (Conditional on Approval)

Only proceed after user approves the solution approach.

### Phase 5: Verification with Confidence

```
Verification Complete

Result: BUG FIXED ✓
Verification Confidence: 95%

Evidence:
- Before: [screenshot/test showing bug]
- After: [screenshot/test showing fix]
- Diff analysis: 98% improvement

All replication steps re-executed successfully.

Proceeding to code review and regression test creation.
```

### Phase 6: Regression Testing with Pattern Learning

```
mcp__ccm__claude_code:
  model: "sonnet"
  prompt: |
    Create regression tests and update bug patterns:
    
    1. Create comprehensive test suite
    2. Include edge cases from similar bugs
    3. Update bug-history/$BUG_ID.json with:
       - Solution patterns
       - Test strategies
       - Confidence scores
    4. Link to similar bugs for future reference
```

### Phase 7: Bug History Update

```json
// Final bug history entry
{
  "bugId": "BUG-2024-XXX",
  "classification": {
    "type": "functional",
    "subtype": "event-handler",
    "confidence": 0.85
  },
  "replication": {
    "attempts": 1,
    "confidence": 0.92,
    "strategy": "playwright"
  },
  "investigation": {
    "rootCause": "Missing event listener",
    "confidence": 0.80,
    "similarBugs": ["BUG-2024-001", "BUG-2024-045"]
  },
  "fix": {
    "attempts": 1,
    "confidence": 0.80,
    "approved": true,
    "verificationConfidence": 0.95
  },
  "regressionTests": [
    "tests/bug-fixes/BUG-2024-XXX.test.js"
  ],
  "patterns": {
    "symptom": "button-not-responding",
    "cause": "missing-event-handler",
    "solution": "add-listener-pattern"
  }
}
```

## Intelligent Failure Recovery

### Flaky Bug Handling
```python
def handle_flaky_bug(bug_id, attempts=3):
    """Handle intermittent bugs with multiple attempts"""
    results = []
    for i in range(attempts):
        result = attempt_replication()
        results.append(result)
        if result.success:
            confidence = calculate_flaky_confidence(results)
            return {
                'reproduced': True,
                'attempts': i + 1,
                'confidence': confidence,
                'frequency': sum(r.success for r in results) / len(results)
            }
    return {'reproduced': False, 'attempts': attempts}
```

## Success Metrics Dashboard

```
Bug Fix Summary for BUG-2024-XXX
================================
Classification Confidence: 85% ✓
Replication Confidence:   92% ✓
Investigation Confidence: 80% ✓
User Approval:           YES ✓
Implementation Time:     3 min
Verification Success:    95% ✓
Regression Tests:        5 created

Overall Success Score: 88%
Time to Resolution: 18 minutes
Similar Bugs Referenced: 2
Pattern Match: button-not-responding
```

## Benefits of Enhanced v3 Approach

1. **Confidence Transparency**: Users see exactly how certain we are
2. **Informed Decisions**: Low confidence triggers more investigation
3. **Pattern Learning**: Each bug makes future fixes smarter
4. **Collaborative Process**: User input at critical decision points
5. **Evidence-Based**: Every decision backed by concrete evidence
6. **Predictable Success**: Confidence scores predict fix success rate

## Example Interaction Flow

```
User: "The submit button on the contact form doesn't work"

System: [CLASSIFICATION] Type: functional, Confidence: 0.85
System: [REPLICATION] Complete, Confidence: 0.92
System: "I've replicated your bug with 92% confidence. [shows evidence] Correct?"
User: "Yes"

System: [INVESTIGATION] Root cause identified, Confidence: 0.80
System: "I found the issue - missing click handler. 80% confident this fix will work. 
         Similar bugs had 8/10 success rate. Proceed?"
User: "What about the hover effect?"
System: "The hover effect uses a different handler that's working correctly. 
         This fix specifically addresses the click action. Updated confidence: 85%"
User: "Yes, proceed"

System: [IMPLEMENTATION] Fix applied
System: [VERIFICATION] Bug fixed, Confidence: 0.95
System: [REGRESSION] 5 tests created
System: "Bug fixed successfully! Tests added to prevent recurrence."
```

This enhanced v3 workflow creates a truly collaborative bug-fixing experience where users have visibility and control at every critical decision point.