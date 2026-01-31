# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("MarkoutType").iloc[:,3:].T
data_frame = data_frame[["Markouts"]]

# Plot figure
fig = px.line(data_frame, y="Markouts",
              title="Markouts Using Child and Parent Filters For POID:20180921-A00")

fig["data"][0]["name"] = "Markouts"
fig["data"][0]["showlegend"] = True

fig.show()