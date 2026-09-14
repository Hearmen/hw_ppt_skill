# Huawei 演示文稿风格规范

---

### Template-Based Workflow

When using an existing presentation as a template:

1. **Analyze existing slides**:
   ```bash
   python scripts/thumbnail.py template.pptx
   python -m markitdown template.pptx
   ```
   Review `thumbnails.jpg` to see layouts, and markitdown output to see placeholder text.

2. **Plan slide mapping**: For each content section, choose a template slide.

   ⚠️ **USE VARIED LAYOUTS** — monotonous presentations are a common failure mode. Don't default to basic title + bullet slides. Actively seek out:
   - Multi-column layouts (2-column, 3-column)
   - Image + text combinations
   - Full-bleed images with text overlay
   - Quote or callout slides
   - Section dividers
   - Stat/number callouts
   - Icon grids or icon + text rows

   **Avoid:** Repeating the same text-heavy layout for every slide.

   Match content type to layout style (e.g., key points → bullet slide, team info → multi-column, testimonials → quote slide).

3. **Unpack**: `python scripts/office/unpack.py template.pptx unpacked/`

4. **Build presentation** (do this yourself, not with subagents):
   - Delete unwanted slides (remove from `<p:sldIdLst>`)
   - Duplicate slides you want to reuse (`add_slide.py`)
   - Reorder slides in `<p:sldIdLst>`
   - **Complete all structural changes before step 5**

5. **Edit content**: Update text in each `slide{N}.xml`.
   **Use subagents here if available** — slides are separate XML files, so subagents can edit in parallel.

6. **Clean**: `python scripts/clean.py unpacked/`

7. **Pack**: `python scripts/office/pack.py unpacked/ output.pptx --original template.pptx`

## Hybrid Workflow: Template Shell + Free Content Area

Use this mode when the template only constrains:
- cover slide
- table of contents slide
- ending slide
- header/footer or other fixed chrome on every page


the template provides the fixed shell, but it does **not** own the content layout.

Recommended flow:

1. Keep template slides for cover / TOC / ending.
2. Duplicate the template's normal content slide as a shell.
3. Lock header/footer/theme elements from that shell.
4. Treat the central content area as an editable canvas.
5. Generate text blocks, cards, diagrams, and tables only inside that content area.
6. If content does not fit, add another content slide instead of shrinking the entire page.

Practical rule:

- **Template controls frame; generator controls body.**
- Do not force generated content to mimic incidental placeholder positions from the template.
- Lock header/footer regions first, then compose the content area using your own layout rules.

Suggested inputs for the model:

- template file path
- which slides are fixed: cover / TOC / ending
- locked regions on normal slides: header / footer
- content area bounds
- overflow policy: split slide before shrinking body text
- optional layout preference: architecture / comparison / timeline / 2-column / cards

---

## Scripts

| Script | Purpose |
|--------|---------|
| `unpack.py` | Extract and pretty-print PPTX |
| `add_slide.py` | Duplicate slide or create from layout |
| `clean.py` | Remove orphaned files |
| `pack.py` | Repack with validation |
| `thumbnail.py` | Create visual grid of slides |

### unpack.py

```bash
python scripts/office/unpack.py input.pptx unpacked/
```

Extracts PPTX, pretty-prints XML, escapes smart quotes.

### add_slide.py

```bash
python scripts/add_slide.py unpacked/ slide2.xml      # Duplicate slide
python scripts/add_slide.py unpacked/ slideLayout2.xml # From layout
```

Prints `<p:sldId>` to add to `<p:sldIdLst>` at desired position.

### clean.py

```bash
python scripts/clean.py unpacked/
```

Removes slides not in `<p:sldIdLst>`, unreferenced media, orphaned rels.

### pack.py

```bash
python scripts/office/pack.py unpacked/ output.pptx --original input.pptx
```

Validates, repairs, condenses XML, re-encodes smart quotes.

### thumbnail.py

```bash
python scripts/thumbnail.py input.pptx [output_prefix] [--cols N]
```

Creates `thumbnails.jpg` with slide filenames as labels. Default 3 columns, max 12 per grid.

**Use for template analysis only** (choosing layouts). For visual QA, use `soffice` + `pdftoppm` to create full-resolution individual slide images—see SKILL.md.

---

## Slide Operations

Slide order is in `ppt/presentation.xml` → `<p:sldIdLst>`.

**Reorder**: Rearrange `<p:sldId>` elements.

**Delete**: Remove `<p:sldId>`, then run `clean.py`.

**Add**: Use `add_slide.py`. Never manually copy slide files—the script handles notes references, Content_Types.xml, and relationship IDs that manual copying misses.

---

## Editing Content

**Subagents:** If available, use them here (after completing step 4). Each slide is a separate XML file, so subagents can edit in parallel. In your prompt to subagents, include:
- The slide file path(s) to edit
- **"Use the Edit tool for all changes"**
- The formatting rules and common pitfalls below

For each slide:
1. Read the slide's XML
2. Identify ALL placeholder content—text, images, charts, icons, captions
3. Replace each placeholder with final content

**Use the Edit tool, not sed or Python scripts.** The Edit tool forces specificity about what to replace and where, yielding better reliability.

### Formatting Rules

---

#### 一、尺寸与布局

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

#### 二、配色方案

##### 主色调

| 用途 | 颜色代码 | 说明 |
|------|---------|------|
| **主强调色（红）** | `C8102E` | 标题文字、边框、关键词高亮 |
| **主强调色（亮红）** | `E9002F` | 品牌标记、图标强调 |
| **深红链接色** | `C8102E` | 超链接 |
| **正文黑** | `000000` / `1D1D1B` | 正文文字 |
| **次级蓝灰** | `44546A` | 次要标签、说明文字 |
| **浅蓝背景** | `DEEBF7` | 信息框背景 |
| **橙色强调** | `ED7D31` | 第二强调色（图表/标签） |
| **线条灰** | `AEB5C0` | 分隔线、次要图形 |
| **浅灰背景** | `E2E6ED` / `F1F1F2` | 卡片/区块背景 |
| **白色** | `FFFFFF` | 反色文字、浅色背景区块 |

##### 配色原则

- **白色背景为主**：正文幻灯片背景为纯白（`FFFFFF`）
- **红色（`C8102E`）主导**：用于顶部标题、关键词、小标题左侧 accent 条
- **黑色正文**：所有正文文字使用黑色 `000000`，次要说明使用 `44546A`
- **禁止使用渐变**：所有填充均为纯色

---

#### 三、排版规范

##### 字体

| 元素 | 字体 | 中文字体 | 尺寸 | 样式 |
|------|------|---------|------|------|
| 标题页主标题 | Arial / 微软雅黑 | 微软雅黑 | 57pt（5700/100） | 常规，白色或黑色 |
| 幻灯片主标题 | 微软雅黑 | 微软雅黑 | 32pt（3200/100） | 粗体，红色 `C8102E` |
| 副标题/摘要 | 微软雅黑 | 微软雅黑 | 14pt（1400/100） | 粗体，黑色 |
| 区块小标题 | 微软雅黑 | 微软雅黑 | 14pt | 粗体， 黑色 或者 红底白字 |
| 正文内容 | 微软雅黑 | 微软雅黑 | **14pt** | 常规，黑色 |
| 结束页标语 | 微软雅黑 | 微软雅黑 | 13pt | 常规，`1D1D1B` 黑色 |

> **注意**：该演示文稿使用 `微软雅黑` 字体作为中文主要字体，`Arial` 作为英文辅助字体。生成中文演示文稿时，`fontFace` 应始终设为 `"微软雅黑"`。

##### 标题栏结构（每张正文幻灯片）

每张幻灯片顶部有两个固定元素：

**1. 主标题栏**（红色文字）
标题字数要多，70字左右，占两行
```javascript
// 主标题文字（红色，粗体）
slide.addText("幻灯片主标题", {
  x: 0.15, y: 0.08, w: 13.03, h: 1.15,
  fontSize: 32, bold: true, color: "C8102E",
  fontFace: "微软雅黑", valign: "middle", margin: 0.06
});
```

**2. 副标题摘要栏**（奶油色背景框 + 细边框，深色文字）

```javascript
// 副标题背景框（奶油色 + 细边框）
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.15,           // 与主标题左对齐
  y: 1.30,           // 主标题下方
  w: 13.03,          // 与主标题同宽
  h: 0.52,           // 适配 14pt 文字
  fill: { color: "F9F2DA" },        // 奶油色背景
  line: { color: "E8DCC0", width: 0.5 }  // 细边框
});

// 副标题文字
slide.addText("一句话总结本页核心观点", {
  x: 0.25,           // 框左侧 + 0.1" 内边距
  y: 1.30,           // 与框对齐
  w: 12.83,          // 框宽 - 0.2" 左右内边距
  h: 0.52,           // 与框同高
  fontSize: 14,      // 14pt
  color: "000000",   // 黑色
  fontFace: "微软雅黑",
  valign: "middle",
  margin: 0
});
```

