"""source-prepped.png -> 행 단위로 타이핑되는 단색 ASCII 초상화 SVG"""
import html
from pathlib import Path

import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # 밝음(성김) -> 어두움(빽빽)
COLS, ROWS = 100, 53
CW, CH = 7.7, 13.0  # 문자 셀 폭/높이
FS = 13
FILL = "#b9bfc7"  # 단색 유지 (무지개색 금지)
CURSOR = "#39d353"
STEP = 0.05  # 행 간 지연
DUR = 0.30  # 행 하나 와이프 시간

src = Path("source-prepped.png")
if not src.exists():
    raise SystemExit("source-prepped.png 없음. prep_photo.py 먼저 실행")

img = Image.open(src).convert("L").resize((COLS, ROWS), Image.LANCZOS)
a = np.array(img)

lines = []
for r in range(ROWS):
    row = "".join(RAMP[min(len(RAMP) - 1, int((255 - v) / 256 * len(RAMP)))] for v in a[r])
    lines.append(row.rstrip())

W, H = int(COLS * CW), int(ROWS * CH)
p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'width="{W}" height="{H}" font-family="SFMono-Regular,Consolas,monospace">'
]

for i, line in enumerate(lines):
    if not line:
        continue
    begin = i * STEP
    y = (i + 1) * CH
    cid = f"clip{i}"
    p.append(
        f'<clipPath id="{cid}"><rect x="0" y="{i * CH:.1f}" height="{CH}" width="0">'
        f'<animate attributeName="width" from="0" to="{W}" begin="{begin:.2f}s" '
        f'dur="{DUR}s" fill="freeze"/></rect></clipPath>'
    )
    p.append(
        f'<text x="0" y="{y:.1f}" font-size="{FS}" fill="{FILL}" xml:space="preserve" '
        f'clip-path="url(#{cid})">{html.escape(line)}</text>'
    )
    # 와이프 경계를 따라가는 커서 블록
    p.append(
        f'<rect y="{i * CH:.1f}" width="{CW:.1f}" height="{CH}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="0" to="{W}" begin="{begin:.2f}s" dur="{DUR}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" '
        f'begin="{begin:.2f}s" dur="{DUR}s" fill="freeze"/></rect>'
    )

p.append("</svg>")
Path("portrait-v2.svg").write_text("\n".join(p), encoding="utf-8")
print(f"wrote portrait-v2.svg  ({W}x{H})")
