# import plotly libary
import plotly.express as px


# Plot figure
fig = px.scatter(data_frame, x="TradeTime", y="NearTradeQuantity", color="Symbol",
                 title="NearTradeQuantity by TradeTime and Symbol")
fig.show()