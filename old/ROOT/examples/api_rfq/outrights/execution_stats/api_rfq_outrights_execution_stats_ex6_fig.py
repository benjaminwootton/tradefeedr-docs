# import plotly libary
import plotly.express as px

# Plot figure
fig = px.scatter(data_frame, x="TradeQuantityUSD", y="Price",
                 title="Bubble plot of Price and TradeQuantityUSD",
                 size="TradeQuantityUSD")
fig.show()