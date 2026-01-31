# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.line(data_frame.iloc[:,3:].T, title="Volatilities by LP")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="Volatilities")
fig.show()