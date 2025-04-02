import openai
import json
from datetime import datetime

# ✅ GPT API 키 (GitHub Actions에서는 환경변수로 관리할 것)
import os
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 🎤 프롬프트: 시 + 감성 스타일 → JSON
prompt = """
한국어로 감성적인 자유시 한 편을 250~400자 이내로 써줘.
그리고 그 시의 분위기와 정서에 어울리는 배경색(background), 글자색(color), 그리고 Google Fonts에서 사용 가능한 한국어 글꼴(fontFamily)을 추천해서
다음 JSON 구조에 맞게 전체 결과를 완성해줘:

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

# 🔮 GPT 호출
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9,
    max_tokens=700
)

# 🧾 응답 파싱
try:
    result_json = json.loads(response.choices[0].message['content'].strip())
except Exception as e:
    print("❌ JSON 파싱 오류:", e)
    print("GPT 응답:\n", response.choices[0].message['content'])
    exit()

# 📂 기존 시집 불러오기
filename = "reflections.json"
try:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

# ➕ 오늘의 시 추가
data.append(result_json)

# 💾 저장
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 오늘의 시가 추가되었습니다.")
