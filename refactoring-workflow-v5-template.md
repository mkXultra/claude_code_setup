# リファクタリングマルチエージェントワークフロー v5テンプレート（自律型）

## 概要
このテンプレートは、様々なタイプのリファクタリングタスクに適用できる汎用的な自律型マルチエージェントワークフローです。
コーディネーターの自律性を大幅に強化し、動的なエージェント管理、適応的な戦略調整、自己組織化を実現します。

## 使用方法
1. このテンプレートをベースに、特定のリファクタリングタイプ用の実装ファイルを作成
2. `{{PLACEHOLDER}}` で示された部分を具体的な内容に置き換え
3. リファクタリングタイプに応じた特別な要件を追加

## 自律型コーディネーターの権限

### 1. 動的エージェント管理
```yaml
dynamic_agent_management:
  初期構成:
    - 最小構成（Agent A: 調査、Agent B: 実装、Agent C: レビュー）で開始
    - 複雑度評価後に動的に拡張
  
  追加トリガー:
    - 影響範囲が5ファイル以上
    - 複数システムへの影響検出
    - テスト失敗率 > 20%
    - パフォーマンス劣化の検出
    - アーキテクチャ変更の必要性
  
  追加可能なエージェント:
    - デバッグ専門エージェント
    - パフォーマンス最適化エージェント
    - セキュリティ監査エージェント
    - アーキテクチャ設計エージェント
    - テスト作成専門エージェント
```

### 2. 戦略的調整権限
```yaml
strategic_authority:
  品質基準:
    - 状況に応じた動的調整
    - critical/nice-to-have の判定
    - トレードオフの自律的決定
  
  リソース配分:
    - Opus/Sonnet 比率の動的調整
    - 並行実行数の最適化
    - 時間配分の再調整
  
  レビューサイクル:
    - 品質達成まで無制限
    - 各サイクルでの改善度測定
    - 収束しない場合は戦略再構築
```

### 3. 自律的判断フレームワーク
```yaml
decision_framework:
  complexity_assessment:
    simple: 基本3エージェント維持
    moderate: 1-2専門エージェント追加
    complex: フルスケール展開（5-8エージェント）
  
  quality_vs_speed:
    critical_fix: スピード優先、Sonnet中心
    improvement: バランス型
    architecture: 品質優先、Opus中心
  
  error_handling:
    minor: 既存エージェントで対処
    major: 専門エージェント追加
    critical: 戦略全体の再構築
```

## ゴール定義テンプレート

```yaml
リファクタリングのゴール:
  タスクタイプ: {{REFACTORING_TYPE}}
  
  主要目的:
    - {{PRIMARY_GOAL}}
    - {{SECONDARY_GOAL_1}}
    - {{SECONDARY_GOAL_2}}
  
  成功基準:
    必須:
      - TypeScriptコンパイルエラー: 0
      - 既存テスト成功率: 100%
      - Lintエラー: 0（{{LINT_RULES}}）
      - 機能的後退: なし
    
    品質向上:
      - コードカバレッジ: {{COVERAGE_TARGET}}
      - ビルド時間: {{BUILD_TIME_TARGET}}
      - バンドルサイズ: {{BUNDLE_SIZE_TARGET}}
      - {{CUSTOM_METRIC}}: {{CUSTOM_TARGET}}
  
  自律的調整:
    - タスクの性質に応じて優先順位を動的に変更
    - ただし、必須基準は常に100%達成
```

## Phase 0: 戦略的分析と環境準備

### 0.1 タスク複雑度評価（新規）
```bash
# コーディネーターが最初に実行
1. リファクタリング要件の複雑度を1-10で評価
2. 影響を受けるファイル数と依存関係を分析
3. 必要なエージェント構成を決定
4. リソース配分戦略を策定
5. 成功指標の優先順位を設定
```

### 0.2 基盤セッション構築
```bash
mcp__ccm__claude_code [
  model: "sonnet",
  prompt: "リファクタリング基盤セッション構築：
  1. コードベースの現状を把握
     - パッケージ構成とビルドツール
     - テストフレームワークと設定
     - Lintルールと設定
     - 型定義の構造
  2. refactoring-requirements.md を読み込み
  3. complexity-assessment.md を読み込み
  4. 複雑度評価結果に基づく戦略を策定
  完了後'REFACTOR_BASE_READY'と報告してセッションIDを提供"
]
```

