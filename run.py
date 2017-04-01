from influx.influx_adapter import *
from config import *
from logging import basicConfig, getLogger

# Set up logger
basicConfig(level=log_level)
logger = getLogger(__name__)

def main():
    """
    The entrypoint of the program.
    """

    if influx_settings['enabled']:
        get_client()

main()