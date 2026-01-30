# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="DecayPM1m", y="Count", barmode="group",
             title="Histogram DecayPM1m")
fig.show()