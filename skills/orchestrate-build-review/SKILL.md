---
name: orchestrate-build-review
description: Orchestrate a multi-model build-and-review workflow with progress-aware waits and two-reviewer degradation. Use when Codex receives YAML input with an optional builder model defaulting to coder-mid, optional builder session_id, fixed reviewer slots, a shared review prompt, a reviewer verification prompt, done criteria, and a max loop count, and must run a builder, gate each round with a cheap pre-review, collect review findings via files, merge and deduplicate findings, resolve contradictions by resuming reviewer sessions, loop the builder until done, and return each agent's final model, session_id, and status.
---

# Orchestrate Build Review

Run this skill as an operator. Accept the YAML input below and apply the Execution Policy.

## Execution Policy

- Use only `mcp__acm__run` for agent launches, `mcp__acm__wait` for normal waiting, `mcp__acm__get_result` plus `mcp__acm__peek` for timeout diagnosis, and `mcp__acm__kill_process` only for a confirmed stalled process.
- Use the current working directory as `workFolder` for every agent launch.
- Use local file reads and writes only for the review artifact flow described here.

## Input

Use this YAML shape:

```yaml
builder:
  model: coder-mid
  session_id: sess_build_optional
  task_prompt: |
    Implement the requested task.

pre_reviewer:
  model: reviewer-low
  fallback_model: gpt-6.1-sol
  session_id: sess_pre_review_optional

reviewers:
  codex:
    model: codex-ultra
    session_id: sess_codex
  glm5.3:
    primary_model: oc-ollama-cloud/glm-5.3
    fallback_model: oc-ollama-cloud/glm-5.2
    session_id: sess_glm53_or_glm52
  claude:
    model: claude-ultra
    session_id: sess_claude

review_prompt: |
  Review the builder result and report actionable findings.

verification_prompt: |
  Verify the implementation by running the relevant checks and describing what was validated.

done_criteria: |
  Stop when the requested task is satisfied and no accepted needs_fix findings remain.

max_loop_rounds: 3

artifacts_dir: .codex-artifacts/orchestrate-build-review
```

### Input Validation and Model Resolution Policy

- Validate that all required fields are present and non-empty: `builder.task_prompt`, `review_prompt`, `verification_prompt`, `done_criteria`, and `max_loop_rounds`. If any required input field is missing or invalid, stop immediately and return `status: failed` with a reason naming the offending field.
- Treat reviewer slots as fixed: `codex`, `glm5.3`, and `claude`.
- Treat `codex.model` as fixed to `codex-ultra`.
- Treat `glm5.3.primary_model` as fixed to `oc-ollama-cloud/glm-5.3` and `glm5.3.fallback_model` as fixed to `oc-ollama-cloud/glm-5.2`.
- Treat `claude.model` as optional, defaulting to `claude-ultra` when absent or empty; allow only `claude-ultra` or `fable`. Select `fable` only when the input explicitly sets `claude.model: fable`, never implicitly or as a fallback.
- Treat `builder.model` as optional. If it is absent or empty, default to `coder-mid`. Use `coder-low`, `coder-high`, or any other model only when the input sets it explicitly; never switch builder models automatically.
- Treat `pre_reviewer.model` and `pre_reviewer.fallback_model` as optional. If absent or empty, default them to `reviewer-low` and `gpt-6.1-sol`.
- Resolve the builder, pre-reviewer, and Claude reviewer models once before round 1; reuse them for every builder round, every pre-review attempt, and every Claude review and contradiction-resolution round, respectively. Change the pre-reviewer model only under the Pre-Review Policy.
- Treat builder, pre-reviewer, and reviewer `session_id` values as optional: pass each provided session into its initial `mcp__acm__run` call; otherwise start a new session.
- Treat `review_prompt` as the shared review instruction for every reviewer round.
- Every reviewer must use `verification_prompt` to validate the builder result, including concrete checks or commands when appropriate, subject to the reliance rule in the Pre-Review Policy.
- Treat `max_loop_rounds` as the current total-round limit. Change it only when the user chooses to extend the workflow at the loop-limit decision in step 9.
- Treat `artifacts_dir` as optional. If omitted, default to `.codex-artifacts/orchestrate-build-review`.

