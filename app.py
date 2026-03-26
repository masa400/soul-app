import math
import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager

# Windowsの日本語フォントを直接指定
font_path = r"C:\Windows\Fonts\msgothic.ttc"
if os.path.exists(font_path):
    font_prop = font_manager.FontProperties(fname=font_path)
else:
    font_path = r"C:\Windows\Fonts\meiryo.ttc"
    if os.path.exists(font_path):
        font_prop = font_manager.FontProperties(fname=font_path)
    else:
        font_prop = None

if font_prop is not None:
    mpl.rcParams["font.family"] = font_prop.get_name()
else:
    mpl.rcParams["font.family"] = "sans-serif"

mpl.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="魂の設計図", layout="centered")

SIGNS = ["牡羊", "牡牛", "双子", "蟹", "獅子", "乙女", "天秤", "蠍", "射手", "山羊", "水瓶", "魚"]

PLANET_COLORS = {
    "太陽": "#e74c3c",
    "月": "#3498db",
    "水星": "#2ecc71",
    "金星": "#9b59b6",
    "火星": "#e67e22",
}

DEMO_POSITIONS = {
    "太陽": 278,
    "月": 96,
    "水星": 286,
    "金星": 314,
    "火星": 251,
}

def pol(lon, r):
    a = math.radians(90 - lon)
    return math.cos(a) * r, math.sin(a) * r

def draw_circle_chart(positions):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)

    # 外円・内円
    for r, lw in [(1.0, 1.8), (0.78, 1.2), (0.52, 1.0)]:
        ax.add_patch(plt.Circle((0, 0), r, fill=False, linewidth=lw, color="black"))

    # サイン区切り線
    for i in range(12):
        lon = i * 30
        x1, y1 = pol(lon, 0.52)
        x2, y2 = pol(lon, 1.0)
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=1)

    # サイン名
    for i, sign in enumerate(SIGNS):
        lon = i * 30 + 15
        x, y = pol(lon, 0.88)
        ax.text(
            x, y, sign,
            ha="center", va="center",
            fontsize=11, fontweight="bold",
            fontproperties=font_prop
        )

    # ハウス番号
    for i in range(12):
        lon = i * 30 + 15
        x, y = pol(lon, 0.33)
        ax.text(
            x, y, f"{i+1}",
            ha="center", va="center",
            fontsize=9, color="gray",
            fontproperties=font_prop
        )

    # 惑星配置
    used = []
    for name, lon in positions.items():
        r = 0.64

        for prev_lon, prev_r in used:
            if abs(((lon - prev_lon + 180) % 360) - 180) < 8:
                r = prev_r - 0.06

        used.append((lon, r))

        x, y = pol(lon, r)
        ax.plot(x, y, "o", markersize=8, color=PLANET_COLORS.get(name, "black"))
        tx, ty = pol(lon, r + 0.08)
        ax.text(
            tx, ty, name,
            ha="center", va="center",
            fontsize=10,
            fontproperties=font_prop
        )

    plt.tight_layout()
    return fig

def build_reading(name):
    display_name = name if name.strip() else "あなた"

    return f"""
### リーディング

{display_name}さんは、

本質を見抜く力とバランス感覚を持っています。

### 【強み】
・本質理解  
・調整力  
・共感力  

### 【課題】
・考えすぎ  
・行動の遅れ  

### 【今のテーマ】
今は「整えてから動く」よりも、  
**動きながら整える**ことが流れを変える鍵になりやすい時期です。

### 【一言メッセージ】
完璧になってから始めるのではなく、  
小さく動くことで、あなた本来の流れが戻ってきます。
""".strip()

st.title("🔮 魂の設計図")

name = st.text_input("名前（ニックネーム可）")
birth = st.text_input("生年月日（YYYY/MM/DD）")
time = st.text_input("出生時間（HH:MM）")

lat = st.number_input("緯度", value=35.68)
lon = st.number_input("経度", value=139.76)

if st.button("鑑定を生成"):
    st.write("ここは出る？")
    st.subheader("ホロスコープ（円形表示版）")
    st.caption("※ 現在は見た目調整版のため、天体位置は仮表示です")

    fig = draw_circle_chart(DEMO_POSITIONS)
    st.pyplot(fig)

    st.markdown(build_reading(name))
