import json


def is_error(response):
    """

    Proper response should contain 'response' key.

    EGeneral:Invalid arguments
    EService:Unavailable
    ETrade:Invalid request
    EOrder:Cannot open position
    EOrder:Cannot open opposing position
    EOrder:Margin allowance exceeded
    EOrder:Margin level too low
    EOrder:Insufficient margin (exchange does not have sufficient funds to allow margin trading)
    EOrder:Insufficient funds (insufficient user funds)
    EOrder:Order minimum not met (volume too low)
    EOrder:Orders limit exceeded
    EOrder:Positions limit exceeded
    EOrder:Rate limit exceeded
    EOrder:Scheduled orders limit exceeded
    EOrder:Unknown position

    :param response: raw responce from requests
    :return: True\False as indicator for possible errors
    """
    if response is None or 'result' not in response:
        return True

    str_repr = json.dumps(response)
    if "EOrder" in str_repr or "Unavailable" in str_repr or "Busy" in str_repr or "ETrade" in str_repr or \
            "EGeneral:Invalid" in str_repr or "timeout" in str_repr:
        return True

    return False
