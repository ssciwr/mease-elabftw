import logging
import os
import time

# enable logging or not

use_logger = True
log_level = logging.DEBUG


def getLogger(
    name, output_file=os.path.join("mease_elabftw", "logging", "logging.log"), logger={}
):
    # use memoization to only setup the logger once.
    if logger == {}:
        if use_logger:
            # Configure the actual logger
            logger[name] = logging.getLogger(name)
            logger[name].setLevel(logging.DEBUG)
            _handler = logging.StreamHandler()
            _handler.setLevel(logging.WARNING)
            logger[name].addHandler(_handler)
            _formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            _handler.setFormatter(_formatter)
            dir_path = os.path.dirname(os.path.realpath(output_file))
            os.makedirs(dir_path, exist_ok=True)
            handler = logging.FileHandler(output_file, mode="w")
            handler.setFormatter(_handler)
            logger[name].addHandler(handler)

            # This determines the final state of the logger.
            logger[name].setLevel(log_level)
            logger[name].info(
                f"Setup logging file at {output_file}, log level ist {log_level}"
            )
        # if logging is disabled we use a dummy logger with no output.
        else:
            logger[name] = logging.getLogger("dummy")
            logger[name].setLevel(logging.CRITICAL)

    return logger[name]
