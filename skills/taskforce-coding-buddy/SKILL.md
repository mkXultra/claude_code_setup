---
name: taskforce-coding-buddy
description: "Run the coding taskforce buddy workflow: implement with codex-ultra, run unit tests with gpt-5.1-codex-mini, triage results, and iterate fixes using the same session_id. Use when asked to follow taskforce_coding_buddy.md or to orchestrate this multi-step coding workflow."
user-invocable: true
---

# Taskforce Coding Buddy Workflow

Act as the operator and drive the workflow steps below.

## Workflow

1. Implement code
   - Use `mcp__acm__run` to implement code based on requirements.
   - Model: `codex-ultra`
   - Capture the returned `session_id`.

2. Run unit tests
   - Use `mcp__acm__run` to run unit tests and report results.
   - Model: `gpt-5.1-codex-mini`

3. Triage test results
   - If tests pass, stop.
   - If tests fail, continue to step 4.

4. Fix failures
   - Use `mcp__acm__run` to identify the failing cause and fix it.
   - Model: `codex-ultra`
   - Use the `session_id` from step 1 (or the most recent fix run).

5. Decide next action
   - Usually go back to step 2 to re-run tests.
   - Stop if the operator decides no further action is needed.
