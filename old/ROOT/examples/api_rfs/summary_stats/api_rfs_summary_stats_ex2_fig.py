# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame =data_frame.sort_values(by="ToxicityOfFills", ascending=False)

# Plot figure
fig = px.bar(data_frame, x="Symbol", y="ToxicityOfFills",
             title="ToxicityOfFills by Symbol",
             barmode="group")
fig.show()