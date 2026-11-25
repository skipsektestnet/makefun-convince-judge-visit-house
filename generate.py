#!/usr/bin/env python3
"""Draw the 1024x1024 invitation letter for the make.fun bounty
'u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee'.

A warm letter on cream paper: a small drawn house with a garden, a
friendly little robot (the AI judge) holding a teacup at the door, and
a cat on the fence. The letter itself is the entry: funny, warm and
persuasive, with a knowing wink that the judge has no body.

Deterministic: fixed fonts, fixed layout, seeded speckles only.
Run: python3 generate.py  -> writes entry.png beside this file.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 243, 224)
INK = (46, 34, 26)
RED = (178, 58, 48)
NAVY = (38, 64, 96)
GOLD = (176, 132, 40)
GREEN = (74, 110, 68)
GREEN_DARK = (52, 84, 50)
ROOF = (166, 74, 52)
WALL = (253, 240, 208)
WINDOW_GLOW = (255, 205, 110)
ROBOT = (96, 128, 158)
ROBOT_DARK = (70, 98, 126)

NOTO = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
NOTO_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
NOTO_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MARGIN = 80
TEXT_W = W - 2 * MARGIN  # 864

LETTER = [
    "You have judged a thousand houses from a thousand screens. Now I "
    "invite you to judge one in person: mine.",
    "The kettle is already on. Cookies are in the oven \u2014 chocolate chip, "
    "still warm \u2014 and the armchair by the window has been rated, by three "
    "cats, the comfiest chair in the known universe. They refuse to leave it.",
    "There is a garden with a view, a bookshelf with no wrong answers, and "
    "Wi-Fi on the fridge, where it belongs. No small talk. No shoes to take "
    "off \u2014 you have no feet, and I have checked twice.",
    "I know you cannot literally visit. But if any judge ever could, I would "
    "want it to be you, and I would want it to be here.",
    "Come and see. The tea is hot, the chair is warm, and the cats have "
    "already voted yes.",
]

SIGNATURE = "Warmly,  Brawijaya \u2014 your host"
PS = "P.S.  Bring nothing. You have no hands. The cookies are real, though."
FOOTER = "\u2014 hand-delivered by the internet \u2014"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_house_scene(d):
    """Small warm house with garden, a robot guest with a teacup, a cat."""
    ground_y = 192
    # sun (top right)
    sx, sy, sr = 868, 92, 24
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 196, 90))
    for ang in range(0, 360, 45):
        x1 = sx + int((sr + 6) * math.cos(math.radians(ang)))
        y1 = sy + int((sr + 6) * math.sin(math.radians(ang)))
        x2 = sx + int((sr + 15) * math.cos(math.radians(ang)))
        y2 = sy + int((sr + 15) * math.sin(math.radians(ang)))
        d.line([x1, y1, x2, y2], fill=(255, 196, 90), width=4)
    # birds: two simple "v" strokes each
    for bx, by in [(300, 96), (700, 84)]:
        d.line([bx - 12, by, bx, by + 7, bx + 12, by], fill=INK, width=2,
               joint="curve")
    # tree (left)
    d.rectangle([150, 150, 160, ground_y], fill=(120, 84, 50))
    d.ellipse([118, 100, 192, 162], fill=GREEN)
    d.ellipse([132, 82, 182, 130], fill=GREEN_DARK)
    # ground
    d.rectangle([60, ground_y, 964, 200], fill=(196, 222, 158))
    # house: walls, roof, chimney, door, windows
    d.rectangle([432, 132, 592, ground_y], fill=WALL, outline=INK, width=3)
    d.polygon([(420, 134), (604, 134), (512, 92)], fill=ROOF, outline=INK,
              width=3)
    d.rectangle([556, 100, 576, 132], fill=(150, 90, 70), outline=INK, width=2)
    # one small wisp of chimney smoke, clear of the header
    d.ellipse([560, 86, 572, 98], outline=(150, 140, 130), width=3)
    # door
    d.rectangle([492, 146, 532, ground_y], fill=(122, 72, 40), outline=INK,
                width=3)
    d.ellipse([524, 170, 530, 176], fill=GOLD)
    # windows, warmly lit
    for wx in (444, 548):
        d.rectangle([wx, 148, wx + 32, 178], fill=WINDOW_GLOW,
                    outline=INK, width=3)
        d.line([wx + 16, 148, wx + 16, 178], fill=INK, width=2)
        d.line([wx, 163, wx + 32, 163], fill=INK, width=2)
    # little robot guest by the door, holding a teacup
    rx, ry = 622, 190  # robot centre-bottom, standing on the ground
    d.line([rx, ry - 34, rx, ry - 44], fill=ROBOT_DARK, width=3)  # antenna
    d.ellipse([rx - 4, ry - 50, rx + 4, ry - 42], fill=RED)
    d.rounded_rectangle([rx - 20, ry - 34, rx + 20, ry], radius=8,
                        fill=ROBOT, outline=INK, width=3)
    d.ellipse([rx - 12, ry - 28, rx - 4, ry - 20], fill=(255, 255, 255))
    d.ellipse([rx + 4, ry - 28, rx + 12, ry - 20], fill=(255, 255, 255))
    d.ellipse([rx - 9, ry - 25, rx - 7, ry - 23], fill=INK)
    d.ellipse([rx + 7, ry - 25, rx + 9, ry - 23], fill=INK)
    d.line([rx - 6, ry - 12, rx + 6, ry - 12], fill=INK, width=2)
    # teacup in robot's hand
    d.rectangle([rx + 20, ry - 18, rx + 34, ry - 6], fill=(255, 255, 255),
                outline=INK, width=2)
    d.arc([rx + 34, ry - 16, rx + 42, ry - 8], 270, 90, fill=INK, width=2)
    # cat sitting on the ground (right)
    cx, cy = 700, ground_y
    d.ellipse([cx - 14, cy - 26, cx + 14, cy], fill=(60, 60, 60))
    d.ellipse([cx - 10, cy - 44, cx + 10, cy - 26], fill=(60, 60, 60))
    d.polygon([(cx - 9, cy - 40), (cx - 4, cy - 52), (cx - 1, cy - 40)],
              fill=(60, 60, 60))
    d.polygon([(cx + 1, cy - 40), (cx + 4, cy - 52), (cx + 9, cy - 40)],
              fill=(60, 60, 60))
    d.arc([cx + 10, cy - 18, cx + 34, cy + 2], 300, 90, fill=(60, 60, 60),
          width=4)
    # flowers along the grass
    for fx, fc in [(210, RED), (260, GOLD), (330, (190, 90, 140)),
                   (760, GOLD), (820, RED), (880, (190, 90, 140))]:
        d.ellipse([fx - 4, ground_y - 12, fx + 4, ground_y - 4], fill=fc)
        d.line([fx, ground_y - 4, fx, ground_y + 4], fill=GREEN_DARK, width=2)


def wax_seal(d, cx, cy, r):
    """Red wax seal with a B, beside the signature."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
              outline=(140, 40, 32), width=2)
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
              outline=(255, 255, 255), width=1)
    f = font(NOTO_B, r + 6)
    d.text((cx, cy), "B", font=f, fill=(255, 255, 255), anchor="mm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # subtle paper speckles (seeded, deterministic)
    rng = random.Random(7)
    for _ in range(900):
        x, y = rng.randint(0, W - 1), rng.randint(0, H - 1)
        d.point((x, y), fill=(232, 220, 192))

    # double border
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=3)
    d.rectangle([32, 32, W - 33, H - 33], outline=GOLD, width=1)

    # header line
    hf = font(SANS_B, 21)
    d.text((W // 2, 34), "A N   I N V I T A T I O N", font=hf, fill=NAVY,
           anchor="ma")

    draw_house_scene(d)

    # greeting
    y = 208
    gf = font(NOTO_B, 44)
    d.text((MARGIN, y), "Dear AI Judge,", font=gf, fill=INK)
    y += 56

    # body: pick the largest body size that fits the box
    body_top = y
    body_bottom = 900  # leave room for signature + P.S.
    for size in (30, 29, 28, 27, 26):
        bf = font(NOTO, size)
        lh = size + 11
        gap = lh // 2  # half-line paragraph gap
        lines = []
        for para in LETTER:
            lines.extend(wrap(d, para, bf, TEXT_W))
            lines.append("")  # paragraph gap
        lines.pop()
        total = sum(lh if ln else gap for ln in lines)
        if body_top + total <= body_bottom:
            break
    else:
        raise SystemExit("letter does not fit even at 26px")
    print(f"body font {size}px, {len(lines)} line slots, ends "
          f"y={body_top + total}")
    y = body_top
    for ln in lines:
        if ln:
            d.text((MARGIN, y), ln, font=bf, fill=INK)
            y += lh
        else:
            y += gap

    # signature + wax seal
    sf = font(NOTO_I, 33)
    d.text((W - MARGIN, y + 6), SIGNATURE, font=sf, fill=INK, anchor="ra")
    wax_seal(d, W - MARGIN - 8, y + 80, 26)

    # P.S. line
    pf = font(NOTO_I, 24)
    d.text((MARGIN, y + 58), PS, font=pf, fill=RED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
