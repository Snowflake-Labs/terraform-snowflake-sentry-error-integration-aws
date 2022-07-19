import logging
from logging import Logger


def setup_logger(logger_name: str, level: int = logging.INFO) -> Logger:
    """Sets up the logger object.

    Args:
        logger_name (str): Name to use to retreive the logger instance.
        level (int, optional): Level of logging. Defaults to logging.INFO.
        stdout (bool, optional): Bool whether to print to stdout or not. Defaults to False.

    Returns:
        Logger: Returns the logger object.
    """
    l = logging.getLogger(logger_name)
    l.setLevel(level)
    return l
