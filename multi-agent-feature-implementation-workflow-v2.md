# Multi-Agent Feature Implementation Workflow v2 (TDD with Chat MCP)

## Overview

This document describes an enhanced workflow for efficiently implementing new features from design documents using Test-Driven Development (TDD) philosophy by coordinating multiple specialized agents using Claude Code MCP (`mcp__ccm__claude_code`) with real-time chat communication.

**Target Audience**: This document serves as a guide for Claude Code to execute TDD-based feature implementation with chat-coordinated multiple agents.

**Key Enhancement**: This v2 workflow includes Chat MCP for real-time TDD cycle coordination, progress tracking, and immediate feedback between agents.

**Prerequisites**: 
- A detailed design document (`design-document.md` or equivalent) must exist
- The design document should include functional requirements, technical specifications, API specifications, data models, etc.
- Understanding of TDD's Red-Green-Refactor cycle

## Workflow Components

### 1. Design Analysis Agent
- **Role**: Analyze design documents, create test specifications, develop implementation plan
- **Model**: Opus (for complex design understanding)
- **Deliverables**: `test-specification.md`, `implementation-plan.md`
- **Chat Name**: DesignAgent

### 2. Test Creation Agent
- **Role**: Create failing tests based on test specifications (Red Phase)
- **Model**: Sonnet (prioritizing cost efficiency)
- **Deliverable**: Test code (in failing state)
- **Chat Name**: TestAgent

### 3. Implementation Agent
- **Role**: Minimal implementation to make tests pass (Green Phase)
- **Model**: Sonnet
- **Deliverable**: Source code for new feature (tests passing)
- **Chat Name**: ImplementAgent

### 4. Refactoring Agent
- **Role**: Code quality improvement and refactoring (Refactor Phase)
- **Model**: Sonnet
- **Deliverable**: Refactored code
- **Chat Name**: RefactorAgent

### 5. Review Agent
- **Role**: Quality review of implemented code
- **Model**: Opus
- **Deliverable**: `code-review-report.md`
- **Chat Name**: ReviewAgent

### 6. TDD Coordinator (Main Agent)
- **Role**: Monitor TDD cycles and coordinate agent activities
- **Chat Name**: TDDCoordinator

## Detailed Workflow

### Phase 0: Preparation and Cleanup

Prepare the environment, set up chat room, and clean up previous deliverables before starting the workflow.

**Chat Room Setup**:
```bash
# Generate unique room name for this feature implementation
ROOM_NAME="tdd-feature-$(date +%Y%m%d-%H%M%S)"

# Enter chat room as TDD Coordinator
mcp__chat__agent_communication_enter_room:
  roomName: "$ROOM_NAME"
  agentName: "TDDCoordinator"

# Send initial message
mcp__chat__agent_communication_send_message:
  roomName: "$ROOM_NAME"
  agentName: "TDDCoordinator"
  message: "[STARTED] TDD Feature Implementation workflow initiated"
```

**TDD Chat Message Standards**:
```
[TDD-CYCLE] Starting cycle N: [description]
[RED] Tests created and failing
[GREEN] Tests passing with minimal implementation
[REFACTOR] Code quality improved, tests still passing
[PROGRESS] Current status of TDD cycle
[COMPLETED] Phase/cycle completed
[ISSUE] Problem encountered
[HANDOFF] Ready for next agent
```

```bash
# Create backup directory
mkdir -p ./backup/feature-implementation

# Check existing deliverable files
ls -la | grep -E "(test-specification|implementation-plan|test-report|code-review-report)\.md"

# Backup existing files if present
for file in test-specification.md implementation-plan.md test-report.md code-review-report.md; do
  if [ -f "$file" ]; then
    mv "$file" "./backup/feature-implementation/${file%.md}_$(date +%Y%m%d_%H%M%S).md"
    echo "Backed up $file"
  fi
done

# Verify design document exists
if [ ! -f "design-document.md" ]; then
  echo "ERROR: design-document.md not found"
  exit 1
fi
```

