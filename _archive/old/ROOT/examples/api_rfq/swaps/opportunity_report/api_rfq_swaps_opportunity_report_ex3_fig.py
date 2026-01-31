# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.TradeCcy=="AUD"]

# Plot figure

fig = px.scatter(data_frame, x="TradeTime", y=["NearPrice","NearPriceShown","FarPrice","FarPriceShown"],
                 title="Select Losing RFQs only (TradeCcy:AUD)")
fig.show()