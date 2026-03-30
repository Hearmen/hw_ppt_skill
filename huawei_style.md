# Huawei 演示文稿风格规范

---

**模板结构说明**：`template/hw_template.pptx` 包含 4 页示例幻灯片，直接在模版上进行修改：
- **slide1**：标题页（使用 slideMaster2）
- **slide2**：目录页（使用 slideMaster1）
- **slide3**：内容页（使用 slideMaster3）
- **slide4**：结束页（使用 slideMaster4）

---

## 一、尺寸与布局

| 属性 | 值 |
|------|-----|
| 幻灯片尺寸 | LAYOUT_WIDE（13.33" × 7.5"） |
| 内容区左边距 | 0.15" |
| 内容区右边距 | 0.15"（右边界约 13.18"） |
| 顶部标题栏高度 | 约 0.62"（y=0.07"） |
| 副标题栏高度 | 约 0.74"（y=0.77"） |
| 内容区起始 y | 约 1.76" |
| 内容区底部 y | 约 6.90"（留出底部 footer） |

---

## 二、配色方案

### 主色调

| 用途 | 颜色代码 | 说明 |
|------|---------|------|
| **主强调色（红）** | `C8102E` | 标题文字、边框、关键词高亮 |
| **主强调色（亮红）** | `E9002F` | 品牌标记、图标强调 |
| **深红链接色** | `C7000B` | 超链接 |
| **正文黑** | `000000` / `1D1D1B` | 正文文字 |
| **次级蓝灰** | `44546A` | 次要标签、说明文字 |
| **浅蓝背景** | `DEEBF7` | 信息框背景 |
| **橙色强调** | `ED7D31` | 第二强调色（图表/标签） |
| **线条灰** | `AEB5C0` | 分隔线、次要图形 |
| **浅灰背景** | `E2E6ED` / `F1F1F2` | 卡片/区块背景 |
| **白色** | `FFFFFF` | 反色文字、浅色背景区块 |
| **页脚背景** | `F0F0F0` | 页脚区域浅灰背景 |

### 配色原则

- **白色背景为主**：正文幻灯片背景为纯白（`FFFFFF`）
- **红色（`C8102E`）主导**：用于顶部标题、关键词、小标题左侧 accent 条
- **黑色正文**：所有正文文字使用黑色 `000000`，次要说明使用 `44546A`
- **黑色边框**：所有边框使用黑色`000000`
- **禁止使用渐变**：所有填充均为纯色

---

## 三、排版规范

### 字体

| 元素 | 字体 | 中文字体 | 尺寸 | 样式 |
|------|------|---------|------|------|
| 标题页主标题 | Arial / 微软雅黑 | 微软雅黑 | 57pt（5700/100） | 常规，白色或黑色 |
| 幻灯片主标题 | 微软雅黑 | 微软雅黑 | 32pt（3200/100） | 粗体，红色 `C8102E` |
| 副标题/摘要 | 微软雅黑 | 微软雅黑 | 14pt（1400/100） | 粗体，`44546A` 或黑色 |
| 区块小标题 | 微软雅黑 | 微软雅黑 | 14pt | 粗体， 黑色 或者 红底白字 |
| 正文内容 | 微软雅黑 | 微软雅黑 | **14pt** | 常规，黑色 |
| 页脚文字 | Arial | 微软雅黑 | 10pt | 常规，`1D1D1B` 黑色 |
| 结束页标语 | 微软雅黑 | 微软雅黑 | 13pt | 常规，`1D1D1B` 黑色 |

> **注意**：该演示文稿使用 `微软雅黑` 字体作为中文主要字体，`Arial` 作为英文辅助字体。生成中文演示文稿时，`fontFace` 应始终设为 `"微软雅黑"`。

### 标题栏结构（每张正文幻灯片）

每张幻灯片顶部有两个固定元素：

**1. 主标题栏**（红色文字）
标题字数要多，70字左右，占两行
```javascript
// 主标题文字（红色，粗体）
slide.addText("幻灯片主标题", {
  x: 0.15, y: 0.07, w: 13.03, h: 0.62,
  fontSize: 32, bold: true, color: "C8102E",
  fontFace: "微软雅黑", valign: "middle", margin: 0
});
```