### Agent State Policy

- Track each reviewer by slot id, not by model name. Preserve `model_used` and whether fallback or artifact repair was used for every reviewer slot.
- Preserve the latest known `session_id` for every agent and use that latest `session_id` for contradiction-resolution reruns, later rounds, and final output.
- For artifact repair and contradiction resolution, resume each reviewer slot's latest successful `model_used` and `session_id`.

## Artifact Contract

Use `artifacts_dir` as the shared workspace for each loop round.

For each round `N`, create this structure:

```text
<artifacts_dir>/
  round-N/
    builder/
      handoff.md
    pre-review/
      attempt-K.yaml
    reviews/
      codex.yaml
      glm5.3.yaml
      claude.yaml
      reconsider/
        codex.yaml
        glm5.3.yaml
        claude.yaml
    merged-findings.yaml
```

Apply these artifact rules:

- Before each round `N`, create `<artifacts_dir>/round-N/builder`, `<artifacts_dir>/round-N/pre-review`, `<artifacts_dir>/round-N/reviews`, and `<artifacts_dir>/round-N/reviews/reconsider`.
- `round-N/pre-review/attempt-K.yaml` is written by the pre-reviewer for attempt `K` of that round. Use a new file for every attempt.
- `round-N/builder/handoff.md` is written by the builder. It must summarize what changed, what remains risky, and how reviewers should verify the result.
- In round 1, instruct the builder to include a concise implementation summary, the files changed or created, suggested verification focus for reviewers, and any known limitations or follow-up risks.
- `round-N/reviews/<reviewer-id>.yaml` is written by each launched reviewer slot and is the only source of record for that reviewer's findings for that round.
- `round-N/reviews/reconsider/<reviewer-id>.yaml` is written only during contradiction resolution and preserves the original round review file.
- `round-N/merged-findings.yaml` is written by the operator after merging and contradiction resolution.
- A review or reconsideration artifact is required only for a reviewer slot that is still active after the stage completes.
- Record active and degraded reviewer slot ids in `round-N/merged-findings.yaml` so later builder and reviewer rounds know which opinions participated.

## Reviewer Output Contract

Wrap the user-provided `review_prompt` and `verification_prompt` with an instruction that every reviewer must write YAML only to its assigned review file in this shape:

```yaml
verification_summary: ran targeted checks for touched files
findings:
  - key: requirement-a-missing
    position: needs_fix
    severity: major
    target: src/example.ts
    reason: Requirement A is missing
    fix: Add the missing requirement A condition
```

Apply these reviewer output rules:

- `verification_summary` is required and must summarize the checks performed.
- `findings` must be a list. Return `findings: []` when nothing needs fixing.
- Every finding must contain all six keys: `key`, `position`, `severity`, `target`, `reason`, and `fix`. Every value must be a non-empty string.
- `key` must identify the issue stably enough for deduplication across reviewers and must not repeat within the same file.
- `position` must be `needs_fix` or `no_fix`.
- `severity` should be a reviewer hint such as `major` or `minor`. Do not use severity to discard accepted findings.
- `target` should identify the affected area.
- `reason` should explain why the reviewer took that position.
- `fix` should describe the proposed change. For `no_fix`, `fix` is still required and must contain a short explanation of why no edit is required.

## Review Artifact Validation and Repair Policy

For every round review file, contradiction-reconsideration file, and pre-review file:

