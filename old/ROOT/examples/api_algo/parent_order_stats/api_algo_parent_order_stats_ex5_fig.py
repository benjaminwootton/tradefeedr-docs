# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame["LP"].isin(["LP1","LP2","LP3"])]

# Plot figure
fig = px.pie(data_frame, values="TradeQuantityUSD", names=data_frame.index,
             title="TradeQuantityUSD by LP")
fig.show()