**2. 副标题摘要栏**（奶油色背景框 + 细边框，深色文字）

```javascript
// 副标题背景框（奶油色 + 细边框）
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.15,           // 与主标题左对齐
  y: 0.75,           // 主标题下方
  w: 13.03,          // 与主标题同宽
  h: 0.55,           // 适配 14pt 文字
  fill: { color: "F9F2DA" },        // 奶油色背景
  line: { color: "E8DCC0", width: 0.5 }  // 细边框
});

// 副标题文字
slide.addText("一句话总结本页核心观点", {
  x: 0.25,           // 框左侧 + 0.1" 内边距
  y: 0.75,           // 与框对齐
  w: 12.83,          // 框宽 - 0.2" 左右内边距
  h: 0.55,           // 与框同高
  fontSize: 14,      // 14pt
  bold: true,
  color: "44546A",   // 蓝灰色
  fontFace: "微软雅黑",
  valign: "middle",
  margin: 0
});
```

### 内容区块小标题

区块小标题使用 **黑色粗体** + 左侧细红色矩形 accent 条：
```javascript
// 红色 accent 竖条
slide.addShape(pres.shapes.RECTANGLE, {
  x: contentX, y: blockY, w: 0.06, h: 0.27,
  fill: { color: "C8102E" }, line: { color: "C8102E" }
});
// 小标题文字
slide.addText("区块名称", {
  x: contentX + 0.1, y: blockY, w: blockW - 0.1, h: 0.27,
  fontSize: 14, bold: true, color: "C8102E",
  fontFace: "微软雅黑", valign: "middle", margin: 0
});
```

---


## 四、内容卡片样式


该风格广泛使用**信息卡片**来组织内容区块，每页都有多种信息卡片类型，每页至少有一个diagrame卡片。
卡片之间可以嵌套
顶层布局之间使用黑色粗虚线分隔

卡片特征：
1.图形全部使用尖角矩形
```javascript
// 卡片背景（白色或浅蓝背景，带边框）
slide.addShape(pres.shapes.RECTANGLE, {
  x: cardX, y: cardY, w: cardW, h: cardH,
  fill: { color: "FFFFFF" },
  line: { color: "000000", width: 1 }  
});
// 或浅蓝背景卡片
slide.addShape(pres.shapes.RECTANGLE, {
  x: cardX, y: cardY, w: cardW, h: cardH,
  fill: { color: "DEEBF7" },
  line: { color: "5B9BD5", width: 0.75 }
});
```

2. 文本框卡片
```javascript
// 红色标题栏（带文字）
slide.addText("文本框主题", {
  x: 0.5, y: 1.0, w: 9.0, h: 0.6,
  fontSize: 18, bold: true, color: "FFFFFF",
  fontFace: "微软雅黑", valign: "middle",
  fill: { color: "C8102E" }  // 红色背景
});

// 白色内容区（带项目符号）
slide.addText([
  { text: "文本内容" },
  { text: "文本内容" }
], {
  x: 0.5, y: 1.6, w: 9.0, h: 2.5,
  fontSize: 14, color: "333333",
  fontFace: "微软雅黑", valign: "top",
  bullet: true,  // 自动项目符号
  fill: { color: "FFFFFF" },           // 白色背景
  line: { color: "DDDDDD", width: 0.5 } // 浅灰边框
});
```

### 卡片内常见布局

卡片布局参考 `layout/materials_library.json`
- **左侧宽图 + 右侧文字列** (60/40 或 55/45 分割)
- **横向均分卡片**：2列、3列、4列等分内容块
- **嵌套标签**：区块内小标题用黑色粗体，正文 14pt 常规

---

## 五、数据与表格

表格样式：
```javascript
slide.addTable(rows, {
  x: tableX, y: tableY, w: tableW,
  border: { pt: 0.5, color: "AEB5C0" },
  colW: [...],  // 按内容比例分配
  // 表头行
  // rows[0] 每个单元格：{ text: "...", options: { fill: { color: "C8102E" }, color: "FFFFFF", bold: true, fontFace: "微软雅黑", fontSize: 12 } }
  // 数据行交替背景
  // 奇数行：fill { color: "FFFFFF" }，偶数行：fill { color: "F1F1F2" }
});
```