- Resolve `scripts/validate_review_yaml.py` relative to this `SKILL.md`, not relative to `workFolder`.
- Give every reviewer the absolute validator path and instruct it to run `python3 <validator-path> <assigned-review-file>` after writing the file, correcting the file until the command succeeds before the reviewer exits.
- After a reviewer finishes successfully, the operator must independently run the same validator command on that reviewer's assigned file. Do not replace this command with ad hoc YAML inspection.
- Validator exit code `0` means the artifact is valid. Exit code `1` means the artifact is missing or violates the review YAML contract. Exit code `2` means the validator itself could not run; stop the workflow with `status: failed` because review validity cannot be established.
- When validation exits `1`, capture the validator diagnostics and resume the same reviewer slot under the Agent State Policy. Give it the exact diagnostics, the same assigned output path, and a direct instruction to repair only the YAML artifact, overwrite it, and run the validator before completing. Do not ask it to re-review or change implementation files.
- Allow exactly one resumed artifact-repair attempt per model run for a given assigned file. Wait for that attempt with the Wait and Stall Detection Policy, then run the validator again independently.
- If the repaired artifact validates, continue with the same reviewer slot and record that artifact repair was used.
- If the repair agent fails or the repaired artifact is still invalid, treat that model run as failed and apply the Reviewer Failure Policy.
- Do not run artifact repair for a reviewer process that itself ended with terminal status `failed`; apply the Reviewer Failure Policy instead.

## Wait and Stall Detection Policy

Resolve the operator's wait mode once before round 1, giving explicit caller instructions precedence:

- If the user or calling controller explicitly specifies background waiting or standard waiting for this workflow, use that mode instead of executable-based detection. For example, a controller instruction to run ACM waits in the background with `timeout: 0` and idle selects background waiting, including when the operator runs in Pi.
- Only when no wait mode is explicitly specified, inspect the command-execution shell and its parent with `ps -o pid,ppid,comm -p $$ -p $PPID`. If an intermediate shell or wrapper is present, follow its parent PID until the nearest `codexg` or `codex` executable is identified. Reuse confirmed process evidence from the current operator session when available.
- In this automatic detection path, if that executable's basename is `codexg`, select background waiting. If it is `codex`, or the executable cannot be identified, use standard waiting. Do not infer the operator's executable from installed commands, the selected model, or a child agent's process name.
- Apply the selected mode to every builder, pre-reviewer, and reviewer wait, including fallback, artifact repair, contradiction resolution, and later loop rounds.

For background waiting, whether explicitly selected or automatically detected:

- Call `mcp__acm__wait` with the unfinished agent PIDs and `timeout: 0`. This means an unlimited wait, not an immediate status check.
- Run that pending tool call through the runtime's background execution mechanism, preserve its continuation handle and workflow state, and yield into idle until its completion notification arrives. While the wait is pending, do not poll with `get_result`, `peek`, repeated `wait` calls, or sleep loops, and do not launch dependent workflow stages.
- On notification, collect the pending wait result, update agent statuses and session ids, and continue from the waiting stage. Preserve PID-to-slot mappings, round numbers, artifact paths, and fallback/repair state across idle and resumption.
- Do not apply the standard 900-second timeout checkpoints or count the immediate background handoff as a stale check.
- If the pending wait itself errors, use `get_result` and, for still-running PIDs, `peek` to diagnose it under the common recovery rules below. A background handoff or an idle period alone is not an error or evidence of a stall.

For standard waiting, use the existing timeout and stall checks:

- Start with `mcp__acm__wait` using `timeout: 900`.
- When a wait times out, call `mcp__acm__get_result` for every unfinished PID and store a compact progress fingerprint from its status and current output. Compare it with that PID's fingerprint from the previous timeout checkpoint when one exists.
- For PIDs still reported as running, call `mcp__acm__peek` once with `peek_time_sec: 60` and `include_tool_calls: true`, then call `mcp__acm__get_result` again.
- Treat a PID as making progress when the first `get_result` differs meaningfully from the previous timeout checkpoint, `peek` observes a message or tool call, or the second `get_result` differs meaningfully from the first fingerprint.
- If progress is observed, reset that PID's consecutive stale-check count to zero and call `mcp__acm__wait` again with `timeout: 900` for unfinished PIDs. Do not stop merely because a cumulative wall-clock budget has elapsed while progress continues.
- If no progress is observed, increment that PID's consecutive stale-check count and re-wait once more with `timeout: 900` while the count is below two.
- Treat a PID as stalled when two consecutive timeout checks observe no progress. A stale check is consecutive only when no intervening `peek` event or meaningful `get_result` change was observed.

