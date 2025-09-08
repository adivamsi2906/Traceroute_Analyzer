import logging
import os

def setup_logger(log_file="logs/app.log"):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("TracerouteLogger")
    logger.setLevel(logging.DEBUG)
    
    # Check if handlers are already added
    if not logger.hasHandlers():
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger