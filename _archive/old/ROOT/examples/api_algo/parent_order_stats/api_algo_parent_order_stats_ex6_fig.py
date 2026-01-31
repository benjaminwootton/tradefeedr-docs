# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[["TWAPMidPerfBPS","HourArrive"]].head()
data_frame = data_frame.reset_index()

# Plot figure
fig = px.bar(data_frame, x=data_frame.HourArrive, y=data_frame.TWAPMidPerfBPS,
title="Select orders wih a low performance metric by arrival hour", color="LP", barmode="group")
fig.show()