import streamlit as st
import requests

st.title("宇宙天気ミニダッシュボード")
st.write("NASAのAPIから、リアルタイムで宇宙天気情報を取得しています✨")

API_KEY = st.secrets["api"]["key"]
URL = f"https://api.nasa.gov/DONKI/FLR?startDate=2024-06-01&api_key={API_KEY}"

response = requests.get(URL)
if response.status_code == 200:
    data = response.json()
    if data:
        st.subheader("最新の太陽フレア情報")
        for flare in data[:3]:  # 最新3件だけ表示
            st.markdown(f"- **開始時刻**: {flare['beginTime']}")
            st.markdown(f"  - クラス: {flare.get('classType', '不明')}")
            st.markdown(f"  - 発生場所: {flare.get('sourceLocation', '不明')}")
            st.markdown("---")
    else:
        st.write("現在、太陽フレアの報告はありません。")
else:
    st.error("宇宙天気のデータ取得に失敗しました。")
