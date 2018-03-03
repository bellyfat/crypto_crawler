from collections import defaultdict, Counter
import sys
import ConfigParser

from dao.db import init_pg_connection

from utils.key_utils import load_keys
from utils.time_utils import get_now_seconds_utc, parse_time
from utils.file_utils import set_log_folder

from analysis.data_load_for_profit_report import fetch_trades_history_to_db
from analysis.binance_order_by_trades import group_binance_trades_per_order

from analysis.grouping_utils import group_trades_by_orders, group_by_pair_id
from analysis.data_preparation import prepare_data
from analysis.profit_report_analysis import compute_loss, compute_profit_by_pair, save_report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: {prg_name} your_config.cfg".format(prg_name=sys.argv[0])
        print "FIXME TODO: we should use argparse module"
        exit(0)

    cfg_file_name = sys.argv[1]

    config = ConfigParser.RawConfigParser()
    config.read(cfg_file_name)

    db_host = config.get("postgres", "db_host")
    db_port = config.get("postgres", "db_port")
    db_name = config.get("postgres", "db_name")

    should_fetch_history_to_db = config.getboolean("common", "fetch_history_from_exchanges")

    key_path = config.get("common", "path_to_api_keys")
    log_folder = config.get("common", "logs_folder")

    start_time = parse_time(config.get("common", "start_time"), '%Y-%m-%d %H:%M:%S')
    end_time = parse_time(config.get("common", "end_time"), '%Y-%m-%d %H:%M:%S')

    if start_time == end_time or end_time <= start_time:
        print "Wrong time interval provided! {ts0} - {ts1}".format(ts0=start_time, ts1=end_time)
        assert False

    pg_conn = init_pg_connection(_db_host=db_host, _db_port=db_port, _db_name=db_name)

    load_keys(key_path)
    set_log_folder(log_folder)

    if should_fetch_history_to_db:
        fetch_trades_history_to_db(pg_conn, start_time, end_time)

    orders, history_trades, binance_trades, binance_orders_at_bot, binance_orders_at_exchange = \
        prepare_data(pg_conn, start_time, end_time)

    missing_orders, failed_orders, orders_with_trades = group_trades_by_orders(orders,
                                                                               history_trades,
                                                                               binance_orders_at_exchange)

    # 2 stage - filling order->trades list for Binances
    binance_trades_group_by_pair = group_by_pair_id(binance_trades)

    binance_orders_with_trades = group_binance_trades_per_order(binance_orders_at_exchange, binance_trades_group_by_pair, binance_orders_at_bot)

    orders_with_trades += binance_orders_with_trades

    # 3 stage - bucketing all that crap by pair_id
    trades_to_order = defaultdict(list)
    for order, trade_list in orders_with_trades:
        trades_to_order[order.pair_id].append( (order, trade_list))

    profit_by_pairs = Counter()
    profit_by_pair_bitcoins = Counter()

    for pair_id in trades_to_order:
        profit_by_pairs[pair_id], profit_by_pair_bitcoins[pair_id] = compute_profit_by_pair(pair_id, trades_to_order[pair_id])

    overall_profit = sum(profit_by_pair_bitcoins.itervalues())

    loss_by_pair, loss_by_pair_bitcoin = compute_loss(orders_with_trades)

    save_report(start_time, end_time, overall_profit, profit_by_pairs, profit_by_pair_bitcoins,
                missing_orders, failed_orders, loss_by_pair, loss_by_pair_bitcoin,
                orders, history_trades
                )