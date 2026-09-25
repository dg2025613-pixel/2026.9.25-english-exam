import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI 영어 모의고사 생성기",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI 영어 모의고사 생성기")
st.write("영어 지문을 입력하면 모의고사형 문제로 자동 변형해 줍니다.")

# API KEY
api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="OpenAI API Key를 입력하세요."
)

# 지문 입력
passage = st.text_area(
    "📖 영어 지문을 입력하세요",
    height=300,
    placeholder="영어 지문을 여기에 붙여넣으세요."
)

# 문제 유형
question_type = st.selectbox(
    "📝 문제 유형",
    [
        "빈칸 추론",
        "문장 순서 배열",
        "문장 삽입",
        "주제 찾기",
        "요지 찾기",
        "내용 일치/불일치"
    ]
)

# 난이도
difficulty = st.selectbox(
    "🎯 난이도",
    [
        "기본",
        "모의고사 수준",
        "어려움"
    ]
)

# 문제 생성
if st.button("🚀 문제 만들기", use_container_width=True):

    if not api_key:
        st.error("OpenAI API Key를 입력해주세요.")

    elif not passage.strip():
        st.warning("영어 지문을 입력해주세요.")

    else:

        client = OpenAI(api_key=api_key)

        prompt = f"""
너는 대한민국 고등학교 영어 모의고사 출제 전문가이다.

다음 영어 지문을 바탕으로 새로운 영어 모의고사 문제를 만들어라.

[원문]
{passage}

[문제 유형]
{question_type}

[난이도]
{difficulty}

다음 조건을 반드시 지켜라.

1. 원문의 핵심 내용과 논리적 흐름을 유지한다.
2. 원문에 없는 새로운 사실을 만들어내지 않는다.
3. 고등학교 영어 모의고사에서 볼 수 있는 자연스러운 문제 형식으로 만든다.
4. 선택지는 5개를 만든다.
5. 정답은 반드시 1개만 존재하도록 한다.
6. 정답이 너무 쉽게 드러나는 선택지를 만들지 않는다.
7. 문제와 선택지는 영어로 작성한다.
8. 해설은 한국어로 작성한다.
9. 정답의 근거가 되는 부분을 지문에서 확인할 수 있도록 한다.

문제 유형별 조건:

[빈칸 추론]
- 지문의 핵심 내용을 나타내는 문장 또는 구절을 빈칸으로 만든다.
- 빈칸에 들어갈 가장 적절한 표현을 고르게 한다.

[문장 순서 배열]
- 지문을 자연스럽게 3개의 부분으로 나눈다.
- 주어진 문장 이후에 이어질 순서를 묻는다.
- A, B, C 형식으로 제시한다.

[문장 삽입]
- 지문의 논리적 흐름에 맞는 문장을 하나 선정한다.
- 삽입할 위치를 묻는다.

[주제 찾기]
- 지문의 전체적인 주제를 묻는다.

[요지 찾기]
- 지문의 핵심 주장을 가장 잘 나타내는 선택지를 묻는다.

[내용 일치/불일치]
- 지문의 내용을 바탕으로 5개의 선택지를 만든다.
- 하나만 지문과 일치하지 않도록 한다.

다음 형식으로 출력한다.

### 문제
문제 내용

### 선택지
① ...
② ...
③ ...
④ ...
⑤ ...

### 정답
정답 번호

### 해설
왜 정답인지 한국어로 설명

### 핵심 포인트
이 문제에서 중요한 영어 표현이나 논리적 흐름을 간단하게 설명
"""

        try:
            with st.spinner("AI가 모의고사 문제를 만들고 있습니다..."):

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "너는 대한민국 고등학교 영어 모의고사 출제 전문가이다."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7
                )

            result = response.choices[0].message.content

            st.success("문제가 생성되었습니다!")

            st.markdown("---")
            st.markdown(result)

        except Exception as e:
            st.error("문제 생성 중 오류가 발생했습니다.")
            st.code(str(e))
