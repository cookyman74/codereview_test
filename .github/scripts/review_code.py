import openai
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 변경된 파일을 읽고 분석하는 함수
def get_code_changes():
    diff_output = os.popen('git diff --name-only FETCH_HEAD').read()
    return diff_output

# OpenAI API를 통해 코드 리뷰 생성
def review_code(diff):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": f"Review the following code changes:\n{diff}"}
        ]
    )
    return response.choices[0].message['content']

# 변경된 코드 읽기
changes = get_code_changes()

# 코드 리뷰 생성
if changes:
    review = review_code(changes)
    print(f"Code Review:\n{review}")
else:
    print("No code changes detected.")

