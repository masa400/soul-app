import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="魂の設計図", layout="centered")

st.title("🔮 魂の設計図")

name = st.text_input("名前（ニックネーム可）")
birth = st.text_input("生年月日（YYYY/MM/DD）")
time = st.text_input("出生時間（HH:MM）")

lat = st.number_input("緯度", value=35.68)
lon = st.number_input("経度", value=139.76)

if st.button("鑑定を生成"):

    st.subheader("ホロスコープ")

    fig, ax = plt.subplots(figsize=(8,2))
    planets = ["太陽","月","水星","金星","火星"]
    positions = [100, 250, 270, 290, 310]

    for i, p in enumerate(planets):
        ax.scatter(positions[i], 1)
        ax.text(positions[i], 1.05, p, ha='center')

    ax.set_xlim(0,360)
    ax.set_yticks([])
    ax.set_title("簡易ホロスコープ")

    st.pyplot(fig)

    st.subheader("リーディング")

    st.write(f"{name}さんは、")
    st.write("本質を見抜く力とバランス感覚を持っています。")

    st.markdown("### 【強み】")
    st.write("・本質理解・調整力・共感力")

    st.markdown("### 【課題】")
    st.write("・考えすぎ・行動の遅れ")
