import os
import logging

def get_logger(log_filename: str) -> logging.Logger:
    BASE_DIR = os.path.abspath(os.getcwd())
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    os.makedirs(LOGS_DIR, exist_ok=True)

    log_file_path = os.path.join(LOGS_DIR, log_filename)
    logger_name = f"logger_{log_filename}"  # make logger name unique

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        file_handler = logging.FileHandler(log_file_path, mode='a')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
