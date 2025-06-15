import streamlit as st
import requests

st.title("宇宙天気ミニダッシュボード")

URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

try:
    response = requests.get(URL)
    data = response.json()

    # 最新のデータ（最後の要素）を取得
    latest = data[-1]
    kp_index = float(latest["k_index"])
    time = latest["time_tag"]

    # 色分けロジック
    if kp_index < 4:
        color = "🟢"
        status = "安定"
    elif kp_index < 6:
        color = "🟡"
        status = "やや不安定"
    else:
        color = "🔴"
        status = "嵐レベル"

    st.subheader(f"{color} 現在のK指数： {kp_index}")
    st.write(f"宇宙天気状況： **{status}**")
    st.caption(f"最終更新時刻：{time}")

except Exception as e:
    st.error("宇宙天気の取得に失敗しました😢")
