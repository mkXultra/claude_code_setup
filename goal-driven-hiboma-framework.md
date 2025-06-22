# Goal-Driven HIBOMA Execution Framework

## Core Principle: Start with WHY, not HOW

---

## 1. Goal Analysis Protocol

Every task begins with structured goal decomposition:

```python
class Goal:
    def __init__(self, description):
        self.what = extract_deliverable(description)
        self.why = extract_purpose(description)
        self.constraints = extract_constraints(description)
        self.success_criteria = extract_criteria(description)
    
    def analyze_requirements(self):
        return {
            "knowledge_needed": self.what_knowledge_required(),
            "skills_needed": self.what_skills_required(),
            "coordination_complexity": self.estimate_coordination_needs(),
            "uncertainty_level": self.estimate_unknowns()
        }
```

---

## 2. Goal → Strategy Mapping

### 2.1 Goal Patterns and Optimal Strategies

| Goal Pattern | Characteristics | HIBOMA Strategy | Initial Structure |
|--------------|----------------|-----------------|-------------------|
| **Discovery** | High uncertainty, broad search | HierTS-heavy | Wide exploration tree |
| **Construction** | Clear specs, parallel work | LOCO-heavy | Specialized teams |
| **Analysis** | Deep understanding needed | TGN-heavy | Knowledge synthesis focus |
| **Optimization** | Iterative improvement | VTA-heavy | Dynamic rebalancing |
| **Debug** | Root cause analysis, systematic | HierTS+TGN | Diagnostic hierarchy |
| **Migration** | Phased transition, compatibility | LOCO+VTA | Parallel validation teams |
| **Integration** | System connectivity, interfaces | LOCO+TGN | Interface mapping teams |
| **Monitoring** | Continuous observation, metrics | VTA+TGN | Distributed collectors |
| **Documentation** | Knowledge extraction, clarity | TGN-heavy | Knowledge mining tree |
| **Testing** | Coverage, validation, quality | LOCO+VTA | Parallel test execution |

### 2.2 Automated Strategy Selection

```python
def select_strategy(goal):
    requirements = goal.analyze_requirements()
    
    # Decision tree based on goal characteristics
    if requirements["uncertainty_level"] > 0.7:
        return DiscoveryStrategy(
            emphasis="exploration",
            initial_structure="Opus → Sonnet×5 → Haiku×10",
            algorithm_weights={"HierTS": 0.6, "LOCO": 0.2, "TGN": 0.2}
        )
    
    elif requirements["coordination_complexity"] > 0.8:
        return IntegrationStrategy(
            emphasis="synthesis",
            initial_structure="Opus → Sonnet_coordinator → Sonnet_teams×N",
            algorithm_weights={"TGN": 0.5, "LOCO": 0.3, "HierTS": 0.2}
        )
    
    elif requirements["skills_needed"].is_homogeneous():
        return ParallelExecutionStrategy(
            emphasis="efficiency",
            initial_structure="Sonnet → Haiku×8",
            algorithm_weights={"LOCO": 0.6, "VTA": 0.3, "HierTS": 0.1}
        )
    
    else:
        return AdaptiveStrategy(
            emphasis="learning",
            initial_structure="Opus → Sonnet",  # Minimal start
            algorithm_weights="balanced"
        )
```

---

## 3. Execution Templates by Goal Type

### 3.1 Discovery Goals
**Example**: "Find all security vulnerabilities in this codebase"

```python
DISCOVERY_TEMPLATE = """
Goal Analysis:
- What: Security vulnerabilities (unknown location, unknown types)
- Why: Ensure system security
- Constraint: Must be thorough
- Success: All critical vulnerabilities found

Strategy: Progressive Discovery with HierTS
1. Start broad (Haiku sweep for obvious issues)
2. Deepen where complexity found (Sonnet analysis)
3. Expert review for subtle issues (Opus verification)

Initial prompt for Opus:
'Your goal is discovering all security vulnerabilities.
Use HierTS to adaptively explore based on discovered complexity.
Start with wide Haiku sweep, deepen with Sonnet where needed.'
"""
```

### 3.2 Construction Goals
**Example**: "Build a REST API with authentication"

