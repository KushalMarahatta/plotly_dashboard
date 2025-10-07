from dash import Dash, html, dcc, Input, Output
import plotly.express as px

#Initialize app and data
app = Dash(__name__)
server = app.server
df = px.data.gapminder()
years = sorted(df["year"].unique())
continents = sorted(df["continent"].unique())

#Layout
app.layout = html.Div([
    html.H2("Update Multiple Graphs at Once"),

    # Controls
    html.Div([
        html.Div([
            html.Label("Select Continent"),
            dcc.Dropdown(
                id="continent",
                options=[{"label": c, "value": c} for c in continents],
                value="Asia",
                clearable=False
            )
        ], style={"width": "250px", "marginRight": "10px"}),

        html.Div([
            html.Label("Select Year"),
            dcc.Dropdown(
                id="year",
                options=[{"label": int(y), "value": int(y)} for y in years],
                value=2007,
                clearable=False
            )
        ], style={"width": "150px"})
    ], style={"display": "flex", "flexWrap": "wrap"}),

    # Graphs (side-by-side)
    html.Div([
        dcc.Graph(id="scatter", style={"flex": "1", "height": "550px"}),
        dcc.Graph(id="hist", style={"flex": "1", "height": "550px"})
    ], style={"display": "flex", "gap": "16px", "marginTop": "20px"})
])

# --- Callback (multi-output)
@app.callback(
    [Output("scatter", "figure"), Output("hist", "figure")],
    [Input("continent", "value"), Input("year", "value")]
)
def update_all(continent, year):
    # Filter data
    dfx = df[(df["continent"] == continent) & (df["year"] == year)]

    # Scatter plot: GDP vs Life Expectancy
    fig1 = px.scatter(
        dfx, x="gdpPercap", y="lifeExp",
        size="pop", color="country", hover_name="country",
        log_x=True, title=f"Life Expectancy vs GDP per Capita ({continent}, {year})",
        template="plotly_white"
    )

    # Histogram: distribution of Life Expectancy
    fig2 = px.histogram(
        dfx, x="lifeExp", nbins=20,
        title=f"Distribution of Life Expectancy ({continent}, {year})",
        template="plotly_white"
    )

    # Adjust layout for spacing
    fig1.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    fig2.update_layout(margin=dict(l=20, r=20, t=50, b=20))

    # Return both figures
    return fig1, fig2

# Run
if __name__ == "__main__":
    app.run(debug=True)