# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.bar(data_frame.iloc[:,3:], barmode="group", title="SpreadPnLPM Percentile Plot")
fig.show()