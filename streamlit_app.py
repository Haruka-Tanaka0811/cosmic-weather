import streamlit as st
import requests

# 宇宙天気API（仮）→ はるかさんのAPI使ってね
API_KEY = "Z4lRtyMc91Hjew51Emf82OPCpNDkpdxJoHpJBLc5"
URL = f"https://api.nasa.gov/DONKI/KP?api_key={API_KEY}"

st.title("宇宙天気ミニダッシュボード")

try:
    response = requests.get(URL)
    data = response.json()

    # 最新のK指数だけ取得（仮に data[0] とする）
    kp_index = float(data[0]["kpIndex"])

    # レベルに応じて色分け
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

except Exception as e:
    st.error("宇宙天気の取得に失敗しました😢")
