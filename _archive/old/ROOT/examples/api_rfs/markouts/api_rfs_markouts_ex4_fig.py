# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.head()
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.line(data_frame.iloc[:,3:].T, title="Markout Curve")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="Markouts")
fig.show()