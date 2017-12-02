class CURRENCY:
    BITCOIN = 0
    DASH = 1
    ETH = 2
    LTC = 3
    XRP = 4
    BCC = 5
    ETC = 6
    SC = 7
    DGB = 8
    XEM = 9
    ARDR = 10
    OMG = 11
    ZEC = 12
    REP = 13
    XMR = 14
    DOGE = 15
    DCR = 16

    USD = 1000
    USDT = 1001

    @classmethod
    def values(cls):
        return [
                CURRENCY.BITCOIN,
                CURRENCY.DASH,
                CURRENCY.ETH,
                CURRENCY.LTC,
                CURRENCY.XRP,
                CURRENCY.BCC,
                CURRENCY.ETC,
                CURRENCY.SC,
                CURRENCY.DGB,
                CURRENCY.XEM,
                CURRENCY.ARDR,
                CURRENCY.OMG,
                CURRENCY.ZEC,
                CURRENCY.REP,
                CURRENCY.XMR,
                CURRENCY.DOGE,
                CURRENCY.DCR,
                CURRENCY.USD,
                CURRENCY.USDT
                ]