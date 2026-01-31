# import plotly libary
import plotly.express as px

# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="ArrivalTime", y="RiskTransferCostBPS",
              title="Risk Transfer Cost by ArrivalTime")
fig.show()