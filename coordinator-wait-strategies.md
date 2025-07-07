# Coordinator Wait Strategies

## Basic Wait Patterns

### 1. Wait Strategy by Task Complexity

#### Simple Tasks (Complexity 1-3)
```
Initial check → 1 min wait → Check → 2 min wait → Check → ... → 10 min wait (max)
N = 1, 2, 3, ..., MAX(10)
```

#### Medium Tasks (Complexity 4-7)
```
Initial check → 2 min wait → Check → 3 min wait → Check → ... → 15 min wait (max)
N = 2, 3, 4, ..., MAX(15)
```

#### Complex Tasks (Complexity 8-10)
```
Initial check → 5 min wait → Check → 5 min wait → Check (fixed interval)
Total execution time: Maximum 30 minutes
```

### 2. Phased Wait Pattern

#### Phase 1: Initial Phase (First 10 minutes)
- Check every 1-2 minutes
- Suitable for quick response tasks

#### Phase 2: Middle Phase (10-20 minutes)
- Check every 3-5 minutes
- Balances resource usage and responsiveness

#### Phase 3: Late Phase (20+ minutes)
- Check every 5-10 minutes
- For long-running tasks

### 3. Adaptive Wait Strategy

```python
def calculate_wait_time(attempt, base_wait=60, factor=1.5, max_wait=600):
    """Calculate adaptive wait time with exponential backoff"""
    wait_time = min(base_wait * (factor ** attempt), max_wait)
    return int(wait_time)
```

### 4. Chat MCP-based Event-Driven Wait

#### Real-time Chat Monitoring
```
while True:
    messages = chat.list_messages(room_name, limit=10)
    
    # Process status updates
    for msg in messages:
        if "[COMPLETED]" in msg:
            return handle_completion()
        elif "[PROGRESS]" in msg:
            reset_timeout()
        elif "[ERROR]" in msg:
            return handle_error()
    
    sleep(30)  # Short interval for responsiveness
```

## Wait Strategy Selection Guide

### Selection Criteria

1. **Task Type**
   - Code analysis: Short initial waits (1-2 min)
   - Implementation: Medium waits (2-5 min)
   - Complex refactoring: Long waits (5-10 min)

2. **Agent Model**
   - Haiku: Quick responses, short waits
   - Sonnet: Balanced performance, medium waits
   - Opus: Deep analysis, longer waits

3. **Multi-agent Coordination**
   - Sequential: Fixed intervals
   - Parallel: Event-driven with chat monitoring
   - Hybrid: Adaptive based on progress

### Recommended Patterns

#### For Multi-Agent Bug Fix
```
Phase 1: Investigation (Opus)
  → Initial: 5 min
  → Recheck: every 2 min (max 3 times)
  
Phase 2: Implementation (Sonnet)
  → Initial: 3 min
  → Recheck: every 2 min (max 5 times)
  
Phase 3: Review (Opus)
  → Initial: 2 min
  → Recheck: every 1 min (iterative)
```

#### For Multi-Agent Investigation
```
Parallel agents:
  → Chat-based monitoring every 30 seconds
  → No fixed waits
  → Timeout after 20 minutes total
```

#### For TDD Feature Implementation
```
Per TDD cycle:
  → Red phase: 2-3 min
  → Green phase: 3-5 min
  → Refactor phase: 2-3 min
  → Review: 3 min initial, 2 min re-review
```

## Advanced Patterns

### 1. Intelligent Timeout with Progress Detection
```
max_silence_time = 10 minutes
last_activity = current_time

while not completed:
    status = check_agent_status()
    
    if status.has_new_output:
        last_activity = current_time
        wait_time = calculate_adaptive_wait(attempts=0)
    else:
        time_since_activity = current_time - last_activity
        if time_since_activity > max_silence_time:
            handle_timeout()
        wait_time = calculate_adaptive_wait(attempts)
    
    sleep(wait_time)
```

### 2. Priority-based Wait Adjustment
```
High priority:    base_wait * 0.5
Normal priority:  base_wait * 1.0
Low priority:     base_wait * 2.0
```

### 3. Resource-aware Waiting
```
If multiple agents running:
  → Increase wait intervals by 50%
  → Use chat coordination to reduce polling
  → Implement queue-based scheduling
```

## Best Practices

1. **Always implement maximum timeout**
   - Prevent infinite waits
   - Typical max: 30-45 minutes per workflow

2. **Use progressive backoff**
   - Start with short intervals
   - Increase gradually
   - Cap at reasonable maximum

3. **Monitor for activity, not just completion**
   - Reset timeout on any progress
   - Detect stuck agents early

4. **Prefer event-driven over polling**
   - Use Chat MCP for real-time updates
   - Reduce unnecessary waiting
   - Improve overall efficiency

5. **Log wait decisions**
   - Track actual vs expected times
   - Optimize based on patterns
   - Identify bottlenecks

## Implementation Examples

### Basic Sleep Command
```bash
# Simple fixed wait
sleep 120  # 2 minutes

# With status message
echo "Waiting for agent completion..." && sleep 180
```

### Advanced Monitoring Loop
```bash
attempt=0
max_attempts=10
base_wait=60

while [ $attempt -lt $max_attempts ]; do
    # Check agent status
    if check_completion; then
        echo "Agent completed successfully"
        break
    fi
    
    # Calculate wait time
    wait_time=$((base_wait * (attempt + 1)))
    [ $wait_time -gt 600 ] && wait_time=600
    
    echo "Attempt $attempt: Waiting ${wait_time}s..."
    sleep $wait_time
    
    attempt=$((attempt + 1))
done
```

### Chat-based Coordination
```bash
# Monitor chat for completion signals
while true; do
    messages=$(get_chat_messages "$ROOM_NAME")
    
    if echo "$messages" | grep -q "\[COMPLETED\]"; then
        echo "Task completed via chat signal"
        break
    fi
    
    sleep 30  # Quick checks for responsiveness
done
```

## Metrics and Optimization

### Key Metrics to Track
1. **Average wait time per task type**
2. **Actual completion time vs first check**
3. **Number of unnecessary checks**
4. **Resource utilization during waits**

### Optimization Strategies
1. **Analyze historical data**
   - Identify patterns by task type
   - Adjust base wait times accordingly

2. **Implement smart predictions**
   - Use task complexity estimation
   - Consider agent workload

3. **Dynamic adjustment**
   - Learn from recent completions
   - Adapt to system performance

## Summary

Effective wait strategies are crucial for multi-agent workflow efficiency. The key is to balance:
- **Responsiveness**: Quick detection of completion
- **Efficiency**: Minimize unnecessary polling
- **Reliability**: Handle edge cases and timeouts
- **Adaptability**: Adjust to different scenarios

Choose the appropriate strategy based on your specific use case, and always prefer event-driven coordination when available.