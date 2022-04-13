import logging
import os
import time

# enable logging or not

log_level = logging.DEBUG


logger = logging.getLogger("dummy")
logger.setLevel(logging.CRITICAL)


def toggleLogger(
    toggle_bool,
    name="mease-elabftw",
    output_file=os.path.join("mease_elabftw", "logging", "logging.log"),
):
    global logger
    # use memoization to only setup the logger once.
    if logger.getEffectiveLevel() == logging.CRITICAL and toggle_bool:
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
        logger.info(f"Setup logging file at {output_file}, log level ist {log_level}")
    # if logging is disabled we use a dummy logger with no output.
    elif logger.getEffectiveLevel != logging.CRITICAL and not toggle_bool:
        logger = logging.getLogger("dummy")
        logger.setLevel(logging.CRITICAL)

    # return logger
