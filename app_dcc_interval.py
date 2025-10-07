from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import datetime

app = Dash(__name__)
server=app.server

app.layout = html.Div([
    html.H3("Live Updates with dcc.Interval"),
    
    # The timer: every 2000 ms (2 seconds)
    dcc.Interval(
        id='tick',
        interval=2_000,   # 2000 ms = 2 seconds
        n_intervals=0
    ),

    # The live-updating graph
    dcc.Graph(id='live')
])

# Callback: runs every time the interval ticks
@app.callback(
    Output('live', 'figure'),
    Input('tick', 'n_intervals')
)
def refresh(n):
    # Fake "latest" data for demonstration
    now = datetime.datetime.now()
    times = pd.date_range(now - datetime.timedelta(seconds=20), now, freq='2s')
    values = np.random.randint(50, 100, len(times))

    dfx = pd.DataFrame({'timestamp': times, 'value': values})

    fig = px.line(
        dfx,
        x='timestamp',
        y='value',
        title=f'Live Metric (update #{n})',
        markers=True
    )
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)