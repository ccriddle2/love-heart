#!/usr/bin/env python3
# love_windows.py - "I love you" heart animation (Windows)
# Needs Python from python.org (tkinter comes with it - keep "tcl/tk" checked in the installer)
# Run:  py love_windows.py   (or double-click the file)

import math
import random as r
import turtle
import tkinter.font as tkf

BG = "black"
FONT = "Segoe UI"   # Windows falls back to its built-in Asian/Hindi/Thai fonts automatically
COLORS = ["#ff1744", "#ff2d55", "#e0103a", "#ff4d6d", "#c9002b"]

s = turtle.Screen()
s.setup(800, 800)
s.bgcolor(BG)
s.title("Love Heart")
s.tracer(0)

cv = s.getcanvas()
rng = r.Random(11)

PHRASES = [
    "I love you", "Seni seviyorum", "Te amo", "Je t'aime",
    "Ich liebe dich", "Ti amo", "Eu te amo", "Я тебя люблю",
    "사랑해", "愛してる", "我爱你", "मैं तुमसे प्यार करता हूँ",
    "Σ' αγαπώ", "Ik hou van jou", "Jag älskar dig", "Kocham cię",
    "ฉันรักเธอ", "Anh yêu em", "Aku cinta kamu", "Я тебе кохаю",
]

_fonts = {}

def font_for(size):
    if size not in _fonts:
        _fonts[size] = tkf.Font(root=cv, family=FONT, size=size, weight="bold")
    return _fonts[size]

def heart(t, scale=17):
    # classic parametric heart; canvas y grows downward so flip it
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x * scale, -y * scale - 20

OUTLINE = [heart(i / 200 * 2 * math.pi, 15.5) for i in range(200)]  # slightly smaller than the traced edge

def inside(px, py):
    # ray-casting point-in-polygon test against the heart outline
    hit = False
    j = len(OUTLINE) - 1
    for i, (xi, yi) in enumerate(OUTLINE):
        xj, yj = OUTLINE[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit

items = []

def place(x, y, size, delay):
    def draw():
        txt = rng.choice(PHRASES)
        items.append(cv.create_text(x, y, text=txt, fill=rng.choice(COLORS),
                                    font=font_for(size)))
        s.update()
    s.ontimer(draw, delay)

# 1) trace the outline
N = 70
delay = 0
for i in range(N):
    t = i / N * 2 * math.pi
    x, y = heart(t)
    place(x, y, rng.choice([9, 10, 11]), delay)
    delay += 45

# 2) fill the inside with random phrases
filled = 0
while filled < 170:
    x, y = rng.uniform(-260, 260), rng.uniform(-300, 250)
    if inside(x, y) and not (abs(x) < 120 and abs(y + 60) < 45):  # keep center clear for her name
        place(x, y, rng.choice([7, 8, 9, 10, 12]), delay)
        delay += 20
        filled += 1

# 3) gentle heartbeat glow once it's drawn
def beat(k=0):
    c = COLORS[k % len(COLORS)]
    for it in items[k % 7::7]:
        cv.itemconfig(it, fill=c)
    s.update()
    s.ontimer(lambda: beat(k + 1), 120)

# 3) her name, big in the middle
def show_name():
    cv.create_text(0, -60, text="Sarah", fill="#b84dff",
                   font=(FONT, 54, "bold"))
    s.update()

s.ontimer(show_name, delay + 300)
s.ontimer(beat, delay + 500)
s.update()
turtle.done()
