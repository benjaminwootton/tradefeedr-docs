# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame.Count, barmode="group", title="bar function in groupby: SpreadPnLPM")
fig.show()