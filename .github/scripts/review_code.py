import openai
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# git diff 명령어를 통해 변경된 파일 내용 가져오기
def get_code_changes():
    diff_output = os.popen('git diff HEAD~1').read()
    return diff_output

# OpenAI API를 사용해 코드 리뷰 생성
def review_code(diff):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Review the following code changes:\n{diff}",
        max_tokens=500
    )
    return response.choices[0].text

if __name__ == "__main__":
    changes = get_code_changes()
    review = review_code(changes)
    print(f"Code Review:\n{review}")

