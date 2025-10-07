import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1,2,3,4], y=[10,15,13,17], mode='lines+markers', name='Series A'))
fig.update_layout(title='Custom Line', xaxis_title='X', yaxis_title='Y')
fig.write_image("graph_test.png")
fig.show()