Apply these result and recovery rules in both modes:

- If `get_result` or `peek` fails or reports an unknown PID, retry the failed diagnostic call once. If it fails again, treat that PID as a wait-recovery failure.
- If `get_result` reports a terminal result during diagnosis, handle it immediately instead of re-waiting.
- Before handling a still-running PID as stalled or as an unrecoverable wait-recovery failure, terminate it with `mcp__acm__kill_process`. Confirm termination from a successful kill result or a subsequent terminal `get_result`; if termination cannot be confirmed, stop the workflow with `status: failed` so an orphaned agent cannot write stale artifacts later.
- Apply the Builder Failure Policy, Reviewer Failure Policy, or Pre-Review Policy, as appropriate, to terminal failures, stalls, and wait-recovery failures.

## Builder Failure Policy

- On any builder launch failure, terminal failure, stall, wait-recovery failure, required builder artifact operation failure, or missing/malformed handoff, stop immediately and return YAML with top-level `status: failed` and a concrete `reason`.

## Reviewer Failure Policy

- Resolve reviewer launch, artifact, and wait failures independently. A launch failure for one slot must not prevent attempts to launch the other slots.
- Treat a launch failure, terminal status `failed`, stall, unrecoverable diagnostic/wait-recovery failure, or exhausted artifact repair without valid YAML as a model-run failure. Apply the Review Artifact Validation and Repair Policy to successfully completed reviewer runs before treating invalid artifacts as failures.
- On a `glm5.3` primary model-run failure, emit a brief progress note to the user that the primary `glm5.3` reviewer failed and the workflow is continuing with `oc-ollama-cloud/glm-5.2`; then launch `oc-ollama-cloud/glm-5.2` for only that slot using the same assigned output file.
- Once fallback is used, use `oc-ollama-cloud/glm-5.2` for later reruns of that slot, including contradiction resolution. The fallback gets its own single resumed artifact-repair attempt under the Review Artifact Validation and Repair Policy if its output is invalid.
- On any model-run failure of `codex`, `claude`, or the `oc-ollama-cloud/glm-5.2` fallback, immediately mark the slot failed and inactive for the rest of the workflow and emit a brief degradation progress note. Never relaunch a degraded slot.
- Require at least two successful reviewer slots with valid artifacts in every review and contradiction-resolution stage. If fewer than two slots remain active or produce valid artifacts, stop immediately and return `status: failed`; otherwise continue with the remaining active slots.

## Pre-Review Policy

Pre-review is a cheap gate that catches objectively verifiable failures before the full review. The pre-reviewer is not a reviewer slot: it does not count toward the minimum-two-reviewers rule, and its findings are not merged or used in contradiction resolution.

- Limit pre-review findings to failures with objective evidence: a failing check requested by `verification_prompt`, such as unit tests, e2e tests, build, or lint, or a `builder.task_prompt` requirement that is not implemented. Require each finding's `reason` to cite the command and its failing output, or the unimplemented requirement. Instruct the pre-reviewer not to report design, style, or quality opinions.
- Pre-review files use the Reviewer Output Contract, and their `verification_summary` must list every check command run with its pass or fail result. Where the Review Artifact Validation and Repair Policy applies the Reviewer Failure Policy, apply the failure rules below instead.
- Allow at most 2 builder bounces per round. Bounces do not count toward `max_loop_rounds`.
- Treat a launch failure, terminal status `failed`, stall, wait-recovery failure, or exhausted artifact repair without valid YAML as a pre-review model-run failure.
- On a primary model-run failure, emit a brief progress note and rerun the same attempt with the fallback model in a new session using the same assigned output file. Use the fallback model for all later attempts and rounds. The fallback gets its own single artifact-repair attempt.
- On a fallback model-run failure, emit a brief progress note, disable pre-review for the rest of the workflow, and continue to the full review. A pre-review failure never fails the workflow by itself.
- Reliance rule: when a round has a valid pre-review file, give every reviewer the latest one. Instruct the `glm5.3` and `claude` slots to rely on the check results it records instead of re-running those checks, re-running only what they need to confirm a reported failure or one of their own findings, and to spend their verification on logic, design, and requirements. The `codex` slot always performs the full verification requested by `verification_prompt`, including re-running the checks, and uses the pre-review file only as supplementary evidence. When a round has no valid pre-review file or the `codex` slot is inactive, every active reviewer performs the full verification.

