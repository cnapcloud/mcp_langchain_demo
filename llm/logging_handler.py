import logging
from conf.logger import get_logger

# Initialize logger
logger = get_logger(__name__)
logger.setLevel(logging.INFO)  

from langchain_core.callbacks.base import BaseCallbackHandler

class LoggingHandler(BaseCallbackHandler):
    """
    LLM 호출 전/후에 프롬프트와 응답을 로깅하는 핸들러
    """
    def __init__(self, logger):
        self.logger = logger

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.logger.debug(f"[LLM Start] prompts={prompts}")

    def on_llm_end(self, response, **kwargs):
        self.logger.debug(f"[LLM End] response={response}")
        
    def on_llm_error(self, error, **kwargs):
        self.logger.debug(f"[LLM Error] {error}")
        
logging_hanlder = LoggingHandler(logger)