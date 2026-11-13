import logging
import os


def get_logger(name):

    log_directory = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "reports",
        "logs"
    )

    os.makedirs(
        log_directory,
        exist_ok=True
    )

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:

        log_file = os.path.join(
            log_directory,
            "automation.log"
        )

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger