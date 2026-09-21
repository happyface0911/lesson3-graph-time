import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 혹시 모를 공백/인코딩 이슈에 대비해 컬럼명 정리
    df.columns = [c.strip() for c in df.columns]
    # 날짜(YYYYMMDD, 하이픈 없는 여덟 자리 숫자) -> datetime
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    return df


df = load_data()

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("일별 박스오피스 데이터를 '시간'이라는 축으로 살펴보는 그래프 모음입니다.")

st.divider()

# ====================================================================
# 구역 1. 영화별 일별 관객수 변화
# ====================================================================
st.header("구역 1. 영화별 일별 관객수 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .loc[:, ["날짜", "일관객"]]
)

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 일별 관객수 추이",
    labels={"날짜": "날짜", "일관객": "일일 관객수"},
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어주세요.)")

st.divider()

# ====================================================================
# 구역 2. 일관객 합계 상위 5편의 날짜별 관객수 비교
# ====================================================================
st.header("구역 2. 일관객 합계 상위 5편의 날짜별 관객수 비교")

top5_movies = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index.tolist()
)

top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values("날짜")
    .loc[:, ["날짜", "영화명", "일관객"]]
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편 - 날짜별 관객수",
    labels={"날짜": "날짜", "일관객": "일일 관객수", "영화명": "영화명"},
)
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(hovermode="x unified", legend_title_text="영화명 (클릭해서 켜고 끄기)")

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어주세요.)")

st.divider()

# ====================================================================
# 구역 3. 날짜별 10위권 일관객 합계 (영역 그래프)
# ====================================================================
st.header("구역 3. 날짜별 10위권 일관객 합계")

daily_total_df = (
    df.groupby("날짜")["일관객"].sum().reset_index().sort_values("날짜")
)
daily_total_df.columns = ["날짜", "합계관객"]

fig3 = px.area(
    daily_total_df,
    x="날짜",
    y="합계관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={"날짜": "날짜", "합계관객": "일일 합계 관객수"},
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra></extra>"
)

# 합계가 가장 컸던 상위 3일 찾기
top3_days = daily_total_df.sort_values("합계관객", ascending=False).head(3)

for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["합계관객"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        yshift=10,
        font=dict(color="crimson", size=12),
        bgcolor="white",
    )
    fig3.add_scatter(
        x=[row["날짜"]],
        y=[row["합계관객"]],
        mode="markers",
        marker=dict(color="crimson", size=10, symbol="star"),
        name="합계 최고 TOP3",
        showlegend=False,
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra>TOP3</extra>",
    )

st.plotly_chart(fig3, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어주세요.)")

st.divider()

# ====================================================================
# 구역 4. 일관객 합계 TOP 10 영화 (가로 막대그래프)
# ====================================================================
st.header("구역 4. 일관객 합계 TOP 10 영화")

top10_summary = (
    df.groupby("영화명")
    .agg(합계관객=("일관객", "sum"), 진입일수=("날짜", "count"))
    .reset_index()
    .sort_values("합계관객", ascending=False)
    .head(10)
    .sort_values("합계관객", ascending=True)  # 가로 막대에서 큰 값이 위로 오도록 오름차순 정렬
)

fig4 = px.bar(
    top10_summary,
    x="합계관객",
    y="영화명",
    orientation="h",
    custom_data=["진입일수"],
    title="일관객 합계 TOP 10 영화",
    labels={"합계관객": "합계 관객수", "영화명": "영화명"},
)
fig4.update_traces(
    hovertemplate="영화명: %{y}<br>합계 관객수: %{x:,}명<br>10위권 진입일수: %{customdata[0]}일<extra></extra>"
)
fig4.update_layout(yaxis_title=None)

st.plotly_chart(fig4, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어주세요.)")

st.divider()

# ====================================================================
# 구역 5. (다음 그래프를 위한 자리)
# ====================================================================
# st.header("구역 5. ...")
