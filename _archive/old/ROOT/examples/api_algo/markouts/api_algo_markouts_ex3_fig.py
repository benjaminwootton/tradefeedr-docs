# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.ParentOrderID=="20180903-A03"]

df1 = data_frame[data_frame.MarkoutType=="MarkoutsAtZero"]
df1 = df1.set_index("ExecVenue").iloc[:,6:]

df2 = data_frame[data_frame.MarkoutType=="MarkoutsAtZeroAverage"]
df2 = df2.set_index("ExecVenue").iloc[:,6:]

# Plot figure 1
fig = px.line(df1.T, title ="MarkoutsAtZero by ExecVenue For POID:20180903-A03")
fig.show()

# Plot figure 2
fig = px.line(df2.T, title ="MarkoutsAtZero by ExecVenue For POID:20180903-A03")
fig.show()