```python
CONSTRUCTION_TEMPLATE = """
Goal Analysis:
- What: REST API with specific features
- Why: Enable secure data access
- Constraint: Must follow REST principles
- Success: All endpoints working with auth

Strategy: Parallel Construction with LOCO
1. Decompose into independent modules
2. Assign specialized teams
3. Coordinate through interfaces

Initial prompt for Opus:
'Your goal is building a REST API with authentication.
Use LOCO for efficient parallel development.
Create specialized teams: auth_team, endpoint_team, testing_team.'
"""
```

### 3.3 Analysis Goals
**Example**: "Understand customer behavior patterns in logs"

```python
ANALYSIS_TEMPLATE = """
Goal Analysis:
- What: Behavior patterns (requires synthesis)
- Why: Improve user experience
- Constraint: Must be actionable insights
- Success: Clear patterns with recommendations

Strategy: Knowledge Building with TGN
1. Distributed log analysis
2. Pattern recognition at each level
3. Synthesis of insights upward

Initial prompt for Opus:
'Your goal is understanding customer behavior patterns.
Use TGN for effective knowledge aggregation.
Build analysis hierarchy focusing on pattern synthesis.'
"""
```

### 3.4 Optimization Goals
**Example**: "Reduce application response time by 50%"

```python
OPTIMIZATION_TEMPLATE = """
Goal Analysis:
- What: Performance improvement (measurable)
- Why: Better user experience
- Constraint: Maintain functionality
- Success: 50% reduction achieved

Strategy: Iterative Optimization with VTA
1. Profile current performance
2. Identify bottlenecks
3. Dynamically allocate resources to biggest impacts

Initial prompt for Opus:
'Your goal is reducing response time by 50%.
Use VTA for dynamic resource allocation.
Continuously rebalance efforts toward highest-impact areas.'
"""
```

### 3.5 Debug Goals
**Example**: "Debug the memory leak in our application"

ゴール分析：
- 何を：メモリリーク（特定の問題、原因不明）
- なぜ：アプリケーションの安定性修正
- 制約：実行中システムへの影響最小化
- 成功：根本原因の特定と修正

戦略：HierTS+TGNによる体系的診断
1. 問題の再現（Haiku監視）
2. 容疑箇所の絞り込み（HierTS探索）
3. 症状の相関分析（TGN知識統合）
4. 修正の検証（制御されたテスト）

### 3.6 Migration Goals
**Example**: "Migrate from MySQL to PostgreSQL"

ゴール分析：
- 何を：データベース移行（明確な開始・終了状態）
- なぜ：パフォーマンスと機能向上
- 制約：データ損失ゼロ、ダウンタイム最小
- 成功：検証済みの完全移行

戦略：LOCO+VTAによる段階的移行
1. スキーマ分析とマッピング
2. 並列データ移行パイプライン
3. 各フェーズでの検証
4. カットオーバー調整

### 3.7 Integration Goals
**Example**: "Integrate payment gateway into our platform"

ゴール分析：
- 何を：決済ゲートウェイ統合
- なぜ：決済処理の有効化
- 制約：PCIコンプライアンス必須
- 成功：セキュアで動作する統合

戦略：LOCO+TGNによるインターフェースマッピング
1. API分析とマッピング
2. セキュリティ実装
3. エラーハンドリング設計
4. エンドツーエンドテスト

### 3.8 Monitoring Goals
**Example**: "Set up comprehensive application monitoring"

ゴール分析：
- 何を：監視システム（メトリクス、ログ、アラート）
- なぜ：運用の可視性
- 制約：パフォーマンスオーバーヘッド低減
- 成功：完全な可観測性の達成

戦略：VTA+TGNによる分散収集
1. メトリクス特定
2. コレクターデプロイ
3. ダッシュボード作成
4. アラート設定

### 3.9 Documentation Goals
**Example**: "Document our API architecture"

ゴール分析：
- 何を：APIドキュメント（包括的、明確）
- なぜ：開発者オンボーディング
- 制約：保守可能であること
- 成功：完全で正確なドキュメント

