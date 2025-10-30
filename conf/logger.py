"""
logger.py
공통 로깅 유틸리티
"""
import logging
import sys
from conf.config import LOG_LEVEL

def get_logger(name: str) -> logging.Logger:
    """모듈별 logger 생성"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
    return logger