### 0.3 Chat MCPルーム作成（拡張）
```bash
Room名: refactor-{{TASK_NAME}}-main
追加Room（必要に応じて）:
- refactor-{{TASK_NAME}}-debug（デバッグ用）
- refactor-{{TASK_NAME}}-review（レビュー議論用）
```

### 0.4 自律型コーディネーター起動
```yaml
コーディネーター責務（拡張版）:
  初期化:
    - workflow-log-spec.mdのプロトコルに準拠してログシステムを初期化
    - complexity-assessment.md から戦略を理解
    - 全エージェントの状態を一元管理
  
  基本責務:
    - 調査結果の評価
    - 実装進捗の監視
    - レビュー結果の管理
    - 品質基準達成の確認
  
  拡張責務:
    - 動的エージェント管理
    - 戦略的判断と調整
    - リソース最適化
    - 自律的問題解決
  
  ログ管理:
    - workflow-log-spec.mdのプロトコルに準拠
    - agents.json、errors.json、workflow-state.jsonの更新
    - cost-summary.jsonの生成
  
  進捗報告:
    - 5分ごとにChat MCPに状況報告
    - 重要な意思決定をログに記録
```

## Phase 1: 深層調査と分析

### 調査エージェント（Opus）
```bash
mcp__ccm__claude_code [
  model: "opus",
  prompt: "【リファクタリング調査】{{REFACTORING_TYPE}}の包括的影響分析
  
  【調査項目】
  1. 対象コードの完全なマッピング
     - {{TARGET_PATTERN}}に該当するファイル一覧
     - 各ファイルの{{ANALYSIS_FOCUS}}
     - 問題箇所の特定と分類
  
  2. 依存関係の分析
     - 影響を受ける可能性のあるファイル
     - インポート/エクスポートの関係
     - 型定義の依存関係
  
  3. リスク評価
     - 破壊的変更の可能性
     - パフォーマンスへの影響
     - セキュリティリスク
  
  4. 改善提案
     - 推奨される修正アプローチ
     - 段階的実装計画
     - 必要な追加エージェント
  
  【自律性付与】
  - 予想より複雑な場合は追加調査を実施
  - 専門エージェントの必要性を判断
  - リスクレベルに応じた戦略修正を提案
  
  Chat MCPルーム'refactor-{{TASK_NAME}}-main'で5分ごとに報告
  
  成果物:
  - investigation-report.md
  - risk-assessment.md
  - recommended-approach.md"
]
```

## Phase 2: 適応的実装

### 初期エージェント構成

#### Agent B: 適応型実装エージェント（Sonnet）
```
【基盤セッション継承】
【ゴール貢献】調査結果に基づく段階的実装
【実装方針】
1. investigation-report.mdの推奨アプローチに従う
2. 小さな変更単位で段階的に実装
3. 各段階で品質チェックを実施

【品質チェック】
- npm run type-check（または{{TYPE_CHECK_COMMAND}}）
- npm run test（または{{TEST_COMMAND}}）  
- npm run lint（または{{LINT_COMMAND}}）

【自律的行動】
- テスト失敗時は原因を分析し、自動修正を試みる
- 3回失敗したらデバッグエージェントを要請
- パフォーマンス劣化を検出したら最適化エージェントを要請

【成果物】
- implementation-log.md（実装の詳細ログ）
- test-results.md（テスト実行結果）
- issues-found.md（発見された問題）
```

#### Agent C: 継続的レビューエージェント（Opus）
```
【基盤セッション継承】
【ゴール貢献】実装の品質保証とリアルタイムフィードバック
【レビュー戦略】
1. 実装の進行と並行してリアルタイムレビュー
2. 問題を早期に発見し、即座にフィードバック
3. 品質スコアの継続的計算

【評価基準（動的調整可）】
- 型安全性: {{TYPE_SAFETY_WEIGHT}}
- コード品質: {{CODE_QUALITY_WEIGHT}}
- パフォーマンス: {{PERFORMANCE_WEIGHT}}
- 保守性: {{MAINTAINABILITY_WEIGHT}}

【自律的判断】
- 重大な問題を発見した場合、即座に実装停止を指示
- 改善の余地がある場合、具体的な修正案を提示
- 追加レビューが必要な場合、専門エージェントを要請

【成果物】
- review-report.md（レビュー結果：PASS/FAIL）
- quality-score.json（品質スコア）
- improvement-suggestions.md（改善提案）
```

