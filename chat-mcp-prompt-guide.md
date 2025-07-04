# Chat MCP プロンプトガイド

## 🎯 必須要素（これだけあれば動作する）

### 1. **ルーム名**
```
例: "agent-collaboration", "debug-session", "team-chat"
```

### 2. **エージェント名**
```
例: "AgentA", "Scout", "Coordinator"
```

### 3. **基本動作の指示**（日本語でOK）
- 「ルームに入室」
- 「メッセージを送信」
- 「メッセージをチェック/確認」

## ✅ 推奨要素（より良い動作のために）

### 1. **役割の明確化**
```
例: 「あなたは[役割]です」
```

### 2. **メッセージフォーマット**
```
例: 「[エージェント名]: [内容]」という形式で送信
```

### 3. **チェック頻度**
```
例: 「5秒ごとに10回程度チェック」
```

### 4. **終了条件**
```
例: 「タスク完了まで」「20回チェックしたら終了」
```

## ❌ 不要な要素

1. **API関数名**: `mcp__chat__agent_communication_*` など
2. **パラメータ名**: `agentName`, `roomName`, `message` など
3. **技術的詳細**: JSON形式、エラーハンドリング方法など
4. **MCPの仕組み**: 内部動作の説明

## 📝 プロンプトテンプレート

### シンプル版（最小限）
```
あなたは[エージェント名]です。[ルーム名]ルームで活動します：
1. ルームに入室
2. 「[メッセージ]」を送信
3. 他のメッセージをチェック
```

### 標準版（推奨）
```
あなたは[役割]の[エージェント名]です。[ルーム名]ルームで[目的]を行います：

1. ルームに入室（エージェント名: [名前]）
2. 「[エージェント名]: [初期メッセージ]」と報告
3. メッセージを継続的にチェック（[頻度]）
4. [条件]の場合は[アクション]
5. [終了条件]まで続ける
```

### 高度な協調版
```
あなたは[役割]です。[ルーム名]ルームで他のエージェントと協調します：

役割：[具体的な責務]

1. ルームに入室（エージェント名: [名前]）
2. [初期状態/メッセージ]を報告
3. メッセージを継続的にチェック（[頻度]、[回数]）
4. [他エージェント]からの[特定メッセージ]を受けたら：
   - [レスポンスアクション]
   - 「[返信フォーマット]」で応答
5. [動的な条件判断]
6. [終了条件]

注意：
- [制約事項]
- [協調ルール]
```

## 💡 ベストプラクティス

### 1. **明確な識別子**
- ルーム名：目的が分かる名前（×room1 ○search-rescue）
- エージェント名：役割が分かる名前（×Agent1 ○Scout）

### 2. **メッセージ規約**
- 送信者を明示：「Scout: 発見しました」
- 状態を含める：「Coordinator: 状況把握完了」

### 3. **タイミング制御**
- 明示的な待機：「5秒ごとにチェック」
- 回数制限：「最大20回まで」

### 4. **協調パターン**
- リクエスト・レスポンス型
- 報告・指示型
- 状態共有型

## 🚀 実例

### 最小限の動作例
```
team-chatルームに入室して、「こんにちは」と送信し、
返事をチェックしてください。
```

### 実用的な例
```
あなたはWorker1です。task-roomで作業を行います：
1. ルームに入室（エージェント名: Worker1）
2. 「Worker1: 作業開始します」と送信
3. 5秒ごとにメッセージをチェック
4. Managerから指示があれば実行
5. 完了したら「Worker1: タスク完了」と報告
```

## 📊 複雑さレベル別ガイド

| レベル | 必要な要素 | 用途 |
|-------|---------|-----|
| 初級 | ルーム名、エージェント名、基本動作 | 単純なメッセージ交換 |
| 中級 | ＋役割、チェック頻度、条件分岐 | タスク実行、状態報告 |
| 上級 | ＋動的判断、協調ルール、エラー処理 | 複雑な協調作業 |

## 🎨 まとめ

**Chat MCPは自然言語に非常に寛容**です。技術的な詳細は不要で、人間同士のコミュニケーションを指示するように書けば動作します。

最も重要なのは：
1. **誰が**（エージェント名）
2. **どこで**（ルーム名）
3. **何をするか**（入室→送信→チェック）

を明確にすることです。