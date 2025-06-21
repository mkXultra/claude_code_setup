# ワークフローログ仕様書

## ログファイル構造

### 1. エージェント管理ログ (`agents.json`)
```json
{
  "workflow_id": "article-mcp-workflow-v1",
  "coordinator": {
    "type": "human|agent",
    "pid": null,
    "session_id": "current-session-id"
  },
  "agents": [
    {
      "agent_id": "agent-a-research",
      "role": "Research-Lead",
      "pid": 12345,
      "session_id": "76a05dbd-91ca-48cc-8142-6c2405c0d9f4",
      "status": "running|completed|failed",
      "started_at": "2025-06-20T14:30:00Z",
      "completed_at": null,
      "retry_count": 0,
      "error_log": [],
      "model": "opus|sonnet",
      "estimated_cost": {
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0
      }
    }
  ]
}
```

### 2. エラーハンドリングログ (`errors.json`)
```json
{
  "errors": [
    {
      "timestamp": "2025-06-20T14:35:00Z",
      "agent_id": "agent-b-writer",
      "error_type": "timeout|crash|api_error",
      "message": "Process terminated unexpectedly",
      "recovery_action": "restart_with_session",
      "session_id": "76a05dbd-91ca-48cc-8142-6c2405c0d9f4"
    }
  ]
}
```

### 3. ワークフロー状態ログ (`workflow-state.json`)
```json
{
  "workflow_status": "initializing|running|completed|failed",
  "total_retries": 0,
  "max_retries_per_agent": 5,
  "checkpoint": {
    "phase": "phase-1",
    "completed_agents": ["agent-a-research"],
    "pending_agents": ["agent-b-writer", "agent-c-code"]
  },
  "cost_tracking": {
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "total_cost_usd": 0.0,
    "by_model": {
      "opus": {
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0
      },
      "sonnet": {
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0
      }
    },
    "by_agent": {}
  }
}
```

### 4. コストサマリーログ (`cost-summary.json`)
```json
{
  "workflow_id": "article-mcp-workflow-v1",
  "completed_at": "2025-06-20T15:30:00Z",
  "duration_minutes": 60,
  "total_cost": {
    "input_tokens": 150000,
    "output_tokens": 50000,
    "cost_usd": 11.52
  },
  "model_breakdown": {
    "opus": {
      "agents": ["agent-d-review", "agent-e-integration"],
      "input_tokens": 50000,
      "output_tokens": 20000,
      "cost_usd": 5.50
    },
    "sonnet": {
      "agents": ["agent-a-research", "agent-b-writer", "agent-c-code", "agent-f-factcheck"],
      "input_tokens": 100000,
      "output_tokens": 30000,
      "cost_usd": 6.02
    }
  },
  "agent_breakdown": [
    {
      "agent_id": "agent-a-research",
      "model": "sonnet",
      "cost_usd": 1.20,
      "percentage": 10.4
    }
  ],
  "cost_efficiency": {
    "average_cost_per_phase": 3.84,
    "most_expensive_agent": "agent-d-review",
    "cost_optimization_suggestions": [
      "レビューエージェントのSonnet化を検討"
    ]
  }
}
```

## エラーリカバリープロトコル

1. **プロセス監視**
   - 1分ごとにPIDチェック
   - 応答なしの場合、session_idで再起動

2. **再起動手順**
   ```bash
   mcp__ccm__claude_code [
     session_id: "保存されたセッションID",
     prompt: "セッション再開：前回の作業を継続してください"
   ]
   ```

3. **失敗閾値**
   - 同一エージェント：最大5回まで再試行
   - 5回失敗後：ワークフロー終了、失敗レポート生成

4. **ログ更新タイミング**
   - エージェント起動時
   - エラー発生時
   - 状態変更時（running→completed/failed）
   - 1分ごとのヘルスチェック時
   - エージェント完了時（コスト更新）

## コスト計算プロトコル

### 1. **モデル料金設定**
```json
{
  "pricing": {
    "opus": {
      "input_per_1k": 0.015,
      "output_per_1k": 0.075
    },
    "sonnet": {
      "input_per_1k": 0.003,
      "output_per_1k": 0.015
    }
  }
}
```

### 2. **コスト追跡手順**
1. コーディネーターが各エージェントのセッションを監視
2. `get_claude_result`実行時にトークン数を取得
3. エージェント完了時に`agents.json`のestimated_costを更新
4. ワークフロー完了時に`cost-summary.json`を生成

### 3. **コスト最適化ルール**
- Opus使用率が50%超過時に警告
- 同一タスクでのリトライコストを追跡
- 効率的なモデル配分の提案を自動生成