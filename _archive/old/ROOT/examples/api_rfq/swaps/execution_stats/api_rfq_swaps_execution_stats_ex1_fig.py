# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.groupby("LP").sum()
data_frame = data_frame.sort_values(by="NearTradeQuantity", ascending=False)

# Plot figure
fig = px.bar(data_frame, y="NearTradeQuantity", title="Swaps RFQ NearTradeQuantity by LP")
fig.show()