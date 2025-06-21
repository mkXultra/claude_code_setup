# 記事作成マルチエージェントワークフロー v5テンプレート（自律型）

## 概要
このテンプレートは、様々なタイプの記事作成に適用できる汎用的な自律型マルチエージェントワークフローです。
コーディネーターの自律性を大幅に強化し、動的なエージェント管理、適応的な戦略調整、自己組織化を実現します。

## 使用方法
1. このテンプレートをベースに、特定の記事タイプ用の実装ファイルを作成
2. `{{PLACEHOLDER}}` で示された部分を具体的な内容に置き換え
3. 記事タイプに応じた特別な要件を追加

## 自律型コーディネーターの権限

### 1. 動的エージェント管理
```yaml
dynamic_agent_management:
  初期構成:
    - 最小構成（Agent A, B, C）で開始
    - 必要に応じて動的に追加
  
  追加トリガー:
    - タスク複雑度が閾値超過
    - 特定専門知識の必要性
    - 品質問題の検出
    - 時間制約への対応
  
  追加可能なエージェント:
    - 専門リサーチエージェント
    - デバッグ特化エージェント
    - パフォーマンス最適化エージェント
    - 追加ファクトチェッカー
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
    - 2回制限の柔軟な拡張
    - 品質達成まで継続可能
```

### 3. 自律的判断フレームワーク
```yaml
decision_framework:
  complexity_assessment:
    simple: 基本3エージェント維持
    moderate: 1-2専門エージェント追加
    complex: フルスケール展開（6-8エージェント）
  
  quality_vs_speed:
    high_quality: Opus比率増加、レビュー強化
    time_critical: Sonnet活用、並行度向上
  
  error_handling:
    minor: 既存エージェントで対処
    major: 専門エージェント追加
    critical: 戦略全体の再構築
```

## ゴール定義テンプレート

```yaml
記事のゴール:
  読者: {{TARGET_AUDIENCE_DESCRIPTION}}
  
  記事の目的:
    - {{PRIMARY_GOAL}}
    - {{SECONDARY_GOAL_1}}
    - {{SECONDARY_GOAL_2}}
  
  成功基準:
    - {{SUCCESS_CRITERION_1}}
    - {{SUCCESS_CRITERION_2}}
    - {{SUCCESS_CRITERION_3}}
    - {{SUCCESS_CRITERION_4}}
    - 適切な長さ: {{WORD_COUNT_RANGE}}
  
  自律的調整:
    - 上記基準の優先順位を状況に応じて調整可能
    - ただし、コア要件（{{CORE_REQUIREMENTS}}）は維持
```

## エラーハンドリング機構（拡張版）

**注意**: ログ管理システムとエラーリカバリープロトコルの詳細は `../workflow-log-spec.md` を参照してください。

## Phase 0: 戦略的分析と環境準備

### 0.1 タスク複雑度評価（新規）
```bash
# コーディネーターが最初に実行
1. 記事要件の複雑度を1-10で評価
2. 必要なエージェント構成を決定
3. リソース配分戦略を策定
4. 成功指標の優先順位を設定
```

### 0.2 基盤セッション構築
```bash
mcp__ccm__claude_code [
  model: "sonnet",
  prompt: "記事作成基盤セッション構築：
  1. prompts/内の全ワークフローMDファイルを読み込み
  2. {{DOMAIN_SPECIFIC_TOOLS}}の内容を理解
  3. 記事に必要な要素を整理（{{WORD_COUNT_RANGE}}に収まる内容）
  4. 複雑度評価結果に基づく戦略を策定
  完了後'ARTICLE_BASE_READY'と報告してセッションIDを提供"
]
```

### 0.3 Chat MCPルーム作成（拡張）
```bash
Room名: article-{{ARTICLE_TYPE}}-workflow-v5
追加Room（必要に応じて）:
- article-debug-room（デバッグ用）
- article-coordination-room（コーディネーター専用）
```

### 0.4 自律型コーディネーター起動
```yaml
コーディネーター責務（拡張版）:
  初期化:
    - ../workflow-log-spec.mdのプロトコルに準拠してログシステムを初期化
    - 全エージェントの状態を一元管理
  
  基本責務:
    - レビュー結果の監視
    - 修正指示の配布
    - レビューサイクルの管理
    - 品質基準達成の確認
  
  拡張責務:
    - 動的エージェント管理
    - 戦略的判断と調整
    - リソース最適化
    - 自律的問題解決
  
  ログ管理:
    - workflow-log-spec.mdのプロトコルに準拠
```

## Phase 1: ゴール判定と計画（適応的）