##### 内容区块小标题

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


#### 四、内容卡片样式


该风格广泛使用**信息卡片**来组织内容区块，每页都有多种信息卡片类型，**每页至少有一个 diagram 卡片**
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
  fontSize: 18, bold: true, color: "FFFFFF", // 白色文字
  fontFace: "微软雅黑", valign: "middle",
  fill: { color: "C8102E" }  // 红色背景
});

/*
//或者 
slide.addText("文本框主题", {
  x: 0.5, y: 1.0, w: 9.0, h: 0.6,
  fontSize: 18, bold: true, color: "000000",  // 黑色文字
  fontFace: "微软雅黑", valign: "middle"
});
*/

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
  line: { color: "F0F0F0", width: 0.5 } // 浅灰边框
});
```

##### 卡片内常见布局

卡片布局参考 `layout/materials_library.json`
- **左侧宽图 + 右侧文字列** (60/40 或 55/45 分割)
- **横向均分卡片**：2列、3列、4列等分内容块
- **嵌套标签**：区块内小标题用黑色粗体，正文 14pt 常规

---

#### 五、数据与表格

表格样式：

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",

  // Custom colors (match your presentation palette)
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],

  // Clean background
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },

  // Muted axis labels
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",

  // Subtle grid (value axis only)
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },

  // Data labels on bars
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "1E293B",

  // Hide legend for single series
  showLegend: false,
});
```

**Key styling options:**
- `chartColors: [...]` - hex colors for series/segments
- `chartArea: { fill, border, roundedCorners }` - chart background
- `catGridLine/valGridLine: { color, style, size }` - grid lines (`style: "none"` to hide)
- `lineSmooth: true` - curved lines (line charts)
- `legendPos: "r"` - legend position: "b", "t", "l", "r", "tr"


---

## 六、插图

图表系列颜色遵循主色调：

```javascript
chartColors: ["C8102E", "5B9BD5", "ED7D31", "44546A", "70AD47"]
// 主红 → 蓝 → 橙 → 蓝灰 → 绿
```

### Image Sources

```javascript
// From file path
slide.addImage({ path: "images/chart.png", x: 1, y: 1, w: 5, h: 3 });

// From URL
slide.addImage({ path: "https://example.com/image.jpg", x: 1, y: 1, w: 5, h: 3 });

// From base64 (faster, no file I/O)
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });
```

### Image Options

```javascript
slide.addImage({
  path: "image.png",
  x: 1, y: 1, w: 5, h: 3,
  rotate: 45,              // 0-359 degrees
  rounding: true,          // Circular crop
  transparency: 50,        // 0-100
  flipH: true,             // Horizontal flip
  flipV: false,            // Vertical flip
  altText: "Description",  // Accessibility
  hyperlink: { url: "https://example.com" }
});
```

### Image Sizing Modes

```javascript
// Contain - fit inside, preserve ratio
{ sizing: { type: 'contain', w: 4, h: 3 } }

// Cover - fill area, preserve ratio (may crop)
{ sizing: { type: 'cover', w: 4, h: 3 } }

// Crop - cut specific portion
{ sizing: { type: 'crop', x: 0.5, y: 0.5, w: 2, h: 2 } }
```

### Calculate Dimensions (preserve aspect ratio)

```javascript
const origWidth = 1978, origHeight = 923, maxHeight = 3.0;
const calcWidth = maxHeight * (origWidth / origHeight);
const centerX = (10 - calcWidth) / 2;

slide.addImage({ path: "image.png", x: centerX, y: 1.2, w: calcWidth, h: maxHeight });
```

### Supported Formats

- **Standard**: PNG, JPG, GIF (animated GIFs work in Microsoft 365)
- **SVG**: Works in modern PowerPoint/Microsoft 365


## 八、表格

```javascript
slide.addTable([
  ["Header 1", "Header 2"],
  ["Cell 1", "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" }, fill: { color: "F1F1F1" }
});

// Advanced with merged cells
let tableData = [
  [{ text: "Header", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } }, "Cell"],
  [{ text: "Merged", options: { colspan: 2 } }]
];
slide.addTable(tableData, { x: 1, y: 3.5, w: 8, colW: [4, 4] });
```

