# -*- coding: utf-8 -*-
"""校验候选文件（目录模式）：candidate_*.md 共 6-9 个，各 17 项 + Baseline 对照，无越权推荐语。
用法: python verify_候选方案.py [dir]"""
import sys, os, re
def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "E:/26数模国赛/流程产物"
    files = sorted(f for f in os.listdir(d) if re.fullmatch(r"候选[ABC][123]\.md", f))
    banned = ["MAIN", "BACKUP", "最终推荐", "推荐 A", "推荐B", "推荐C", "首选方案", "综合来看"]
    issues = []
    if not (6 <= len(files) <= 9):
        issues.append(f"候选文件数 {len(files)} 不在 6-9")
    for f in files:
        seg = open(os.path.join(d, f), encoding="utf-8").read()
        for n in range(1, 18):
            if f"\n{n}. " not in seg and not seg.startswith(f"{n}. "):
                issues.append(f + f" 缺第{n}点")
        if "Baseline 对照" not in seg:
            issues.append(f + " 缺 Baseline 对照")
        for b in banned:
            if b in seg:
                issues.append(f + " 越权语「" + b + "」")
    if issues: print("FAIL:", issues[:10]); sys.exit(1)
    print(f"PASS: {len(files)} 个候选文件（6-9），17 项 + Baseline 齐全，无越权"); sys.exit(0)
if __name__ == "__main__":
    main()
