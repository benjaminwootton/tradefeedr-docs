# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.Symbol=="USDJPY"]
data_frame = data_frame.sort_values(by="DecayPM30s", ascending=False)

# Plot figure 1
fig = px.bar(data_frame[data_frame.OrderStatus=="F"], x="LP", y="DecayPM30s",
             title="Filled Trades: USDJPY DecayPM30s by LP")
fig.show()

# Plot figure 2
fig = px.bar(data_frame[data_frame.OrderStatus=="R"], x="LP", y="DecayPM30s",
             title="Rejected Trades :USDJPY DecayPM30s by LP")
fig.show()