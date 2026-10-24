#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""常用配色与主次参考图 · Gemini 深蓝玻璃风"""
from pathlib import Path
import html, subprocess
from PIL import Image, ImageFont

OUT = Path("/workspace/qa/art-standards")
W, H = 1520, 1180
CX = W // 2
MARGIN = 56
FONT_FILE = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_IDX = 2
FONT = "Noto Sans CJK SC, Noto Sans CJK, 'Source Han Sans SC', sans-serif"

BG = "#071018"
TXT = "#f6f8ff"
MUTED = "#c8d4e8"
BLUE = "#5b8cff"
TEAL = "#2ed7bd"
PURPLE = "#a66bff"
GOLD = "#ffd43b"
ORANGE = "#ff9b52"
BORDER = "#bad0ff"
CORE_BLUE = "#4d7cff"

_fc = {}
def font(sz):
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT_FILE, sz, index=FONT_IDX)
    return _fc[sz]
def ink(s, sz):
    return font(sz).getbbox(s, anchor="ls")
def tw(s, sz):
    l,t,r,b = ink(s, sz); return r-l
def esc(s): return html.escape(s, quote=True)
def text(x,y,s,sz,fill=TXT,wt=700,anchor="middle",op=1.0):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{sz}" font-weight="{wt}" fill="{fill}" fill-opacity="{op}">{esc(s)}</text>')

def glass_card(x,y,w,h,stroke, rx=24, fill_tint=None, tint_op=0.22):
    p = []
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{stroke}" '
             f'stroke-width="20" stroke-opacity="0.20" filter="url(#softGlow)"/>')
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{stroke}" '
             f'stroke-width="7" stroke-opacity="0.28" filter="url(#tightGlow)"/>')
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#050b14" fill-opacity="0.90"/>')
    if fill_tint:
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill_tint}" fill-opacity="{tint_op}" '
                 f'stroke="{stroke}" stroke-opacity="0.95" stroke-width="2.4"/>')
    else:
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" '
                 f'stroke="{stroke}" stroke-opacity="0.9" stroke-width="2.4"/>')
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#frost)"/>')
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#glassHi)"/>')
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{max(h*0.4, 24):.1f}" rx="{rx}" fill="url(#glassTopBand)"/>')
    p.append(f'<rect x="{x+3.5}" y="{y+3.5}" width="{w-7}" height="{h-7}" rx="{max(rx-3.5,4)}" fill="none" '
             f'stroke="#ffffff" stroke-opacity="0.22" stroke-width="1.4"/>')
    return "\n".join(p)

parts = []

# palette chips
swatches = [
    ("底色", BG, "永远是底，不要纯黑"),
    ("主文字", TXT, "标题、主节点"),
    ("次文字", MUTED, "副说明 · 更淡"),
    ("蓝强调", BLUE, "步骤 / 主轴"),
    ("青绿", TEAL, "前进 / 成功"),
    ("紫强调", PURPLE, "支路 / 装饰"),
    ("金强调", GOLD, "判断 / 门槛"),
    ("橙警告", ORANGE, "另线 / 风险"),
    ("玻璃描边", BORDER, "玻璃卡外轮廓"),
]

# layout: title + subtitle + divider + swatch row + hierarchy demo + footer tip
y = MARGIN + 40
parts.append(text(CX, y, "常用配色与主次", 44, TXT, 800))
y += 38
parts.append(text(CX, y, "Gemini 深蓝玻璃 · 一眼分清谁主谁次", 20, MUTED, 500, op=0.72))
y += 22
parts.append(f'<rect x="{CX-380}" y="{y}" width="760" height="2" rx="1" fill="url(#divider)"/>')

# section label
y += 42
parts.append(text(MARGIN + 8, y, "色板", 18, MUTED, 700, anchor="start", op=0.78))
y += 18

chip_w, chip_h = 132, 118
gap_x = 18
total_w = 9 * chip_w + 8 * gap_x
sx0 = (W - total_w) / 2
for i, (name, hexv, when) in enumerate(swatches):
    x = sx0 + i * (chip_w + gap_x)
    # chip card
    parts.append(glass_card(x, y, chip_w, chip_h, BORDER if hexv not in (GOLD, ORANGE, TEAL, BLUE, PURPLE) else hexv,
                            rx=18, fill_tint=hexv if hexv != BG else None,
                            tint_op=0.55 if hexv != BG else 0))
    # color block inside
    bx, by, bw, bh = x + 14, y + 14, chip_w - 28, 36
    if hexv == BG:
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{hexv}" '
                     f'stroke="{BORDER}" stroke-opacity="0.35" stroke-width="1"/>')
    elif hexv == TXT:
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{hexv}"/>')
    else:
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{hexv}" fill-opacity="0.95"/>')
    parts.append(text(x + chip_w/2, by + bh + 22, name, 15, TXT, 700))
    parts.append(text(x + chip_w/2, by + bh + 40, hexv.upper(), 12, MUTED, 600, op=0.7))
    # when — wrap if needed, keep short
    parts.append(text(x + chip_w/2, by + bh + 58, when, 11, MUTED, 500, op=0.55))

