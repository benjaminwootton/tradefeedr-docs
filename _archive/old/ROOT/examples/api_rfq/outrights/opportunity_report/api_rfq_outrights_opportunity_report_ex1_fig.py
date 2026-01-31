# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.Symbol=="AUDUSD"]

# Plot figure
fig= px.scatter(data_frame, x="TradeTime", y=["PriceShown"], color="OutCome",
                title="Scatter plot of AUDUSD PriceShown by OutCome")
fig.show()