### ゴール判定エージェント（Opus）
```bash
mcp__ccm__claude_code [
  model: "opus",
  prompt: "【ゴール】{{ARTICLE_TYPE_DESCRIPTION}}の記事作成
  
  【現在の資源】
  - {{AVAILABLE_RESOURCES}}
  - {{DOMAIN_SPECIFIC_RESOURCES}}
  
  【判断事項】
  1. 記事に必要な{{DOMAIN}}要素の特定
  2. 実用的な{{CONTENT_TYPE}}の選定
  3. 必要タスクの定義
  4. 推奨エージェント構成（最小〜最大）
  5. リスク要因の特定
  
  【自律性付与】
  - 追加調査が必要な場合は提案
  - 代替アプローチの提示
  
  Chat MCPルーム'article-{{ARTICLE_TYPE}}-workflow-v5'で報告"
]
```

## Phase 2: 適応的並行実行

### 初期エージェント構成（最小構成）

#### Agent A: リサーチ・構成担当（Sonnet）
```
【基盤セッション継承】
【ゴール貢献】{{TARGET_AUDIENCE}}向けの実用的な記事構成を設計
【成果物】
- article-outline.md (記事の構成案)
- key-points.md (押さえるべき{{DOMAIN}}ポイント)
【自律的協調】
- 複雑な{{DOMAIN}}要素発見時は追加リサーチャーを要請
```

#### Agent B: メインライティング担当（Sonnet）
```
【基盤セッション継承】
【ゴール貢献】{{TARGET_AUDIENCE}}向けの{{CONTENT_STYLE}}記事を執筆
【成果物】
- {{ARTICLE_FILENAME}}-draft.md（{{DRAFT_WORD_COUNT}}）
【注意事項】
- {{SPECIFIC_WRITING_GUIDELINES}}
- 全体の文字数制限を意識した簡潔な説明
【自律的協調】
- {{DOMAIN}}的疑問はAgent Aに確認
- 文字数超過時は自動的に要約
```

#### Agent C: 実装例・コード担当（Sonnet）
```
【基盤セッション継承】
【ゴール貢献】実際の{{EXAMPLE_TYPE}}を提供
【成果物】
- {{EXAMPLE_FILENAME_1}}.md ({{EXAMPLE_DESCRIPTION_1}}、{{EXAMPLE_WORD_COUNT_1}})
- {{EXAMPLE_FILENAME_2}}.md ({{EXAMPLE_DESCRIPTION_2}}、{{EXAMPLE_WORD_COUNT_2}})
【禁止事項】{{PROHIBITED_ACTIONS}}
【自律的協調】
- 動作確認が必要な場合はテストエージェントを要請
```

### 動的追加可能エージェント

#### Agent G: 専門技術リサーチャー（Opus）
```
【トリガー】複雑な{{DOMAIN}}要素の発見時
【専門性】特定{{DOMAIN}}領域の深掘り調査
【成果物】{{DOMAIN}}-deep-dive.md
```

#### Agent H: パフォーマンス最適化（Sonnet）
```
【トリガー】文字数制限への対応必要時
【専門性】コンテンツの要約と最適化
【成果物】optimized-content.md
```

## Phase 2.5: 適応的レビューサイクル

### Agent D: レビュー・品質管理担当（Opus）
```
【基盤セッション継承】
【ゴール貢献】記事の構成と実用性を検証
【レビュー基準】
- 記事構成の論理性確認
- {{DOMAIN_SPECIFIC_REVIEW_CRITERIA}}
- 実用性の検証
- 不要な{{AVOID_ELEMENTS}}の排除確認
- 文字数が指定範囲内か確認
【成果物】
- review-report.md（レビュー結果：PASS/FAIL）
- improvement-suggestions.json（修正が必要な場合の具体的指示）
【Chat MCP通知】
- レビュー結果を'article-{{ARTICLE_TYPE}}-workflow-v5'ルームに投稿
- FAILの場合は修正箇所を明確に指示
```

### Agent F: ファクトチェック専門担当（Sonnet）
```
【基盤セッション継承】
【ゴール貢献】{{DOMAIN}}的事実の正確性を検証
【検証項目】
- {{FACT_CHECK_ITEM_1}}
- {{FACT_CHECK_ITEM_2}}
- {{FACT_CHECK_ITEM_3}}
- コマンド例の動作検証
【検証方法】
- 公式ドキュメントの参照
- 実際のコマンド実行テスト
- WebSearchツールでの確認
【成果物】
- fact-check-report.md（検証結果）
- factual-errors.json（事実誤認リスト）
【Chat MCP通知】
- 事実誤認を発見した場合は即座に報告
```

### レビュー戦略の動的決定
```yaml
review_strategy:
  Agent_D_戦略（ハイブリッド方式）:
    基本動作: 固定（必須レビュー）
    動的要素:
      - レビュー深度の調整
      - 追加レビュアーの起動判断
      - レビューサイクル数の動的決定
    判断基準:
      記事複雑度_低: 簡易レビュー（5分）
      記事複雑度_中: 標準レビュー（10分）
      記事複雑度_高: 詳細レビュー＋追加レビュアー（15分）
  
  Agent_F_戦略（条件付き動的）:
    起動条件:
      - {{DOMAIN}}的主張が3つ以上
      - 外部ツール/APIの記述あり
      - 数値データの引用あり
    スキップ条件:
      - 概念説明のみの記事
      - 内部システムの説明
      - チュートリアル形式
  
  問題検出時:
    - 重要度評価（critical/major/minor）
    - 修正戦略の自律的決定
    - 必要に応じて専門エージェント追加
  
  サイクル管理:
    - 基本は2回だが、品質達成まで継続可能
    - 各サイクルでの改善度を測定
    - 収束しない場合は戦略見直し
```

