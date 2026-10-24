# 出图美术标准提示词（Gemini 深蓝玻璃光效 + 流程图硬规矩）

给 Grok Bot / 画图模型 / 程序化 SVG 出图用。信息图、日报卡、推特复盘、数据海报、流程图默认都按这套，不要另起赛博霓虹或白底办公风。

---

## 一、一句话生成式提示词（文生图 / GenerateImage）

复制整段，末尾再补具体主题：

> Dark cinematic dashboard poster in Google Gemini keynote visual language, deep navy void background #071018, soft radial blue glow top-left and teal cyan glow top-right like orbital nebula, subtle concentric thin rings in the corner (purple and mint strokes, low opacity), blurred rainbow ribbon path (blue → violet → teal → gold) sweeping behind glass panels, frosted glass cards with soft white-to-cyan gradient fill and hairline light border, high-end product keynote aesthetic, clean sans-serif typography, generous inner padding inside every panel so text never hugs edges, large readable Chinese UI text, compact layout with minimal wasted empty space, flat 2D infographic with depth from glow only, no clutter, no 3D chrome, no neon cyberpunk, no purple haze overload, no stock photo people, no overlapping text or boxes

中文可再加一句约束：

「Gemini 发布会同款光效；深蓝玻璃卡片；轨道环或淡丝带；框内文字左右上下都要留足内边距，禁止贴边；字要大、布局要紧凑但不能重叠；禁止赛博霓虹、禁止真人照片、禁止密密麻麻糊成一片的小字。」

---

## 二、程序化渲染色板（SVG / Canvas / Pillow）

| 角色 | 色值 |
|---|---|
| 底色 | `#071018`（可略渐变到 `#101827` → `#061017`） |
| 主文字 | `#f6f8ff` |
| 次要文字 | `#c8d4e8`（透明度约 0.66–0.78） |
| 蓝强调 | `#5b8cff` / 光晕核 `#4d7cff` `#5577ff` |
| 青绿强调 | `#2ed7bd` / 光晕核 `#19e7d0` `#00dbc3` |
| 紫强调 | `#a66bff` `#8e63ff` |
| 金强调（数字 / 判断 / 门槛标） | `#ffd43b` |
| 橙警告 / 另线出口 | `#ff9b52` / `#ffc18a` |
| 玻璃描边 | `#bad0ff` 或白色，opacity ≈ 0.12–0.22 |

丝带渐变：`#4285f4` → `#8e63ff` → `#2ed7bd` → `#ffd43b`。

字体优先 Noto Sans CJK SC（简体），标题与主节点用 Bold。

---

## 三、背景层（由下到上）

1. 满铺深空蓝底，不是纯黑，也不是浅灰。
2. 左上大椭圆 / 径向蓝光（大、软、半透明，模糊约 30–40）。
3. 右上青绿径向光。
4. 可选：右上角 1–2 圈细轨道环（紫 / 青描边，低透明）。
5. 可选：一条很淡的模糊彩虹丝带横穿背景（opacity 约 0.12–0.2），不抢字。
6. 内容全部放在玻璃圆角面板上，不要直接把正文糊在裸底上。

玻璃面板：圆角约 24–28；填充为白 / 淡青线性渐变，opacity 约 0.04–0.14；外圈可柔和外发光；框内约 4px 处可加一圈白色细描边（内高光）；顶部可加一层很淡的渐变高光。

判断节点用更深金底 + 金色渐变描边，和普通步骤框区分开。

---

## 四、排版与可读性（硬规矩）

这些是从实际改图里总结出来的，必须遵守：

1. 字要大，远看也能读。参考量级（约 1920 宽竖图）：标题约 48；主步骤 / 判断约 36；副说明约 20。不要为了「塞满」把字缩到糊。
2. 框内内边距：文字距框左右至少 28–36px，上下至少 18–24px；按真实字体宽度量字再定框宽，禁止手估导致贴边。
3. 整图外边距：任何内容距画布四边至少约 60px。
4. 零重叠：节点不碰节点；标注不压框、不互相压；同一框内行与行不叠。交付前用碰撞检测（文字实际笔画边缘）清零。
5. 紧凑但不空：大片空底不要；为填空而堆假模块也不要。空白只该出现在连线转弯处。宁可图稍长，也不要挤成密麻矩阵或挤到重叠。
6. 同类框统一宽度：主轴步骤一样宽、判断一样宽、左右成对支路一样宽。
7. 连线：圆角拐弯、箭头样式统一；线上标注下面垫深色底，避免和线混在一起。
8. 强调色只用蓝 / 青 / 紫 / 金（另线可用橙），不滥加杂色。

社交横图优先约 1200×675～1200×900。流程图可以略竖、加长，但导出要附一份便于聊天预览的 JPG（宽约 1400）。

---

## 五、流程图专规（真流程图，不是卡片墙）

适用：接待流程、业务路径、分叉汇合说明图。

必须做到：

- 自上而下（或明确主轴方向）。
- 步骤用大玻璃圆角按钮节点；判断用金色（或轻菱形 / 圆角金框），不要做成课程表格子。
- 遇判断就分叉，分支用带文字标注的箭头，之后再汇合到下一节点。
- 起点、终点明确；并行支路可分可合。

明确禁止：

- 四列 / 多列玻璃卡并排的「卡片墙」「课程表」「仪表盘格子」。
- 把箭头做成装饰小三角、逻辑关系看不清。
- 文生图糊字交付（流程图优先程序化 SVG → PNG / PDF）。
- 赛博霓虹网格、扫描线、故障风、过度紫雾、拟物金属厚阴影、真人照片、白底办公 PPT。

---

## 六、落地检查清单

出图后逐项过：

- [ ] 底是深空蓝 `#071018` 一带，不是纯黑或浅灰
- [ ] 至少有蓝 + 青两团软光晕；光晕不抢字
- [ ] 内容在玻璃圆角卡里；有细描边 / 内高光更佳
- [ ] 有轨道环或淡丝带之一（更像 Gemini 发布会）
- [ ] 标题与主字远看清晰；副字也能读
- [ ] 每个框内文字不贴边（左右 ≥28–36px，上下 ≥18–24px）
- [ ] 整图四边外边距 ≥60px
- [ ] 节点 / 标注 / 行内文字零重叠（有自动检测更佳）
- [ ] 若是流程图：有分叉与汇合，不是卡片墙
- [ ] 导出：清晰 PNG（或 SVG）+ PDF + 小预览 JPG；聊天大图加载失败时至少预览能看

---

## 七、给助手的交付说法

跟主人说话用完整自然中文，不要黑话。交付时直接给预览图和 PDF / PNG，用一两句说明改了什么（例如内边距、是否重叠、字号有没有动），不要堆内部版本号和检测术语。
