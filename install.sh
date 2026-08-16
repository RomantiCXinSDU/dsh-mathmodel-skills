#!/usr/bin/env bash
# dsh-mathmodel-skills 一键安装（Linux/macOS DSH）
set -e
DST="${DSH_HOME:-$HOME/.dsh}/skills"
REPO="https://github.com/RomantiCXinSDU/dsh-mathmodel-skills.git"
TMP=$(mktemp -d)
echo "==> 下载 $REPO"
git clone --depth 1 "$REPO" "$TMP/repo"
mkdir -p "$DST"
for s in data-profiler data-ruler data-pattern-to-method model-explorer formalizer solver-verifier; do
  cp -R "$TMP/repo/skills/$s" "$DST/"
  echo "已安装: $s"
done
rm -rf "$TMP"
echo "完成！技能已安装到 $DST（新开会话生效）"