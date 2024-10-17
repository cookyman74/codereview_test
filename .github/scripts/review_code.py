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
            {"role": "user", "content": f"""
            Review the following code changes:\n{diff}

            Please provide detailed feedback considering the following criteria:

            1. Are there any potential bugs introduced by these changes?
            2. Is there any duplicated code or areas where reusable modules could be implemented?
            3. Does the code follow the existing code conventions? Point out any inconsistencies.
            4. Provide refactoring suggestions to improve the code's quality, readability, and maintainability.
            5. Are there any performance issues that could arise? Suggest any optimizations.
            6. Are there any security vulnerabilities that might be introduced by these changes?
            7. Is there sufficient test coverage for the changes? If not, suggest additional test cases.
            8. Are the comments and documentation adequate? Is there anything unclear or that needs further explanation?

            Please provide your review in Korean.
            """}
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