## Workflow

1. Initialize loop state
   - Apply all policies and contracts above to every stage.
   - Validate input, resolve models and the operator's wait mode, and initialize agent tracking.
   - Create `artifacts_dir` if needed and start with `N = 1`.

2. Run builder for round N
   - Prepare the round directories.
   - For round 1, use `builder.task_prompt` and pass `builder.session_id` when present.
   - For later rounds, resume the latest builder session and build one natural-language continuation prompt that includes:
     - the original `builder.task_prompt`,
     - the current `done_criteria`,
     - the previous round's findings path, `<artifacts_dir>/round-(N-1)/merged-findings.yaml`,
     - a direct instruction to implement all accepted fixes.
   - Start one builder agent with the resolved builder model. Instruct it to write `<artifacts_dir>/round-N/builder/handoff.md`.
   - Wait until the builder finishes.
   - Record the latest builder `session_id` and agent status from the result.
   - Read `<artifacts_dir>/round-N/builder/handoff.md`.

3. Pre-review round N
   - Skip this step when pre-review is disabled.
   - Start the pre-reviewer for attempt `K`, starting at 1, passing its provided or latest `session_id` when present. Give it `builder.task_prompt`, `verification_prompt`, the handoff path, and its assigned output file `<artifacts_dir>/round-N/pre-review/attempt-K.yaml`.
   - Wait for the pre-reviewer, then validate its file.
   - If the file has no `needs_fix` findings, or 2 bounces have been used this round, continue to step 4.
   - Otherwise bounce to the builder: resume the latest builder session with the pre-review file path and direct instructions to fix every `needs_fix` finding in it and rewrite `<artifacts_dir>/round-N/builder/handoff.md`. Wait for the builder, record its latest `session_id` and status, reread the handoff, and run attempt `K+1`.

4. Run reviewers for round N
   - In round 1, start all three reviewer slots in parallel; in later rounds, start only active slots. Pass each slot's provided or latest `session_id` when present.
   - Give every reviewer:
     - the shared `review_prompt`,
     - the shared `verification_prompt`,
     - the current `done_criteria`,
     - the path to `<artifacts_dir>/round-N/builder/handoff.md`,
     - the path to this round's latest valid pre-review file when one exists, with that slot's instruction from the reliance rule in the Pre-Review Policy,
     - the path to its assigned output file `<artifacts_dir>/round-N/reviews/<reviewer-id>.yaml`.
   - Instruct each reviewer to:
     - read the builder handoff,
     - inspect the working tree as needed,
     - perform the requested verification,
     - write its assigned review file per the Reviewer Output Contract and run the validator on it before completing.

5. Wait for reviewers
   - Wait until all launched review agents finish.
   - Record each reviewer slot's agent status from the result and update tracking.
   - Apply the Review Artifact Validation and Repair Policy to successful runs before declaring a reviewer failed under the Reviewer Failure Policy.

6. Merge findings
   - Extract findings only from each active reviewer's valid assigned review file.
   - Deduplicate findings by `key` when keys match directly.
   - When keys differ but the issue is clearly equivalent, treat them as the same logical finding and merge them.
   - Keep all accepted `needs_fix` findings as fix candidates. Do not discard findings because they seem lower priority.

