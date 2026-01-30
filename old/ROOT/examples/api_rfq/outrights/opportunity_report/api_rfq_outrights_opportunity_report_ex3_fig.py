# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.TradeCcy=="AUD"].head(50)

# Plot figure
fig = px.scatter(data_frame, x="TradeTime" , y="MissedByPIPS", title="Selecting Losing RFQs only (TradeCcy:AUD)")
fig.show()