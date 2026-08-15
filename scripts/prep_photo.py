"""사진 전처리: 배경 제거 -> CLAHE 대비 향상 -> 흰 배경 합성 -> source-prepped.png"""
import io
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

src = Path(sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg")
out = Path("source-prepped.png")

if not src.exists():
    sys.exit(f"파일 없음: {src}")

# 1. 배경 제거 (RGBA)
cut = remove(src.read_bytes())
img = Image.open(io.BytesIO(cut)).convert("RGBA")

# 2. 흰 배경 합성 후 그레이스케일
bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
bg.alpha_composite(img)
gray = np.array(bg.convert("L"))

# 3. CLAHE: 피사체 영역만 국소 대비 향상
alpha = np.array(img.split()[-1])
mask = alpha > 10
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
enhanced = clahe.apply(gray)
result = np.where(mask, enhanced, 255).astype(np.uint8)

Image.fromarray(result).save(out)
print(f"wrote {out}  ({result.shape[1]}x{result.shape[0]})")
