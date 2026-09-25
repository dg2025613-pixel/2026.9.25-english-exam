import streamlit as st
from openai import OpenAI

st.title("📚 AI 영어 모의고사 생성기")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

passage = st.text_area(
    "영어 지문을 입력하세요",
    height=300
)

question_type = st.selectbox(
    "문제 유형",
    [
        "빈칸 추론",
        "문장 순서 배열",
        "문장 삽입",
        "주제 찾기",
        "요지 찾기",
        "내용 일치/불일치"
    ]
)

if st.button("🚀 문제 만들기"):

    prompt = f"""
다음 영어 지문을 바탕으로
{question_type} 유형의
고등학교 영어 모의고사 문제를 만들어라.

지문:
{passage}

선택지는 5개를 만들고,
정답과 한국어 해설도 작성하라.
"""

    response = client.chat.completions.create(
        model="사용할 모델",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    st.write(
        response.choices[0].message.content
    )
