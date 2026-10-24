# 出图美术标准提示词（Gemini 深蓝玻璃光效 + 流程图硬规矩）

给 Grok Bot / 画图模型 / 程序化 SVG 出图用。信息图、日报卡、推特复盘、数据海报、流程图默认都按这套。

核心气质一句话：Google Gemini 发布会那种深空蓝 + 软光晕 + 磨砂玻璃，字大、不贴边、不重叠，远看像发布会海报，近看信息仍清楚。

---

## 〇、先选通道（这一步做错，后面再美也救不回来）

| 图类型 | 用什么出 | 为什么 |
|---|---|---|
| 流程图、带大量中文节点的业务路径图 | 只做程序化 SVG → PNG / PDF | 文生图几乎必然糊字、叠字、乱改节点文案 |
| 情绪海报、封面、少字信息图、数据卡 | 文生图可以，中文尽量少、大、短 | 字越少越稳；长句中文交给后期叠字或程序化 |
| 推特 / 社交横图 | 程序化或文生图均可 | 优先 1200×675～1200×900，避免超长竖图被平台压糊 |

规则：只要图上超过大约六句中文说明，就默认程序化，不要赌文生图。

---

## 一、文生图主提示词（复制用）

结构故意拆开：风格锚定 → 构图 → 材质光效 → 文字 → 气质。模型对「靠前的词」更听话，所以把最重要的放前面。

复制整段，末尾只补「具体主题 + 画幅」：

> Google Gemini keynote visual language, premium product launch poster, deep navy void background #071018, one clear focal hierarchy (large title, then glass panels, sparse supporting text), soft radial blue glow top-left and teal cyan glow top-right, subtle low-opacity orbital rings, faint blurred rainbow ribbon (blue to violet to teal to gold) behind panels only, frosted glass cards with hairline luminous border and soft top-edge specular highlight as if lit from upper-left, depth from glow and glass only, flat 2D, clean geometric layout, large high-contrast sans-serif typography, generous padding inside every panel, text never touches edges, compact premium spacing with no large empty voids and no cramped overlap, cinematic but calm, readable Chinese short labels if any

画幅示例（择一写进末尾）：`aspect ratio 16:9` / `aspect ratio 4:5` / `square 1:1`。

中文短约束（可叠在后面）：

「Gemini 发布会同款；深蓝玻璃；光从左上来；框内留白充足；主标题最大、其余递降；禁止贴边、禁止重叠、禁止密密麻麻小字。」

### 否定提示词（单独贴，别和主提示揉成一锅）

> neon cyberpunk grid, scanlines, glitch, heavy purple fog, rainbow noise, 3D chrome, skeuomorphic metal buttons, thick drop shadows, cluttered dashboard wall, four-column card grid, timetable layout, stock photo people, logos collage, tiny unreadable text, overlapping text, text cut off at edges, watermark, low contrast gray-on-gray, pure black background, white office PowerPoint, Material Design blue bars, isometric city, anime characters stealing focus

---

## 二、程序化渲染色板（SVG / Canvas / Pillow）

| 角色 | 色值 | 什么时候用 |
|---|---|---|
| 底色 | `#071018`（可略到 `#101827` → `#061017`） | 永远是底，不要纯黑 `#000` |
| 主文字 | `#f6f8ff` | 标题、主节点 |
| 次要文字 | `#c8d4e8` @ 0.66–0.78 | 副说明；不要和主文字一样亮 |
| 蓝强调 | `#5b8cff` / 核 `#4d7cff` | 主轴连线、普通步骤描边光 |
| 青绿强调 | `#2ed7bd` / 核 `#19e7d0` | 成功 / 前进方向、高光点缀 |
| 紫强调 | `#a66bff` `#8e63ff` | 轨道环、次要装饰；少用在正文上 |
| 金强调 | `#ffd43b` | 判断节点、关键数字、门槛标、唯一 CTA |
| 橙警告 | `#ff9b52` / `#ffc18a` | 另线出口、风险提示；一图最多一处主橙 |
| 玻璃描边 | `#bad0ff` 或白 @ 0.12–0.22 | 所有玻璃卡外轮廓 |

丝带：`#4285f4` → `#8e63ff` → `#2ed7bd` → `#ffd43b`，只做背景，opacity 约 0.12–0.2。

字体：Noto Sans CJK SC；标题与主节点 Bold。中文不要拉字距（西文 tracking 会把汉字拆散）。行高约 1.35–1.5。

语义配色（显著提升「读得懂」）：

- 普通步骤 = 蓝玻璃
- 判断 = 金框 / 深金底
- 「是 / 前进」箭头偏青，「否 / 另线」偏橙或淡金标注
- 一图里金色判断框不要超过必要数量，金太多就不再显眼

色板与主次示范见 [palette-hierarchy.png](./palette-hierarchy.png)（源文件 [palette-hierarchy.svg](./palette-hierarchy.svg)）。

---

## 三、光与玻璃（成片高级感主要靠这里）

光向统一：主光在左上。所有高光、内描边亮边都假设光从左上来，不要有的卡亮在左、有的亮在右。

背景由下到上：

