# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="Date", y="MarketShare", title="LP Market Share Analysis 2", color="LP")
fig.show()