from core.binance.spot import Spot
from core.binance.usds_m_future import USDSMFuture
import pandas as pd 
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 页面设置
st.set_page_config(page_title="币种信息汇总", layout="wide")
st.title("📊 币种信息汇总")

# 初始化
spot_api = Spot()
usds_m_future_api = USDSMFuture()
symbol = ""  

#现货24小时资金流入
net_capital_in = spot_api.net_capital_in(symbol)
net_capital_in_df = pd.DataFrame(net_capital_in["data"])
net_capital_in_df["startTime"] = pd.to_datetime(net_capital_in_df["startTime"], unit="ms").dt.tz_localize("UTC").dt.tz_convert("Asia/Shanghai")
net_capital_in_df["endTime"] = pd.to_datetime(net_capital_in_df["endTime"], unit="ms").dt.tz_localize("UTC").dt.tz_convert("Asia/Shanghai")
fig = px.line(
    net_capital_in_df,
    x="startTime",
    y="netCapitalInflowVolume",
    title=f"{symbol} - 24小时资金净流入",
    labels={"startTime": "时间", "netCapitalInflowVolume": "资金净流入"},
)
st.plotly_chart(fig, use_container_width=True)


# 2. 合约未平仓量和合约总价值
oi_stats = usds_m_future_api.open_interest_stats(symbol, period="15m", limit=96)
oi_stats_df = pd.DataFrame(oi_stats)
oi_stats_df["timestamp"] = pd.to_datetime(oi_stats_df["timestamp"], unit="ms")
oi_stats_df["sumOpenInterest"] = oi_stats_df["sumOpenInterest"].astype(float)
oi_stats_df["sumOpenInterestValue"] = oi_stats_df["sumOpenInterestValue"].astype(float)

# 创建图形对象
fig2 = go.Figure()

# 左 Y 轴：未平仓合约数量
fig2.add_trace(go.Scatter(
    x=oi_stats_df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Asia/Shanghai"),
    y=oi_stats_df["sumOpenInterest"],
    mode="lines",
    name="未平仓合约数量",
    line=dict(color="green"),
    yaxis="y1"
))

# 右 Y 轴：合约总价值
fig2.add_trace(go.Scatter(
    x=oi_stats_df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Asia/Shanghai"),
    y=oi_stats_df["sumOpenInterestValue"],
    mode="lines",
    name="合约总价值",
    line=dict(color="red"),
    yaxis="y2"
))
fig2.update_layout(
    title=f"{symbol} - 未平仓合约数量 & 总价值",
    xaxis=dict(title="时间"),
    yaxis=dict(
        title=dict(text="未平仓合约数量", font=dict(color="green")),
        tickfont=dict(color="green"),
        side="left"
    ),
    yaxis2=dict(
        title=dict(text="合约总价值", font=dict(color="red")),
        tickfont=dict(color="red"),
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.01, y=0.99),
    hovermode="x unified",
    template="plotly_white"
)


st.plotly_chart(fig2, use_container_width=True)