```javascript
// Bar chart
slide.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1", "Q2", "Q3", "Q4"], values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: 'col',
  showTitle: true, title: 'Quarterly Sales'
});

// Line chart
slide.addChart(pres.charts.LINE, [{
  name: "Temp", labels: ["Jan", "Feb", "Mar"], values: [32, 35, 42]
}], { x: 0.5, y: 4, w: 6, h: 3, lineSize: 3, lineSmooth: true });

// Pie chart
slide.addChart(pres.charts.PIE, [{
  name: "Share", labels: ["A", "B", "Other"], values: [35, 45, 20]
}], { x: 7, y: 1, w: 5, h: 4, showPercent: true });
```

### Better-Looking Charts

Default charts look dated. Apply these options for a modern, clean appearance:

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",

  // Custom colors (match your presentation palette)
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],

  // Clean background
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },

  // Muted axis labels
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",

  // Subtle grid (value axis only)
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },

  // Data labels on bars
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "1E293B",

  // Hide legend for single series
  showLegend: false,
});
```

**Key styling options:**
- `chartColors: [...]` - hex colors for series/segments
- `chartArea: { fill, border, roundedCorners }` - chart background
- `catGridLine/valGridLine: { color, style, size }` - grid lines (`style: "none"` to hide)
- `lineSmooth: true` - curved lines (line charts)
- `legendPos: "r"` - legend position: "b", "t", "l", "r", "tr"


## 七、风格总结

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
| 卡片边框 | 浅灰色 `F0F0F0` 细边框（1pt）或无边框白底 |
| 禁止 | 渐变、阴影装饰、蓝色标题 |

---

## 八、颜色常量参考

```javascript
const COLORS = {
  red: "C8102E",           // 主红色（Pantone 186C）
  brightRed: "E9002F",     // 亮红色
  linkRed: "C8102E",       // 链接红色
  black: "000000",         // 正文黑
  darkText: "1D1D1B",      // 深色文字
  blueGray: "44546A",      // 蓝灰色
  lightBlue: "DEEBF7",     // 浅蓝背景
  orange: "ED7D31",        // 橙色强调
  lineGray: "AEB5C0",      // 线条灰
  lightGray: "E2E6ED",     // 浅灰
  white: "FFFFFF"          // 白色
};
```

---

## 九、常见错误与注意事项

1. **字号过小**：正文请勿小于 14pt，标题页主标题应使用 50pt+
2. **颜色错误**：使用 `C8102E` 而非 `C00000` 作为主红色
4. **字体不一致**：中文请始终使用 "微软雅黑"，不要使用 "Microsoft YaHei"
5. **渐变填充**：华为风格禁止使用任何渐变，使用纯色填充
6. **占位符残留**：使用模板编辑时，确保清除所有 placeholder 文字
7. **Multi-Item Content**

If source has multiple items (numbered lists, multiple sections), create separate `<a:p>` elements for each — **never concatenate into one string**.

**❌ WRONG** — all items in one paragraph:
```xml
<a:p>
  <a:r><a:rPr .../><a:t>Step 1: Do the first thing. Step 2: Do the second thing.</a:t></a:r>
</a:p>
```

**✅ CORRECT** — separate paragraphs with bold headers:
```xml
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 1</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" .../><a:t>Do the first thing.</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 2</a:t></a:r>
</a:p>
<!-- continue pattern -->
```

Copy `<a:pPr>` from the original paragraph to preserve line spacing. Use `b="1"` on headers.

### Smart Quotes

Handled automatically by unpack/pack. But the Edit tool converts smart quotes to ASCII.

**When adding new text with quotes, use XML entities:**

```xml
<a:t>the &#x201C;Agreement&#x201D;</a:t>
```

| Character | Name | Unicode | XML Entity |
|-----------|------|---------|------------|
| `“` | Left double quote | U+201C | `&#x201C;` |
| `”` | Right double quote | U+201D | `&#x201D;` |
| `‘` | Left single quote | U+2018 | `&#x2018;` |
| `’` | Right single quote | U+2019 | `&#x2019;` |

### Other

- **Whitespace**: Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces
- **XML parsing**: Use `defusedxml.minidom`, not `xml.etree.ElementTree` (corrupts namespaces)

