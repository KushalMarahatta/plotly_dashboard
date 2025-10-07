from dash import Dash, html, dcc, Input, Output
import plotly.express as px

app = Dash(__name__)
server=app.server
df = px.data.gapminder()

app.layout = html.Div([
    html.H2("Tabs Demo — One Page, Multiple Views"),

    dcc.Tabs(
        id="tabs",
        value="tab-1",  # default selected tab
        children=[
            dcc.Tab(label="Overview", value="tab-1"),
            dcc.Tab(label="Details",  value="tab-2"),
        ],
        persistence=True  # remembers selection on refresh
    ),

    html.Div(id="tab-content", style={"marginTop": "16px"})
])

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "tab-1":
        # Overview: single year, colored by continent
        dfx = df[df["year"] == 2007]
        fig = px.scatter(
            dfx, x="gdpPercap", y="lifeExp",
            size="pop", color="continent", hover_name="country",
            log_x=True, title="Overview — GDP vs Life Expectancy (2007)",
            template="plotly_white"
        )
        fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
        return dcc.Graph(figure=fig, style={"height": "560px"})

    # Details: histogram for the most recent selected year (example uses 2007)
    dfx = df[df["year"] == 2007]
    fig = px.histogram(
        dfx, x="lifeExp", nbins=20, color="continent",
        title="Details — Life Expectancy Distribution (2007)",
        template="plotly_white"
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return dcc.Graph(figure=fig, style={"height": "560px"})

if __name__ == "__main__":
    app.run(debug=True)