# dsh-mathmodel-skills 一键安装（Windows PowerShell / DSH）
$ErrorActionPreference = "Stop"
$DST = Join-Path $env:USERPROFILE ".dsh\skills"
$TMP = Join-Path $env:TEMP ("dsh-skills-" + [guid]::NewGuid().ToString("N"))
Write-Host "==> 下载仓库..."
git clone --depth 1 "https://github.com/RomantiCX77/dsh-mathmodel-skills.git" $TMP | Out-Null
New-Item -ItemType Directory -Force -Path $DST | Out-Null
foreach ($s in @("data-profiler","data-ruler","data-pattern-to-method","model-explorer","formalizer","solver-verifier")) {
  Copy-Item (Join-Path $TMP "skills\$s") $DST -Recurse -Force
  Write-Host "已安装: $s"
}
Remove-Item $TMP -Recurse -Force
Write-Host "完成！技能已安装到 $DST（新开会话生效）"
