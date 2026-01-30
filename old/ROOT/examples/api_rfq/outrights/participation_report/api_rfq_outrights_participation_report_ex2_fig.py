# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y="WinPerformanceScore",
             barmode="group", title="WinPerformanceScore by LP")
fig.show()