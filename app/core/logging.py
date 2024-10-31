import logging
import sys
from .config import get_settings

def setup_logging():
    settings = get_settings()
    
    logger = logging.getLogger("agentsystem")
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