---

## 六、图表配色

图表系列颜色遵循主色调：

```javascript
chartColors: ["C8102E", "5B9BD5", "ED7D31", "44546A", "70AD47"]
// 主红 → 蓝 → 橙 → 蓝灰 → 绿
```

---

## 七、基于模板的创建方式

使用 `hw_template.pptx` 作为模板创建演示文稿的推荐工作流程：

```bash
# 1. 解压模板
python scripts/office/unpack.py hw_template.pptx unpacked/

# 2. 复制幻灯片（以 slide3 内容页为模板创建新幻灯片）
python scripts/add_slide.py unpacked/ slide3.xml

# 3. 编辑各 slide{N}.xml 中的内容

# 4. 清理未引用的文件
python scripts/clean.py unpacked/

# 5. 打包生成最终 PPT
python scripts/office/pack.py unpacked/ output.pptx --original hw_template.pptx
```

**模板幻灯片用途**：
- **slide1**：标题页模板（slideMaster2）
- **slide2**：目录页模板（slideMaster1）
- **slide3**：内容页模板（slideMaster3）
- **slide4**：结束页模板（slideMaster4）

### 当模板只约束固定壳层时

如果你的模板要求实际上只有这些固定部分：
- 封面
- 目录
- 结束页
- 正文页的页眉与页脚

那么应采用 **混合模式**，而不是全文照搬模板布局。

原则如下：

1. **封面 / 目录 / 结束页**：直接基于模板页修改内容。
2. **正文页**：复制 `slide3` 作为内容页壳层。
3. **页眉页脚**：视为锁定区域，不移动、不删除。
4. **正文内容区**：重新布局，卡片、结构图、对比区、时间线都可以在内容区自由生成。
一句话：

**模板负责“页框”，生成器负责“版心”。**

---

## 八、完整幻灯片代码模板

以下是符合 Huawei 风格的单张正文幻灯片完整代码框架：

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";  // 13.33" × 7.5"

const slide = pres.addSlide();

// ── 背景 ──────────────────────────────────────────
slide.background = { color: "FFFFFF" };

// ── 顶部主标题栏 ──────────────────────────────────
slide.addText("幻灯片主标题", {
  x: 0.15, y: 0.07, w: 13.03, h: 0.62,
  fontSize: 32, bold: true, color: "C8102E",
  fontFace: "微软雅黑", valign: "middle", margin: 8
});

// ── 副标题摘要行 ──────────────────────────────────
// 副标题背景框（奶油色 + 细边框）
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.15,           // 与主标题左对齐
  y: 0.75,           // 主标题下方
  w: 13.03,          // 与主标题同宽
  h: 0.55,           // 适配 14pt 文字
  fill: { color: "F9F2DA" },        // 奶油色背景
  line: { color: "E8DCC0", width: 0.5 }  // 细边框
});

// 副标题文字
slide.addText("本页核心观点一句话摘要", {
  x: 0.25,           // 框左侧 + 0.1" 内边距
  y: 0.75,           // 与框对齐
  w: 12.83,          // 框宽 - 0.2" 左右内边距
  h: 0.55,           // 与框同高
  fontSize: 14, bold: true, color: "44546A",
  fontFace: "微软雅黑", valign: "middle", margin: 0
});

// ── 内容区（示例：两列布局）─────────────────────────
const COL1_X = 0.15, COL1_W = 6.3;
const COL2_X = 6.6,  COL2_W = 6.58;
const CONTENT_Y = 1.76;

// 左列小标题
slide.addShape(pres.shapes.RECTANGLE, {
  x: COL1_X, y: CONTENT_Y, w: 0.06, h: 0.27,
  fill: { color: "C8102E" }, line: { color: "C8102E" }
});
slide.addText("左侧区块标题", {
  x: COL1_X + 0.1, y: CONTENT_Y, w: COL1_W - 0.1, h: 0.27,
  fontSize: 14, bold: true, color: "000000",
  fontFace: "微软雅黑", valign: "middle", margin: 0
});
// 左列正文
slide.addText([
  { text: "核心定义：", options: { bold: true, color: "000000" } },
  { text: "正文内容描述……", options: { bold: false, color: "000000" } }
], {
  x: COL1_X, y: CONTENT_Y + 0.35, w: COL1_W, h: 4.8,
  fontSize: 14, fontFace: "微软雅黑", valign: "top",
  color: "000000", margin: 4, wrap: true
});

// 分割线
const LINE_X = COL1_X + COL1_W + 0.15;  // 左列右边缘 + 间距
const LINE_Y_START = CONTENT_Y;          // 与标题同高
const LINE_Y_END = CONTENT_Y + 5.2;      // 延伸至底部（比正文稍长）

slide.addShape(pres.shapes.LINE, {
  x: LINE_X, y: LINE_Y_START, w: 0, h: LINE_Y_END - LINE_Y_START,
  line: { 
    color: "000000",      // 黑色
    width: 2.25,          // 粗线（2.25pt）
    dashType: "dash"      // 虚线样式
  }
});

// 右列小标题
const COL2_X_NEW = LINE_X + 0.15;  // 虚线右侧 + 间距

slide.addShape(pres.shapes.RECTANGLE, {
  x: COL2_X_NEW, y: CONTENT_Y, w: 0.06, h: 0.27,
  fill: { color: "C8102E" }, line: { color: "C8102E" }
});
slide.addText("右侧区块标题", {
  x: COL2_X_NEW + 0.1, y: CONTENT_Y, w: COL2_W - 0.1, h: 0.27,
  fontSize: 14, bold: true, color: "000000",
  fontFace: "微软雅黑", valign: "middle", margin: 0
});
// 右列内容...


pres.writeFile({ fileName: "output.pptx" });
```

---

## 十三、风格总结

| 特征 | 规则 |
|------|------|
| 背景 | 纯白 `FFFFFF` |
| 主强调色 | 深红 `C8102E`（Pantone 186C） |
| 字体 | 中文 `微软雅黑`，英文 `Arial` |
| 正文字号 | **14pt**（较旧版增大） |
| 标题栏 | 红色粗体，顶部偏左，全宽 |
| 副标题 | 白底深蓝灰色粗体 |
| 区块标题 | 红色左侧 accent 竖条 + 黑色粗体文字 |
| 正文 | 黑色 `000000`，14pt，微软雅黑常规 |
| 卡片边框 | 红色 `C8102E` 细边框（1pt）或无边框白底 |
| 页脚 | 浅灰 `F0F0F0` 背景，`Security Level:` 文字 |
| 禁止 | 渐变、阴影装饰、蓝色标题 |

---

## 十四、颜色常量参考

```javascript
const COLORS = {
  red: "C8102E",           // 主红色（Pantone 186C）
  brightRed: "E9002F",     // 亮红色
  linkRed: "C7000B",       // 链接红色
  black: "000000",         // 正文黑
  darkText: "1D1D1B",      // 深色文字
  blueGray: "44546A",      // 蓝灰色
  lightBlue: "DEEBF7",     // 浅蓝背景
  orange: "ED7D31",        // 橙色强调
  lineGray: "AEB5C0",      // 线条灰
  lightGray: "E2E6ED",     // 浅灰
  bgGray: "F0F0F0",        // 页脚背景
  white: "FFFFFF"          // 白色
};
```

---

## 十五、常见错误与注意事项

1. **字号过小**：正文请勿小于 14pt，标题页主标题应使用 50pt+
2. **颜色错误**：使用 `C8102E` 而非 `C00000` 作为主红色
3. **页脚缺失**：每张正文幻灯片都应包含页脚
4. **字体不一致**：中文请始终使用 "微软雅黑"，不要使用 "Microsoft YaHei"
5. **渐变填充**：华为风格禁止使用任何渐变，使用纯色填充
6. **占位符残留**：使用模板编辑时，确保清除所有 placeholder 文字
