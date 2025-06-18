# Claude Code Model Selection Guide: Opus vs Sonnet vs Haiku

*Claude Codeでのモデル選択参考資料*

## Quick Decision Tree

```
Start Here
    │
    ├─ Is this highest complexity/scale work?
    │   ├─ YES → Use opus
    │   └─ NO → Continue ↓
    │
    ├─ Is this for production use?
    │   ├─ YES → Use sonnet
    │   └─ NO → Continue ↓
    │
    ├─ Does it involve security/auth?
    │   ├─ YES → Use sonnet
    │   └─ NO → Continue ↓
    │
    ├─ Is it a complex system/architecture?
    │   ├─ YES → Use sonnet
    │   └─ NO → Continue ↓
    │
    ├─ Will others maintain this code?
    │   ├─ YES → Use sonnet
    │   └─ NO → Continue ↓
    │
    ├─ Is it a simple utility/script?
    │   ├─ YES → Can use claude-3-5-haiku-20241022
    │   └─ NO → Use sonnet
```

## Instant Selection Guide

### Use `opus` (Maximum Capability)
- 🏗️ **Large-Scale System Design**
- 🧠 **Complex Algorithm Development**
- 📚 **Research & Advanced Analysis**
- 🎯 **Multi-System Integration**
- 🧩 **Advanced Problem Solving**
- 🔬 **Machine Learning Architecture**
- 📖 **Advanced Technical Writing**

### Use `sonnet` (Production Standard)
- 🏢 **Enterprise Applications**
- 🔐 **Security-Critical Code**
- 🏗️ **Standard System Architecture**
- 🐛 **Production Debugging**
- 💳 **Financial Systems**
- 🏥 **Healthcare Applications**
- 📊 **Data Processing Pipelines**
- 🚀 **Performance Optimization**
- 👥 **Team Projects**
- 📝 **API Development**

### Consider `claude-3-5-haiku-20241022` Only For
- 📜 **Single-file Scripts**
- 🧪 **Learning Exercises**
- 🔧 **Quick Utilities**
- 🎯 **Prototypes** (plan to rewrite)

## Task Complexity Matrix

| Complexity Indicators | Model Choice | Why |
|----------------------|--------------|-----|
| **Advanced Research/Design** | `opus` | Maximum reasoning capability |
| **Large-scale Architecture** | `opus` | Complex system understanding |
| **Novel Algorithm Development** | `opus` | Advanced problem solving |
| **Multiple files/modules** | `sonnet` | Better architecture patterns |
| **Database operations** | `sonnet` | SQL injection prevention |
| **User authentication** | `sonnet` | Security best practices |
| **API endpoints** | `sonnet` | Production-ready features |
| **Error handling needed** | `sonnet` | Comprehensive coverage |
| **Performance matters** | `sonnet` | Optimization strategies |
| **Docker/K8s deployment** | `sonnet` | DevOps best practices |
| **Testing required** | `sonnet` | Complete test suites |

## Code Examples: When to Use Each

### `opus` Required: System Architecture
```bash
claude --model opus "Design distributed microservices architecture"
# Opus provides:
# - Service mesh design
# - Event sourcing patterns
# - CQRS implementation
# - Circuit breaker patterns
# - Advanced monitoring strategy
# - Scalability planning
# - Performance modeling
# - Technology selection analysis
```

### `sonnet` Required: API Endpoint
```bash
claude --model sonnet "Create user registration endpoint"
# Sonnet provides:
# - Input validation
# - SQL injection prevention  
# - Password hashing
# - Rate limiting
# - Error handling
# - Logging
# - Response schemas
# - OpenAPI documentation
```

### `claude-3-5-haiku-20241022` Acceptable: File Renaming
```bash
claude --model claude-3-5-haiku-20241022 "Rename files in directory"
# Haiku sufficient for:
# - Basic os.rename() operations
# - Simple string manipulation
# - Basic error catching
```

## Team Development Guidelines

### Architecture Team
- **System Design**: `opus`
- **Technology Evaluation**: `opus`  
- **Research & POCs**: `opus`
- **Architecture Reviews**: `opus`

