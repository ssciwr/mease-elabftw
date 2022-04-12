import logging
import os

# enable logging or not

use_logger = True
log_level = logging.DEBUG


def getLogger(
    name, output_file=os.path.join("mease_elabftw", "logging", "logging.log")
):
    if use_logger:
        # Configure the actual logger
        logger = logging.getLogger(name)
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

    # if logging is disabled we use a dummy logger with no output.
    else:
        logger = logging.getLogger("dummy")
        logger.setLevel(logging.CRITICAL)

    return logger
