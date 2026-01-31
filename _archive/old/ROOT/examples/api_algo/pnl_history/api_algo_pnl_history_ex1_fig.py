# import plotly libary
import plotly.express as px
import plotly.graph_objs as go

# Plot figure 1
fig = px.line(data_frame,
              y=["SlippageToArrivalMidPMUser","SlippageToArrivalMidPMBank"],
              x="Time",
              title="PnL Dynamics of an Active Algo")
fig.show()

# Plot figure 2
fig = px.line(data_frame, y=["Mid"], x="Time", title="Market data and LimitPrice Chart")
fig.add_trace(go.Scatter(x=data_frame["Time"], y=data_frame["LimitPrice"], mode="lines"))
fig.show()