## Phase 3: 統合・最終化（品質保証）

### Agent E: 最終統合担当（Opus）
```
【基盤セッション継承】
【ゴール貢献】全要素を統合し、実用的な{{ARTICLE_TYPE}}記事を完成
【タスク】
1. 全成果物の統合（{{WORD_COUNT_RANGE}}に収める）
2. {{QUALITY_CHECK_ITEMS}}の最終確認
3. {{PROHIBITED_ELEMENTS}}が含まれていないことを確認
4. {{SPECIFIC_REQUIREMENTS}}の確認
5. 文字数が適切な範囲内であることを確認
【自律的判断】
- 統合時の優先順位付け
- 必要に応じた内容の取捨選択
【成果物】
- {{FINAL_ARTICLE_FILENAME}}.md（{{WORD_COUNT_RANGE}}）```

## 実行タイムライン（適応的）

```
├─ Phase 0: 戦略的分析と環境準備（3-5分）
│  ├─ 複雑度評価
│  ├─ 基盤セッション作成
│  ├─ ログシステム初期化
│  └─ Chat MCPルーム作成
├─ Phase 1: ゴール判定（5分）
│  └─ Opusエージェントによる分析と計画
├─ Phase 2: 適応的並行実行（10-15分）
│  ├─ 初期エージェント起動
│  ├─ [必要時] 追加エージェント起動
│  └─ 自律的協調
├─ Phase 2.5: 適応的レビューサイクル（10-20分）
│  ├─ 並行レビュー実行
│  ├─ [必要時] 修正サイクル（回数制限なし）
│  └─ 品質収束確認
└─ Phase 3: 統合（5-7分）
   └─ Agent E: 最終統合と品質保証
```

## 自律的協調プロトコル

### Chat MCPメッセージ標準
```yaml
message_types:
  progress_update:
    interval: adaptive（2-5分）
    content: "進捗率、課題、次のアクション"
  
  help_request:
    trigger: 問題検出時
    content: "問題内容、必要な支援、緊急度"
  
  coordination:
    trigger: エージェント間調整必要時
    content: "調整事項、関係エージェント、提案"
  
  decision_log:
    trigger: 重要な判断時
    content: "判断内容、理由、期待効果"
```

## 成功指標と評価

### KPIダッシュボード
```yaml
real_time_metrics:
  quality_score: 0-100
  progress_rate: 完了タスク/全タスク
  agent_efficiency: 有効作業時間/総時間
  error_rate: エラー数/タスク数
  
adaptive_thresholds:
  quality_alert: < 80
  progress_alert: < 期待値の70%
  efficiency_alert: < 60%
  error_alert: > 10%
```

### 最終評価基準
- 記事品質: 90%以上
- 文字数準拠: {{WORD_COUNT_RANGE}}
- {{DOMAIN}}的正確性: 100%
- 実行効率: 80%以上
- 自律的調整の適切性: 成功率90%以上

## 継続的改善

### 学習メカニズム
```yaml
learning_system:
  success_patterns:
    - 成功したエージェント構成を記録
    - 効果的な修正パターンを蓄積
  
  failure_patterns:
    - エラーパターンとその対処法を記録
    - 回避すべきアプローチを特定
  
  optimization:
    - 各フェーズの最適時間配分を学習
    - リソース配分の最適化パターンを発見
```

## 実装上の注意事項

1. **段階的導入**
   - まずv4の基本機能を維持
   - 自律的機能は段階的に有効化
   - 各機能の効果を測定しながら調整

2. **フェイルセーフ**
   - 自律的判断の上限を設定
   - 人間による介入ポイントを確保
   - 暴走防止のための制約

3. **透明性の維持**
   - 全ての自律的判断をログに記録
   - 判断理由を明確に文書化
   - レビュー可能な形式で保存

## テンプレート使用例

MCP記事用の実装例：
```yaml
{{TARGET_AUDIENCE_DESCRIPTION}} → "ソフトウェア開発者（Claude Code使用中、MCPは聞いたことがある程度）"
{{PRIMARY_GOAL}} → "MCPの仕組みを理解（Chat MCPとCCMの役割）"
{{DOMAIN}} → "技術"
{{ARTICLE_TYPE}} → "mcp"
```

チュートリアル記事用の実装例：
```yaml
{{TARGET_AUDIENCE_DESCRIPTION}} → "Reactの基礎は理解しているが、Hooksはまだよく分からないフロントエンド開発者"
{{PRIMARY_GOAL}} → "useState、useEffectの実践的な使い方を身につけてもらう"
{{DOMAIN}} → "プログラミング"
{{ARTICLE_TYPE}} → "tutorial"
```