from dash import Dash, dcc, html, Input, Output
import plotly.express as px


app = Dash(__name__)
server =app.server


df = px.data.gapminder()


app.layout = html.Div([
    html.H3('Life Expectancy by Continent'),
    dcc.Dropdown(
        id='year', value=2007,
        options=[{'label': int(y), 'value': int(y)} for y in sorted(df['year'].unique())]
    ),
    dcc.Graph(id='fig')
])


@app.callback(Output('fig', 'figure'), Input('year', 'value'))
def update(year):
    dfx = df[df['year'] == year]
    fig = px.scatter(dfx, x='gdpPercap', y='lifeExp', color='continent', size='pop',hover_name='country', log_x=True, title=f'Year: {year}')
    return fig


if __name__ == '__main__':
    app.run(debug=True)