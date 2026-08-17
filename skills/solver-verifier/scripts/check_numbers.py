#!/usr/bin/env python3
"""check_numbers.py —— 数字溯源校验（确定性门禁）

约定：报告里每个含数字的陈述行，必须带来源标记 [src: ...]，或该数字在常量白名单中。
用法: python check_numbers.py <report.md> [--constants constants.txt]
"""
import sys, re

def main():
    if len(sys.argv) < 2:
        print("用法: python check_numbers.py <report.md> [--constants constants.txt]"); sys.exit(2)
    report = sys.argv[1]
    constants = set()
    if "--constants" in sys.argv:
        cf = sys.argv[sys.argv.index("--constants") + 1]
        constants = {l.strip() for l in open(cf, encoding="utf-8") if l.strip()}
    num = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')
    fails = []
    for i, line in enumerate(open(report, encoding="utf-8"), 1):
        s = line.strip()
        if not s or not num.search(line):
            continue
        if s.startswith("#"):            # 标题
            continue
        if set(s) <= set("|-: "):        # 表格分隔行
            continue
        if "[src:" in line or "src:" in line:
            continue
        if any(c and c in line for c in constants):
            continue
        fails.append((i, s[:110]))
    if fails:
        print(f"FAIL: {len(fails)} 条含数字的陈述缺少来源标记 [src:...]")
        for i, t in fails: print(f"  L{i}: {t}")
        sys.exit(1)
    print("PASS: 所有数字陈述均有来源标记"); sys.exit(0)

if __name__ == "__main__":
    main()
