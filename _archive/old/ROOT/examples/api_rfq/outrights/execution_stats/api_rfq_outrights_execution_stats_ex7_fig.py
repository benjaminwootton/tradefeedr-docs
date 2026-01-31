# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="TradeQuantityUSD", y="Count", title="TradeQuantityUSD frequency plot")
fig.show()