import openai
import os
import json
from git import Repo

# OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_file_content(file_path):
    """파일의 내용을 읽어오는 함수"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def review_code(file_path, content):
    """OpenAI API로 개별 파일에 대한 코드 리뷰 요청"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "당신은 코드 리뷰어입니다."},
                {"role": "user", "content": f"""
                다음 파일의 코드를 리뷰해주세요:\n
                파일: {file_path}\n
                코드:\n{content}\n
                다음 기준을 고려하여 상세한 피드백을 제공해주세요:

                1. 이 변경으로 인해 발생할 수 있는 잠재적인 버그가 있나요?
                2. 중복된 코드나 재사용 가능한 모듈로 구현할 수 있는 영역이 있나요?
                3. 코드가 기존의 코드 규칙을 따르고 있나요? 일관성이 없는 부분을 지적해주세요.
                4. 코드의 품질, 가독성, 유지보수성을 향상시키기 위한 리팩토링 제안을 해주세요.
                5. 발생할 수 있는 성능 문제가 있나요? 최적화 방안을 제안해주세요.
                6. 이 변경으로 인해 도입될 수 있는 보안 취약점이 있나요?
                7. 변경 사항에 대한 테스트 커버리지가 충분한가요? 부족하다면 추가적인 테스트 케이스를 제안해주세요.
                8. 주석과 문서화가 적절한가요? 불명확하거나 추가 설명이 필요한 부분이 있나요?

                리뷰를 다음 형식으로 제공해주세요:
                - 한 문장으로 된 주요 개선사항 또는 문제점 요약
                - 최대 3개의 구체적인 제안 사항 (있는 경우)

                응답은 한국어로 해주세요.
                """}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error during OpenAI API call for {file_path}: {e}")
        return f"Error during review of {file_path}"

def main():
    try:
        repo = Repo(".")
        changed_files = repo.git.diff("--name-only", "FETCH_HEAD..HEAD").split("\n")

        review_summary = "코드 리뷰가 완료되었습니다. 세부 사항은 아래를 참조하세요."
        review_details = []

        for file in changed_files:
            if file.endswith(('.py', '.js', '.java', '.cpp', '.h')):  # 필요한 파일 확장자 추가
                content = get_file_content(file)
                if content is not None:
                    review = review_code(file, content)
                    review_details.append({"file": file, "comment": review})

        output = {
            "summary": review_summary,
            "details": review_details
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
