#!/usr/bin/env python3
"""check_repro.py —— 可复现校验（确定性门禁）

读取 results/repro_manifest.json，依次重跑脚本，确认输出文件生成。
manifest 格式: [{"script": "solve_q1.py", "outputs": ["outputs/q1_result.json"]}, ...]
用法: python check_repro.py [manifest]
"""
import sys, os, json, subprocess

def main():
    manifest = sys.argv[1] if len(sys.argv) > 1 else "results/repro_manifest.json"
    if not os.path.exists(manifest):
        print("SKIP: 无 repro_manifest.json（尚未配置可复现清单）"); sys.exit(0)
    entries = json.load(open(manifest, encoding="utf-8"))
    ok = True
    for e in entries:
        script = e["script"]
        print(f"[RUN] {script}")
        r = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  FAIL: {script} 退出码 {r.returncode}\n{r.stderr[:400]}")
            ok = False; continue
        for out in e.get("outputs", []):
            if os.path.exists(out):
                print(f"  OK: {out} 已生成")
            else:
                print(f"  FAIL: 缺少输出 {out}")
                ok = False
    print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
