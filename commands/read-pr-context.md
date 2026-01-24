---
allowed_tools: Bash(gh *)
description: "現在のブランチのPR情報を取得し概要を理解する"
---

# 目的
`gh` コマンドを使用して現在のディレクトリ（リポジトリ）のPR情報を取得し、概要を理解する。

# 手順
1. まずgitリポジトリかどうか確認する
   - **重要**: gitリポジトリでない場合は、即座に処理を中止し、ユーザーに報告する
2. 現在のブランチに関連するPRを取得する
   ```bash
   gh pr view --json number,title,body,state,author,baseRefName,headRefName,reviewDecision,additions,deletions,changedFiles,comments,reviews,labels,milestone,isDraft
   ```
3. PRが存在しない場合は、その旨を報告する
4. PRが存在する場合は、以下の情報を整理して報告する

# 出力フォーマット
以下の情報を簡潔に報告する：

## PR基本情報
- PR番号・タイトル
- 状態（Open/Closed/Merged）
- ドラフトかどうか
- 作成者
- ブランチ情報（head → base）

## 変更概要
- 追加/削除行数
- 変更ファイル数

## PR説明
- 本文の要約

## レビュー状況
- レビュー決定（Approved/Changes Requested/Review Required等）
- レビューコメントの概要（あれば）

## ラベル・マイルストーン
- 設定されているラベル
- マイルストーン（あれば）

# 注意事項
- gitリポジトリでない場合は即座に中止する
- PRが存在しない場合は明確に報告する
- 長いPR説明は要約して報告する
- レビューコメントが多い場合は重要なものをピックアップする
