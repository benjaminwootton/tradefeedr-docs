# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y=["ActualWinRatio", "ActualVolumeWinRatio"],
             barmode="group", title="Comparing WinRatios")
fig.show()