from kraken.constants import KRAKEN_BASE_API_URL, KRAKEN_GET_CLOSE_ORDERS
from data.Trade import Trade

from data_access.classes.PostRequestDetails import PostRequestDetails
from data_access.internet import send_post_request_with_header
from data_access.memory_cache import generate_nonce

from debug_utils import should_print_debug, print_to_console, LOG_ALL_MARKET_RELATED_CRAP

from enums.status import STATUS

from utils.file_utils import log_to_file
from utils.key_utils import sign_kraken


def get_closed_orders_kraken_post_details(key, pair_name=None):
    final_url = KRAKEN_BASE_API_URL + KRAKEN_GET_CLOSE_ORDERS

    body = {
        "nonce": generate_nonce()
    }

    headers = {"API-Key": key.api_key, "API-Sign": sign_kraken(body, KRAKEN_GET_CLOSE_ORDERS, key.secret)}

    res = PostRequestDetails(final_url, headers, body)

    if should_print_debug():
        msg = "get_closed_orders_kraken: {res}".format(res=res)
        print_to_console(msg, LOG_ALL_MARKET_RELATED_CRAP)
        log_to_file(msg, "market_utils.log")

    return res


def get_order_history_kraken_result_processor(json_document, pair_name):
    """
    json_document - response from exchange api as json string
    pair_name - for backwords compabilities
    """
    orders = []
    if json_document is None or "result" not in json_document or "closed" not in json_document["result"]:
        return orders

    for order_id in json_document["result"]["closed"]:
        new_order = Trade.from_kraken(order_id, json_document["result"]["closed"][order_id])
        if new_order is not None:
            orders.append(new_order)

    return orders


def get_order_history_kraken(key, pair_name=None):

    post_details = get_closed_orders_kraken_post_details(key, pair_name)

    err_msg = "check kraken closed orders called"

    error_code, json_document = send_post_request_with_header(post_details.final_url, post_details.headers, post_details.body,
                                                    err_msg, max_tries=5)

    closed_orders = []
    if error_code == STATUS.SUCCESS:
        closed_orders = get_order_history_kraken_result_processor(json_document, pair_name)

    return error_code, closed_orders
