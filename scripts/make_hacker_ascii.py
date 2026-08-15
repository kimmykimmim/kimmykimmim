"""사진 없이 해킹 테마 ASCII 아트(후드 실루엣) -> ascii-portrait.svg
prep_photo.py / make_ascii_svg.py 대신 이거 하나만 실행하면 됨."""
import html
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---- 도형 그리기 -------------------------------------------------------
W, H = 620, 700
img = Image.new("L", (W, H), 255)
d = ImageDraw.Draw(img)
cx = W // 2
random.seed(7)

# 배경 코드 레인 (아주 옅게)
try:
    f = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
except Exception:
    f = ImageFont.load_default()
for x in range(10, W, 26):
    y = random.randint(-200, 200)
    while y < H:
        d.text((x, y), random.choice("01"), fill=random.randint(198, 226), font=f)
        y += 22

# 어깨 / 몸통
d.polygon([(cx - 250, H), (cx - 200, 585), (cx - 120, 545),
           (cx + 120, 545), (cx + 200, 585), (cx + 250, H)], fill=72)

# 후드 바깥
d.ellipse([cx - 170, 120, cx + 170, 520], fill=48)
d.polygon([(cx - 170, 320), (cx - 196, 575), (cx + 196, 575), (cx + 170, 320)], fill=48)
d.polygon([(cx - 196, 545), (cx - 130, 528), (cx - 146, 600)], fill=40)
d.polygon([(cx + 196, 545), (cx + 130, 528), (cx + 146, 600)], fill=40)

# 후드 안쪽 어둠 (얼굴 없음)
d.ellipse([cx - 108, 182, cx + 108, 462], fill=12)

# 눈
d.ellipse([cx - 66, 292, cx - 20, 324], fill=250)
d.ellipse([cx + 20, 292, cx + 66, 324], fill=250)

# 후드 테두리 하이라이트
d.arc([cx - 170, 120, cx + 170, 520], start=192, end=348, fill=118, width=13)

img = img.filter(ImageFilter.GaussianBlur(1.1))

# ---- ASCII 변환 --------------------------------------------------------
RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 92, 46
CW, CH = 7.7, 13.0
FS = 13
FILL = "#b9bfc7"
EYE = "#39d353"
CURSOR = "#39d353"
STEP, DUR = 0.05, 0.30

a = np.array(img.resize((COLS, ROWS), Image.LANCZOS))
lines = [
    "".join(RAMP[min(len(RAMP) - 1, int((255 - v) / 256 * len(RAMP)))] for v in a[r]).rstrip()
    for r in range(ROWS)
]

SW, SH = int(COLS * CW), int(ROWS * CH)
p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SW} {SH}" '
    f'width="{SW}" height="{SH}" font-family="SFMono-Regular,Consolas,monospace">'
]

# 눈 위치(행 범위)에만 초록 강조
eye_rows = {r for r in range(ROWS) if 0.41 <= r / ROWS <= 0.47}

for i, line in enumerate(lines):
    if not line:
        continue
    begin = i * STEP
    y = (i + 1) * CH
    cid = f"clip{i}"
    color = EYE if i in eye_rows else FILL
    p.append(
        f'<clipPath id="{cid}"><rect x="0" y="{i * CH:.1f}" height="{CH}" width="0">'
        f'<animate attributeName="width" from="0" to="{SW}" begin="{begin:.2f}s" '
        f'dur="{DUR}s" fill="freeze"/></rect></clipPath>'
    )
    p.append(
        f'<text x="0" y="{y:.1f}" font-size="{FS}" fill="{color}" xml:space="preserve" '
        f'clip-path="url(#{cid})">{html.escape(line)}</text>'
    )
    p.append(
        f'<rect y="{i * CH:.1f}" width="{CW:.1f}" height="{CH}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="0" to="{SW}" begin="{begin:.2f}s" dur="{DUR}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" '
        f'begin="{begin:.2f}s" dur="{DUR}s" fill="freeze"/></rect>'
    )

p.append("</svg>")
Path("ascii-portrait.svg").write_text("\n".join(p), encoding="utf-8")
print(f"wrote ascii-portrait.svg  ({SW}x{SH})")
