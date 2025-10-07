from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the app
app = Dash(__name__)
server=app.server
df = px.data.gapminder()

# 💡 Reusable KPI component
kpi = lambda title, value: html.Div([
    html.Div(title, style={'fontSize': '12px', 'color': '#666'}),
    html.Div(value, style={'fontSize': '28px', 'fontWeight': '600'})
], style={
    'padding': '12px',
    'border': '1px solid #eee',
    'borderRadius': '10px',
    'backgroundColor': '#f9f9f9',
    'textAlign': 'center',
    'flex': '1'
})

# App layout
app.layout = html.Div([
    html.H2("🌍 Life Expectancy Dashboard"),

    # KPI row
    html.Div(id='kpis', style={
        'display': 'flex',
        'gap': '12px',
        'marginBottom': '20px',
        'justifyContent': 'space-between'
    }),

    # Dropdown and Graph section
    html.Div([
        html.Div([
            html.H4("Select Year:"),
            dcc.Dropdown(
                id='year',
                value=2007,
                options=[{'label': int(y), 'value': int(y)} for y in sorted(df['year'].unique())]
            )
        ], style={'flex': '25%', 'border': '1px solid #ccc', 'padding': '10px'}),

        html.Div([
            html.H4("Visualization"),
            dcc.Graph(id='fig', style={'height': '600px'})
        ], style={'flex': '75%', 'border': '1px solid #ccc', 'padding': '10px', 'minWidth': 0})

    ], style={'display': 'flex', 'gap': '16px', 'marginTop': '10px'})
])

# Callback to update both KPIs and scatter plot
@app.callback(
    [Output('kpis', 'children'),
     Output('fig', 'figure')],
    Input('year', 'value')
)
def update_dashboard(year):
    dfx = df[df['year'] == year]

    # --- KPI values ---
    num_countries = dfx['country'].nunique()
    avg_life = dfx['lifeExp'].mean()
    avg_gdp = dfx['gdpPercap'].mean()
    total_pop = dfx['pop'].sum() / 1_000_000_000  # in billions

    kpi_cards = [
        kpi("Number of Countries", f"{num_countries}"),
        kpi("Average Life Expectancy", f"{avg_life:.1f}"),
        kpi("Average GDP per Capita", f"${avg_gdp:,.0f}"),
        kpi("Total Population (B)", f"{total_pop:.2f}")
    ]

    # --- Scatter Plot ---
    fig = px.scatter(
        dfx,
        x='gdpPercap',
        y='lifeExp',
        color='continent',
        size='pop',
        hover_name='country',
        log_x=True,
        title=f"Life Expectancy vs GDP per Capita — {year}"
    )
    fig.update_layout(margin=dict(l=30, r=30, t=50, b=30))

    return kpi_cards, fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)