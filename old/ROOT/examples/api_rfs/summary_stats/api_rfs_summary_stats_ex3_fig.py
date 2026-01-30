# import plotly libary
import plotly.express as px

# Plot figure 1
fig = px.bar(data_frame.groupby("LP").sum(), y="RejectVolume",
             title="Rejected Volume Bar Chart")

fig.update_layout(xaxis={"categoryorder":"total descending"})
fig.show()

# Plot figure 2
fig = px.bar(data_frame, x="LP", y="SpreadPaid",
             color="Symbol",
             title="Spread analysis Bar Chart",
             barmode="group")
fig.show()