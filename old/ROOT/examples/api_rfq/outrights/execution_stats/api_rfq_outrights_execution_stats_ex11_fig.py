# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")
data_frame1 = data_frame[(data_frame.Symbol=="EURUSD") & (data_frame.Side=="B")]
data_frame2 = data_frame[(data_frame.Symbol=="EURUSD") & (data_frame.Side=="S")]

# Plot figure 1
fig = px.scatter(data_frame1, y=["Price","Price_Pct90"],
          title="Buying EURUSD Price by LP" )
fig.show()

# Plot figure 2
fig = px.scatter(data_frame2, y=["Price","Price_Pct90"],
          title="Selling EURUSD Price by LP" )
fig.show()