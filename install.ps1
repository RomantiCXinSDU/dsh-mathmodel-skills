# dsh-mathmodel-skills 一键安装（Windows PowerShell）
# 用法: powershell -File install.ps1 [目标skills目录]
#   默认 $env:USERPROFILE\.dsh\skills
param([string]$DST = (Join-Path $env:USERPROFILE ".dsh\skills"))
$ErrorActionPreference = "Stop"
$TMP = Join-Path $env:TEMP ("dsh-skills-" + [guid]::NewGuid().ToString("N"))
$SKILLS = @("data-profiler","data-ruler","professional-method-scout","model-explorer","formalizer","solver-verifier","cumcm-problem-spec","cumcm-model-review","cumcm-markdown-protocol")
Write-Host "==> 下载仓库..."
git clone --depth 1 "https://github.com/RomantiCXinSDU/dsh-mathmodel-skills.git" $TMP | Out-Null
New-Item -ItemType Directory -Force -Path $DST | Out-Null
foreach ($s in $SKILLS) {
  Copy-Item (Join-Path $TMP "skills\$s") $DST -Recurse -Force
  Write-Host "已安装: $s"
}
Remove-Item $TMP -Recurse -Force
Write-Host "完成！9 个技能已安装到 $DST（新开 Agent 会话生效）"
