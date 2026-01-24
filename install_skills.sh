#!/bin/bash

# Skills シンボリックリンク インストールスクリプト
# - claude/gemini: ディレクトリ全体をリンク
# - codex: 個別スキルをリンク（.system を保持）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${SCRIPT_DIR}/skills"

CLAUDE_SKILLS="${HOME}/.claude/skills"
GEMINI_SKILLS="${HOME}/.gemini/skills"
CODEX_SKILLS="${HOME}/.codex/skills"

echo "Skills のシンボリックリンクを設定します..."

# ディレクトリ全体をリンクする関数
link_full_dir() {
    local target_dir="$1"
    local parent_dir="$(dirname "$target_dir")"

    # 親ディレクトリが存在しない場合は作成
    if [ ! -d "${parent_dir}" ]; then
        echo "Creating ${parent_dir} directory..."
        mkdir -p "${parent_dir}"
    fi

    # 既存の処理
    if [ -e "${target_dir}" ]; then
        if [ -L "${target_dir}" ]; then
            echo "既存のシンボリックリンクを削除: ${target_dir}"
            rm "${target_dir}"
        elif [ -d "${target_dir}" ]; then
            echo "警告: ${target_dir} は既存のディレクトリです。"
            read -p "バックアップを作成して続行しますか？ (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                BACKUP_DIR="${target_dir}.backup.$(date +%Y%m%d_%H%M%S)"
                echo "バックアップを作成: ${BACKUP_DIR}"
                mv "${target_dir}" "${BACKUP_DIR}"
            else
                echo "スキップ: ${target_dir}"
                return 1
            fi
        fi
    fi

    echo "リンク作成: ${target_dir} -> ${SKILLS_DIR}"
    ln -s "${SKILLS_DIR}" "${target_dir}"
}

# 個別スキルをリンクする関数（codex用）
link_individual_skills() {
    local target_dir="$1"

    # ディレクトリが存在しない場合は作成
    if [ ! -d "${target_dir}" ]; then
        echo "Creating ${target_dir} directory..."
        mkdir -p "${target_dir}"
    fi

    # skills/ 内の各ディレクトリをリンク
    for skill_path in "${SKILLS_DIR}"/*; do
        if [ -d "$skill_path" ]; then
            skill_name="$(basename "$skill_path")"
            target_link="${target_dir}/${skill_name}"

            if [ -L "${target_link}" ]; then
                echo "既存のシンボリックリンクを更新: ${target_link}"
                rm "${target_link}"
            elif [ -e "${target_link}" ]; then
                echo "警告: ${target_link} が既に存在します。スキップ"
                continue
            fi

            echo "リンク作成: ${target_link} -> ${skill_path}"
            ln -s "${skill_path}" "${target_link}"
        fi
    done
}

echo ""
echo "=== Claude ==="
link_full_dir "${CLAUDE_SKILLS}" && echo "✓ Claude 完了" || echo "✗ Claude スキップ"

echo ""
echo "=== Gemini ==="
link_full_dir "${GEMINI_SKILLS}" && echo "✓ Gemini 完了" || echo "✗ Gemini スキップ"

echo ""
echo "=== Codex (個別リンク) ==="
link_individual_skills "${CODEX_SKILLS}"
echo "✓ Codex 完了"

echo ""
echo "インストールが完了しました！"
