# import plotly libary
import plotly.express as px

# Plot figure
fig = px.scatter(data_frame, x="LP", y=["SpreadPnLPM"], color="Symbol",
                 title="SpreadPnL by Symbol")
fig.show()