### 動的追加可能エージェント

#### Agent D: デバッグ専門エージェント（Opus）
```
【トリガー】
- テスト失敗率 > 20%
- 原因不明のエラーが3回以上
- 実装エージェントからの要請

【専門性】
- 根本原因分析
- スタックトレース解析
- 依存関係の問題解決
- 非同期処理のデバッグ

【成果物】
- debug-analysis.md
- fix-recommendations.md
```

#### Agent E: パフォーマンス最適化エージェント（Sonnet）
```
【トリガー】
- ビルド時間が{{BUILD_TIME_THRESHOLD}}以上増加
- バンドルサイズが{{BUNDLE_SIZE_THRESHOLD}}以上増加
- 実行時パフォーマンスの劣化検出

【専門性】
- コード分割戦略
- 依存関係の最適化
- アルゴリズム改善
- キャッシング戦略

【成果物】
- performance-analysis.md
- optimization-plan.md
- performance-results.md
```

#### Agent F: アーキテクチャ設計エージェント（Opus）
```
【トリガー】
- 大規模な構造変更が必要
- 循環依存の検出
- モジュール境界の再定義が必要

【専門性】
- リファクタリング戦略の設計
- モジュール構成の最適化
- 依存関係の整理
- 将来の拡張性確保

【成果物】
- architecture-proposal.md
- migration-plan.md
- impact-analysis.md
```

## Phase 2.5: 品質収束サイクル

### 収束戦略
```yaml
quality_convergence:
  target_score: {{TARGET_QUALITY_SCORE}}
  max_iterations: unlimited
  
  iteration_strategy:
    1-3回目:
      focus: 必須基準の達成
      approach: 段階的修正
    
    4-6回目:
      focus: 品質向上目標
      approach: 最適化とリファクタリング
    
    7回目以降:
      focus: 問題の根本解決
      approach: 戦略の見直しまたは専門エージェント追加
  
  convergence_check:
    - 各イテレーションで改善度を測定
    - 改善が停滞したら戦略変更
    - 必須基準達成後、品質目標に移行
```

## Phase 3: 統合と最終化

### 最終統合エージェント（Opus）
```
【基盤セッション継承】
【ゴール貢献】全変更の統合と最終品質保証
【タスク】
1. 全変更の統合確認
   - すべてのファイルが正しく修正されているか
   - 一貫性のある変更か
   - 取りこぼしはないか

2. 最終品質チェック
   - フルテストスイートの実行
   - パフォーマンスベンチマーク
   - セキュリティスキャン
   - 総合的なLintチェック

3. ドキュメント生成
   - 変更内容のサマリー
   - 今後の推奨事項
   - 技術的負債の評価

【自律的判断】
- 追加の最適化機会の特定
- 将来のリファクタリング提案
- ベストプラクティスの提案

【成果物】
- final-report.md（最終レポート）
- change-summary.md（変更サマリー） 
- metrics-report.json（各種メトリクス）
- future-recommendations.md（今後の推奨事項）
```

## 実行タイムライン（適応的）

```
時間配分は完全に動的。タスクの複雑さと進捗に応じて自動調整。

├─ Phase 0: 戦略的分析と環境準備（5-10分）
│  ├─ 複雑度評価
│  ├─ 基盤セッション作成
│  ├─ Chat MCPルーム作成
│  └─ コーディネーター起動
├─ Phase 1: 深層調査（5-15分）
│  └─ 複雑度に応じて自動延長
├─ Phase 2: 適応的実装（10分-無制限）
│  ├─ 初期エージェント展開
│  ├─ [必要時] 追加エージェント起動
│  └─ 品質チェックループ
├─ Phase 2.5: 品質収束（5分-無制限）
│  └─ 品質達成まで継続
└─ Phase 3: 統合と最終化（5-10分）
   └─ 完全性確認と文書化
```

## 自律的協調プロトコル

