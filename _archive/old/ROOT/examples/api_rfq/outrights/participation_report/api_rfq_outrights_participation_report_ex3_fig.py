# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y="VolumePerformanceScore",
              title="VolumePerformanceScore by LP")
fig.show()