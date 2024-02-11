import logging.config

from src.config.logger import LOGGING
from src.config.config import unwanted_event_names

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def filter_datalayer(datalayer):
    try:
        filtered_data_layer = [event for event in datalayer if event.get("event") not in unwanted_event_names]
        return filtered_data_layer
    except TypeError as e:
        logger.error(f"TypeError encountered: {e}. Ensure 'data_layer' is a list of dictionaries.")
        return []
    except KeyError as e:
        logger.error(f"KeyError encountered: {e}. One of the dictionaries might be missing the 'event' key.")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []


def data_layer_dct_initializer():
    return {"homepage_page": "", "listing_page": "", "product_page": "", "basket_page": "", "sales_page": ""}
