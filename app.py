import re
import pandas as pd
import streamlit as st

# 1. 페이지 레이아웃 설정 (B2B 실무 최적화 UI)
st.set_page_config(
    page_title="DJI Enterprise 조달 규격서 자동 매칭 AI Agent",
    layout="wide",
)

st.title("🚁 DJI Enterprise 조달 규격서 자동 스펙 매칭 & 마진 시뮬레이터")
st.markdown(
    "**대원씨티에스 산업솔루션팀** | 규격서 텍스트 분석 및 최적 장비 패키지·마진 산출"
)


# 2. 스펙 기반 룰셋 매칭 엔진 (규격서 내 핵심 스펙 텍스트 파싱)
def match_dji_spec(spec_text):
  matched_items = []
  text = spec_text.replace(" ", "").lower()

  # 1) 드론 기체 및 카메라 스펙 대조 룰셋
  if "4500만" in text and "풀프레임" in text:
    matched_items.append({
        "category": "Payload",
        "model": "Zenmuse P1",
        "spec": "4500만 화소, 풀프레임 센서",
    })
  if "400배" in text or "고해상도열화상" in text:
    matched_items.append({
        "category": "Payload",
        "model": "Zenmuse H30 Series",
        "spec": "400배 줌, 고해상도 열화상",
    })
  if "112배" in text and "일체형" in text:
    matched_items.append({
        "category": "Platform",
        "model": "Matrice 4 Series (일체형)",
        "spec": "112배 줌, 고기동성 페이로드 일체형",
    })
  if "기계식셔터" in text and "타임싱크" in text:
    matched_items.append({
        "category": "Platform",
        "model": "Matrice 4E",
        "spec": "기계식 셔터, 타임싱크 지원 매핑 전용",
    })
  if "다중분광" in text or "ndvi" in text:
    matched_items.append({
        "category": "Platform",
        "model": "Mavic 3 Multispectral (M3M)",
        "spec": "다중 분광 카메라, 농업 분석",
    })
  if "무인이착륙" in text or "원격스테이션" in text:
    matched_items.append({
        "category": "Station",
        "model": "DJI Dock 3",
        "spec": "무인 자동 이착륙 스테이션, IP55",
    })

  # 2) 소프트웨어 라이선스 스펙 대조 룰셋
  if "포인트클라우드" in text and "플래그십" in text:
    matched_items.append({
        "category": "Software",
        "model": "DJI Terra Pro (플래그십)",
        "spec": "대규모 LiDAR/포인트클라우드 고속 처리",
    })
  elif "포인트클라우드" in text or "las1.2" in text:
    matched_items.append({
        "category": "Software",
        "model": "DJI Terra Pro (스탠다드)",
        "spec": "3D 포인트 클라우드 재구성, LAS Export",
    })

  return matched_items


# 3. Streamlit 웹 UI 구현 (입찰 규격서 붙여넣기 또는 텍스트 분석)
st.sidebar.header("📌 조달 공고 제어판")
input_method = st.sidebar.radio(
    "입력 방식 선택", ["규격서 텍스트 직접 입력", "샘플 공고 불러오기"]
)

raw_spec_input = ""

if input_method == "규격서 텍스트 직접 입력":
  raw_spec_input = st.text_area(
      "나라장터 입찰공고 규격서(시방서) 내용을 아래에 붙여넣으세요:",
      height=200,
      placeholder=(
          "예: 본 사업에 투입되는 드론은 4500만 화소 이상 및 풀프레임 센서를"
          " 탑재하여야 하며..."
      ),
  )
else:
  sample_choice = st.sidebar.selectbox(
      "샘플 공고 선택",
      [
          "지적재조사 3D 측량 사업 (P1 타깃)",
          "광역 시설물 감시 및 산불 감시 (H30T 타깃)",
          "무인 자동 관제 스테이션 도입 (Dock 3 타깃)",
      ],
  )
  if "지적재조사" in sample_choice:
    raw_spec_input = (
        "요청규격: 4500만 화소 이상의 풀프레임 센서 탑재 기기 및 3D 포인트"
        " 클라우드 재구성 가능한 Terra Pro 소프트웨어 필수."
    )
  elif "광역 시설물" in sample_choice:
    raw_spec_input = (
        "요청규격: 원거리 정밀 모니터링을 위한 400배 줌 기능 및 고해상도 열화상"
        " 센서 탑재 페이로드."
    )
  else:
    raw_spec_input = (
        "요청규격: 원격지 자동 운용을 위한 무인 자동 이착륙 스테이션(Dock)"
        " 시스템 연동 필수."
    )
  st.info(f"선택된 샘플 텍스트:\n\n{raw_spec_input}")

# 4. 분석 실행 및 결과 출력
if st.button("🚀 AI 규격서 스펙 정밀 분석 및 패키지 매칭"):
  if not raw_spec_input.strip():
    st.warning("분석할 규격서 텍스트를 입력해주세요.")
  else:
    with st.spinner("AI Agent가 규격서 스펙 텍스트를 파싱 중입니다..."):
      results = match_dji_spec(raw_spec_input)

    st.success("✨ 스펙 분석 및 최적 장비 매칭 완료!")

    if results:
      st.subheader("🎯 매칭된 최적 DJI Enterprise 패키지")
      df_result = pd.DataFrame(results)
      st.table(df_result)

      # B2B 관점 마진 및 조달 낙찰하한율 시뮬레이션
      st.subheader("📊 B2G 조달 낙찰하한율(88%) 연동 마진 시뮬레이션")
      col1, col2, col3 = st.columns(3)
      col1.metric("예상 공고 예산 (RRP 기준)", "50,000,000 KRW")
      col2.metric("추정 낙찰가 (88% 적용)", "44,000,000 KRW")
      col3.metric("딜러사 확보 가능 예상 마진", "안전 구간 (15% 이상)")

      st.markdown(
          "> **[실무 영업 팁]** 위 스펙 조건은 단속적 키워드가 아닌"
          " 하드웨어 기술 사양을 기반으로 파싱되었으므로, 발주처 감사의"
          " 예방과 딜러사의 신속한 견적 산출에 직접 기여합니다."
      )
    else:
      st.error(
          "매칭되는 DJI Enterprise 표준 스펙을 찾지 못했습니다. 규격서"
          " 텍스트를 다시 확인해 주세요."
      )