y_demo = y + chip_h + 48
parts.append(text(MARGIN + 8, y_demo, "主次示范 · 同款玻璃卡一眼看出层次", 18, MUTED, 700, anchor="start", op=0.78))
y_demo += 22

# three demo cards in a row + orange exit small
demo_h = 168
# left: title sample (wide)
dw1 = 420
# mid: blue step
dw2 = 360
# right: gold decision
dw3 = 320
# far right: orange pill exit
dw4 = 260
gapd = 24
row_w = dw1 + dw2 + dw3 + dw4 + 3 * gapd
rx0 = (W - row_w) / 2

# Title sample card
x = rx0
parts.append(glass_card(x, y_demo, dw1, demo_h, BLUE, rx=24, fill_tint=BLUE, tint_op=0.14))
parts.append(text(x + dw1/2, y_demo + 58, "大标题 · 最亮最大", 36, TXT, 800))
parts.append(text(x + dw1/2, y_demo + 96, "整图只有这一档最抢眼", 18, MUTED, 500, op=0.72))
parts.append(text(x + dw1/2, y_demo + 128, "什么时候用：封面 / 流程总标题", 14, MUTED, 500, op=0.55))

# Blue step
x = rx0 + dw1 + gapd
parts.append(glass_card(x, y_demo, dw2, demo_h, BLUE, rx=24, fill_tint=BLUE, tint_op=0.22))
parts.append(text(x + dw2/2, y_demo + 58, "步骤 · 蓝玻璃", 28, TXT, 800))
parts.append(text(x + dw2/2, y_demo + 96, "主动作写在这里", 18, MUTED, 500, op=0.72))
parts.append(text(x + dw2/2, y_demo + 128, "什么时候用：普通流程节点", 14, MUTED, 500, op=0.55))

# Gold decision
x = rx0 + dw1 + gapd + dw2 + gapd
parts.append(glass_card(x, y_demo, dw3, demo_h, GOLD, rx=24, fill_tint=GOLD, tint_op=0.26))
# override with gold stroke gradient look
parts.append(f'<rect x="{x}" y="{y_demo}" width="{dw3}" height="{demo_h}" rx="24" fill="none" stroke="{GOLD}" '
             f'stroke-width="18" stroke-opacity="0.22" filter="url(#softGlow)"/>')
parts.append(f'<rect x="{x}" y="{y_demo}" width="{dw3}" height="{demo_h}" rx="24" fill="url(#goldFill)" '
             f'stroke="url(#goldStroke)" stroke-width="2.6"/>')
