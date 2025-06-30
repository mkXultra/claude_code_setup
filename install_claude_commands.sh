#!/bin/bash

# Claude commands シンボリックリンク インストールスクリプト

set -e

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMANDS_DIR="${SCRIPT_DIR}/commands"
CLAUDE_DIR="${HOME}/.claude"
CLAUDE_COMMANDS_DIR="${CLAUDE_DIR}/commands"

echo "Claude commands のシンボリックリンクを設定します..."

# .claude ディレクトリが存在しない場合は作成
if [ ! -d "${CLAUDE_DIR}" ]; then
    echo "Creating ${CLAUDE_DIR} directory..."
    mkdir -p "${CLAUDE_DIR}"
fi

# 既存の ~/.claude/commands が存在する場合の処理
if [ -e "${CLAUDE_COMMANDS_DIR}" ]; then
    if [ -L "${CLAUDE_COMMANDS_DIR}" ]; then
        echo "既存のシンボリックリンクを削除します: ${CLAUDE_COMMANDS_DIR}"
        rm "${CLAUDE_COMMANDS_DIR}"
    elif [ -d "${CLAUDE_COMMANDS_DIR}" ]; then
        echo "警告: ${CLAUDE_COMMANDS_DIR} は既存のディレクトリです。"
        read -p "バックアップを作成してから続行しますか？ (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            BACKUP_DIR="${CLAUDE_COMMANDS_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
            echo "バックアップを作成: ${BACKUP_DIR}"
            mv "${CLAUDE_COMMANDS_DIR}" "${BACKUP_DIR}"
        else
            echo "インストールを中止しました。"
            exit 1
        fi
    fi
fi

# シンボリックリンクを作成
echo "シンボリックリンクを作成: ${CLAUDE_COMMANDS_DIR} -> ${COMMANDS_DIR}"
ln -s "${COMMANDS_DIR}" "${CLAUDE_COMMANDS_DIR}"

echo "✓ インストールが完了しました！"
echo "  ${CLAUDE_COMMANDS_DIR} は ${COMMANDS_DIR} にリンクされています。"