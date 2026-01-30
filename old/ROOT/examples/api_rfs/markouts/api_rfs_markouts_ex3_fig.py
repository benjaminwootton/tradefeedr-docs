# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")

# Plot figure 1
fig = px.line(data_frame[data_frame.MarkoutType=="MarkoutsAtZero"].iloc[:,5:].T, title="MarkoutsAtZero by LP")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="MarkoutsAtZero")
fig.show()

# Plot figure 2
fig = px.line(data_frame[data_frame.MarkoutType=="MarkoutsAtZeroAverage"].iloc[:,5:].T, title="MarkoutsAtZeroAverage by LP")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="MarkoutsAtZeroAverage")
fig.show()