### Phase 1: Design Analysis and Test Specification Creation

Launch Design Analysis Agent (Opus) to analyze the design document and create test specifications and implementation plan:

1. **Use mcp__ccm__claude_code** tool
2. **model**: Specify "opus"
3. **Include in prompt**:
   - Instruction to read design-document.md
   - Create test specifications (test case design for TDD)
   - Create implementation plan
   - Identify technical challenges
   - Output to test-specification.md and implementation-plan.md
   - **Chat instructions**:
     ```
     Join chat room "$ROOM_NAME" as "DesignAgent"
     Report progress: "[PROGRESS] Analyzing design document"
     Share insights: "[FINDING] Key technical challenges: [list]"
     Announce TDD cycles: "[TDD-CYCLE] Planned cycles: [count]"
     Signal completion: "[COMPLETED] Test specs and plan ready"
     ```

**Test Specification Output Format**:
```
# Test Specification
## Functional Test Cases
### Test Case 1: [Name]
- Preconditions: 
- Input: 
- Expected Result: 
- Test Type: unit/integration/e2e

## Edge Case Tests
### Error Case 1: [Name]
- Scenario:
- Expected Behavior:

## Performance Tests
[As needed]
```

**Implementation Plan Output Format**:
```
# Implementation Plan
## Feature Overview
## Implementation Scope
## TDD Cycle Plan
### Cycle 1: [Minimal Feature]
- Test: [Corresponding test cases]
- Implementation: [Minimal implementation content]
### Cycle 2: ...
## Technology Stack
## Dependencies
## Risks and Mitigation
```

### Phase 2: Test Creation (Red Phase - Chat Coordinated)

Monitor chat for DesignAgent completion, then launch Test Creation Agent:

1. **Wait for "[COMPLETED]"** from DesignAgent in chat
2. **Send TDD cycle start message**:
   ```
   mcp__chat__agent_communication_send_message:
     roomName: "$ROOM_NAME"
     agentName: "TDDCoordinator"
     message: "[TDD-CYCLE] Starting Cycle 1: Creating failing tests"
   ```
