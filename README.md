# 半潜船装载计算软件 (Semi-Submersible Ship Loading Computer)

## 项目简介
基于船舶装载手册要求开发的专业装载计算软件，用于半潜船的浮态、稳性和强度计算。

本软件严格按照装载手册 G-8-1-装载手册(B3598.1174.102) 的要求，实现了完整的船舶装载计算功能，包括：
- 浮态计算（吃水、纵倾、排水量）
- 稳性计算（GZ曲线、稳性衡准、自由液面修正）
- 强度计算（剪力、弯矩）

## 功能特性

### 1. 浮态计算 (Flotation Calculation)
- ✅ 排水量计算
- ✅ 平均吃水、首吃水、尾吃水计算
- ✅ 纵倾计算（纵倾值和纵倾角）
- ✅ 静水力参数插值（LCB、VCB、LCF、TPC、MCT、GMT、BMT等）
- ✅ 基于静水力曲线的精确计算

### 2. 稳性计算 (Stability Calculation)
- ✅ 初稳性高GM计算
- ✅ 自由液面修正（FSM）
- ✅ GZ曲线（静稳性曲线）计算和绘制
- ✅ 稳性衡准检查：
  - IMO规范（航行工况）
  - DNV规范（半潜工况）
  - CCS规范（半潜工况）
- ✅ 稳性曲线面积计算
- ✅ 最大GZ及对应角度识别

### 3. 强度计算 (Strength Calculation)
- ✅ 剪力曲线计算
- ✅ 弯矩曲线计算
- ✅ 强度衡准检查（中拱、中垂）
- ✅ 不同工况的许用值设置

### 4. 多工况支持
- ✅ Transit（航行工况）
- ✅ Semi-Submerged（半潜工况）
- ✅ Aftload（艉部装载工况）
- ✅ Sideload（侧向装载工况）

### 5. 用户界面
- ✅ 直观的PyQt5图形界面
- ✅ 装载工况编辑器
- ✅ 舱室装载管理
- ✅ 货物装载管理
- ✅ 实时计算结果显示
- ✅ GZ曲线、剪力弯矩曲线可视化
- ✅ 稳性衡准检查结果表格

## 技术栈
- **Python 3.8+** - 主要编程语言
- **PyQt5** - GUI框架
- **NumPy** - 数值计算
- **SciPy** - 科学计算（插值）
- **Matplotlib** - 图表绘制

## 项目结构
```
semiSubMergedLoadingComputer/
├── src/                          # 源代码
│   ├── core/                     # 核心计算模块
│   │   ├── flotation.py         # 浮态计算
│   │   ├── stability.py         # 稳性计算
│   │   ├── strength.py          # 强度计算
│   │   ├── loading_condition.py # 装载工况管理
│   │   └── calculation_engine.py # 计算引擎
│   ├── ui/                       # UI界面
│   │   ├── main_window.py       # 主窗口
│   │   ├── loading_tab.py       # 装载工况编辑
│   │   ├── results_tab.py       # 计算结果显示
│   │   └── plot_widget.py       # 绘图组件
│   ├── data/                     # 数据管理
│   └── utils/                    # 工具函数
├── ship_data/                    # 船舶数据（只读）
│   ├── ship_particulars.py      # 船舶主要参数
│   ├── hydrostatic_data.py      # 静水力数据
│   ├── tank_data.py             # 舱室数据
│   └── stability_criteria.py   # 稳性衡准
├── Documents/                    # 装载手册文档
│   └── G-8-1-装载手册(B3598.1174.102).pdf
├── main.py                       # 程序入口
├── test_calculation.py          # 测试脚本
├── requirements.txt             # 依赖包
├── README.md                    # 项目说明
└── 使用说明.md                   # 用户手册
```

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 测试核心计算功能
```bash
python test_calculation.py
```

### 3. 运行GUI程序
```bash
python main.py
```

## 使用示例

### 命令行测试
```python
from src.core.loading_condition import LoadingCondition
from src.core.calculation_engine import CalculationEngine

# 创建装载工况
condition = LoadingCondition("航行工况", "TRANSIT")

# 添加压载水
condition.add_tank_loading('BT1P', 95)  # 左舷1号压载舱 95%
condition.add_tank_loading('BT1S', 95)  # 右舷1号压载舱 95%

# 添加货物
condition.add_cargo("甲板货物", 5000, 84.0, 10.5)

# 执行计算
engine = CalculationEngine()
engine.set_loading_condition(condition)
results = engine.calculate_all(standard='IMO')

# 查看结果
summary = engine.get_summary()
print(f"排水量: {summary['displacement']:.2f} t")
print(f"GM: {summary['gm']:.3f} m")
print(f"稳性检查: {'通过' if summary['stability_ok'] else '不通过'}")
```

## 核心算法

### 浮态计算
1. 根据总重量从静水力曲线插值得到平均吃水
2. 计算纵倾力矩：M = Δ × (LCG - LCB)
3. 计算纵倾：Trim = M / MCT
4. 计算首尾吃水

### 稳性计算
1. 计算自由液面修正：ΔKG = FSM / Δ
2. 计算修正重心高度：KG' = KG + ΔKG
3. 计算初稳性高：GM = KM - KG'
4. 从稳性横截曲线插值得到KN值
5. 计算GZ：GZ = KN - KG' × sin(θ)
6. 检查稳性衡准

### 强度计算
1. 将重量分布到各站位
2. 计算浮力分布
3. 计算载荷分布：q = 浮力 - 重量
4. 积分得到剪力：SF = ∫q dx
5. 积分得到弯矩：BM = ∫SF dx
6. 检查强度衡准

## 参考规范
- **IMO** - International Maritime Organization
- **DNV** - Det Norske Veritas
- **CCS** - China Classification Society
- **装载手册** - G-8-1-装载手册(B3598.1174.102)

## 开发说明

### 代码规范
- 遵循PEP 8编码规范
- 使用类型注解
- 完整的文档字符串
- 模块化设计

### 数据管理
- 所有船舶数据存储在 `ship_data/` 目录
- 数据文件为只读，不可修改
- 使用Python字典和NumPy数组存储数据

### 扩展性
- 易于添加新的工况类型
- 易于添加新的稳性规范
- 易于修改船舶参数

## 许可证
本项目仅供学习和参考使用。

## 免责声明
本软件仅供参考，实际装载作业应严格遵守船舶装载手册和相关国际公约。最终装载方案应由船长批准。

