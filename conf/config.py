"""
config.py
환경 설정 파일: LLM, 서버 URL, 모델 이름 등
"""
import os

LLM_TYPE = os.getenv("LLM_TYPE", "ollama")  # "ollama" 또는 "openai"

# Ollama 설정
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://192.168.0.75:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

# OpenAI 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# MCP 서버 설정
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")

# 로깅 레벨
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")