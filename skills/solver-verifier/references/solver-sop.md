# 求解代码规范与自证模式（solver-verifier 参考）

## 代码结构
```text
results/
├── solve_q1.py          # 每问一个求解脚本
├── verify_q1.py         # 每问一个自证脚本
├── outputs/q1_result.json
└── figures/
```

## solve 脚本骨架
```python
# solve_q1.py
import pandas as pd, numpy as np, json
df = pd.read_excel("../附件.xlsx")
# ... 按 正式模型 实现 ...
result = {"coef": ..., "p_value": ..., "r2": ...}
json.dump(result, open("outputs/q1_result.json","w"), ensure_ascii=False, indent=2)
print("[OUT] q1_result.json written")
```

## verify 自证模式
```python
# verify_q1.py —— 校验 solve 输出的正确性
checks = [("无 NaN", not np.isnan(result["r2"])), ("R2 在 [0,1]", 0 <= result["r2"] <= 1)]
for name, ok in checks: print(("PASS " if ok else "FAIL ") + name)
assert all(ok for _, ok in checks), "verify failed"
```

## 数字溯源约定
论文/报告里每个结果数字后标注来源：`β=0.42 [src: outputs/q1_result.json]`

## 铁律
- verify FAIL 的结果不得进入论文
- 结果落盘后一律引用文件，不口头引用数字
