# Refactoring v5 ワークフロー実行ガイド

## 概要
このガイドは、Claude Codeがユーザーのリファクタリング要求を受けて、v5自律型ワークフローを実行するための手順です。
v5テンプレート（refactoring-workflow-v5-template.md）を使用して、様々なタイプのリファクタリングタスクを実行できます。

**対象読者**: Claude Codeが参照して、リファクタリング要求に対応するためのガイドです。

## 重要な注意事項
**このワークフローでは、Claude Codeは直接リファクタリング作業を行いません。**
代わりに、以下の手順でコーディネーターエージェントを起動し、全ての作業をコーディネーターに委任します：

1. 要件ドキュメントを作成
2. Git worktreeで独立した作業環境を準備
3. mcp__ccm__claude_codeツールでコーディネーターエージェントを起動
4. コーディネーターが自律的にリファクタリングを完了するまで監視

**Claude Codeの役割は、環境準備とコーディネーター起動のみです。**

## 実行フロー

### 1. ユーザー要求の受付
ユーザー: 「{{REFACTORING_REQUEST}}」
例：
- 「as anyを削除してください」
- 「ESLint違反を修正してください」
- 「パフォーマンスを最適化してください」
- 「TypeScriptの型安全性を改善してください」

### 2. 要件の整理
Claude Codeは対話的に情報を収集し、自然言語形式で要件をまとめます。

#### 要件ドキュメントの形式
```markdown
# リファクタリング要件

## ユーザーの要望
[ユーザーの最初の要望をそのまま記載]

## 対話で明確になった詳細

### 対象範囲
[ユーザーの回答をそのまま記載]
例：
- src/ディレクトリ配下のすべてのTypeScriptファイル
- 特定のコンポーネント群
- プロジェクト全体

### 必須成功基準
[ユーザーが指定した必須要件]
例：
- TypeScriptのコンパイルエラーが0になること
- 既存のテストがすべて通ること
- 指定されたLintルール違反が0になること

### 品質向上目標
[ユーザーが期待する追加的な改善]
例：
- ビルド時間の短縮
- バンドルサイズの削減
- コードカバレッジの向上

### 制約条件
[ユーザーが述べた制約]
例：
- 特定のライブラリのバージョンは変更しない
- APIインターフェースは変更しない
- 実行時の動作は完全に同一にする
```

### 3. 対話的な情報収集テンプレート

```markdown
## リファクタリングのための情報を教えてください

1. **具体的な改善対象**は何ですか？
   - 型安全性（as any削除、型定義改善など）
   - コード品質（ESLint違反、コードスメルなど）
   - パフォーマンス（ビルド時間、実行速度など）
   - アーキテクチャ（依存関係、モジュール構造など）
   → [ユーザー回答を待つ]

2. **対象範囲**を教えてください：
   - 特定のディレクトリやファイル
   - ファイルパターン（例：*.tsx、*.test.tsなど）
   - プロジェクト全体
   → [ユーザー回答を待つ]

3. **品質基準**を教えてください：
   - 必須要件（テスト通過、型エラーなしなど）
   - 望ましい改善（パフォーマンス、可読性など）
   → [ユーザー回答を待つ]

4. **制約条件**はありますか？
   - 避けるべき変更
   - 時間的制約
   - 特定のツールやライブラリの使用
   → [ユーザー回答を待つ]
```

### 4. 要件の確認とコーディネーター起動

```markdown
## 確認
以下の要件でリファクタリングを実行します：

[要件ドキュメントの内容を表示]

よろしいですか？

## Claude Codeの実行
ユーザーの確認が取れたら、Claude Codeが直接コーディネーターエージェントを起動します。
```

### 5. Claude Codeによるコーディネーター起動

**重要**: 以下の処理はClaude Codeが実行しますが、実際のリファクタリング作業はすべてコーディネーターエージェントが行います。

Claude Codeが実行する処理：

