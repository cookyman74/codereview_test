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
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": f"""
                Please review the following file:\n
                File: {file_path}\n
                Code:\n{content}\n
                Provide detailed feedback based on the following criteria:

                1. Are there any potential bugs introduced by these changes?
                2. Are there sections with duplicated code or opportunities for reusable modules?
                3. Does the code follow established coding conventions? Point out any inconsistencies.
                4. Provide refactoring suggestions to improve code quality, readability, and maintainability.
                5. Are there any performance issues? Suggest possible optimizations.
                6. Could any security vulnerabilities be introduced by these changes?
                7. Is the test coverage sufficient for these changes? If not, suggest additional test cases.
                8. Are the comments and documentation adequate? Point out anything unclear or needing further explanation.

                Provide your feedback only on the most relevant points. You may omit unnecessary criteria.

                The response should be in Korean.
                """}
            ]
        )

        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error during review of {file_path}: {str(e)}"

def get_changed_files():
    """원격 저장소와 로컬 저장소의 공통 조상을 기준으로 변경된 파일 목록을 가져오는 함수"""
    try:
        repo = Repo(".")

        # 원격 저장소 정보 갱신
        origin = repo.remotes.origin
        origin.fetch()

        # 현재 브랜치의 마지막 공통 조상(commit merge-base)을 기준으로 diff 수행
        merge_base = repo.git.merge_base('origin/main', 'HEAD')
        diff_index = repo.git.diff(merge_base, 'HEAD', '--name-only')

        # 변경된 파일 목록 출력 및 반환
        if not diff_index:
            print("No changes found between the last common ancestor and the current commit.")
            return []

        # 파일 목록을 줄바꿈 기준으로 분리하고 빈 문자열 제거
        changed_files = diff_index.splitlines()
        return changed_files
    except Exception as e:
        print(f"Error occurred while fetching changed files: {e}")
        return []



def main():
    try:
        changed_files = get_changed_files()

        if not changed_files:
            print("No code changes detected.")
            return

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