parts.append(f'<rect x="{x}" y="{y_demo}" width="{dw3}" height="{demo_h}" rx="24" fill="url(#frost)"/>')
parts.append(f'<rect x="{x}" y="{y_demo}" width="{dw3}" height="{demo_h}" rx="24" fill="url(#glassHi)"/>')
parts.append(f'<rect x="{x}" y="{y_demo}" width="{dw3}" height="{demo_h*0.4:.1f}" rx="24" fill="url(#glassTopBand)"/>')
parts.append(text(x + dw3/2, y_demo + 58, "判断 · 金框", 28, GOLD, 800))
parts.append(text(x + dw3/2, y_demo + 96, "分叉问一句", 18, MUTED, 500, op=0.72))
parts.append(text(x + dw3/2, y_demo + 128, "什么时候用：要不要分叉", 14, MUTED, 500, op=0.55))

# Orange exit
x = rx0 + dw1 + gapd + dw2 + gapd + dw3 + gapd
pill_h = 72
py = y_demo + (demo_h - pill_h) / 2 - 12
parts.append(glass_card(x, py, dw4, pill_h, ORANGE, rx=pill_h/2, fill_tint=ORANGE, tint_op=0.26))
parts.append(text(x + dw4/2, py + pill_h/2 + 8, "另线 · 橙出口", 22, ORANGE, 800))
parts.append(text(x + dw4/2, py + pill_h + 28, "一图最多一处主橙", 14, MUTED, 500, op=0.55))
parts.append(text(x + dw4/2, py + pill_h + 48, "什么时候用：其他业务 / 风险", 13, MUTED, 500, op=0.5))

# hierarchy callout strip
y_strip = y_demo + demo_h + 36
sw = W - 2 * MARGIN
parts.append(f'<rect x="{MARGIN}" y="{y_strip}" width="{sw}" height="96" rx="20" fill="#060c15" fill-opacity="0.82" '
             f'stroke="{BORDER}" stroke-opacity="0.28" stroke-width="1.4"/>')
parts.append(f'<rect x="{MARGIN}" y="{y_strip}" width="{sw}" height="96" rx="20" fill="url(#glassHi)"/>')
parts.append(text(MARGIN + 36, y_strip + 40, "三档层次", 20, TXT, 800, anchor="start"))
parts.append(text(MARGIN + 36, y_strip + 68,
                  "主标题（最亮最大）  →  节点主字（统一白字）  →  副说明 / 标注（#c8d4e8 · 约 0.72 透明）",
                  16, MUTED, 500, anchor="start", op=0.72))
parts.append(text(MARGIN + sw - 36, y_strip + 54,
                  "光统一从左上 · 玻璃有顶高光与内描边",
                  14, TEAL, 600, anchor="end", op=0.85))

# tip row
y_tip = y_strip + 96 + 28
parts.append(text(CX, y_tip,
                  "强调色克制：蓝 / 青 / 紫 / 金；橙仅另线或警告。装饰加多了，第一眼反而变杂。",
                  15, MUTED, 500, op=0.55))
y_tip2 = y_tip + 28
parts.append(text(CX, y_tip2,
                  "详见 PROMPT.md 第二节色板 · 第四节排版 · 第六节五刀",
                  13, MUTED, 500, op=0.42))

H = int(y_tip2 + ink("x", 13)[3] + MARGIN)

