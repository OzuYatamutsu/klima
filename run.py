from influx.influx_setup import *
from config import log_level
from logging import basicConfig, getLogger

# Set up logger
basicConfig(level=log_level)
logger = getLogger(__name__)
