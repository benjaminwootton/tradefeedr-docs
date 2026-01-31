# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, y="ArrivalMidPerfBPS", x="LP", title="Comparing algo performance metrics across LPs")
fig.update_layout(xaxis={"categoryorder":"total ascending"})
fig.show()