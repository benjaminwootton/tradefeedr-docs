# import plotly libary
import plotly.express as px

# Plot figure
fig= px.scatter(data_frame.head(1), x="TradeID", y=["Price", "SecondBestPrice"],
                title="TradeID:Trade_00001 Price Comparison")
fig.show()