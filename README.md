# 半潜船装载计算软件 (Semi-Submersible Ship Loading Computer)

## 项目简介 / Project Introduction

基于船舶装载手册要求开发的专业装载计算软件，用于半潜船的浮态、稳性和强度计算。

本软件严格按照装载手册 G-8-1-装载手册(B3598.1174.102) 的要求，实现了完整的船舶装载计算功能。

A professional loading calculation software developed based on ship loading manual requirements, designed for flotation, stability, and strength calculations of semi-submersible ships.

This software strictly follows the requirements of Loading Manual G-8-1-装载手册(B3598.1174.102) and implements complete ship loading calculation functions.

## 功能特性 / Features

### 1. 浮态计算 (Flotation Calculation)
- ✅ 排水量计算 / Displacement calculation
- ✅ 平均吃水、首吃水、尾吃水计算 / Mean draft, forward draft, aft draft calculation
- ✅ 纵倾计算（纵倾值和纵倾角） / Trim calculation (trim value and angle)
- ✅ 静水力参数插值（LCB、VCB、LCF、TPC、MCT、GMT、BMT等） / Hydrostatic parameters interpolation
- ✅ 基于静水力曲线的精确计算 / Accurate calculation based on hydrostatic curves

### 2. 稳性计算 (Stability Calculation)
- ✅ GZ曲线计算 / GZ curve calculation
- ✅ 稳性衡准检查（IMO标准） / Stability criteria check (IMO standards)
- ✅ 自由液面修正 / Free surface correction
- ✅ 初稳性高计算 / Metacentric height calculation

### 3. 强度计算 (Strength Calculation)
- ✅ 剪力分布计算 / Shear force distribution calculation
- ✅ 弯矩分布计算 / Bending moment distribution calculation
- ✅ 最大剪力和弯矩值 / Maximum shear force and bending moment values

### 4. 数据管理 (Data Management)
- ✅ 舱室装载管理 / Compartment loading management
- ✅ 货物装载管理 / Cargo loading management
- ✅ 装载工况保存与加载 / Loading condition save and load

### 5. 用户界面 (User Interface)
- ✅ 直观的PyQt5图形界面 / Intuitive PyQt5 GUI
- ✅ 装载工况编辑器 / Loading condition editor
- ✅ 舱室装载管理 / Compartment loading management
- ✅ 货物装载管理 / Cargo loading management
- ✅ 实时计算结果显示 / Real-time calculation results display
- ✅ GZ曲线、剪力弯矩曲线可视化 / GZ curve, shear force and bending moment curve visualization
- ✅ 稳性衡准检查结果表格 / Stability criteria check results table

## 安装说明 / Installation

### 系统要求 / Requirements
- Python 3.7+
- PyQt5
- NumPy
- Matplotlib
- Pandas
- SciPy

### 安装步骤 / Installation Steps

1. 克隆仓库 / Clone repository:
```bash
git clone https://github.com/JMU0802/semiSubMergedLoadingComputer.git
cd semiSubMergedLoadingComputer
```

2. 安装依赖 / Install dependencies:
```bash
pip install -r requirements.txt
```

3. 运行程序 / Run application:
```bash
python main.py
```

## 使用说明 / Usage Guide

### 基本工作流程 / Basic Workflow

1. **输入装载数据 / Input Loading Data**
   - 在"装载输入"标签页中查看船舶基本参数
   - 添加/编辑舱室装载信息
   - 添加/编辑货物装载信息

2. **执行计算 / Execute Calculation**
   - 点击"计算"按钮执行所有计算

3. **查看结果 / View Results**
   - 浮态结果：查看吃水、纵倾等参数
   - 稳性：查看GZ曲线和稳性衡准检查结果
   - 强度：查看剪力和弯矩曲线

### 舱室管理 / Compartment Management

- 点击"添加"按钮添加新舱室
- 输入舱室参数：名称、类型、容积、重心位置、密度、装载率
- 自由液面力矩可根据需要设置

### 货物管理 / Cargo Management

- 点击"添加"按钮添加新货物
- 输入货物参数：名称、重量、重心位置

## 技术架构 / Technical Architecture

### 项目结构 / Project Structure
```
semiSubMergedLoadingComputer/
├── main.py                 # 主入口 / Main entry point
├── requirements.txt        # 依赖包 / Dependencies
├── README.md              # 说明文档 / Documentation
├── src/                   # 源代码 / Source code
│   ├── models/           # 数据模型 / Data models
│   │   └── ship_models.py
│   ├── calculations/     # 计算模块 / Calculation modules
│   │   ├── flotation.py  # 浮态计算
│   │   ├── stability.py  # 稳性计算
│   │   └── strength.py   # 强度计算
│   ├── data/            # 数据文件 / Data files
│   │   └── hydrostatic_data.py
│   └── gui/             # 用户界面 / GUI
│       ├── main_window.py
│       ├── loading_editor.py
│       ├── compartment_manager.py
│       └── cargo_manager.py
└── tests/               # 测试文件 / Tests
```

### 核心算法 / Core Algorithms

#### 浮态计算 / Flotation Calculation
- 基于静水力曲线的三次样条插值
- 迭代法求解吃水
- 纵倾力矩平衡计算

#### 稳性计算 / Stability Calculation
- GZ曲线计算（含自由液面修正）
- IMO稳性衡准检查
- 初稳性高计算

#### 强度计算 / Strength Calculation
- 重量和浮力沿船长分布
- 剪力和弯矩曲线积分计算

## 开发计划 / Development Plan

### 已完成功能 / Completed Features
- ✅ 完整的浮态计算系统
- ✅ 完整的稳性计算系统
- ✅ 完整的强度计算系统
- ✅ 完整的PyQt5用户界面
- ✅ 舱室和货物管理系统

### 计划功能 / Planned Features
- [ ] 装载工况保存和加载（JSON/CSV格式）
- [ ] 打印和报表生成功能
- [ ] 更多稳性衡准（风压倾侧力矩、乘客集中等）
- [ ] 多语言支持
- [ ] 数据库支持

## 许可证 / License

本软件仅供学习和研究使用。

This software is for educational and research purposes only.

## 联系方式 / Contact

- GitHub: https://github.com/JMU0802/semiSubMergedLoadingComputer
- Issues: https://github.com/JMU0802/semiSubMergedLoadingComputer/issues

## 致谢 / Acknowledgments

感谢所有为船舶工程软件开发做出贡献的工程师和研究人员。

Thanks to all engineers and researchers who have contributed to marine engineering software development.
