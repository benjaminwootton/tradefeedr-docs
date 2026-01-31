# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame=data_frame.groupby("Date").sum()

# Plot figure
fig = px.line(data_frame, y="TradeQuantity", title="Daily Traded Volume")
fig.show()