1. 满铺深空蓝底。
2. 左上大软蓝光（模糊约 30–40），面积大、透明度低。
3. 右上青绿软光，略小于左上。
4. 可选 1–2 圈细轨道环（角落，低透明）。
5. 可选一条淡丝带，只走面板背后，绝不穿过文字。
6. 内容只放在玻璃圆角卡上。

玻璃卡做法（比「一块半透明矩形」高级一个档）：

- 圆角约 24–28（小标签可 16–20）
- 填充：白→淡青很淡的线性渐变，opacity 约 0.04–0.14；太乳浊会吃掉字对比
- 外描边：细、亮、低透明
- 框内约 4px 再描一圈更淡的内高光
- 顶边一条很淡的高光带（左上光的结果）
- 外圈柔和外发光，模糊大、强度低；发光在字后面，绝不盖字
- 判断卡：更深金底 + 金色渐变描边，和步骤卡一眼能分

对比底线：主文字压在玻璃上时，仍然要「远看是白字」，不要灰成一片。若字发灰，先减玻璃不透明度，再加字，不要靠描边硬描一圈黑边（会变土）。

---

## 四、排版与可读性（硬规矩）

1. 字要大。约 1920 宽竖图参考：标题 ~48；主步骤 / 判断 ~36；副说明 ~20。主节点标题尽量不超过两行。
2. 框内内边距：左右 ≥28–36px，上下 ≥18–24px。用真实字体量宽再定框，禁止手估贴边。
3. 整图外边距 ≥60px。
4. 零重叠：节点、标注、行内文字；交付前用笔画级碰撞检测清零。
5. 紧凑公式（解决「太空」和「太挤」来回拧）：节点间距大约是节点高度的 0.35～0.55 倍；有箭头标注的缝再加大一点。空白只出现在连线转弯处，不要大片空底，也不要为填空堆假模块。
6. 同类框同宽；左右成对支路同宽、尽量同高。
7. 连线：圆角拐弯、箭头统一；线上字下面垫深色底。线宽有层次：主轴略粗，支路略细。
8. 视觉层次只有三档：主标题 → 节点主字 → 副说明 / 标注。不要出现第四档差不多大的字在抢戏。
9. 缩略图自检：缩到约 400px 宽，仍能认出标题和主路径；认不出就加大主字或减支路文案，而不是加装饰。
10. 强调色克制：蓝 / 青 / 紫 / 金；橙仅另线或警告。

社交横图：1200×675～1200×900。流程图可略竖，但必须另附宽约 1400 的预览 JPG 方便聊天打开。

导出：优先 SVG 源 + 清晰 PNG + PDF；预览 JPG 用 sRGB，不要过锐化。程序化出图建议 2× 渲染再缩小，边缘更干净。

---

## 五、流程图专规（真流程图，不是卡片墙）

必须：

- 自上而下主轴清楚。
- 步骤 = 大玻璃圆角按钮；判断 = 金色（圆角金框即可，不必硬菱形）。
- 遇判断就分叉；箭头上有短标注；之后再汇合。
- 起点、终点明确；并行可分可合。
- 节点文案短：主行说动作，细节进副行或旁标，不要把话术说明书塞进框里。

禁止：

- 四列 / 多列「卡片墙」「课程表」「仪表盘格子」
- 装饰小三角冒充箭头、看不清因果
- 文生图交付带密密中文的流程图
- 赛博霓虹、故障风、紫雾、厚重拟物、真人照片、白底办公 PPT

---

## 六、最容易让成片「立刻变好看」的五刀（优先改这些）

按收益排序，改图时先动前面的：

1. 层次：只留一个最亮最大的标题区；节点主字统一；副字明显更淡更小。
2. 内边距与量字定框：字一离开边缘，玻璃卡立刻像产品，而不是截出来的 UI 渣图。
3. 光向 + 内高光 + 低强度外发光：成本低，高级感上升最明显。
4. 判断用金色、步骤用蓝玻璃、另线用橙：颜色开始「说话」，不用读完字也能跟路径。
5. 碰撞清零 + 缩略图自检：保证能拿出去给别人看，而不是聊天里放大才发现叠字。

不要优先去堆：更多丝带、更多环、更多渐变杂色。装饰加多了，第一眼反而变杂。

---

## 七、落地检查清单

- [ ] 通道选对了（密中文流程图 = 程序化）
- [ ] 底是深空蓝，不是纯黑或浅灰
- [ ] 蓝 + 青软光晕在；丝带 / 环不穿字
- [ ] 光统一从左上；玻璃有淡顶高光与内描边
- [ ] 主文字对比够，远看仍是亮字
- [ ] 三档字号层次清楚
- [ ] 框内边距、整图外边距达标
- [ ] 零重叠；缩到约 400px 宽仍能认主路径
- [ ] 流程图有分叉汇合，不是卡片墙
- [ ] 交付 PNG（或 SVG）+ PDF + 预览 JPG

---

## 八、给助手的交付说法

跟主人用完整自然中文。直接发预览和 PDF / PNG，一两句说清改了什么（例如内边距、层次、光效），不要堆内部版本号和检测术语。
