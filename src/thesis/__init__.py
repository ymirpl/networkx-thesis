import logging
import logging.config

# file = open("logging.conf")
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("thesis")
