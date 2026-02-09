---
argument-hint: [base-branch]
allowed_tools: Bash(git:*, gh pr create:*), Read(*)
description: "gh pr createでPRを作成する"
---

# 目的
gh コマンドで GitHub PR を作成する

# 前提条件
- gh CLI がインストールされていること
- GitHub に認証済みであること
- `pr_desc.md` が作成済みであること（`/create-pr-desc` で事前に作成）

# 手順

## 1. pr_desc.md の確認
- `pr_desc.md` が存在するか確認
- **存在しない場合は処理を終了**し、先に `/create-pr-desc` を実行するよう案内する

## 2. PR の作成
pr_desc.md の内容を使って PR を作成：

```bash
gh pr create --base $1 --title "PRタイトル" --body-file pr_desc.md
```

- `--title`: pr_desc.md の「## 概要」セクションから簡潔なタイトルを抽出
- `--body-file`: pr_desc.md をそのまま使用
- `--base`: 引数で指定されたブランチ（デフォルト: main）

## 3. 作成後
- PR の URL を表示
- pr_desc.md と pr.diff を削除

# 注意事項
- ドラフト PR にしたい場合は `--draft` オプションを追加
- PR 作成前に必ず内容を確認してから実行
- コミット漏れがないか `git status` で確認
