# import plotly libary
import plotly.express as px

# Plot figure
fig = px.scatter(data_frame, x="TradeTime", y="TradeQuantityUSD",
                 title="Volume Traded by TradeTime", color="Symbol")

fig.show()