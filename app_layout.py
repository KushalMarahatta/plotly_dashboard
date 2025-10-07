from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
server=app.server
df = px.data.gapminder()

app.layout = html.Div([
    html.H2("Life Expectancy Dashboard"),

    # Flex row
    html.Div([
        # Left panel: controls
        html.Div([
            html.H4("Controls"),
            html.Label("Select Year:"),
            dcc.Dropdown(
                id='year', value=2007,
                options=[{'label': int(y), 'value': int(y)} for y in sorted(df['year'].unique())]
            )
        ], style={
            'flex': '30%',
            'border': '1px solid #ccc',
            'padding': '10px',
            'boxSizing': 'border-box'
        }),

        # Right panel: graph
        html.Div([
            html.H4("Visualization"),
            dcc.Graph(
                id='fig',
                style={
                    # IMPORTANT: fix height to prevent infinite resize loop
                    'height': '600px',
                    # Let the flex item actually shrink; prevents overflow loops
                    'width': '100%',
                    'boxSizing': 'border-box'
                },
                config={'responsive': True}
            )
        ], style={
            'flex': '70%',
            'minWidth': 0,             # <-- CRITICAL in flex layouts
            'border': '1px solid #ccc',
            'padding': '10px',
            'boxSizing': 'border-box'
        })

    ], style={
        'display': 'flex',
        'gap': '16px',
        'marginTop': '10px',
        'alignItems': 'stretch'  # stretch heights evenly
    })
])

@app.callback(Output('fig', 'figure'), Input('year', 'value'))
def update(year):
    dfx = df[df['year'] == year]
    fig = px.scatter(
        dfx,
        x='gdpPercap', y='lifeExp',
        color='continent', size='pop',
        hover_name='country', log_x=True,
        title=f'Year: {year}'
    )
    # Tighten margins so the figure doesn't push container
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=30))
    return fig

if __name__ == '__main__':
    app.run(debug=True)