```python
# 1. Git Worktreeの作成
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
task_name = extract_task_name(user_request)  # 例: "remove-any-assertions"
work_dir = f"../refactor-{task_name}-{timestamp}"

# Git worktree作成
subprocess.run(["git", "worktree", "add", work_dir])

# 環境ファイルのコピー
for env_file in glob.glob(".env*"):
    shutil.copy(env_file, work_dir)

# node_modulesのシンボリックリンク
os.symlink(
    os.path.abspath("node_modules"),
    os.path.join(work_dir, "node_modules")
)

# guideディレクトリのシンボリックリンク
os.symlink(
    os.path.abspath("guide"),
    os.path.join(work_dir, "guide")
)

# 2. 要件ドキュメントの保存
requirements_path = os.path.join(work_dir, "refactoring-requirements.md")
with open(requirements_path, "w") as f:
    f.write(requirements_doc)

# 3. コーディネータープロンプトの作成
coordinator_prompt = f"""
# v5 自律型リファクタリングコーディネーター

## 作業ディレクトリ
現在のディレクトリ（{work_dir}）で作業を実行してください。
このディレクトリに存在するコードを対象にリファクタリングを行います。

## 重要な前提条件
- ログ管理プロトコルファイルが必ず存在すること
- 存在しない場合は作業を開始しないこと

## 初期タスク
1. refactoring-requirements.md を読み込んで要件を理解
2. guide/refactoring-workflow-v5-template.md を読み込んでテンプレートを理解
3. ログ管理プロトコルファイル（workflow-log-spec.md等）を探して必ず読み込む
   - guideディレクトリ内を検索
   - 見つからない場合は作業を中断してエラーを報告
4. プロトコルファイルの指示に従ってログ管理を実施
5. 要件に基づいて、テンプレートのプレースホルダーを具体的な内容に置き換え
6. 要件に基づいて初期複雑度評価（1-10）を実施

## リファクタリング要件
{requirements_doc}

## 実行指示
上記の要件に従って、v5自律型ワークフローを実行してください。
すべてのエージェントは現在の作業ディレクトリ（{work_dir}）で起動してください。

### 動的判断の考慮事項
- 影響範囲が5ファイル以上の場合は追加エージェントを検討
- テスト失敗が多い場合はデバッグエージェントを起動
- パフォーマンス問題を検出したら最適化エージェントを起動
- アーキテクチャレベルの変更が必要な場合は設計エージェントを起動

### 品質基準
必須:
- TypeScriptコンパイルエラー: 0
- 既存テスト成功率: 100%
- 機能的後退: なし

品質達成まで自律的に継続してください。
開始してください。
"""

# 4. コーディネーターエージェントの起動
os.chdir(work_dir)
mcp__ccm__claude_code(
    model="opus",
    workFolder=work_dir,  # 明示的に作業ディレクトリを指定
    prompt=coordinator_prompt
)
```

## 要件ドキュメントの例

### 型安全性改善の例
```markdown
# リファクタリング要件

## ユーザーの要望
プロジェクト内のすべての`as any`を削除して、型安全性を向上させてください

## 対話で明確になった詳細

### 対象範囲
src/ディレクトリ配下のすべての.ts/.tsxファイル
ただし、テストファイル（*.test.ts, *.spec.ts）は除外

### 必須成功基準
- TypeScriptのコンパイルエラーが0
- 既存のテストがすべて通る
- 新たなLintエラーが発生しない

### 品質向上目標
- より厳密な型定義の使用
- 型推論の活用による冗長な型注釈の削除
- 型ガードの適切な使用

### 制約条件
- 実行時の動作は変更しない
- パブリックAPIの型定義は変更しない
```

### ESLint違反修正の例
```markdown
# リファクタリング要件

## ユーザーの要望
ESLintのルール違反をすべて修正してください

## 対話で明確になった詳細

### 対象範囲
- src/components/配下のすべてのReactコンポーネント
- src/hooks/配下のカスタムフック

### 必須成功基準
- 指定ディレクトリ内のESLintエラーが0
- 既存のテストがすべて通る
- TypeScriptのコンパイルエラーが発生しない

### 品質向上目標
- 一貫性のあるコードスタイル
- React Hooks のベストプラクティスに準拠
- アクセシビリティの改善

### 制約条件
- 自動修正で対応できない箇所は手動で修正
- コメントでのルール無効化は最小限に
```

