import logging
import os
import time

# By default no log will be written.
log_level = logging.DEBUG

logger = logging.getLogger("mease-elabftw")
logger.setLevel(logging.CRITICAL)

# this is the default log-file path
output_file = os.path.join("mease_elabftw", "logging", "logging.log")


def activate_logger(toggle_bool):
    """
    This function enables or disables the logging feature.

    When enabled the logger will write important information into a file.

    By default the logger is not active.

    To activate or deactive use either:

    ``from mease_elabftw.logger import toggle_logger``

    ``toggle_logger(bool)``

    or:

    ``mease_elabftw.toggle_logger(bool)``




    :param toggle_bool: The bool to turn the logger on or of
    :type toggle_bool: bool
    """
    logger = logging.getLogger("mease-elabftw")
    # use memoization to only setup the logger once.
    if logger.getEffectiveLevel() == logging.CRITICAL and toggle_bool:
        # Configure the actual logger
        logger = logging.getLogger("mease-elabftw")
        logger.setLevel(logging.DEBUG)
        _handler = logging.StreamHandler()
        _handler.setLevel(logging.WARNING)
        logger.addHandler(_handler)
        _formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        _handler.setFormatter(_formatter)
        dir_path = os.path.dirname(os.path.realpath(output_file))
        os.makedirs(dir_path, exist_ok=True)
        handler = logging.FileHandler(output_file, mode="w")
        handler.setFormatter(_handler)
        logger.addHandler(handler)

        # This determines the final state of the logger.
        logger.setLevel(log_level)
        logger.info(f"Setup logging file at {output_file}, log level ist {log_level}")
    # if logging is disabled we use a dummy logger with no output.
    elif logger.getEffectiveLevel != logging.CRITICAL and not toggle_bool:
        logger = logging.getLogger("mease-elabftw")
        logger.setLevel(logging.CRITICAL)

    # return logger


def set_log_level(level):
    """
    User function to change the log level.

    Possible values are:

     * 10: Debug
     * 20: Info
     * 30: Warning
     * 40: Error
     * 50: Critical

    It is also possible to use ``logging.DEBUG`` etc.

    This function will automatically enable the logger if used.

    :param level: New log level.
    :type level: int
    """
    logger = logging.getLogger("mease-elabftw")
    activate_logger(True)
    logger.setLevel(level)
