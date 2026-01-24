---
name: review-to-tasks
description: "PRのレビューコメントを取得してタスク化する。レビュー対応やPRのコメント確認が必要な時に使用"
allowed-tools: Bash(gh *), TodoWrite(*)
user-invocable: true
---

# Review to Tasks

現在のブランチに紐づくPRのレビューコメントとインラインコメントを全て取得し、アクション可能な項目をTodoリストとして整理する。

## 手順

### 1. PR番号を取得

```bash
gh pr view --json number -q .number
```

### 2. PR情報とレビューを取得

```bash
# PR基本情報とレビュー
gh pr view --json number,title,body,reviews

# 会話コメント（PRのタイムラインコメント）
gh api repos/:owner/:repo/issues/{PR_NUM}/comments --jq '.[]'

# インラインコメント（コードレビューコメント）
gh api repos/:owner/:repo/pulls/{PR_NUM}/comments --jq '.[]'
```

### 3. コメントを解析

以下の条件でアクション可能な項目を抽出：
- 質問や指摘が含まれているコメント
- 「修正してください」「変更してください」などの指示
- 「TODO」「FIXME」などが含まれるコメント
- コードの特定行に対する具体的な指摘

以下は除外：
- 単なる確認や情報共有のコメント
- 「LGTM」「承認済み」などのポジティブフィードバック
- 既に対応済みと思われるコメント

### 4. TodoWriteツールでタスクリスト作成

各タスクは以下の形式で作成：
- content: 「[ファイル名:行番号] コメント内容の要約」または「コメント内容の要約」
- activeForm: 現在進行形（例：「〜を修正中」）
- status: "pending"

### 5. ユーザーに報告

- 取得したレビューコメント数
- タスク化した項目数
- 主な対応内容の概要

## 注意事項

- PRが存在しない場合はエラーメッセージを表示
- コメントが0件の場合は「レビューコメントはありません」と表示
- TodoWriteツールは必ず使用する（コメントがある場合）
- インラインコメントの場合はファイルパスと行番号を含める
- 日本語のコメントは日本語でタスク化、英語のコメントは日本語で要約
