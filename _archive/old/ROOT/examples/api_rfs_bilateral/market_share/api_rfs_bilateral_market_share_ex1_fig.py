# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.LP=="LP1masked"]

# Plot figure
fig = px.line(data_frame, x="Date", y="MarketShare", title="LP1masked MarketShare Plot")
fig.show()