### Frontend Team
- **Component Architecture**: `sonnet`
- **State Management**: `sonnet`
- **Simple UI Utilities**: `claude-3-5-haiku-20241022`
- **CSS Helpers**: `claude-3-5-haiku-20241022`

### Backend Team
- **API Development**: `sonnet`
- **Database Models**: `sonnet`
- **Business Logic**: `sonnet`
- **Dev Scripts**: `claude-3-5-haiku-20241022`

### DevOps Team
- **Infrastructure Code**: `sonnet`
- **CI/CD Pipelines**: `sonnet`
- **Monitoring Setup**: `sonnet`
- **Quick Scripts**: `claude-3-5-haiku-20241022`

## Time-Based Selection

### Urgent Deadline?
```
Need complex architecture decision NOW?
    → opus (gets design right first time)

Need it in production TODAY?
    → sonnet (gets it right first time)

Just experimenting?
    → Any model

Building for the future?
    → sonnet (maintainable code)
```

## Quality Requirements

### Maximum Quality Needed
- Research publications → `opus`
- Advanced architecture → `opus`
- Complex problem solving → `opus`

### High Quality Needed
- Code reviews required → `sonnet`
- Compliance audits → `sonnet`
- Customer-facing → `sonnet`
- Open source project → `sonnet`

### Lower Stakes
- Personal scripts → `claude-3-5-haiku-20241022`
- Throwaway code → `claude-3-5-haiku-20241022`
- Learning only → `claude-3-5-haiku-20241022`

## Common Scenarios

### Scenario 1: "Design enterprise system architecture"
**Choose**: `opus`
**Why**: Requires maximum reasoning, complex trade-offs, long-term thinking

### Scenario 2: "Build a REST API"
**Choose**: `sonnet`
**Why**: Needs auth, validation, error handling, documentation

### Scenario 3: "Parse a CSV file"
**Choose**: `sonnet` if production, `claude-3-5-haiku-20241022` if one-time script
**Why**: Production needs error handling, streaming, validation

### Scenario 4: "Debug production issue"
**Choose**: `sonnet`
**Why**: Complex root cause analysis, multiple factors

### Scenario 5: "Research new ML algorithms"
**Choose**: `opus`
**Why**: Advanced analysis, novel approaches, research depth

### Scenario 6: "Rename variables in file"
**Choose**: `claude-3-5-haiku-20241022`
**Why**: Simple find/replace operation

### Scenario 7: "Design microservices"
**Choose**: `sonnet` (or `opus` for large-scale)
**Why**: Architecture decisions, opus for enterprise scale

## Red Flags: Always Use `sonnet`

🚨 **User data involved**
🚨 **Money/payments**
🚨 **Authentication/authorization**
🚨 **External API integration**
🚨 **Database operations**
🚨 **Concurrent operations**
🚨 **File uploads**
🚨 **Email sending**
🚨 **Cryptographic operations**
🚨 **Third-party dependencies**

## The 5-Second Rule

If you spend more than 5 seconds thinking about which model to use:

For **complex design/research** → **Use `opus`**
For **everything else** → **Use `sonnet`**

The quality difference is significant enough that when in doubt, choose the higher capability model.

## Migration Checklist

Starting with `claude-3-5-haiku-20241022` code? Upgrade to `sonnet` when:
- [ ] Adding authentication
- [ ] Connecting to database
- [ ] Handling user input
- [ ] Going to production
- [ ] Others will use it
- [ ] Security matters
- [ ] Performance matters

## Summary

**For Complex Design/Research**: `opus`
**Default Choice**: `sonnet`
**Exception**: Only use `claude-3-5-haiku-20241022` for trivial, throwaway scripts

The capability hierarchy ensures you get the right level of intelligence for your task:
- **`opus`**: Maximum reasoning for complex problems
- **`sonnet`**: Production-ready code with 84% quality improvement
- **`claude-3-5-haiku-20241022`**: Fast iteration for simple tasks

## Claude Code Usage Examples

```bash
# Complex system design
claude --model opus "Design a scalable event-driven architecture"

# Production development
claude --model sonnet "Create a secure user authentication system"

# Simple scripts
claude --model claude-3-5-haiku-20241022 "Write a script to backup files"
```