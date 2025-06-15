import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="宇宙天気ミニダッシュボード", page_icon="☀️")

st.title("☀️ 宇宙天気ミニダッシュボード")
st.caption("NASAのAPIから、リアルタイムで宇宙天気情報を取得しています✨")

API_KEY = st.secrets["api"]["key"]
URL = f"https://api.nasa.gov/DONKI/FLR?startDate=2024-06-01&api_key={API_KEY}"

# クラスに応じた色を返す関数
def get_class_color(class_type):
    if not class_type:
        return "gray"
    if class_type.startswith("X"):
        return "red"
    elif class_type.startswith("M"):
        return "orange"
    elif class_type.startswith("C"):
        return "gold"
    elif class_type.startswith("B"):
        return "green"
    else:
        return "gray"

# 🌈 凡例を表示
st.markdown("### 🌈 フレアクラスの色分け（強さの目安）")
st.markdown("""
- <span style='color:red'>🔴 **Xクラス**</span>：非常に強い  
- <span style='color:orange'>🟠 **Mクラス**</span>：中程度  
- <span style='color:gold'>🟡 **Cクラス**</span>：弱め  
- <span style='color:green'>🟢 **Bクラス以下**</span>：微弱または通常レベル
""", unsafe_allow_html=True)

# データ取得と表示
response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    if data:
        st.subheader("🛰️ 最新の太陽フレア情報（上位3件）")

        flare_records = []  # グラフ用リスト

        for i, flare in enumerate(data[:3], 1):
            class_type = flare.get("classType", "不明")
            color = get_class_color(class_type)

            # グラフ用にクラスの頭文字を保存（例: "X1.2" → "X"）
            if class_type not in ["不明", None]:
                flare_records.append(class_type[0])

            with st.container():
                st.markdown(f"### 🌟 太陽フレア {i}")
                st.write(f"**開始時刻**: `{flare['beginTime']}`")
                st.markdown(f"**クラス**: <span style='color:{color}'><strong>{class_type}</strong></span>", unsafe_allow_html=True)
                st.write(f"**発生場所**: `{flare.get('sourceLocation', '不明')}`")
                st.markdown("---")

        # クラス別件数を棒グラフで可視化
        if flare_records:
            st.subheader("📈 太陽フレア クラス別発生数（過去分含む）")
            df = pd.DataFrame(flare_records, columns=["class"])
            class_counts = df["class"].value_counts().reindex(["X", "M", "C", "B"], fill_value=0)

            class_colors = {
                "X": "red",
                "M": "orange",
                "C": "gold",
                "B": "green"
            }

            fig, ax = plt.subplots()
            class_counts.plot(kind="bar", color=[class_colors[c] for c in class_counts.index], ax=ax)
            ax.set_xlabel("フレアクラス")
            ax.set_ylabel("件数")
            ax.set_title("フレアクラス別発生件数")
            st.pyplot(fig)
    else:
        st.success("🎉 現在、太陽フレアの報告はありません。宇宙は穏やかです。")
else:
    st.error("⚠️ 宇宙天気のデータ取得に失敗しました。もう一度お試しください。")
