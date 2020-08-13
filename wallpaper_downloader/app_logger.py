# -*- coding: utf-8 -*-

import logging


def _get_stream_handler() -> logging.StreamHandler:
    """
    Define parameters of logging in the console.

    Returns:
        logging.StreamHandler: console handler of the logger.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter("%(levelname)s: %(message)s"),
    )
    return stream_handler


def get_logger(name: str) -> logging.Logger:
    """
    Define all parameters of logging.

    Args:
        name (str): name of the logger.

    Returns:
        logging.Logger: logger with specified parameters.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_stream_handler())
    return logger
