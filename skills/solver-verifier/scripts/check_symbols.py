#!/usr/bin/env python3
"""check_symbols.py —— 符号一致性校验（确定性门禁）

从 正式模型.md 提取 $...$ 符号定义，与代码目录中的变量名比对，报告无对应实现的符号。
用法: python check_symbols.py <正式模型.md> <code_dir>
"""
import sys, os, re

def extract_symbols(spec):
    text = open(spec, encoding="utf-8").read()
    cleaned = set()
    for s in re.findall(r'\$([^$\s]+)\$', text):
        s2 = re.sub(r'\\(?:mathbf|mathrm|text|boldsymbol|hat|bar|tilde)\{([^}]*)\}', r'\1', s)
        s2 = re.sub(r'\\[a-zA-Z]+', '', s2)
        s2 = re.sub(r'[{}_\\]', '', s2)
        if s2.strip():
            cleaned.add(s2.strip())
    return cleaned

def extract_code_names(code_dir):
    names = set()
    for root, _, files in os.walk(code_dir):
        for f in files:
            if f.endswith(".py"):
                names |= set(re.findall(r'\b[a-zA-Z_]\w*\b',
                              open(os.path.join(root, f), encoding="utf-8").read()))
    return names

def main():
    if len(sys.argv) < 3:
        print("用法: python check_symbols.py <正式模型.md> <code_dir>"); sys.exit(2)
    syms = extract_symbols(sys.argv[1])
    code = extract_code_names(sys.argv[2])
    missing = [s for s in sorted(syms) if not ({s, s.replace("_", "")} & code)]
    if missing:
        print(f"FAIL: {len(missing)} 个符号在代码中无对应变量")
        for s in missing: print("  $" + s + "$")
        sys.exit(1)
    print(f"PASS: 提取 {len(syms)} 个符号，均在代码中有对应"); sys.exit(0)

if __name__ == "__main__":
    main()
