#!/usr/bin/env bash
# dsh-mathmodel-skills 一键安装（Linux/macOS）
# 用法: bash install.sh [目标skills目录]
#   默认 $HOME/.dsh/skills；例: bash install.sh ~/.claude/skills
set -e
DST="${1:-${DSH_HOME:-$HOME/.dsh}/skills}"
REPO="https://github.com/RomantiCXinSDU/dsh-mathmodel-skills.git"
SKILLS="data-profiler data-ruler professional-method-scout model-explorer formalizer solver-verifier cumcm-problem-spec cumcm-model-review cumcm-markdown-protocol"
TMP=$(mktemp -d)
echo "==> 下载 $REPO"
git clone --depth 1 "$REPO" "$TMP/repo"
mkdir -p "$DST"
for s in $SKILLS; do
  cp -R "$TMP/repo/skills/$s" "$DST/"
  echo "已安装: $s"
done
rm -rf "$TMP"
echo "完成！9 个技能已安装到 $DST（新开 Agent 会话生效）"
