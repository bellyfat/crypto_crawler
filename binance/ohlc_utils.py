from constants import BINANCE_GET_OHLC
from data.Candle import Candle
from debug_utils import should_print_debug
from data_access.internet import send_request
from enums.status import STATUS


def get_ohlc_bittrex(currency, date_start, date_end, period):
    result_set = []

    # https://api.binance.com/api/v1/klines?symbol=XMRETH&interval=15m&startTime=
    final_url = BINANCE_GET_OHLC + currency + "&interval=" + period + "&startTime=" + str(date_start)

    if should_print_debug():
        print final_url

    err_msg = "get_ohlc_binance called for {pair} at {timest}".format(pair=currency, timest=date_start)
    error_code, r = send_request(final_url, err_msg)

    if error_code == STATUS.SUCCESS and r is not None :
        """
         [
		    1499040000000,      // Open time
		    "0.01634790",       // Open
		    "0.80000000",       // High
		    "0.01575800",       // Low
		    "0.01577100",       // Close
		    "148976.11427815",  // Volume
		    1499644799999,      // Close time
		    "2434.19055334",    // Quote asset volume
		    308,                // Number of trades
		    "1756.87402397",    // Taker buy base asset volume
		    "28.46694368",      // Taker buy quote asset volume
		    "17928899.62484339" // Can be ignored
		  ]
        """
        for record in r:
            result_set.append(Candle.from_binance(record, currency))

    return result_set