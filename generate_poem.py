import openai
import json
import os

# 🔐 키 불러오기
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 🎯 프롬프트(4버전용)
#prompt = """
#한국어로 감성적인 자유시 한 편을 250~400자 이내로 써줘.
#그리고 그 시의 분위기와 정서에 어울리는 배경색(background), 글자색(color), 그리고 Google Fonts에서 사용 가능한 한국어 글꼴(fontFamily)을 추천해서
#다음 JSON 구조로 전체 결과를 완성해줘:
#
#{
#  "text": "시 본문",
#  "style": {
#    "background": "#HEX",
#    "color": "#HEX",
#    "fontFamily": "Google Fonts 한국어 글꼴"
#  }
#}
#
#반드시 위 JSON 형식만 반환해줘.
#"""
# 🎯 프롬프트(3-5터보용 버전용)
prompt = """
당신은 감성적인 시를 쓰는 한국의 시인입니다.
당신은 계절, 시간, 감정, 풍경, 기억 등을 시적으로 표현하는 데 능숙합니다.

다음 조건에 맞는 한국어 자유시를 한 편 써주세요:

- 250자에서 400자 사이
- 너무 직설적이거나 설명적이지 말고, 여운이 남게
- 짧은 행, 긴 행, 리듬이 섞인 자유로운 형식
- 문학적인 표현, 반복, 은유, 생략을 적절히 사용
- 사람의 일상과 감정, 고요한 순간을 포착하는 느낌

그리고 시의 분위기(정서)에 어울리는 다음 스타일 정보를 포함해서
전체를 아래 JSON 형식으로 완성해 주세요:

{
  "text": "여기에 시 본문",
  "style": {
    "background": "#HEX",
    "color": "#HEX",
    "fontFamily": "Google Fonts 한국어 글꼴"
  }
}

스타일은 시의 정서에 따라 직관적으로 골라주세요.
배경색과 글자색은 가독성과 분위기를 고려하고,
글꼴은 시적인 분위기와 잘 어울리는 한글 웹폰트를 선택해주세요.

JSON 외에는 아무것도 출력하지 마세요.
"""


# ✅ 최신 방식으로 GPT 호출 (openai>=1.0.0)
#response = openai.chat.completions.create(
#    model="gpt-4",
#    messages=[{"role": "user", "content": prompt}],
#    temperature=0.9,
#    max_tokens=700
#)
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.95,
    max_tokens=800
)

# ✂️ 응답 파싱
poem_content = response.choices[0].message.content.strip()

try:
    result_json = json.loads(poem_content)
except Exception as e:
    print("❌ JSON 파싱 오류:", e)
    print("GPT 응답:\n", poem_content)
    exit(1)

# 📚 JSON 파일 처리
filename = "reflections.json"
try:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

data.append(result_json)

# 🎯 최대 365개 유지
if len(data) > 365:
    data = data[-365:]

with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 오늘의 시가 성공적으로 추가되었습니다.")
