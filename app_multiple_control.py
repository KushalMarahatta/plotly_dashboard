from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ----- App & data
app = Dash(__name__)
server=app.server

df = px.data.gapminder()
years = sorted(df["year"].unique())
continents = sorted(df["continent"].unique())

# ----- Layout
app.layout = html.Div([
    html.H3("Multi-Input → One Figure"),
    html.Div([
        html.Div([
            html.Label("Continent"),
            dcc.Dropdown(
                id="continent",
                options=[{"label": c, "value": c} for c in continents],
                value=continents[0],  # default
                clearable=False
            )
        ], style={"width": "300px", "marginRight": "12px"}),

        html.Div([
            html.Label("Year"),
            dcc.Dropdown(
                id="year",
                options=[{"label": int(y), "value": int(y)} for y in years],
                value=2007,
                clearable=False
            )
        ], style={"width": "200px"})
    ], style={"display": "flex", "flexWrap": "wrap"}),

    dcc.Graph(id="scatter", style={"height": "560px"})
])

# ----- Callback: multi-input -> one figure
@app.callback(
    Output("scatter", "figure"),
    [Input("continent", "value"), Input("year", "value")]
)
def update(continent, year):
    dfx = df[(df["continent"] == continent) & (df["year"] == year)]
    fig = px.scatter(
        dfx, x="gdpPercap", y="lifeExp",
        size="pop", color="country", hover_name="country",
        log_x=True, title=f"{continent} — {year}",
        template="plotly_white"
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

# ----- Run
if __name__ == "__main__":
    app.run(debug=True)