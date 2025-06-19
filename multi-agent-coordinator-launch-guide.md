# マルチエージェント調査コーディネーター起動ガイド

## 概要

このドキュメントは、`@guide/multi-agent-investigation-workflow_v2_ja.md`に基づいたOpusコーディネーターエージェントを効率的に起動するためのガイドです。

**対象読者**: Claude Codeを使用してマルチエージェント調査を実行したい開発者

**前提条件**: 
- `mcp__ccm__claude_code` (Claude Code MCP)が利用可能
- 調査対象のファイルまたはディレクトリが存在
- `/guide/multi-agent-investigation-workflow_v2_ja.md`が存在

## クイックスタート

### 1. 単一ファイル調査の起動

```bash
# 使用例: 特定のmdファイルを調査する場合
@guide/multi-agent-coordinator-launch-guide.md を参照して
/path/to/target/file.md の調査コーディネーターを起動してください
```

### 2. 複数ファイル調査の一括起動

```bash
# 使用例: ディレクトリ内の全mdファイルを調査する場合
@guide/multi-agent-coordinator-launch-guide.md を参照して
/path/to/directory/ 内の全mdファイルに対して
調査コーディネーターを順次起動してください。
【重要】各ファイルについて、調査方向を私に確認してから
コーディネーターを起動してください。
```

## コーディネータープロンプトテンプレート

以下は、Opusコーディネーターエージェント用の標準プロンプトです：

```
あなたは調査ワークフローコーディネーターです。

【調査対象】
[ファイルのフルパス]

【調査方向の指定】（ユーザー確認済み）
[確認プロセスで承認された具体的な調査方向]

【実行指示】
@guide/multi-agent-investigation-workflow_v2_ja.mdに厳密に従って、マルチエージェント調査を実行してください。

【注意事項】
- issue.mdの内容に引きずられず、指定された調査方向を優先
- 元の疑問/課題を常に念頭に置いて調査を実施

【あなたの責務】
1. ワークフロー全体の設計・管理・実行
2. 専門エージェントの起動と監視
3. Chat MCPを使用したエージェント間連携
4. 成果物の品質管理と統合
5. TodoWriteツールによる進捗管理

【重要】
- ガイドラインを最初に完全に読み込んでから開始
- 継続実行プロトコルに従い、最大90分間実行を継続
- 基盤セッション戦略を必ず活用（85-90%のコスト削減）
- 全フェーズ（Phase 0, 1, 2）を確実に実行

【デバッグ情報の記録】
起動直後に以下の情報を記録：
- ファイル: [プロジェクトルート]/debug/coordinator-info.txt
- 記録内容: PID、セッションID、開始時刻、対象ファイル名

【期待される成果物（フルパス）】
1. [出力ディレクトリ]/[調査名]-final-report.md
2. [出力ディレクトリ]/[調査名]-analysis-matrix.md
3. [出力ディレクトリ]/[調査名]-implementation-guide.md
4. [出力ディレクトリ]/[調査名]-improvement-roadmap.md
5. [出力ディレクトリ]/[調査名]-[専門資料].md

【クリーンアップ指示】
- 専門エージェントが作成した一時ファイルは統合後に削除
- 最終成果物のみを指定ディレクトリに保存
- Chat MCPのメッセージ履歴は保持（デバッグ用）

【品質基準】
- 調査網羅度: 95%以上
- 情報正確度: 98%以上
- 実用性評価: 90%以上
- 成果物完成度: 100%

今すぐガイドラインの読み込みから開始してください。
```

## 実装手順

### ステップ1: 環境準備

```typescript
// 必要なディレクトリを作成
await bash('mkdir -p /path/to/project/debug');
await bash('mkdir -p /path/to/project/results');
```

### ステップ2: 調査方向の確認（重要）

調査を開始する前に、必ず以下の確認プロセスを実行します：

1. **issue.mdの内容分析**
   - 元の疑問・課題を抽出
   - ドキュメントが焦点を当てている内容を特定
   - 両者の相違点を明確化

2. **調査方向の候補提示**
   - 元の疑問に基づく調査方向
   - issue.mdに基づく調査方向
   - その他考えられる調査方向

3. **ユーザーへの確認**
   以下の形式で確認を求める：
   ```
   [ファイル名]を分析しました。
   
   【元の疑問/課題】
   （抽出した内容）
   
   【issue.mdの焦点】
   （分析した内容）
   
   【調査方向の候補】
   A) （根本的な調査方向）
   B) （ドキュメントに沿った調査方向）
   
   どちらの方向で調査を進めるべきでしょうか？
   ```

4. **承認待機と反映**
   - ユーザーの回答を待つ
   - 承認された方向性をコーディネータープロンプトに明記

### 確認が特に重要なケース
- issue.mdの内容が元の疑問から逸れている場合
- 複数の調査方向が考えられる場合
- 調査の範囲が不明確な場合

### ステップ3: コーディネーター起動

```typescript
// Opusモデルでコーディネーターを起動
const result = await mcp__ccm__claude_code({
  model: "opus",
  workFolder: "/path/to/project",
  prompt: coordinatorPrompt // 上記テンプレートを使用
});

// PIDを記録
const pid = result.pid;
```

### ステップ4: デバッグ情報の記録

```typescript
// coordinator-info.txtに情報を追記
await write('/path/to/project/debug/coordinator-info.txt', 
  `\n${targetFile} Investigation\nPID: ${pid}\nStart Time: ${new Date()}\nStatus: Running\n`
);
```

### ステップ5: 複数ファイルの一括処理

