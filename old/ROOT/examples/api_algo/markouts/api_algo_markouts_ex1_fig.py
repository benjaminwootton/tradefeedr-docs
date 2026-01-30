# import plotly libary
import plotly.express as px
import plotly.graph_objs as go

# Modify dataframe
data_frame = data_frame.set_index("MarkoutType").iloc[:,3:].T
data_frame = data_frame[["Markouts", "Volatilities"]]

# Plot figure
fig = px.line(data_frame, y="Markouts", title ="Markouts with Volatility Bands For POID:20180921-A00")

fig["data"][0]["name"] = "Markouts"
fig["data"][0]["showlegend"] = True

fig.add_trace(go.Scatter(y=data_frame["Markouts"]-data_frame["Volatilities"], x=data_frame.index, mode="lines",
                         fill="tonexty", name="Confidence Interval 2"))
fig.add_trace(go.Scatter(y=data_frame["Markouts"]+data_frame["Volatilities"], x=data_frame.index, mode="lines",
                         fill="tonexty", name="Confidence Interval 1"))
fig.show()