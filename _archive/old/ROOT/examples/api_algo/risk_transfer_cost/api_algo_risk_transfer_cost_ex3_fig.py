# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="OrderQuantity", y="RiskTransferCostBPS",
              title="Risk Transfer Cost by OrderQuantity")
fig.show()