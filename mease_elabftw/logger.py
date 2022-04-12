import logging
import os

# Use this to stop logging
use_logging = True


# Configure the basic logger
logger = logging.getLogger("mease-elabftw")
logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler()
_handler.setLevel(logging.WARNING)
logger.addHandler(_handler)
_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
_handler.setFormatter(_formatter)

if use_logging:
    os.makedirs("mease_elabftw/logging", exist_ok=True)
    handler = logging.FileHandler("mease_elabftw/logging/logging.log", mode="w")
    handler.setFormatter(_handler)
    logger.addHandler(handler)

# This determines the final state of the logger.
logger.setLevel(logging.DEBUG)

if use_logging == False:
    logging.disable(logging.CRITICAL)