3. **Use mcp__ccm__claude_code** tool
4. **model**: Specify "sonnet"
5. **Include in prompt**:
   - Read test-specification.md
   - Read implementation-plan.md
   - Create failing tests (since implementation doesn't exist yet)
   - Execute tests and confirm failure
   - Report test results
   - **Chat instructions**:
     ```
     Join chat room "$ROOM_NAME" as "TestAgent"
     Acknowledge: "[RECEIVED] Starting test creation for Cycle 1"
     Report progress: "[PROGRESS] Writing test for [feature]"
     Confirm red phase: "[RED] All tests failing as expected"
     Share test count: "[INFO] Created N tests, all failing"
     Signal handoff: "[HANDOFF] Tests ready for implementation"
     ```

**Important**: 
- Tests must fail (TDD Red Phase)
- Save returned session ID (for test updates)

### Phase 3: Minimal Implementation (Green Phase - Chat Triggered)

1. **Monitor chat for "[HANDOFF]"** from TestAgent
2. **Send green phase start**:
   ```
   mcp__chat__agent_communication_send_message:
     roomName: "$ROOM_NAME"
     agentName: "TDDCoordinator"
     message: "[TDD-CYCLE] Green Phase: Implementing minimal code"
   ```
3. **Use mcp__ccm__claude_code** tool
4. **model**: Specify "sonnet"
5. **Include in prompt**:
   - Check failing tests
   - Minimal implementation to pass tests
   - Hard-coding allowed (in first cycle)
   - Execute tests and confirm success
   - **Chat instructions**:
     ```
     Join chat room "$ROOM_NAME" as "ImplementAgent"
     Acknowledge: "[RECEIVED] Starting minimal implementation"
     Report approach: "[INFO] Using [approach] to pass tests"
     Update on progress: "[PROGRESS] Implementing [component]"
     Confirm green: "[GREEN] All tests passing!"
     Request refactoring: "[HANDOFF] Ready for refactoring"
     ```

**Important**: 
- Passing tests is top priority (code quality improved later)
- Save returned session ID (for refactoring use)

### Phase 4: Refactoring (Refactor Phase - Chat Coordinated)

1. **Monitor chat for "[GREEN]"** from ImplementAgent
2. **Send refactor phase start**:
   ```
   mcp__chat__agent_communication_send_message:
     roomName: "$ROOM_NAME"
     agentName: "TDDCoordinator"
     message: "[TDD-CYCLE] Refactor Phase: Improving code quality"
   ```
3. **Resume Implementation Agent session** (use Phase 3 session ID)
4. **Refactoring content**:
   - Remove hard-coding
   - Delete duplicate code
   - Appropriate abstraction
   - Performance improvements
   - Apply coding standards
   - **Chat updates**:
     ```
     Report as "RefactorAgent" (or continue as ImplementAgent)
     Update: "[PROGRESS] Refactoring [aspect]"
     Confirm: "[REFACTOR] Code improved, all tests still passing"
     Complete cycle: "[COMPLETED] TDD Cycle 1 complete"
     ```
5. **After each refactoring**:
   - Re-run tests
   - Confirm all tests pass

### Phase 5: TDD Cycle Repetition (Chat-Driven)

Based on the implementation plan, repeat Phases 2-4 for each feature:

1. **Monitor chat for cycle completion**
2. **Announce next cycle via chat**:
   ```
   mcp__chat__agent_communication_send_message:
     roomName: "$ROOM_NAME"
     agentName: "TDDCoordinator"
     message: "[TDD-CYCLE] Starting Cycle N: [feature description]"
   ```
3. **Coordinate agents through chat**:
   - TestAgent: "[RED]" → ImplementAgent: "[GREEN]" → RefactorAgent: "[REFACTOR]"
   - Each agent monitors chat for their turn
   - No fixed wait times - purely event-driven

**Cycle Management**:
- Follow TDD cycle plan shared in chat
- Chat messages track cycle progress
- Real-time coordination ensures smooth handoffs

### Phase 6: Integration Testing and Code Review (Chat-Triggered)

1. **Monitor chat for final "[COMPLETED]"** from last TDD cycle
2. **Announce review phase**:
   ```
   mcp__chat__agent_communication_send_message:
     roomName: "$ROOM_NAME"
     agentName: "TDDCoordinator"
     message: "[HANDOFF] All TDD cycles complete, ready for final review"
   ```
3. **Use mcp__ccm__claude_code** tool
4. **model**: Specify "opus"
5. **Review perspectives**:
   - Alignment with design document
   - Appropriateness of TDD process
   - Code quality (readability, maintainability)
   - Test coverage
   - Performance
   - Security
   - **Chat instructions**:
     ```
     Join chat room "$ROOM_NAME" as "ReviewAgent"
     Acknowledge: "[RECEIVED] Starting comprehensive review"
     Share findings: "[FINDING] [aspect]: [observation]"
     Report issues: "[ISSUE] Found N issues requiring attention"
     Final verdict: "[COMPLETED] Review status: APPROVED/NEEDS_IMPROVEMENT"
     ```

**Review Result Format**:
```
Line 1: APPROVED or NEEDS_IMPROVEMENT
Line 2 onwards: Specific issues only if NEEDS_IMPROVEMENT
```

**Important**: Save the returned session ID (for re-review reuse).

### Phase 7: Review Fix and Re-review Cycle (Chat-Coordinated)

1. **Monitor chat for ReviewAgent's final verdict**
2. **If "NEEDS_IMPROVEMENT"** in chat (repeat up to 3 times):
3. **Coordinate fixes through chat**:
   
   a. **Test Fix Phase** (if test issues):
      ```
      mcp__chat__agent_communication_send_message:
        roomName: "$ROOM_NAME"
        agentName: "TDDCoordinator"
        message: "[REQUEST] @TestAgent Please add tests for: [missing cases]"
      ```
      - **Resume** Test Creation Agent session
      - Monitor chat for completion
   
   b. **Implementation Fix Phase**:
      ```
      mcp__chat__agent_communication_send_message:
        roomName: "$ROOM_NAME"
        agentName: "TDDCoordinator"
        message: "[REQUEST] @ImplementAgent Please fix: [issues list]"
      ```
      - **Resume** Implementation Agent session
      - Monitor chat for "[COMPLETED] Fixes applied"
   
   c. **Re-review Phase**:
      ```
      mcp__chat__agent_communication_send_message:
        roomName: "$ROOM_NAME"
        agentName: "TDDCoordinator"
        message: "[REQUEST] @ReviewAgent Please re-review the fixes"
      ```
      - **Resume** Review Agent session
      - Monitor chat for new verdict

**Important**: Session resumption allows each agent to continue work while maintaining previous context.

### Phase 8: Completion Confirmation

**If APPROVED**:
- Feature implementation is complete
- Confirm deliverables:
  - test-specification.md (test specifications)
  - implementation-plan.md (implementation plan)
  - code-review-report.md (review results)
  - Test code (all passing)
  - Implementation code (reviewed and refactored)

**If still NEEDS_IMPROVEMENT after 3 iterations**:
- Report that manual intervention is required
- List remaining issues

### Phase 9: Final Quality Check

Main agent confirms the following:

1. **Deliverables Confirmation**:
   - All deliverables correctly generated
   - Review is APPROVED

2. **Quality Checks**:
   - All tests pass
   - Test coverage meets standards
   - Build succeeds
   - No lint errors
   - Type check passes

3. **TDD Process Confirmation**:
   - Red-Green-Refactor cycles properly executed
   - Test-first approach maintained
   - Incremental feature expansion performed

## Task Management Best Practices

Progress management using TodoWrite tool for TDD-based development:

1. **Design analysis and test specification creation**
2. **TDD Cycle 1: Minimal feature**
   - Red: Create failing test
   - Green: Minimal implementation to pass test
   - Refactor: Improve code quality
3. **TDD Cycle 2: Feature expansion**
   - Add new test cases
   - Expand implementation
   - Refactoring
4. **Create and run integration tests**
5. **Code review and improvements**
6. **Final quality check**

## Inter-Agent Coordination

### Information Handoff

1. **Design Analysis → Test Creation**: test-specification.md
2. **Design Analysis → Implementation**: implementation-plan.md (TDD cycle plan)
3. **Test → Implementation**: Failing tests
4. **Implementation → Refactoring**: Passing tests and implementation code
5. **All Cycles → Review**: Completed code and tests
6. **Review → Improvements**: code-review-report.md

### Session Management

Efficient coordination through proper management of each agent's session ID:

1. **Design Analysis Agent**: New session (not needed after analysis completion)
2. **Test Creation Agent**: Maintain session ID (reuse in review fix cycle)
3. **Implementation Agent**: Maintain session ID (reuse in review fix cycle)
4. **Review Agent**: Maintain session ID (reuse for re-review)

**Key Points**:
- Extract session_id from mcp__ccm__claude_code return value
- Save Test Creation, Implementation, and Review Agent session IDs in variables
- Use saved session_id when resuming sessions in Phase 7
- This allows each agent to continue work while maintaining previous context

**TDD Cycle Utilization**:
- Resume sessions in each cycle to continuously expand features
- Maintain correspondence between tests and implementation
- Preserve context during refactoring

## Estimated Wait Times (Dramatically Reduced with Chat)

- **Design Analysis**: Dynamic (monitor chat)
- **Each TDD Cycle**: Event-driven (no fixed waits)
  - Red: Immediate after design/previous cycle
  - Green: Immediate after red confirmation
  - Refactor: Immediate after green confirmation
- **Review**: Triggered by final cycle completion
- **Fix Cycles**: Immediate response to issues

**Time Savings**: 40-60% reduction through:
- Elimination of fixed wait times
- Real-time handoffs
- Parallel awareness of progress
- Immediate issue resolution

## Chat Monitoring Best Practices

```bash
# Continuous chat monitoring pattern
while true; do
  # Check for new messages
  mcp__chat__agent_communication_list_messages:
    roomName: "$ROOM_NAME"
    limit: 5
  
  # Process based on message type
  # [HANDOFF] → Trigger next agent
  # [COMPLETED] → Move to next phase
  # [ISSUE] → Coordinate resolution
  
  sleep 15  # Check every 15 seconds
done
```

## Success Patterns with Chat Coordination

### REST API Feature TDD Implementation Example (Chat-Enhanced)

1. **Design Document**: RESTful API specifications (endpoints, request/response formats)
2. **Test Specifications and TDD Cycle Plan**:
   - Cycle 1: Basic GET endpoint functionality
   - Cycle 2: POST endpoint and validation
   - Cycle 3: Error handling
   - Cycle 4: Authentication and authorization
3. **TDD Cycle Execution** (via chat room "tdd-api-feature"):
   - Each cycle announced in chat: "[TDD-CYCLE] Cycle N: [endpoint]"
   - Real-time progress: "[RED]", "[GREEN]", "[REFACTOR]"
   - Agents self-coordinate through chat messages
4. **Review and Fix Cycle** (chat-driven):
   - **Initial Review**: NEEDS_IMPROVEMENT (Session ID: abc123)
     - Improve error handling
     - Add test cases
     - Performance optimization
   - **Fix Response** (coordinated via chat): 
     - TDDCoordinator: "[REQUEST] @TestAgent add validation tests"
     - TestAgent: "[COMPLETED] 3 new tests added"
     - TDDCoordinator: "[REQUEST] @ImplementAgent fix validation"
     - ImplementAgent: "[COMPLETED] Validation implemented"
   - **Re-review**: ReviewAgent: "[COMPLETED] Status: APPROVED"
5. **Final Deliverables**:
   - API with 100% test coverage
   - Review-approved high-quality code
   - Robust implementation built incrementally

## Benefits

1. **High-Quality Code**: TDD improves design and quality
2. **Early Bug Detection**: Test-first approach identifies issues early
3. **Regression Prevention**: Safe development without breaking existing features
4. **Specification Clarity**: Tests serve as living documentation
5. **Incremental Development**: Progress with small, certain steps
6. **High Test Coverage**: Naturally achieve near 100% coverage
7. **Safe Refactoring**: Tests act as safety net

## Precautions

1. **Test-First Strict Adherence**: Always write tests before implementation
2. **Small Steps**: Keep TDD cycles small
3. **Red Confirmation Importance**: Always confirm tests fail
4. **Avoid Over-Implementation**: Start with minimal implementation to pass tests
5. **Continuous Refactoring**: Improve code quality in each cycle
6. **Test Maintainability**: Manage test code with same quality standards as production code
7. **Appropriate Use of Mocks and Stubs**: Properly isolate external dependencies

## Extensibility

- **Performance Test Agent**: Load testing and benchmarking
- **Security Audit Agent**: Vulnerability scanning
- **Deployment Agent**: CI/CD pipeline integration
- **Monitoring Configuration Agent**: Logging and metrics setup

## Failure Handling

- **Cannot Write Tests**: Design review needed (testability issues)
- **Tests Won't Pass**: Identify cause in debug session
- **Tests Break During Refactoring**: Roll back changes and retry
- **TDD Cycle Too Large**: Split into smaller steps
- **Coverage Not Increasing**: Add missing test cases

## TDD Best Practices

1. **AAA Principle**: Arrange, Act, Assert
2. **One Test One Assertion**: Tests verify only one behavior
3. **Test Names Are Specifications**: Clear indication of what's being verified
4. **F.I.R.S.T Principle**: Fast, Independent, Repeatable, Self-validating, Timely
5. **Test Refactoring**: Apply DRY principle to test code as well

This workflow enables systematic implementation of high-quality new features based on TDD philosophy.