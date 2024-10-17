import openai
import os

# OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_code_changes():
    """changed_files.txt 파일에서 변경된 파일 목록 읽기"""
    try:
        with open("changed_files.txt", "r") as f:
            diff_output = f.read()
        return diff_output
    except Exception as e:
        print(f"Error reading changed files: {e}")
        return ""

def review_code(diff):
    """OpenAI API로 코드 리뷰 요청"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": f"Review the following code changes:\n{diff}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return "Error during review"

if __name__ == "__main__":
    changes = get_code_changes()

    if changes:
        review = review_code(changes)
        print(f"Code Review:\n{review}")
    else:
        print("No code changes detected.")