```typescript
// ディレクトリ内のファイルを取得
const files = await ls('/path/to/directory');
const mdFiles = files.filter(f => f.endsWith('.md'));

// 各ファイルに対してコーディネーターを起動
for (const file of mdFiles) {
  // ステップ2の調査方向確認プロセスを実行
  const approvedDirection = await confirmInvestigationDirection(file);
  
  const prompt = generateCoordinatorPrompt(file, approvedDirection);
  const result = await mcp__ccm__claude_code({
    model: "opus",
    workFolder: "/path/to/project",
    prompt: prompt
  });
  
  // PID記録
  recordPID(file, result.pid);
  
  // 短い待機時間を設定（オプション）
  await sleep(30); // 30秒待機
}
```

## カスタマイズオプション

### 1. 調査名の命名規則

```typescript
function generateInvestigationName(filePath: string): string {
  // 例: /issues/investigation/casl-mongoability-alternatives.md
  // → casl-alternatives
  const fileName = path.basename(filePath, '.md');
  const parts = fileName.split('-');
  return `${parts[0]}-${parts[parts.length - 1]}`;
}
```

### 2. 出力ディレクトリの構造

```
project/
├── debug/
│   ├── coordinator-info.txt     # 全コーディネーターの情報
│   └── coordinator-pids.txt     # PIDリスト
├── results/
│   ├── investigation-1/         # 調査ごとのディレクトリ
│   │   ├── final-report.md
│   │   ├── analysis-matrix.md
│   │   └── ...
│   └── investigation-2/
└── temp/                        # 一時ファイル（クリーンアップ対象）
```

### 3. 品質基準のカスタマイズ

```typescript
const qualityCriteria = {
  coverageScore: 95,      // 調査網羅度
  accuracyScore: 98,      // 情報正確度
  usabilityScore: 90,     // 実用性評価
  completeness: 100       // 成果物完成度
};
```

## ベストプラクティス

### 1. エラーハンドリング

```typescript
try {
  const result = await mcp__ccm__claude_code(params);
  if (result.status !== 'started') {
    throw new Error(`Failed to start coordinator: ${result.message}`);
  }
} catch (error) {
  console.error(`Coordinator launch failed: ${error}`);
  // 再試行ロジック
}
```

### 2. 進捗モニタリング

```typescript
// 定期的な状態確認
setInterval(async () => {
  const processes = await mcp__ccm__list_claude_processes();
  const activeCoordinators = processes.filter(p => 
    p.status === 'running' && p.prompt.includes('調査ワークフローコーディネーター')
  );
  console.log(`Active coordinators: ${activeCoordinators.length}`);
}, 300000); // 5分ごと
```

### 3. リソース管理

```typescript
// 同時実行数の制限
const MAX_CONCURRENT = 5;
const queue = [];

async function launchWithLimit(files: string[]) {
  for (let i = 0; i < files.length; i += MAX_CONCURRENT) {
    const batch = files.slice(i, i + MAX_CONCURRENT);
    await Promise.all(batch.map(file => launchCoordinator(file)));
    await sleep(60); // バッチ間の待機
  }
}
```

### 4. 調査方向の事前確認

推奨される確認フローの重要性：

1. **調査リソースの無駄を防ぐ**
   - 誤った方向での調査を回避
   - 時間とコストの節約

2. **本来の課題解決に集中**
   - 元の疑問に対する直接的な回答
   - より価値の高い成果物

3. **後からの手戻り防止**
   - 再調査の必要性を削減
   - 一度で正確な結果を取得

調査方向の相違例：
- 元の疑問：「リアクティブ性は必要か？」
- issue.mdの焦点：「watchEffectの最適化方法」
- 適切な調査：前者（根本的な必要性の検証）

## トラブルシューティング

### 問題1: コーディネーターが起動しない
- `@guide/multi-agent-investigation-workflow_v2_ja.md`が存在することを確認
- workFolderが正しく設定されているか確認
- Opusモデルが利用可能か確認

### 問題2: 成果物が生成されない
- 最大90分の実行時間を待つ
- debugディレクトリのログを確認
- Chat MCPルームのメッセージを確認

### 問題3: 複数コーディネーターの競合
- 各調査で異なるChat MCPルーム名を使用
- 出力ディレクトリを分離
- 適切な待機時間を設定

### 問題4: 調査結果が期待と異なる
- issue.mdの内容確認
- 調査開始前の方向性確認を実施したか検証
- 必要に応じて新しい方向性で再調査

### 問題5: issue.mdが誤導的な内容を含む
- 元の疑問を明確化
- 複数の調査方向を提示してユーザーに確認
- 承認された方向のみで調査を実施

## 使用例

### 実際の使用例: 権限システム調査（改善版）

```bash
# Claude Codeへの指示例
@guide/multi-agent-coordinator-launch-guide.md を参照して
/home/miyagi/dev/front/issues/investigation/ ディレクトリ内の
全てのmdファイルに対して調査コーディネーターを起動してください。

【重要】各ファイルについて、調査方向を私に確認してから
コーディネーターを起動してください。
```

### 期待される動作（改善版）
1. ガイドラインの読み込み
2. 環境準備（debug/resultsディレクトリ作成）
3. 各mdファイルの分析と調査方向の確認 【新規】
4. ユーザー承認を待機 【新規】
5. 承認された方向でOpusコーディネーター起動
6. PIDと起動情報の記録
7. 各コーディネーターが指定方向で調査を実行

## まとめ

このガイドを使用することで、`@guide/multi-agent-investigation-workflow_v2_ja.md`に基づいた高品質な調査を効率的に実行できます。重要なポイント：

1. **標準化されたプロンプト**を使用して一貫性を保つ
2. **デバッグ情報**を確実に記録して追跡可能性を確保
3. **リソース管理**を適切に行い、システムの安定性を維持
4. **品質基準**を明確にして高品質な成果物を生成

これにより、従来数日かかっていた調査を15分程度で完了し、85-90%のコスト削減を実現できます。