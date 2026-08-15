"""공개 HTML 엔드포인트에서 잔디 데이터 스크랩 -> data/contributions.json (토큰 불필요)"""
import json
import re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "kimmykimmim"
URL = f"https://github.com/users/{USER}/contributions"

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}, timeout=30)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

# 툴팁에서 날짜별 기여 수 추출 (예: "3 contributions on ...")
counts = {}
for tip in soup.find_all("tool-tip"):
    target = tip.get("for")
    m = re.match(r"\s*(No|\d+)\s+contribution", tip.get_text(strip=True))
    if target and m:
        counts[target] = 0 if m.group(1) == "No" else int(m.group(1))

days = []
for td in soup.select("td.ContributionCalendar-day"):
    d = td.get("data-date")
    if not d:
        continue
    days.append(
        {
            "date": d,
            "level": int(td.get("data-level") or 0),
            "count": counts.get(td.get("id"), 0),
        }
    )

days.sort(key=lambda x: x["date"])
if not days:
    raise SystemExit("파싱 실패: GitHub HTML 구조가 바뀌었을 수 있음")

total = sum(d["count"] for d in days)

# 연속 기록
longest = cur = 0
for d in days:
    cur = cur + 1 if d["count"] > 0 else 0
    longest = max(longest, cur)

# 현재 연속 (오늘이 0이면 어제부터 셈)
current = 0
for d in reversed(days):
    if d["count"] > 0:
        current += 1
    elif d["date"] != date.today().isoformat():
        break

best = max(days, key=lambda x: x["count"])

monthly = defaultdict(int)
for d in days:
    monthly[d["date"][:7]] += d["count"]

out = {
    "user": USER,
    "generated": date.today().isoformat(),
    "total": total,
    "current_streak": current,
    "longest_streak": longest,
    "best_day": best,
    "monthly": dict(sorted(monthly.items())),
    "days": days,
}

Path("data").mkdir(exist_ok=True)
Path("data/contributions.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"wrote data/contributions.json  days={len(days)} total={total}")
