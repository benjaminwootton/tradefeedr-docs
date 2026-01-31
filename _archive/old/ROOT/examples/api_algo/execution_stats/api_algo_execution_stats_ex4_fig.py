# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.LP=="LP1"].set_index("ExecVenue")

# Plot figure
fig = px.bar(data_frame["SpreadPnLPM"], title="LP1 ExecVenue Analysis")
fig.update_layout(xaxis={"categoryorder":"total ascending"})
fig.show()