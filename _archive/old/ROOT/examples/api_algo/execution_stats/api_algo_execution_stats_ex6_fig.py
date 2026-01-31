# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.LP=="LP1"].set_index("ExecVenue")

# Plot figure
fig = px.bar(data_frame["DecayPM1s"], barmode="group",
             title="LP1 DecayPM1s ExecVenue Analysis for Trades greater than $50m")
fig.update_layout(xaxis={"categoryorder":"total ascending"})
fig.show()