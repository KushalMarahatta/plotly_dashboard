from dash import Dash, html, dcc
import plotly.express as px
import plotly.io as pio

import os, plotly.express as px
token = os.getenv("MAPBOX_TOKEN")
if token:
    px.set_mapbox_access_token(token)

#Set token (only once)
pio.templates.default = "plotly"
px.set_mapbox_access_token("YOUR_MAPBOX_TOKEN_HERE")

#Sample data
df = px.data.carshare()

#Create map
fig = px.scatter_map(
    df,
    lat='centroid_lat',
    lon='centroid_lon',
    color='peak_hour',
    size='car_hours',
    zoom=10,
    map_style='carto-positron',
    title='Car Share Locations on Mapbox'
)

#Dash app layout
app = Dash(__name__)
server=app.server

app.layout = html.Div([
    html.H2("Mapbox Example in Dash"),
    dcc.Graph(figure=fig, style={"height": "700px"})
])

if __name__ == '__main__':
    app.run(debug=True)