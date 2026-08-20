# -*- coding: utf-8 -*-
"""校验 method_candidates.md：MC 编号 + 必备字段齐全。"""
import sys, re
txt = open(sys.argv[1] if len(sys.argv) > 1 else "E:/26数模国赛/流程产物/method_candidates.md", encoding="utf-8").read()
mcs = re.findall(r"## MC-\d+", txt)
issues = []
if not mcs and "未检出特殊结构" not in txt: issues.append("无 MC 条目也无空说明")
need_fields = ["触发的数据规则","特殊结构","数学本质","候选专业方法","适用条件","普通方法的风险","文献依据","建议进入 Model Explorer"]
for mc in mcs:
    start = txt.find(mc)
    nxt = re.search(r"## MC-\d+", txt[start+4:])
    seg = txt[start:(start+4+nxt.start())] if nxt else txt[start:]
    for f in need_fields:
        if f not in seg: issues.append(mc + " 缺 " + f)
if issues: print("FAIL:", issues[:8]); sys.exit(1)
print(f"PASS: {len(mcs)} 个 MC 格式齐全"); sys.exit(0)
