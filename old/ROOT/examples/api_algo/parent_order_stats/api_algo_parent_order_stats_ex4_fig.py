# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y ="RiskTransferPricePerfBPS", title="Comparing different risk transfer price benchmarks")
fig.update_layout(xaxis={"categoryorder":"total ascending"})
fig.show()