# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.bar(data_frame, y=["SpreadPnLPM_Pct25", "SpreadPnLPM_Pct50",
                            "SpreadPnLPM_Pct75", "SpreadPnLPM_Pct90", "SpreadPnLPM_Pct100"],
             barmode="group", title="SpreadPnLPM Percentiles by LP")
fig.show()