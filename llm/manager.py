# lmm_manager.py
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from conf import config
from conf.logger import get_logger
from llm.logging_handler import logging_hanlder

# Initialize logger
logger = get_logger(__name__)

# LLM 생성 함수
def create_llm(llm_type=None):
    """
    llm_type 우선, 없으면 settings.LLM_TYPE, 없으면 "ollama" 기본값
    """
    llm_type = llm_type or config.LLM_TYPE

    if llm_type == "ollama":
        logger.info(f"Connecting to Ollama at {config.OLLAMA_URL} ...")
        llm = ChatOllama(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_URL,
        )
    elif llm_type == "openai":
        logger.info(f"Connecting to OpenAI model: {config.OPENAI_MODEL} ...")
        llm = ChatOpenAI(model_name=config.OPENAI_MODEL,
                         temperature=1)
    else:
        raise ValueError(f"Unsupported LLM type: {llm_type}")

    return llm


# 글로벌 LLM 변수
_callback_llm = None

def get_llm(llm_type=None):
    global _callback_llm
    if _callback_llm is not None:
        return _callback_llm
        
    _callback_llm = create_llm(llm_type)
    _callback_llm.callbacks=[logging_hanlder]

    return _callback_llm