### パフォーマンス最適化の例
```markdown
# リファクタリング要件

## ユーザーの要望
ビルド時間を短縮し、バンドルサイズを削減してください

## 対話で明確になった詳細

### 対象範囲
プロジェクト全体のビルド設定とソースコード

### 必須成功基準
- アプリケーションの動作が変わらない
- すべてのテストが通る
- ビルドが正常に完了する

### 品質向上目標
- ビルド時間を30%以上短縮
- バンドルサイズを20%以上削減
- 初回ロード時間の改善

### 制約条件
- 主要な依存関係のバージョンは変更しない
- IE11のサポートは維持する
- 開発体験を損なわない
```

## プロセス監視と進捗管理

### エージェントの監視
```bash
# 5分ごとに自動実行
while true; do
  # プロセス一覧の確認
  processes=$(mcp__ccm__list_claude_processes)
  
  # Chat MCPから最新の進捗を取得
  messages=$(mcp__chat__agent_communication_get_messages \
    --roomName "refactor-${TASK_NAME}-main" \
    --limit 10)
  
  # 進捗のサマリーを表示
  echo "=== リファクタリング進捗 ==="
  echo "アクティブエージェント: $(echo $processes | jq '.active_count')"
  echo "完了タスク: $(echo $messages | grep -c 'COMPLETE')"
  echo "発見された問題: $(echo $messages | grep -c 'ISSUE')"
  
  # 完了チェック
  if grep -q "REFACTORING_COMPLETE" <<< "$messages"; then
    echo "リファクタリングが完了しました！"
    break
  fi
  
  sleep 300
done
```

## トラブルシューティング

### よくある問題
1. **複雑度の過小評価**
   - 初期評価で単純と判断されたが、実際は複雑だった
   - 対策: コーディネーターが動的に追加エージェントを起動

2. **テスト環境の問題**
   - テストの実行に特別な設定が必要
   - 対策: 環境準備フェーズでテスト実行を確認

3. **予期しない依存関係**
   - リファクタリングが他のモジュールに影響
   - 対策: 調査フェーズで依存関係を完全に把握

## 拡張可能性

### タスクタイプ別の特化
今後追加可能な専門実装：
- `refactoring-workflow-v5-typescript.md` - TypeScript特化
- `refactoring-workflow-v5-react.md` - React最適化特化
- `refactoring-workflow-v5-performance.md` - パフォーマンス特化
- `refactoring-workflow-v5-architecture.md` - アーキテクチャ改善特化

### 成功パターンの蓄積
```bash
# 成功したリファクタリングのパターンを記録
./save-refactoring-pattern.sh \
  --task-type "$TASK_TYPE" \
  --complexity "$COMPLEXITY" \
  --agents-used "$AGENTS" \
  --duration "$DURATION" \
  --success-factors "$FACTORS"
```

## ベストプラクティス

### 1. 要件の明確化
- 曖昧な要求は必ず具体化する
- 成功基準を数値化できる場合は数値化
- 制約条件を事前に洗い出す

### 2. 段階的実行
- 大規模な変更は小さなステップに分割
- 各ステップで品質を確認
- ロールバック可能な単位で実行

### 3. 継続的な品質チェック
- 変更のたびにテストを実行
- 型チェックとLintを継続的に実行
- パフォーマンスメトリクスを監視

## まとめ

このガイドに従うことで、Claude Codeは様々なリファクタリングタスクに対して、適切にv5自律型ワークフローを起動し、高品質な結果を達成できます。コーディネーターの自律性により、複雑なタスクでも人間の介入を最小限に抑えながら、確実に品質基準を満たすリファクタリングを実行します。