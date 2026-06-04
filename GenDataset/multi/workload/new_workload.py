# -*- coding: utf-8 -*-
import random
import numpy as np

# 假定你已在同一工程内
import gen_workload  # 或者 from xxx import generate_workload

#############################
# 1) High-skew（高度偏斜）
#############################
params_high_skew = {
    "table": {
        # 表选择策略：偏向热点表（例如事实表），Zipf 越大越偏
        "zipf": {"top_k": 3, "s": 1.2}
    },
    "attr": {
        # 属性选择策略：偏向长尾/热点列
        "zipf": {"k": 3, "s": 1.1}
    },
    "center": {
        # 谓词中心：从分布尾部（≥P95）抽样
        "tail": {"p": 0.95}
    },
    "width": {
        # 谓词宽度：指数分布的小宽度（越窄越激进）
        "expnarrow": {"lambda": 50, "min_width_ratio": 0.001}
    },
    "table_params": {},
    "attr_params": {},
    "center_params": {},
    "width_params": {},
    "number": {
        "high_skew": 100  # 产出 2000 条 high-skew 查询
    }
}

#############################
# 2) Adversarial（对抗性/近空）
#############################
params_adversarial = {
    "table": {
        # 表选择：偏向稀疏连接的组合（没有专门策略就仍用 zipf）
        "zipf": {"top_k": 4, "s": 1.3}
    },
    "attr": {
        # 属性选择：优先稀有值（长尾/低频值所在列）
        "rare": {"k": 2, "min_freq_ratio": 0.001}  # <0.1% 的值优先
    },
    "center": {
        # 谓词中心：域边界/极端分位（≤P1 或 ≥P99）→ OOD/错配
        "edge": {"p_low": 0.01, "p_high": 0.99, "mode": "two_sided"}
    },
    "width": {
        # 宽度：以点查询为主，辅以超窄范围；可小概率取“不存在”的值制造空结果
        "pointmix": {"point_prob": 0.9, "ultra_ratio": 0.0005, "nonexist_prob": 0.05}
    },
    "table_params": {},
    "attr_params": {},
    "center_params": {},
    "width_params": {},
    "number": {
        "adversarial": 100  # 产出 1500 条 adversarial 查询
    }
}

if __name__ == "__main__":
    seed = 42
    # 生成 high-skew
    gen_workload(seed, name="imdb_multi_high_skew", params=params_high_skew)
    # 生成 adversarial
    gen_workload(seed + 1, name="imdb_multi_adversarial", params=params_adversarial)
