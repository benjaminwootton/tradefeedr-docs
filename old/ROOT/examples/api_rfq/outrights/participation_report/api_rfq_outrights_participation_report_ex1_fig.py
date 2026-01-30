# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y=["NumberOfWins", "ExpectedWins"],
             barmode="group", title="Number of Outright RFQs Won by LP")
fig.show()