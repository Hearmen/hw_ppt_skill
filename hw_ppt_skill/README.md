# HW PPT Skill

一个用于创建和编辑专业 PowerPoint 演示文稿的 AI Skill 工具包，特别针对 **华为风格（Huawei Style）** 的企业级演示文稿进行了优化。

## 项目简介

本项目提供了一套完整的工具和指南，用于：
- 基于模板编辑现有 PPTX 文件
- 使用 PptxGenJS 从零创建演示文稿
- 提取和分析 PowerPoint 内容
- 遵循华为视觉设计规范创建专业中文演示文稿

## 项目结构

```
hw_ppt_skill/
├── SKILL.md                  # 主技能文档 - 快速参考和指南
├── huawei_style.md           # 华为风格设计规范详解
├── editing.md                # 基于模板的编辑工作流
├── pptxgenjs.md              # PptxGenJS 使用教程
├── LICENSE.txt               # 许可证信息
├── template/                 # 华为风格 PPT 模板
│   └── hw_template.pptx      # 包含 4 页示例幻灯片的模板
├── layout/                   # 布局资源库
│   └── materials_library.json # 设计令牌、布局、图表配置
└── scripts/                  # 实用脚本工具
    ├── office/               # Office 文档处理脚本
    │   ├── unpack.py         # 解压 PPTX 文件
    │   ├── pack.py           # 重新打包 PPTX
    │   ├── soffice.py        # LibreOffice 集成
    │   └── validators/       # PPTX 验证器
    ├── add_slide.py          # 添加/复制幻灯片
    ├── clean.py              # 清理未引用资源
    ├── thumbnail.py          # 生成缩略图网格
    └── extract_layout_contract.py # 提取布局契约
```

`template_unpacked/` 和 `unpacked/` 属于本地解包产物，按需通过 `unpack.py` 生成，不再作为仓库内常驻文件维护。

## 快速开始

### 环境依赖

```bash
# 文本提取
pip install "markitdown[pptx]"

# 图像处理
pip install Pillow

# PPTX 生成（使用 PptxGenJS）
npm install -g pptxgenjs

# PDF 转换（可选）
# 需要 LibreOffice 和 Poppler (pdftoppm)
```

### 基本使用

#### 1. 分析现有演示文稿

```bash
# 提取文本内容
python -m markitdown presentation.pptx

# 生成视觉概览缩略图
python scripts/thumbnail.py presentation.pptx

# 解压查看原始 XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

#### 2. 基于模板创建（华为风格）

```bash
# 1. 解压模板
python scripts/office/unpack.py template/hw_template.pptx unpacked/

# 2. 复制幻灯片（以 slide3 内容页为模板）
python scripts/add_slide.py unpacked/ slide3.xml

# 3. 编辑各 slide{N}.xml 文件内容

# 4. 清理未引用的文件
python scripts/clean.py unpacked/

# 5. 打包生成最终 PPTX
python scripts/office/pack.py unpacked/ output.pptx --original template/hw_template.pptx
```

#### 3. 使用 PptxGenJS 从零创建

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

// 使用华为风格宽屏布局
pres.layout = "LAYOUT_WIDE";  // 13.33" × 7.5"

// 添加幻灯片
const slide = pres.addSlide();

// 主标题（红色粗体）
slide.addText("幻灯片主标题", {
  x: 0.15, y: 0.07, w: 13.03, h: 0.62,
  fontSize: 32, bold: true, color: "C8102E",
  fontFace: "微软雅黑", valign: "middle"
});

// 副标题摘要（奶油色背景）
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.75, w: 13.03, h: 0.55,
  fill: { color: "F9F2DA" },
  line: { color: "E8DCC0", width: 0.5 }
});

// 保存文件
pres.writeFile({ fileName: "output.pptx" });
```

## 核心功能

### 华为风格设计规范

本项目提供了详细的华为风格设计规范（`huawei_style.md`）：

| 属性 | 规范 |
|------|------|
| **幻灯片尺寸** | 宽屏 13.33" × 7.5" (LAYOUT_WIDE) |
| **主强调色** | 深红 `C8102E` |
| **正文字体** | 微软雅黑 14pt |
| **标题字体** | 微软雅黑 32pt 粗体 |
| **正文颜色** | 黑色 `000000` |
| **背景** | 纯白 `FFFFFF` |

完整规范请参考 [huawei_style.md](huawei_style.md)。

### 布局资源库

`layout/materials_library.json` 包含：
- **设计令牌**：颜色、字体、间距定义
- **布局模板**：SPLIT_LEFT、THREE_COL、STACKED_SECTIONS 等
- **图表配置**：表格、柱状图、雷达图等
- **示意图**：架构图、流程图、网络拓扑等

### 脚本工具

| 脚本 | 用途 |
|------|------|
| `unpack.py` | 解压 PPTX，美化 XML 输出 |
| `pack.py` | 重新打包，验证并修复 |
| `add_slide.py` | 安全地复制幻灯片 |
| `clean.py` | 清理未引用的媒体文件 |
| `thumbnail.py` | 生成缩略图网格用于预览 |
| `extract_layout_contract.py` | 提取布局契约 |

## 工作流指南

### 编辑工作流

详细指南请参见 [editing.md](editing.md)。

```
分析模板 → 规划映射 → 解压 → 编辑 → 清理 → 打包 → QA
```

### 华为风格创建工作流

详细指南请参见 [huawei_style.md](huawei_style.md)。

```
解压模板 → 复制内容页 → 编辑内容 → 清理 → 打包
```

### QA 流程

1. **内容 QA**：使用 `markitdown` 检查文本内容
2. **视觉 QA**：转换为图片后使用子代理检查
3. **修复循环**：发现问题 → 修复 → 重新验证

```bash
# 转换为图片进行视觉检查
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

## 文档索引

| 文档 | 内容 |
|------|------|
| [SKILL.md](SKILL.md) | 主技能文档，快速参考 |
| [huawei_style.md](huawei_style.md) | 华为风格设计规范 |
| [editing.md](editing.md) | 模板编辑工作流 |
| [pptxgenjs.md](pptxgenjs.md) | PptxGenJS API 教程 |

## 许可证

© 2025 Anthropic, PBC. All rights reserved.

使用这些材料（包括所有代码、提示、资源、文件和 Skill 的其他组件）受您与 Anthropic 关于使用 Anthropic 服务的协议管辖。请参阅 [LICENSE.txt](LICENSE.txt) 获取完整条款。

## 贡献

本项目作为 AI Skill 工具包，主要用于 Anthropic 服务内的 PPTX 处理任务。

---

**提示**：当用户要求创建"华为风格"、"华为风格 PPT"或"专业中文 PPT"时，请务必先阅读 [huawei_style.md](huawei_style.md) 并严格遵循其中的设计规范。
