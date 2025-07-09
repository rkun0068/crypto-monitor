import requests
import json
import time 

class USDSMFuture:
    def __init__(self):
        self.base_endpoint = "https://fapi.binance.com"

    # refer to https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio
    def top_long_short_pos_ratio(self, symbol: str, period: str = "15m", limit: int = 30):
        endpoint = f"{self.base_endpoint}/futures/data/topLongShortPositionRatio"
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit
        }
        response_json = requests.get(endpoint, params=params).json()
        return response_json
    # refer to https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest-Statistics
    # 设置为5分钟 更快捕获庄家行为
    def open_interest_stats(self, symbol: str, period: str = "5m", limit: int = 30):
        endpoint = f"{self.base_endpoint}/futures/data/openInterestHist"
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit
        }
        response_json = requests.get(endpoint, params=params).json()
        return response_json

    """
    检查未平仓合约数量和合约总价值是否出现背离，如果背离，则可能存在庄家行为
    """
    def check_anomalies_in_oi(self, symbol: str, period: str = "5m", limit: int = 10):
        oi_stats = self.open_interest_stats(symbol, period, limit)
        # 循环遍历oi_stats 对比与前一个时间点的未平仓合约数量和合约总价值
        oi_stats_anomalies = []
        is_last_anomaly = False
        for i in range(1, len(oi_stats)):
            # 合约数量增加 合约总价值增加 or 合约数量减少 合约总价值减少 则可能存在庄家行为
            if (oi_stats[i]["sumOpenInterest"] > oi_stats[i-1]["sumOpenInterest"] and oi_stats[i]["sumOpenInterestValue"] > oi_stats[i-1]["sumOpenInterestValue"]):
                pass
            elif (oi_stats[i]["sumOpenInterest"] < oi_stats[i-1]["sumOpenInterest"] and oi_stats[i]["sumOpenInterestValue"] < oi_stats[i-1]["sumOpenInterestValue"]):
                pass 
            elif (oi_stats[i]["sumOpenInterest"] > oi_stats[i-1]["sumOpenInterest"] and oi_stats[i]["sumOpenInterestValue"] < oi_stats[i-1]["sumOpenInterestValue"]):
                oi_stats[i]["msg"] = "合约数量增加 合约总价值减少"
                oi_stats_anomalies.append(oi_stats[i])
                if i == len(oi_stats) - 1:
                    is_last_anomaly = True
            elif (oi_stats[i]["sumOpenInterest"] < oi_stats[i-1]["sumOpenInterest"] and oi_stats[i]["sumOpenInterestValue"] > oi_stats[i-1]["sumOpenInterestValue"]):
                oi_stats[i]["msg"] = "合约数量减少 合约总价值增加"
                oi_stats_anomalies.append(oi_stats[i])
                if i == len(oi_stats) - 1:
                    is_last_anomaly = True

        return oi_stats_anomalies,is_last_anomaly

    # refer to https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History
    # 资金费率 一次4小时 一天24小时 6次 
    def funding_rate(self, symbol: str, limit: int = 6):
        endpoint = f"{self.base_endpoint}/fapi/v1/fundingRate"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        response_json = requests.get(endpoint, params=params).json()
        return response_json
    
    """
    查看资金费率差值列表  5条数据 返回一个列表 列表中每个元素是两个时间点的资金费率差值
    """
    def funding_rate_diff(self, symbol: str, limit: int = 6):
        funding_rate = self.funding_rate(symbol, limit)
        funding_rate_diff = []
        for i in range(1, len(funding_rate)):
            funding_rate_diff.append(float(funding_rate[i]["fundingRate"]) - float(funding_rate[i-1]["fundingRate"]))
        return funding_rate_diff







