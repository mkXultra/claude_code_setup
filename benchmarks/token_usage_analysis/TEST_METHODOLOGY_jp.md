# トークン使用量比較テスト実施方法

## 概要
このドキュメントでは、Claude Code（CCM MCP経由）を使用して、異なるモデル（Opus、Sonnet、Haiku）のトークン使用量を比較した方法を記載します。

## テスト環境
- **実行環境**: Claude Code with CCM MCP
- **テスト日時**: 2025-06-21
- **使用モデル**:
  - claude-opus-4-20250514
  - claude-3-5-sonnet
  - claude-3-5-haiku-20241022

## テスト手順

### 1. 準備
1. 作業ディレクトリの作成
   ```bash
   mkdir -p opus_test sonnet_test haiku_test
   ```

2. 共通プロンプトファイルの作成（`test_prompt.txt`）
   - フィボナッチ数列の実装タスクを記載
   - メモ化、エラーハンドリング、ユニットテストの要件を含む

### 2. 各モデルでの実行

#### Opus実行
```bash
mcp__ccm__claude_code(
  workFolder="/path/to/opus_test",
  model="opus",
  prompt_file="/path/to/test_prompt.txt"
)
```

#### Sonnet実行
```bash
mcp__ccm__claude_code(
  workFolder="/path/to/sonnet_test",
  model="sonnet",
  prompt_file="/path/to/test_prompt.txt"
)
```

#### Haiku実行
```bash
mcp__ccm__claude_code(
  workFolder="/path/to/haiku_test",
  model="claude-3-5-haiku-20241022",
  prompt_file="/path/to/test_prompt.txt"
)
```

### 3. 結果の取得
各プロセスのPIDを使用して結果を取得：
```bash
mcp__ccm__get_claude_result(pid=<process_id>)
```

### 4. 測定項目
- **入力トークン数**
- **キャッシュ作成トークン数**
- **キャッシュ読み取りトークン数**
- **出力トークン数**
- **総コスト（USD）**
- **実行時間**
- **ターン数**

## 注意事項

### ファイル名の競合回避
各モデルで別々の作業ディレクトリを使用することで、生成されるファイル（`fibonacci.py`、`test_fibonacci.py`）の競合を回避。

### 実行タイミング
- 各モデルの実行は並行して開始
- 結果の取得は適切な待機時間（30-60秒）後に実施

### トークン数の差異
Haikuモデルの入力トークン数が他モデルより少ない（34 vs 76）ことを確認。これは内部的なトークナイザーやシステムプロンプトの違いによる可能性がある。

## 実装ファイルの確認方法

各モデルの実装結果は以下で確認可能：
- `implementations/opus/fibonacci.py` - Opusの実装
- `implementations/sonnet/fibonacci.py` - Sonnetの実装
- `implementations/haiku/fibonacci.py` - Haikuの実装

テストコードも同様に各ディレクトリに保存。

## 結果の活用
- プロジェクトの予算に応じたモデル選択
- タスクの複雑度に応じた適切なモデルの使い分け
- コストパフォーマンスの最適化