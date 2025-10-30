# MCP 기반 LangChain 에이전트 데모

이 리포지토리는 MCP 아키텍처 기반 도구(Tool)를 정의하고, 이를 활용해 LangChain ReAct 에이전트를 구성하는 방법을 소개합니다

- 3개의 도구를 가진 MCP 서버(`mcp_server.py`)
- 도구 호출 테스트 클라이언트(`fastmcp_client.py`)
- LangChain ReAct 에이전트(`langchain_client.py`)


## 1. 가상환경 구성 및 패키지 설치

- Python 3.13 이상
- pip
- 가상환경 사용 권장


```bash
# 가상환경 생성
python3 -m venv .venv

# 가상환경 활성화
source .venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```


## 2. 모델 설정

### Ollama 사용 시

```bash
# Ollama 서버 실행
ollama run

# 모델 다운로드 (예: qwen3:8b)
ollama pull qwen3:8b

# 모델 설정
export OLLAMA_MODEL="qwen3:8b"
```

※ Ollama 사용할 때는 해당 모델이 "tool calling"(또는 "function calling") 기능을 지원해야 합니다. 

### OpenAI 사용 시

```bash
# 환경 변수 설정
export LLM_TYPE="openai"
export OPENAI_API_KEY="YOUR_API_KEY"
```


## 3. MCP 서버 실행

```bash
python3 mcp_server.py
```

서버가 실행되면 클라이언트에서 도구 목록 조회 및 호출이 가능합니다.


## 4. 클라이언트 실행

### 도구 호출 테스트

```bash
python3 fastmcp_client.py
```

### LangChain ReAct 에이전트 실행

```bash
python3 langchain_client.py
```

- 프롬프트를 구성하고 LLM을 통해 도구 호출 결정
- LLM은 LLM_TYPE에 따라 Ollama 또는 OpenAI를 사용
- ReAct 에이전트는 질문에 따라 적절한 도구를 동적으로 선택하고 실행

## 라이선스

MIT License

