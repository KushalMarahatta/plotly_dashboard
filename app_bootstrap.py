from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server=app.server

df = px.data.gapminder()

def kpi(title, value):
    return dbc.Card(
        dbc.CardBody([
            html.Small(title, className="text-muted"),
            html.H3(value, className="mb-0")
        ]),
        className="shadow-sm"
    )

app.layout = dbc.Container(fluid=True, children=[

    dbc.Row([dbc.Col(html.H2(" LIFE EXPECTANCY DASHBOARD WITH BOOTSTRAP"))], className="my-3"),

    dbc.Row([
        dbc.Col(id="kpi-countries", md=3, xs=6, className="mb-3"),
        dbc.Col(id="kpi-lifeexp",   md=3, xs=6, className="mb-3"),
        dbc.Col(id="kpi-gdp",       md=3, xs=6, className="mb-3"),
        dbc.Col(id="kpi-pop",       md=3, xs=6, className="mb-3"),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filters"),
                dbc.CardBody([
                    dbc.Label("Select Year"),
                    dcc.Dropdown(
                        id="year",
                        value=2007,
                        options=[{"label": int(y), "value": int(y)} for y in sorted(df["year"].unique())],
                        clearable=False
                    )
                ])
            ], className="shadow-sm")
        ], md=3, xs=12, className="mb-3"),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Life Expectancy vs GDP per Capita"),
                dbc.CardBody([
                    dcc.Graph(id="fig", style={"height": "560px", "width": "100%"})
                ])
            ], className="shadow-sm h-100")
        ], md=9, xs=12, className="mb-3"),
    ], align="stretch", className="g-3")
])

@app.callback(
    [Output("kpi-countries", "children"),
     Output("kpi-lifeexp",   "children"),
     Output("kpi-gdp",       "children"),
     Output("kpi-pop",       "children"),
     Output("fig", "figure")],
    Input("year", "value")
)
def update(year):
    dfx = df[df["year"] == year]

    k1 = kpi("Countries",              f"{dfx['country'].nunique()}")
    k2 = kpi("Avg Life Expectancy",    f"{dfx['lifeExp'].mean():.1f}")
    k3 = kpi("Avg GDP per Capita",     f"${dfx['gdpPercap'].mean():,.0f}")
    k4 = kpi("Total Population (B)",   f"{dfx['pop'].sum()/1_000_000_000:.2f}")

    fig = px.scatter(
        dfx, x="gdpPercap", y="lifeExp",
        color="continent", size="pop", hover_name="country",
        log_x=True, template="plotly_white", title=f"Year: {year}"
    )
    fig.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return k1, k2, k3, k4, fig

if __name__ == "__main__":
    app.run(debug=True)
