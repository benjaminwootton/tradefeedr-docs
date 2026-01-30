# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("ArrivalTime")


# Plot figure 1
fig = px.line(data_frame[data_frame.ParentChild=="Child"][["TradeQuantityUSD"]],
             title="Child Fills TradeQuantityUSD")

fig.show()

# Plot figure 2
fig = px.line(data_frame[data_frame.ParentChild=="Child"][["Price", "Mid0"]],
             title="Price and Mid Price of Child Fills ")
fig.show()

# Plot figure 3
fig = px.line(data_frame[data_frame.ParentChild=="Child"][["SpreadPnLPM"]],
             title="Child Fills SpreadPnLPM")

fig.show()