from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import dash

# Initialize app
app = Dash(__name__)
server=app.server
df = px.data.gapminder()

# --- Layout ---
app.layout = html.Div([
    html.H2("🌍 Cross-Filtering Example"),

    html.Div([
        dcc.Graph(id='overview', style={'flex': '1', 'height': '550px'}),
        dcc.Graph(id='detail', style={'flex': '1', 'height': '550px'})
    ], style={'display': 'flex', 'gap': '16px'})
])

# --- Callback for first chart (Overview) ---
@app.callback(
    Output('overview', 'figure'),
    Input('overview', 'id')  # dummy input just to draw chart once
)
def draw_overview(_):
    # Start with one year for the overview
    dfx = df[df['year'] == 2007]
    fig = px.scatter(
        dfx, x='gdpPercap', y='lifeExp',
        size='pop', color='continent',
        hover_name='country',
        log_x=True, title='Click a Country Bubble (2007)',
        template='plotly_white'
    )
    return fig

# --- Callback for cross-filtering (click one → update the other) ---
@app.callback(
    Output('detail', 'figure'),
    Input('overview', 'clickData')
)
def show_detail(clickData):
    if not clickData:
        raise dash.exceptions.PreventUpdate

    # Extract the clicked country name
    country = clickData['points'][0]['hovertext']  # hovertext holds country name

    # Filter dataframe for that country
    dfx = df[df['country'] == country]

    # Create a line chart for that country
    fig = px.line(
        dfx, x='year', y='lifeExp',
        title=f"{country}: Life Expectancy Over Time",
        template='plotly_white'
    )
    return fig

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)