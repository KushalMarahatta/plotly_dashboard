from dash import Dash, html, dcc
import plotly.express as px

#Create the app
app = Dash(__name__)
server=app.server

#Load data
df = px.data.gapminder().query("year==2007")

#Create the map
fig = px.choropleth(
    df,
    locations='iso_alpha',          # country codes
    color='lifeExp',                # color by life expectancy
    hover_name='country',
    color_continuous_scale='Viridis',
    title='Life Expectancy by Country (2007)'
)

#Layout — show map in Dash
app.layout = html.Div([
    html.H2("Geospatial Dashboard Example"),
    dcc.Graph(figure=fig, style={"height": "700px"})
])

#Run
if __name__ == '__main__':
    app.run(debug=True)