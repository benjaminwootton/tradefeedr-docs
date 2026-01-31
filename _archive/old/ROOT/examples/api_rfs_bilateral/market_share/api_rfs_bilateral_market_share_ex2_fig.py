# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="Date", y="MarketShare", title="LP Market Share Analysis 1", color="LP")
fig.show()