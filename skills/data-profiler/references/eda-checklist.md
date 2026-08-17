# EDA 操作清单（data-profiler 参考）

## 1. 读取与结构
```python
import pandas as pd
df = pd.read_excel("附件.xlsx", sheet_name=None)  # 多 sheet 逐个看
df.info(); df.shape; df.head()
```

## 2. 每列画像
- 类型：`df.dtypes`
- 数值列描述：`df.describe(include='all').T`
- 取值域：分类列 `df[col].value_counts()`

## 3. 缺失
```python
miss = df.isna().mean().sort_values(ascending=False)
miss[miss > 0]  # 只报有缺失的列
```
- 看缺失是否集中/是否与某变量相关（MAR 线索）

## 4. 异常值
- IQR：`Q1,Q3 = df[col].quantile([.25,.75]); 超出 Q1-1.5IQR ~ Q3+1.5IQR 记为离群`
- 结合领域常识（如"孕周应在 10~25"，超范围即异常）

## 5. 重复与多重观测
- 完全重复：`df.duplicated().sum()`
- 同对象多次观测：`df.groupby('ID').size()`，>1 即多重观测

## 6. 分布
```python
import matplotlib.pyplot as plt
df[col].hist(bins=30); plt.savefig("results/figures/data_"+col+".png")
```
- 判断偏态、双峰、长尾

## 7. 相关性
```python
df.select_dtypes('number').corr(method='pearson')
df.select_dtypes('number').corr(method='spearman')
```
- |r|>0.8 记为强相关对

## 8. 图表规范
- 中文：`plt.rcParams['font.sans-serif']=['SimHei']; plt.rcParams['axes.unicode_minus']=False`
- 每图有标题、坐标轴带单位、样本量标注

## 9. 事实清单（输出末尾）
只写"观察到什么"，例：「孕周列 12% 缺失，集中在某批次」；「ID=xxx 有 3 次采血记录」
