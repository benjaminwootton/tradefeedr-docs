# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("ArrivalTime")
data_frame = data_frame.iloc[:-1,:]

# Plot figure
fig = px.line(data_frame.drop("TradeQuantityUSD", axis=1), x=data_frame.index,
              y=["ArrivalMidPerfBPS","TWAPMidPerfBPS","RiskTransferPricePerfBPS"],
              title="Intraday pattern of different performance metrics")
fig.show()