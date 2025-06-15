import streamlit as st
import requests

st.set_page_config(page_title="宇宙天気ミニダッシュボード", page_icon="☀️")

st.title("☀️ 宇宙天気ミニダッシュボード")
st.caption("NASAのAPIから、リアルタイムで宇宙天気情報を取得しています✨")

API_KEY = st.secrets["api"]["key"]
URL = f"https://api.nasa.gov/DONKI/FLR?startDate=2024-06-01&api_key={API_KEY}"

response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    if data:
        st.subheader("🛰️ 最新の太陽フレア情報（上位3件）")

        for i, flare in enumerate(data[:3], 1):
            with st.container():
                st.markdown(f"### 🌟 太陽フレア {i}")
                st.write(f"**開始時刻**: `{flare['beginTime']}`")
                st.write(f"**クラス**: `{flare.get('classType', '不明')}`")
                st.write(f"**発生場所**: `{flare.get('sourceLocation', '不明')}`")
                st.markdown("---")
    else:
        st.success("🎉 現在、太陽フレアの報告はありません。宇宙は穏やかです。")
else:
    st.error("⚠️ 宇宙天気のデータ取得に失敗しました。もう一度お試しください。")
