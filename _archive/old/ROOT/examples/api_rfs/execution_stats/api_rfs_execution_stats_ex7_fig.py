# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y="DecayPM1s", title="Rank Percentile Plot")
fig.update_layout(xaxis={"categoryorder":"total descending"})
fig.show()