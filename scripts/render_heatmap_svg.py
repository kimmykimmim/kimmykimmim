"""data/contributions.json -> 대각선으로 등장하는 잔디 히트맵 SVG"""
import json
from datetime import date
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP, R = 13, 3, 3
W = 860
LEFT, TOP = 34, 30

data = json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
days = data["days"]

# 열(주) 인덱스 계산: 첫 칸의 요일 기준
first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7  # 일요일=0
cells = []
for i, d in enumerate(days):
    idx = i + offset
    cells.append((idx // 7, idx % 7, d))

weeks = max(c[0] for c in cells) + 1
H = TOP + 7 * (CELL + GAP) + 46

p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="SFMono-Regular,Consolas,monospace">',
    "<style>"
    ".c{opacity:0;animation:pop .4s ease-out forwards}"
    "@keyframes pop{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}"
    "</style>",
]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
seen = set()
for col, row, d in cells:
    dt = date.fromisoformat(d["date"])
    if dt.day <= 7 and dt.month not in seen:
        seen.add(dt.month)
        x = LEFT + col * (CELL + GAP)
        p.append(f'<text x="{x}" y="{TOP - 8}" font-size="10" fill="#8b949e">{MONTHS[dt.month - 1]}</text>')

for i, lbl in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
    p.append(
        f'<text x="0" y="{TOP + i * (CELL + GAP) + 10}" font-size="10" fill="#8b949e">{lbl}</text>'
    )

for col, row, d in cells:
    x = LEFT + col * (CELL + GAP)
    y = TOP + row * (CELL + GAP)
    delay = (col + row) * 0.012  # 대각선 순서
    fill = PALETTE[min(d["level"], len(PALETTE) - 1)]
    p.append(
        f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{R}" fill="{fill}" '
        f'style="animation-delay:{delay:.2f}s"><title>{d["date"]}: {d["count"]}</title></rect>'
    )

# 푸터
fy = TOP + 7 * (CELL + GAP) + 24
p.append(
    f'<text x="{LEFT}" y="{fy}" font-size="12" fill="#8b949e">'
    f'{data["total"]:,} contributions in the last year &#183; '
    f'current streak {data["current_streak"]} &#183; longest {data["longest_streak"]}</text>'
)

# 범례
lx = W - 190
p.append(f'<text x="{lx}" y="{fy}" font-size="11" fill="#8b949e">Less</text>')
for i, c in enumerate(PALETTE):
    p.append(
        f'<rect x="{lx + 34 + i * (CELL + GAP)}" y="{fy - 11}" width="{CELL}" height="{CELL}" '
        f'rx="{R}" fill="{c}"/>'
    )
p.append(f'<text x="{lx + 34 + len(PALETTE) * (CELL + GAP) + 6}" y="{fy}" font-size="11" fill="#8b949e">More</text>')

p.append("</svg>")
Path("contrib-heatmap.svg").write_text("\n".join(p), encoding="utf-8")
print(f"wrote contrib-heatmap.svg  weeks={weeks}")
