# 项目文件清单

## 文档文件

| 文件名 | 说明 |
|--------|------|
| README.md | 项目说明文档 |
| PROJECT_SUMMARY.md | 详细项目总结报告（包含所有技术细节和数据校准参数） |
| USER_GUIDE.md | 用户使用指南 |
| PROJECT_FILES.md | 本文件 - 项目文件清单 |
| requirements.txt | Python依赖包列表 |

## 程序入口

| 文件名 | 说明 |
|--------|------|
| run_gui.py | GUI主程序入口 |

## GUI模块 (gui/)

| 文件名 | 说明 |
|--------|------|
| main_window.py | 主窗口（4个标签页，13个工况菜单） |
| form1_widget.py | FORM 1 - 装载数据输入界面 |
| form2_widget.py | FORM 2 - 稳性与强度结果显示界面 |
| report_widget.py | 报表输出界面 |
| ship_data_viewer.py | 船舶数据可视化界面 |
| calculation_engine.py | 计算引擎协调器 |

## 核心计算模块 (src/core/)

| 文件名 | 说明 |
|--------|------|
| buoyancy_calculator.py | 浮力计算器（包含体积校准因子1.006） |
| stability.py | 稳性计算（GM、GZ曲线、稳性衡准） |
| strength.py | 强度计算（剪力、弯矩、重量分布、浮力分布） |
| flotation.py | 浮态计算（吃水、纵倾迭代求解） |
| loading_condition.py | 装载工况数据结构 |
| calculation_engine.py | 计算引擎核心 |
| draught_survey.py | 吃水测量相关计算 |
| onboard_stability.py | 船上稳性计算 |
| strength_advanced.py | 高级强度计算 |

## 船舶数据模块 (ship_data/)

### 原始数据文件

| 文件名 | 说明 |
|--------|------|
| bonjeancurve.txt | 邦氏曲线数据（21个站位，吃水0-26m） |
| Crosscurves.txt | 静稳性曲线数据（用于GZ曲线计算） |
| frameToLength.txt | Frame号与位置对照表（271个Frame） |
| lightshipWeight.txt | 空船重量分布数据（271个Frame） |
| tanksdetails.txt | 舱室详细信息（115个舱室） |
| tankSummary.txt | 舱室汇总表 |
| data.txt | 静水力表数据 |

### 数据解析模块

| 文件名 | 说明 |
|--------|------|
| bonjean_curve_data.py | 邦氏曲线数据解析 |
| crosscurves_data.py | 静稳性曲线数据解析 |
| frame_data.py | Frame数据解析（包含空船重量校准因子0.9743654958） |
| tanks_details_data.py | 舱室数据解析 |
| tanks_details_data.json | 舱室数据JSON格式 |
| hydrostatic_tables_complete.py | 完整静水力表解析 |
| hydrostatic_tables_2d.py | 二维静水力表 |
| hydrostatic_tables.py | 静水力表基础模块 |
| lcb_mct_data.py | LCB和MCT数据 |
| ship_particulars.py | 船舶主要参数 |
| stability_criteria.py | 稳性衡准定义 |
| tank_data.py | 舱室基础数据 |
| tank_definitions.py | 舱室定义 |
| sectional_area_curve.py | 横剖面面积曲线 |
| loading_conditions.py | 装载工况数据 |
| loading_conditions_manual.py | 手册装载工况 |
| default_loading_conditions.py | 默认装载工况 |
| parse_tanks_details.py | 舱室详细信息解析工具 |

## 标准工况数据 (default_conditions/)

| 文件名 | 工况名称 | 排水量(t) |
|--------|---------|----------|
| LC00.json | Lightship | 20,871.4 |
| LC01.json | Light ballast, departure | 47,516.4 |
| LC02.json | Light ballast, arrival | 45,016.4 |
| LC03.json | Light ballast, departure (alt) | 47,516.4 |
| LC04.json | Light ballast, arrival (alt) | 45,016.4 |
| LC05.json | Maximum deadweight | 68,000.0 |
| LC11.json | Medium ballast, departure | 52,000.0 |
| LC12.json | Medium ballast, arrival | 50,000.0 |
| LC23.json | Heavy ballast, departure | 55,000.0 |
| LC24.json | Heavy ballast, arrival | 53,000.0 |
| LC25.json | Full ballast, departure | 60,000.0 |
| LC26.json | Full ballast, arrival | 58,000.0 |
| LC31.json | Maximum ballast | 65,000.0 |

## 参考文档 (Documents/)

| 文件名 | 说明 |
|--------|------|
| G-5-邦氏数值表(SC9122-100-06).pdf | 邦氏曲线数值表 |
| G-8-1-装载手册(B3598.1174.102).pdf | 装载手册主文档 |
| G-8-2-装载手册附录1(B3598.1174.102).pdf | 装载手册附录1 |
| G-8-3-装载手册附录2(B3598.1174.102).pdf | 装载手册附录2 |

## 关键数据校准参数

### 1. 空船重量校准因子
- **数值**: 0.9743654958
- **位置**: `ship_data/frame_data.py`
- **原因**: 将原始数据总和21420.8t缩放到精确的20871.40t
- **应用**: 所有空船重量密度数据乘以此因子

### 2. 浮力体积校准因子
- **数值**: 1.006
- **位置**: `src/core/buoyancy_calculator.py`
- **原因**: 修正邦氏曲线数据与静水力表之间约0.6%的系统误差
- **应用**: 所有浮力体积计算乘以此因子

### 3. 坐标系统参数
- **Frame间距**: 0.8 m
- **AP位置**: 4.24 m (从Frame 0算起)
- **FP位置**: 216.37 m (从Frame 0算起)
- **LPP**: 212.13 m (垂线间长)
- **位置**: `ship_data/frame_data.py`

## 项目统计

- **总代码行数**: 约8000行
- **Python文件数**: 约40个
- **数据文件数**: 13个
- **工况文件数**: 13个
- **参考文档数**: 4个
- **开发时间**: 2026年2月
- **Python版本**: 3.13
- **主要依赖**: PyQt5, NumPy, SciPy, Matplotlib

## 文件完整性检查

所有核心文件均已验证：
- ✅ 所有数据文件完整
- ✅ 所有计算模块正常工作
- ✅ 所有13个工况可正常加载
- ✅ GUI界面功能完整
- ✅ 计算精度满足要求（排水量误差<0.1t）

## 注意事项

1. **不要修改原始数据文件**（ship_data/目录下的.txt文件）
2. **不要删除校准参数**（会导致计算精度下降）
3. **保留所有参考文档**（Documents/目录）
4. **保留所有工况文件**（default_conditions/目录）

---

*本清单最后更新：2026年2月*

