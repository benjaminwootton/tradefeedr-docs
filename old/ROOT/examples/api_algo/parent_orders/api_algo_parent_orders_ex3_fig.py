# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")
data_frame = data_frame[["mean","std","min", "max"]]

# Plot figure
fig = px.bar(data_frame, barmode="group", title="Descriptive statistics for algo performance")
fig.show()