# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="SpreadPnLPM", y="Count",
             title="hist function in groupby:SpreadPnLPM" )
fig.show()