7. Resolve contradictions
   - Treat a contradiction as a case where the same or equivalent finding has conflicting `position` values across reviewers.
   - Do not treat silence as a contradiction. If one reviewer omits a finding and others report it, merge based on the reported findings and continue.
   - If no contradictions remain, continue to the next step.
   - If contradictions remain, start a contradiction-resolution round for only the conflicting items.
   - Resume each active reviewer session, applying the Reviewer Failure Policy, and provide:
     - the conflicting opinions from the other reviewers,
     - the current builder handoff path,
     - the reconsideration output file path at `<artifacts_dir>/round-N/reviews/reconsider/<reviewer-id>.yaml`,
     - the same `review_prompt`, `verification_prompt`, and `done_criteria`.
   - Ask each reviewer to reconsider only the conflicting items and write YAML only for those items to its reconsideration file using the same Reviewer Output Contract.
   - Wait for each contradiction-resolution round.
   - Apply the Review Artifact Validation and Repair Policy to successful runs before declaring a reviewer failed under the Reviewer Failure Policy or updating positions.
   - After each contradiction-resolution round, read each active reviewer's valid reconsideration file.
   - If a reviewer was degraded during contradiction resolution, remove its opinion from the current contradiction set before recomputing positions.
   - Update the conflicting findings with the latest reviewer positions from those reconsideration files.
   - Recompute the remaining contradiction set before deciding whether another contradiction round is needed.
   - Repeat until all active reviewers converge or 3 contradiction-resolution rounds have completed.
   - Treat convergence as all active reviewers agreeing on `position` for a conflicting item.
   - If round 3 ends with three active reviewers and a `2:1` split, adopt the majority view for that item.
   - If round 3 ends with two active reviewers in a `1:1` split, stop immediately and return `status: stopped` with a reason that the two remaining reviewer opinions did not converge after 3 rounds.
   - If any other unresolved contradiction has no majority after round 3, stop immediately and return `status: stopped` with a concrete reason.

8. Decide whether the round is done
   - Write `<artifacts_dir>/round-N/merged-findings.yaml` with the accepted merged findings and contradiction-resolution outcomes.
   - If no accepted `needs_fix` findings remain after merge and contradiction resolution, stop and return `status: completed` with reason `done criteria satisfied and no fixes required`.

9. Decide whether to continue looping
   - If round `N` reaches `max_loop_rounds` and accepted `needs_fix` findings remain, pause with `status: ask` and request the user's decision before launching another builder round.
   - Explain that the configured loop limit requires this decision, and include the completed round count, a concise summary of the remaining accepted `needs_fix` findings, and the path to `<artifacts_dir>/round-N/merged-findings.yaml`.
   - Offer three choices: continue for one additional round, continue with a user-specified higher total-round limit, or stop here. Use an available user-question tool; if none is available, return the `ask` YAML with `decision_request` as defined below.
   - While awaiting an answer, preserve the workflow state and launch no further agents. No answer or an unclear answer keeps the workflow in `ask`; clarify an unclear decision without assuming continuation or stopping.
   - If the user chooses one additional round, set `max_loop_rounds` to `N + 1`. If the user specifies a higher total-round limit, require an integer greater than `N` and update `max_loop_rounds` to that value. A request to continue without a count authorizes one additional round.
   - If the limit has not been reached or the user chooses to continue, increment `N` and return to step 2 with the existing artifacts, latest session ids, resolved models, and active/degraded reviewer state. Preserve cumulative round numbering and ask again if the updated limit is reached with accepted `needs_fix` findings remaining.
   - If the user chooses to stop, return `status: stopped` with a reason that the user chose to stop after reaching the loop limit; preserve the remaining findings in the output.

## Output

Return status reports as YAML only. Background idle keeps the workflow in progress and does not produce a final status report or change its outcome to `ask`, `stopped`, or `completed`. The loop-limit decision in step 9 may use an interactive user-question tool. Use this shape:

