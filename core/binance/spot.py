import requests

class Spot:
    def __init__(self):
        self.base_url = "https://www.binance.com"
    """
    24小时资金净流入
    """
    def net_capital_in(self, symbol: str, interval: str = "FIFTEEN_MINUTES", size: int = 96):
        endpoint = f"{self.base_url}/bapi/earn/v1/public/indicator/capital-flow/netCapitalIn"
        params = {
            "symbol": symbol,
            "intervalEnum": interval,
            "size": size
        }
        response_json = requests.get(endpoint, params=params).json()
        return response_json