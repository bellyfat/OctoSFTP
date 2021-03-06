
import logging
from sys import stdout


def load_logging(log_file, log_level=logging.DEBUG):
    """
    Initialise logging
    :param log_file:
    :param log_level:
    """
    # Initialise logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Initialise log file
    handler = logging.FileHandler(log_file, encoding='utf-8', mode='a')
    handler.setLevel(log_level)

    # Set logging format string
    log_template = '%(asctime)s (%(levelname)s) - %(name)s: %(message)s'
    handler.setFormatter(logging.Formatter(log_template))

    logger.addHandler(handler)

    # Create stdout handler
    stdout_handler = logging.StreamHandler(stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(logging.Formatter(log_template))

    logger.addHandler(stdout_handler)
