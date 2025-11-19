import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly import colors

# ---------- 데이터 로드 ----------
@st.cache_data
def load_data():
    # 같은 폴더에 있는 CSV 파일이라고 가정
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

MBTI_TYPES = list(df.columns[1:])  # Country 제외 나머지 16개 타입

# ---------- 앱 기본 설정 ----------
st.set_page_config(
    page_title="세계 MBTI 분포 대시보드",
    layout="wide"
)

st.title("🌍 국가별 MBTI 분포 대시보드")
st.markdown("선택한 **국가의 MBTI 비율**을 인터랙티브한 Plotly 막대그래프로 보여줄게요!")

# ---------- 사이드바에서 국가 선택 ----------
country_list = df["Country"].sort_values().tolist()
selected_country = st.sidebar.selectbox("국가를 선택하세요", country_list)

# 선택한 국가 데이터 가져오기
row = df[df["Country"] == selected_country].iloc[0]
data = pd.DataFrame({
    "Type": MBTI_TYPES,
    "Value": [row[t] for t in MBTI_TYPES]
})

# 값 기준 내림차순 정렬 (1등이 왼쪽에 오도록)
data = data.sort_values(by="Value", ascending=False).reset_index(drop=True)

# ---------- 색상 설정 (1등: 빨간색, 나머지: 그라데이션) ----------
values = data["Value"].tolist()
max_val = max(values)
max_idx = values.index(max_val)

n = len(values)

# Plotly 색상 팔레트 사용 (예: Blues)
# top 1은 'red', 나머지는 Blues 그라데이션
non_top_indices = [i for i in range(n) if i != max_idx]
n_non_top = len(non_top_indices)

if n_non_top > 1:
    # 0~1 사이 값으로 샘플링해서 그라데이션 느낌
    positions = [i / (n_non_top - 1) for i in range(n_non_top)]
    grad_colors = colors.sample_colorscale("Blues", positions)
else:
    # 비정상 케이스 방지용
    grad_colors = ["#1f77b4"] * n_non_top

bar_colors = [None] * n
for idx in range(n):
    if idx == max_idx:
        bar_colors[idx] = "red"  # 1등은 빨강
    else:
        # non_top_indices 순서대로 그라데이션 색 부여
        grad_idx = non_top_indices.index(idx)
        bar_colors[idx] = grad_colors[grad_idx]

# ---------- Plotly 그래프 생성 ----------
fig = go.Figure(
    data=[
        go.Bar(
            x=data["Type"],
            y=data["Value"],
            marker=dict(color=bar_colors),
            hovertemplate="MBTI: %{x}<br>비율: %{y:.3f}<extra></extra>"
        )
    ]
)

fig.update_layout(
    title=f"📊 {selected_country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (0~1 사이)",
    yaxis=dict(tickformat=".2f"),
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

# ---------- 하단에 간단한 요약 ----------
top_type = data.iloc[0]["Type"]
top_value = data.iloc[0]["Value"]

st.markdown(
    f"""
### 🔎 요약
- 선택한 국가: **{selected_country}**
- 가장 비율이 높은 MBTI 유형: **{top_type}** (약 {top_value:.3f})
- 그래프에서 **빨간 막대**가 1등 MBTI, 나머지 막대는 **그라데이션 색상**으로 표시되어 있어요.
"""
)
