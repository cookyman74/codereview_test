name: AI Code Review

on:
  push:
    branches-ignore:
      - main

jobs:
  code_review:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3  # v2에서 v3로 업데이트

    - name: Install Python
      uses: actions/setup-python@v3  # v2에서 v3로 업데이트
      with:
        python-version: '3.x'

    - name: Run AI Code Review
      run: python .github/scripts/review_code.py

