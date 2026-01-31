import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.Symbol=="AUDUSD"]

# Plot figure
fig= px.scatter(data_frame, x="TradeTime", y="NearPrice",
                color="OutCome", title="Scatter plot of AUDUSD NearPrice by OutCome")
fig.show()