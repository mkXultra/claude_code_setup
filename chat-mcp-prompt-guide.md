# Chat MCP Prompt Guide

## 🎯 Essential Elements (Minimum requirements for operation)

### 1. **Room Name**
```
Examples: "agent-collaboration", "debug-session", "team-chat"
```

### 2. **Agent Name**
```
Examples: "AgentA", "Scout", "Coordinator"
```

### 3. **Basic Action Instructions** (Natural language OK)
- "Enter the room"
- "Send message"
- "Check/monitor messages"

## ✅ Recommended Elements (For better operation)

### 1. **Role Clarification**
```
Example: "You are [role]"
```

### 2. **Message Format**
```
Example: Send in format "[Agent Name]: [Content]"
```

### 3. **Check Frequency**
```
Example: "Check every 5 seconds, about 10 times"
```

### 4. **Termination Condition**
```
Example: "Until task completion" or "End after 20 checks"
```

## ❌ Unnecessary Elements

1. **API Function Names**: `mcp__chat__agent_communication_*` etc.
2. **Parameter Names**: `agentName`, `roomName`, `message` etc.
3. **Technical Details**: JSON format, error handling methods, etc.
4. **MCP Mechanics**: Internal operation explanations

## 📝 Prompt Templates

### Simple Version (Minimal)
```
You are [Agent Name]. Operate in [Room Name] room:
1. Enter the room
2. Send "[Message]"
3. Check other messages
```

### Standard Version (Recommended)
```
You are [Agent Name] with role of [Role]. Perform [Purpose] in [Room Name] room:

1. Enter room (agent name: [Name])
2. Report "[Agent Name]: [Initial Message]"
3. Continuously check messages ([Frequency])
4. If [Condition], then [Action]
5. Continue until [Termination Condition]
```

### Advanced Coordination Version
```
You are [Role]. Coordinate with other agents in [Room Name] room:

Role: [Specific Responsibilities]

1. Enter room (agent name: [Name])
2. Report [Initial State/Message]
3. Continuously check messages ([Frequency], [Count])
4. When receiving [Specific Message] from [Other Agent]:
   - [Response Action]
   - Respond with "[Reply Format]"
5. [Dynamic Condition Judgment]
6. [Termination Condition]

Notes:
- [Constraints]
- [Coordination Rules]
```

## 💡 Best Practices

### 1. **Clear Identifiers**
- Room names: Purpose-clear names (❌room1 ✓search-rescue)
- Agent names: Role-clear names (❌Agent1 ✓Scout)

### 2. **Message Conventions**
- Identify sender: "Scout: Found something"
- Include state: "Coordinator: Situation assessment complete"

### 3. **Timing Control**
- Explicit waiting: "Check every 5 seconds"
- Count limits: "Maximum 20 times"

### 4. **Coordination Patterns**
- Request-Response type
- Report-Instruction type
- State-Sharing type

## 🚀 Examples

### Minimal Working Example
```
Enter the team-chat room, send "Hello", and check for replies.
```

### Practical Example
```
You are Worker1. Perform tasks in task-room:
1. Enter room (agent name: Worker1)
2. Send "Worker1: Starting work"
3. Check messages every 5 seconds
4. Execute if instructions from Manager
5. Report "Worker1: Task completed" when done
```

## 📊 Complexity Level Guide

| Level | Required Elements | Use Case |
|-------|------------------|----------|
| Basic | Room name, agent name, basic actions | Simple message exchange |
| Intermediate | + Role, check frequency, conditionals | Task execution, status reports |
| Advanced | + Dynamic judgment, coordination rules, error handling | Complex collaborative work |

## 🎨 Summary

**Chat MCP is very tolerant of natural language**. Technical details are unnecessary - write as if instructing human-to-human communication and it will work.

Most important is to clarify:
1. **Who** (Agent name)
2. **Where** (Room name)
3. **What to do** (Enter → Send → Check)