戦略：TGNによる知識抽出
1. API発見のためのコード分析
2. 使用パターン抽出
3. サンプル生成
4. ドキュメント統合

### 3.10 Testing Goals
**Example**: "Create comprehensive test suite"

ゴール分析：
- 何を：テストスイート（単体、統合、E2E）
- なぜ：品質保証
- 制約：最低80%カバレッジ
- 成功：全テスト合格、カバレッジ達成

戦略：LOCO+VTAによる並列テスト
1. テストケース生成
2. 並列テスト実行
3. カバレッジ分析
4. 継続的インテグレーション

---

## 4. Dynamic Adaptation Based on Progress

### 4.1 Goal-Aware Monitoring

```python
class GoalMonitor:
    def __init__(self, goal, strategy):
        self.goal = goal
        self.strategy = strategy
        self.progress_indicators = self.define_indicators()
    
    def should_adapt_strategy(self, current_state):
        progress = self.measure_progress(current_state)
        
        if progress.is_blocked():
            return "increase_exploration"  # More HierTS
        
        elif progress.is_inefficient():
            return "improve_coordination"  # More LOCO
        
        elif progress.lacks_synthesis():
            return "enhance_integration"  # More TGN
        
        elif progress.is_imbalanced():
            return "rebalance_load"  # More VTA
        
        return None
```

### 4.2 Strategy Evolution Examples

```
Initial: "Find bugs" → Wide search
→ (found complex area)
Adapted: "Understand complex module" → Deep analysis
→ (understanding achieved)
Adapted: "Fix interconnected issues" → Coordinated repair
```

---

## 5. Success Criteria and Termination

### 5.1 Goal-Specific Success Metrics

```python
def evaluate_success(goal, current_state):
    if goal.type == "discovery":
        return coverage_achieved(current_state) > goal.required_coverage
    
    elif goal.type == "construction":
        return all_requirements_met(current_state, goal.requirements)
    
    elif goal.type == "analysis":
        return insights_quality(current_state) > goal.quality_threshold
    
    elif goal.type == "optimization":
        return improvement_achieved(current_state) >= goal.target_improvement
```

### 5.2 Termination Decision

```python
def should_terminate(goal, current_state, resources):
    return any([
        goal.is_achieved(current_state),
        resources.exhausted(),
        marginal_value(resources) < threshold,
        goal.deadline_reached()
    ])
```

---

## 6. Practical Implementation Guide

### 6.1 For Opus Agents

```
When you receive a task:

1. FIRST: Analyze the goal
   - What exactly needs to be achieved?
   - What type of goal is this?
   - What are the success criteria?

2. SECOND: Select appropriate strategy
   - Match goal type to strategy template
   - Determine algorithm emphasis
   - Choose initial structure

3. THIRD: Execute with goal awareness
   - Monitor progress toward goal
   - Adapt strategy based on discoveries
   - Terminate when goal achieved

Remember: The goal drives everything. HIBOMA is just the tool.
```

### 6.2 Key Prompting Pattern

```
Instead of: "Use HIBOMA to analyze these files"
Use: "Goal: Understand the architecture of this codebase
      Constraint: 200 unit budget
      Success: Can diagram all major components
      
      Apply appropriate coordination strategy."
```

---

## 7. Meta-Learning: Goal → Strategy Mappings

Over time, the system learns:

```python
learned_mappings = {
    "security_audit": {
        "best_strategy": "progressive_discovery",
        "typical_structure": "Opus → Sonnet×5 → Haiku×10",
        "key_algorithms": ["HierTS", "TGN"],
        "average_cost": 156,
        "success_rate": 0.89
    },
    "api_development": {
        "best_strategy": "parallel_construction",
        "typical_structure": "Opus → Sonnet×4 → Haiku×12",
        "key_algorithms": ["LOCO", "VTA"],
        "average_cost": 203,
        "success_rate": 0.94
    }
    # ... more learned patterns
}
```

This enables: "Goal: Security audit" → Instant optimal strategy

---

## Remember

**The goal is not to use HIBOMA. The goal is to achieve the user's objective efficiently.**

HIBOMA algorithms are powerful tools, but they must serve the goal, not become the goal.