```yaml
status: completed
reason: all reviews merged and builder completed
accepted_findings_count: 0
contradiction_rounds: 1
unresolved_items_count: 0
loop_rounds: 2
active_reviewers_count: 3
degraded_reviewer_ids: []
pre_review_bounces: 0

pre_reviewer:
  model_used: reviewer-low
  fallback_used: false
  session_id: sess_pre_review_final
  status: completed

reviewers:
  codex:
    model_used: codex-ultra
    fallback_used: false
    artifact_repair_used: false
    session_id: sess_codex_final
    status: completed
  glm5.3:
    primary_model: oc-ollama-cloud/glm-5.3
    fallback_model: oc-ollama-cloud/glm-5.2
    model_used: oc-ollama-cloud/glm-5.3
    fallback_used: false
    artifact_repair_used: false
    fallback_reason: null
    session_id: sess_glm53_or_glm52_final
    status: completed
  claude:
    model_used: claude-ultra
    fallback_used: false
    artifact_repair_used: false
    session_id: sess_claude_final
    status: completed

builder:
  model: coder-mid
  session_id: sess_build_final
  status: completed
```

For `status: ask`, include the normal state fields above and add `decision_request` in this shape, using the actual current limit, artifact path, and remaining findings in the question:

```yaml
decision_request:
  current_max_loop_rounds: 3
  merged_findings_path: .codex-artifacts/orchestrate-build-review/round-3/merged-findings.yaml
  question: "Round 3 reached the configured limit of 3. Requirement A is still missing. How should the workflow proceed?"
  options:
    - Continue for one additional round
    - Continue with a higher total-round limit (specify the new limit)
    - Stop here
```

Apply these output rules:

- Use top-level `status` values: `completed`, `ask`, `stopped`, `failed`. `ask` means the workflow is paused awaiting the user's loop-limit decision.
- Use agent-level `status` values: `completed`, `skipped`, `failed`.
- Always include `accepted_findings_count`, `contradiction_rounds`, `unresolved_items_count`, and `loop_rounds`.
- Always include `active_reviewers_count` and `degraded_reviewer_ids` based on the final reviewer set.
- Always return all three reviewer entries.
- Always return the builder entry.
- Always return the `pre_reviewer` entry with `model_used` and `fallback_used`, and `pre_review_bounces`, the total number of pre-review bounces across all rounds. Set `pre_reviewer.status` to `failed` when pre-review was disabled after a failure.
- Set `builder.model` to the resolved builder model used for all builder rounds.
- Use `session_id` consistently in both input and output.
- For every reviewer slot, include `model_used`, `fallback_used`, and `artifact_repair_used`. Set `artifact_repair_used: true` if any review or reconsideration artifact repair was attempted for that slot, whether or not it succeeded.
- For `claude`, set `model_used` to the resolved Claude reviewer model and always set `fallback_used: false`; selecting `fable` explicitly is not fallback behavior.
- For `glm5.3`, also include `primary_model`, `fallback_model`, and `fallback_reason`; set `fallback_reason: null` when no fallback was used. When invalid YAML caused fallback, include the post-repair validator diagnostics in `fallback_reason`.
- When processing fails before an agent launches, preserve the provided input `session_id` if one exists and mark that agent `status: skipped`.
- When an attempted reviewer launch fails or a reviewer is degraded after launch, preserve its provided or latest known `session_id` when available and mark that reviewer `status: failed`.
- A top-level `status: completed`, `status: ask`, or `status: stopped` may include one reviewer with `status: failed` when two reviewer slots remained active and the workflow otherwise reached that outcome.
- When processing fails after an agent launches or after stall detection, return the latest known `session_id` and mark that agent `status: failed`.
- When no `session_id` was ever observed for a failed newly started agent, set `session_id: null`.
- When processing stops because no accepted `needs_fix` findings remain and `done_criteria` is satisfied, set top-level `status: completed`; if degraded, mention the two-reviewer completion in `reason`.
- When processing stops because reviewer opinions do not converge, set top-level `status: stopped` and explain the contradiction outcome in `reason`.
- When the loop limit is reached with accepted `needs_fix` findings remaining, set top-level `status: ask`, explain that the workflow awaits the user's decision, and include `decision_request`. Preserve each agent's latest status and session id while waiting.
- When the user chooses to stop at the loop-limit decision, set top-level `status: stopped` and state that this was the user's decision. Omit `decision_request` once no decision is pending.