defs = f'''
<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#0b1422"/><stop offset="70%" stop-color="{BG}"/>
  <stop offset="100%" stop-color="#060e16"/>
</linearGradient>
<radialGradient id="glowBlue" cx="8%" cy="0%" r="50%">
  <stop offset="0%" stop-color="{CORE_BLUE}" stop-opacity="0.40"/><stop offset="55%" stop-color="{CORE_BLUE}" stop-opacity="0.12"/>
  <stop offset="100%" stop-color="{CORE_BLUE}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowTeal" cx="94%" cy="2%" r="36%">
  <stop offset="0%" stop-color="#19e7d0" stop-opacity="0.30"/><stop offset="60%" stop-color="#19e7d0" stop-opacity="0.09"/>
  <stop offset="100%" stop-color="#19e7d0" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowBot" cx="50%" cy="100%" r="32%">
  <stop offset="0%" stop-color="#8e63ff" stop-opacity="0.20"/><stop offset="100%" stop-color="#8e63ff" stop-opacity="0"/>
</radialGradient>
<linearGradient id="divider" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{BORDER}" stop-opacity="0"/><stop offset="50%" stop-color="{BORDER}" stop-opacity="0.55"/>
  <stop offset="100%" stop-color="{BORDER}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="glassHi" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0%" stop-color="#ffffff" stop-opacity="0.20"/><stop offset="28%" stop-color="#ffffff" stop-opacity="0.07"/>
  <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="glassTopBand" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#ffffff" stop-opacity="0.18"/><stop offset="55%" stop-color="#b8d4ff" stop-opacity="0.06"/>
  <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="frost" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#dce8ff" stop-opacity="0.10"/><stop offset="40%" stop-color="#a8c4ff" stop-opacity="0.045"/>
  <stop offset="100%" stop-color="#071018" stop-opacity="0.02"/>
</linearGradient>
<linearGradient id="goldFill" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="{GOLD}" stop-opacity="0.34"/><stop offset="100%" stop-color="#b8860b" stop-opacity="0.18"/>
</linearGradient>
<linearGradient id="goldStroke" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="#fff3b0"/><stop offset="45%" stop-color="{GOLD}"/><stop offset="100%" stop-color="#c99214"/>
</linearGradient>
<linearGradient id="ribbon" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#4285f4" stop-opacity="0.32"/><stop offset="40%" stop-color="#8e63ff" stop-opacity="0.24"/>
  <stop offset="75%" stop-color="#2ed7bd" stop-opacity="0.18"/><stop offset="100%" stop-color="#ffd43b" stop-opacity="0.12"/>
</linearGradient>
<filter id="softGlow" x="-40%" y="-60%" width="180%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="tightGlow" x="-20%" y="-35%" width="140%" height="170%"><feGaussianBlur stdDeviation="5"/></filter>
'''

bg = (f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>'
      f'<rect width="{W}" height="{H}" fill="url(#glowBlue)"/>'
      f'<rect width="{W}" height="{H}" fill="url(#glowTeal)"/>'
      f'<rect width="{W}" height="{H}" fill="url(#glowBot)"/>'
      f'<ellipse cx="1390" cy="120" rx="190" ry="120" fill="none" stroke="{PURPLE}" stroke-opacity="0.22" stroke-width="1.6"/>'
      f'<ellipse cx="1390" cy="120" rx="140" ry="88" fill="none" stroke="{TEAL}" stroke-opacity="0.18" stroke-width="1.3"/>'
      f'<ellipse cx="1390" cy="120" rx="92" ry="56" fill="none" stroke="{BLUE}" stroke-opacity="0.14" stroke-width="1.1"/>'
      f'<ellipse cx="140" cy="680" rx="130" ry="90" fill="none" stroke="{PURPLE}" stroke-opacity="0.12" stroke-width="1.2"/>'
      f'<path d="M -20 420 C 280 360, 560 500, 900 440 S 1300 360, 1560 470" fill="none" stroke="url(#ribbon)" '
      f'stroke-width="20" stroke-opacity="0.16" stroke-linecap="round"/>'
      f'<path d="M -30 620 C 350 560, 700 700, 1050 620 S 1400 580, 1580 650" fill="none" stroke="url(#ribbon)" '
      f'stroke-width="12" stroke-opacity="0.10" stroke-linecap="round"/>')

svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
       f'<defs>{defs}</defs>\n{bg}\n' + "\n".join(parts) + "\n</svg>\n")

sp = OUT / "palette-hierarchy.svg"
pp = OUT / "palette-hierarchy.png"
jp = OUT / "palette-hierarchy-preview.jpg"
sp.write_text(svg, encoding="utf-8")
subprocess.check_call(["rsvg-convert", "-w", str(W), "-f", "png", "-o", str(pp), str(sp)])
im = Image.open(pp).convert("RGB")
pw = 1400
im.resize((pw, int(im.height * pw / im.width)), Image.Resampling.LANCZOS).save(jp, "JPEG", quality=90, optimize=True)
print(f"PALETTE {W}x{H} preview {pw}x{int(H*pw/W)}")
print("wrote", sp.name, pp.name, jp.name)
