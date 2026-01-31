# import plotly libary
import plotly.express as px

# Plot figure 1
fig =  px.histogram(data_frame, x="ArrivalMidPerfBPS", title="Histogram of ArrivalMidPerfBPS")
fig.show()