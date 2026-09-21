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
# 구역 2. (다음 그래프를 위한 자리)
# ====================================================================
# st.header("구역 2. ...")
# ...그래프 코드...
# st.info("💡 **이 그래프로 알 수 있는 것:** ...")
# st.divider()

# ====================================================================
# 구역 3. (다음 그래프를 위한 자리)
# ====================================================================
# st.header("구역 3. ...")