### Chat MCPメッセージ標準
```yaml
message_types:
  progress_update:
    interval: 5分（負荷に応じて2-10分で調整）
    format: "[PROGRESS] {phase} - {完了率}% - {現在のタスク}"
  
  issue_alert:
    trigger: 問題検出時即座に
    format: "[ISSUE] {severity} - {問題の概要} - {提案する対処}"
  
  agent_request:
    trigger: 追加リソース必要時
    format: "[REQUEST] {エージェントタイプ} - {理由} - {期待効果}"
  
  decision_log:
    trigger: 重要な判断時
    format: "[DECISION] {判断内容} - {理由} - {代替案}"
```

### エージェント間協調
```yaml
coordination_rules:
  情報共有:
    - 成果物は即座に共有
    - 問題は発見次第報告
    - 進捗は定期的に更新
  
  意思決定:
    - コーディネーターが最終決定権
    - エージェントは提案と実行
    - 緊急時は自律的に行動
  
  競合解決:
    - 同一ファイルの編集は順次実行
    - 優先順位はコーディネーターが決定
    - デッドロックは自動検出・解決
```

## 成功指標と評価

### リアルタイムメトリクス
```yaml
quality_metrics:
  type_safety_score: 0-100
  test_coverage: percentage
  code_quality_index: composite
  performance_score: 0-100

progress_metrics:
  files_processed: current/total
  tests_passed: current/total
  issues_resolved: current/total
  
health_metrics:
  agent_efficiency: percentage
  error_rate: percentage
  retry_count: number
```

### 最終評価基準
```yaml
mandatory_criteria:
  typescript_errors: 0
  test_success_rate: 100%
  lint_errors: 0
  functional_regression: none

quality_goals:
  code_coverage: {{COVERAGE_TARGET}}
  build_time: {{BUILD_TIME_TARGET}}
  bundle_size: {{BUNDLE_SIZE_TARGET}}
  type_safety: improved

overall_score:
  calculation: weighted_average
  minimum: 85
  target: 95
```

## エラーハンドリング機構（拡張版）

**注意**: ログ管理システムとエラーリカバリープロトコルの詳細は `workflow-log-spec.md` を参照してください。

## 継続的改善

### 学習メカニズム
```yaml
learning_system:
  success_patterns:
    - 成功したリファクタリング戦略を記録
    - 効果的なエージェント構成を蓄積
    - 最適な実行順序を学習
  
  failure_patterns:
    - エラーパターンとその対処法を記録
    - 回避すべきアプローチを特定
    - タイムアウトの原因を分析
  
  optimization:
    - 各フェーズの最適時間配分を学習
    - リソース配分パターンを最適化
    - 品質とスピードのバランスを調整
```

## 実装上の注意事項

1. **Git Worktreeの活用**
   - 常に独立した環境で作業
   - メインブランチへの影響を防止
   - 問題時は簡単に破棄可能

2. **段階的実装**
   - 大きな変更は小さく分割
   - 各段階で品質を確認
   - ロールバック可能な単位

3. **継続的な品質チェック**
   - 変更ごとにテスト実行
   - 型チェックとLintを継続
   - パフォーマンスを監視

## テンプレート使用例

### 型安全性改善の実装例
```yaml
{{REFACTORING_TYPE}} → "remove-any-assertions"
{{PRIMARY_GOAL}} → "すべての`as any`を削除し、適切な型定義に置き換える"
{{TARGET_PATTERN}} → "src/**/*.{ts,tsx}"
{{TYPE_SAFETY_WEIGHT}} → 90
{{CODE_QUALITY_WEIGHT}} → 10
```

### ESLint違反修正の実装例
```yaml
{{REFACTORING_TYPE}} → "fix-eslint-violations"
{{PRIMARY_GOAL}} → "すべてのESLintエラーを修正"
{{LINT_RULES}} → "@typescript-eslint/recommended"
{{TARGET_PATTERN}} → "src/**/*.{js,ts,jsx,tsx}"
{{CODE_QUALITY_WEIGHT}} → 80
{{MAINTAINABILITY_WEIGHT}} → 20
```

### パフォーマンス最適化の実装例
```yaml
{{REFACTORING_TYPE}} → "optimize-performance"
{{PRIMARY_GOAL}} → "ビルド時間とバンドルサイズの削減"
{{BUILD_TIME_TARGET}} → "30%削減"
{{BUNDLE_SIZE_TARGET}} → "20%削減"
{{PERFORMANCE_WEIGHT}} → 70
{{MAINTAINABILITY_WEIGHT}} → 30
```