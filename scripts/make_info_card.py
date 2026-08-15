"""neofetch 스타일 정보 카드 SVG. 행 단위 페이드+슬라이드인.
STATIC=1 로 실행하면 애니메이션 없는 정지 프레임 (미리보기용)."""
import html
import os
from pathlib import Path

USER = "kimmykimmim"
HOST = "github"

# ---- 여기만 고치면 됨 -------------------------------------------------
ROWS = [
    ("Now", "성균관대 소프트웨어학과 재학"),
    ("Focus", "Cybersecurity / Systems"),
    ("Stack", "C, Python, Linux, Networking"),
    ("Learning", "CompTIA Network+, Linux Master"),
    ("Next", "대학원 진학 준비"),
]
# ----------------------------------------------------------------------

W, H = 490, 300
PAD = 22
LH = 30  # 행 높이
KEY = "#39d353"
VAL = "#c9d1d9"
DIM = "#6e7681"
BORDER = "#30363d"
STATIC = os.environ.get("STATIC") == "1"

p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="SFMono-Regular,Consolas,monospace">'
]

if not STATIC:
    p.append(
        "<style>"
        ".row{opacity:0;animation:in .45s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-10px)}"
        "to{opacity:1;transform:translateX(0)}}"
        "</style>"
    )

p.append(
    f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="#0d1117" '
    f'stroke="{BORDER}" stroke-width="1"/>'
)

# 타이틀 바
p.append(f'<circle cx="{PAD}" cy="24" r="5" fill="#ff5f56"/>')
p.append(f'<circle cx="{PAD + 18}" cy="24" r="5" fill="#ffbd2e"/>')
p.append(f'<circle cx="{PAD + 36}" cy="24" r="5" fill="#27c93f"/>')
p.append(f'<line x1="0" y1="46" x2="{W}" y2="46" stroke="{BORDER}"/>')

y = 76
cls = "" if STATIC else ' class="row"'


def anim(i):
    return "" if STATIC else f' style="animation-delay:{0.15 + i * 0.12:.2f}s"'


p.append(
    f'<text x="{PAD}" y="{y}" font-size="14" fill="{KEY}"{cls}{anim(0)}>'
    f'{USER}<tspan fill="{DIM}">@</tspan>{HOST}</text>'
)
y += 20
p.append(
    f'<text x="{PAD}" y="{y}" font-size="12" fill="{DIM}"{cls}{anim(1)}>'
    f'{"-" * 34}</text>'
)
y += 26

for i, (k, v) in enumerate(ROWS):
    d = anim(i + 2)
    p.append(f'<text x="{PAD}" y="{y}" font-size="13" fill="{KEY}"{cls}{d}>{html.escape(k)}</text>')
    p.append(
        f'<text x="{PAD + 100}" y="{y}" font-size="13" fill="{VAL}"{cls}{d}>{html.escape(v)}</text>'
    )
    y += LH

Path("info-card.svg").write_text("\n".join(p) + "\n</svg>", encoding="utf-8")
print("wrote info-card.svg" + (" (static)" if STATIC else ""))
