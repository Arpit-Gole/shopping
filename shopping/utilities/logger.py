"""
A module to support logging settings effectively across the codebase.
"""

import logging
import sys


def get_default_logger(format_string: str = None, level: int = None) -> logging.Logger:
    """
    Return a root logger by modifying the basic logger configurations:
    1. Logs for DEBUG and INFO levels goes to `stdout` stream.
    2. Logs for other levels, i.e., (WARNING, ERROR and CRITICAL) goes
    to `stderr` stream.
    Parameters
    ----------
    format_string: A log record format string.
    level: A log level.

    Returns
    -------
    Returns the modified root logger object.
    """
    if format_string is None:
        format_string = "%(asctime)s [%(levelname)s] -- %(message)s -- (%(filename)s:%(lineno)s)"

    if level is None:
        level = logging.DEBUG

    # Set handlers with the appropriate filters.
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stdout_handler.setLevel(level)
    stderr_handler.setLevel(max(level, logging.WARNING))

    # Set a log format.
    formatter = logging.Formatter(format_string)
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    logger.setLevel(level)

    return logger
