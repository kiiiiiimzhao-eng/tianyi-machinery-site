"""
生成首页产品卡片统一缩略图 card.jpg / card.webp

背景：产品原图为 1:1 方图，且内容区被白边"信箱化"（有的只占 47% 高度），
      直接用 object-fit:cover 塞进 4:3 卡片会把设备主体裁掉。
做法：裁掉白边 → 等比缩放 → 居中贴到统一 4:3 白底画布。
      产出图本身就是 4:3，页面里 cover / contain 效果一致，永不裁切。

用法：python tools/make_card_thumbs.py
"""
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_DIR = os.path.join(ROOT, "images", "products")

CANVAS_W, CANVAS_H = 900, 675      # 4:3
INNER_RATIO = 0.92                 # 内容占画布比例，四周留 4% 呼吸空间
WHITE_THRESHOLD = 244              # 判定为"白边"的阈值
BG = (255, 255, 255)

# 每个产品目录使用的源图（按优先级尝试）
SOURCE_CANDIDATES = ["1.jpg", "1.JPG", "main.jpg", "main.JPG", "2.jpg"]


def find_source(product_dir: str):
    for name in SOURCE_CANDIDATES:
        fp = os.path.join(product_dir, name)
        if os.path.exists(fp):
            return fp
    return None


def content_bbox(im: Image.Image):
    """返回非白色内容的包围盒；全白则返回整图。"""
    w, h = im.size
    px = im.load()
    step = max(1, w // 300)
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y]
            if not (r > WHITE_THRESHOLD and g > WHITE_THRESHOLD and b > WHITE_THRESHOLD):
                if x < minx:
                    minx = x
                if x > maxx:
                    maxx = x
                if y < miny:
                    miny = y
                if y > maxy:
                    maxy = y
    if maxx <= minx or maxy <= miny:
        return (0, 0, w, h)
    # 向外扩一点，避免把边缘细节切掉
    pad = max(2, step * 2)
    return (
        max(0, minx - pad),
        max(0, miny - pad),
        min(w, maxx + pad),
        min(h, maxy + pad),
    )


def build_card(src_path: str, out_dir: str):
    im = Image.open(src_path).convert("RGB")
    box = content_bbox(im)
    im = im.crop(box)

    max_w = int(CANVAS_W * INNER_RATIO)
    max_h = int(CANVAS_H * INNER_RATIO)
    scale = min(max_w / im.width, max_h / im.height)
    new_size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    im = im.resize(new_size, Image.LANCZOS)

    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    canvas.paste(im, ((CANVAS_W - im.width) // 2, (CANVAS_H - im.height) // 2))

    jpg = os.path.join(out_dir, "card.jpg")
    webp = os.path.join(out_dir, "card.webp")
    canvas.save(jpg, "JPEG", quality=88, optimize=True, progressive=True)
    canvas.save(webp, "WEBP", quality=85, method=6)
    return jpg, webp, box


def main():
    if not os.path.isdir(PRODUCTS_DIR):
        print("找不到 images/products 目录", file=sys.stderr)
        return 1

    total = 0
    for name in sorted(os.listdir(PRODUCTS_DIR)):
        pdir = os.path.join(PRODUCTS_DIR, name)
        if not os.path.isdir(pdir):
            continue
        src = find_source(pdir)
        if not src:
            print(f"[skip] {name}: 未找到可用源图")
            continue
        jpg, webp, box = build_card(src, pdir)
        sj = os.path.getsize(jpg) / 1024
        sw = os.path.getsize(webp) / 1024
        print(
            f"[ok]   {name:22s} 源={os.path.basename(src):10s} "
            f"裁白边={box}  card.jpg={sj:.0f}KB  card.webp={sw:.0f}KB"
        )
        total += 1

    print(f"\n完成，共生成 {total} 组卡片图（{CANVAS_W}x{CANVAS_H}, 4:3）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
