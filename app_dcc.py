from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import time

app = Dash(__name__)
server=app.server
df = px.data.gapminder()

# Simulate a slow function
def heavy_query(continent):
    time.sleep(2)  # pretend this takes long
    return df[df["continent"] == continent]

# Layout
app.layout = html.Div([
    html.H3("App-Wide State with dcc.Store"),
    dcc.Store(id='cache'),   # invisible data storage

    html.Label("Select Continent:"),
    dcc.Dropdown(
        id='continent',
        options=[{'label': c, 'value': c} for c in sorted(df['continent'].unique())],
        value='Asia'
    ),

    html.Div("Loading data... (wait a second on first load)", style={'marginTop': '10px'}),
    dcc.Graph(id='chart', style={'height': '550px'})
])

# Callback 1: Expensive step → store data in cache
@app.callback(Output('cache', 'data'), Input('continent', 'value'))
def load_data(continent):
    dfx = heavy_query(continent)   # heavy work
    return dfx.to_dict('records')  # store as dictionary list (JSON-like)

# Callback 2: Use cached data → draw chart
@app.callback(Output('chart', 'figure'), Input('cache', 'data'))
def draw(data):
    dfx = pd.DataFrame(data)
    fig = px.scatter(
        dfx,
        x='gdpPercap', y='lifeExp',
        color='country',
        log_x=True,
        title=f"{dfx['continent'].iloc[0]} — Life Expectancy vs GDP"
    )
    fig.update_layout(template='plotly_white', margin=dict(l=20, r=20, t=40, b=20))
    return fig

if __name__ == '__main__':
    app.run(debug=True)