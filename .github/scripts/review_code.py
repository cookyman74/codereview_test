import openai
import os
import json
from git import Repo
import logging
import sys

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logging.error("OPENAI_API_KEY is not set")
    sys.exit(1)

def review_code(file_path, content):
    """OpenAI API로 개별 파일에 대한 코드 리뷰 요청"""
    try:
        logging.info(f"Reviewing file: {file_path}")
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 코드 리뷰어입니다."},
                {"role": "user", "content": f"다음 파일의 코드를 리뷰해주세요:\n파일: {file_path}\n코드:\n{content}\n..."}
            ],
            timeout=30  # 30초 타임아웃 설정
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error for {file_path}: {str(e)}")
        return f"Error during review of {file_path}: {str(e)}"
    except Exception as e:
        logging.error(f"Unexpected error during review of {file_path}: {str(e)}")
        return f"Unexpected error during review of {file_path}: {str(e)}"

def main():
    try:
        repo = Repo(".")
        changed_files = repo.git.diff("--name-only", "FETCH_HEAD..HEAD").split("\n")

        review_summary = "코드 리뷰가 완료되었습니다. 세부 사항은 아래를 참조하세요."
        review_details = []

        for file in changed_files:
            if file.endswith(('.py', '.js', '.java', '.cpp', '.h')):
                content = get_file_content(file)
                if content is not None:
                    review = review_code(file, content)
                    review_details.append({"file": file, "comment": review})

        output = {
            "summary": review_summary,
            "details": review_details
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))
        logging.info("Review completed successfully")
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
