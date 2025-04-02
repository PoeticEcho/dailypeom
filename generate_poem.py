import openai
import json
import os

# 🔐 키 불러오기
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 🎯 프롬프트
prompt = """
한국어로 감성적인 자유시 한 편을 250~400자 이내로 써줘.
그리고 그 시의 분위기와 정서에 어울리는 배경색(background), 글자색(color), 그리고 Google Fonts에서 사용 가능한 한국어 글꼴(fontFamily)을 추천해서
다음 JSON 구조로 전체 결과를 완성해줘:

{
  "text": "시 본문",
  "style": {
    "background": "#HEX",
    "color": "#HEX",
    "fontFamily": "Google Fonts 한국어 글꼴"
  }
}

반드시 위 JSON 형식만 반환해줘.
"""

# ✅ 최신 방식으로 GPT 호출 (openai>=1.0.0)
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9,
    max_tokens=700
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
