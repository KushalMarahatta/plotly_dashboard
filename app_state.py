from dash import Dash, html, dcc, Input, Output, State
import dash

app = Dash(__name__)
server=app.server

app.layout = html.Div([
    html.H4("State Example: Apply Threshold"),

    # Numeric input
    dcc.Input(
        id='threshold',
        type='number',
        placeholder='Enter threshold...',
        value=10
    ),

    # Button (user must click it)
    html.Button('Apply', id='apply-btn', n_clicks=0),

    # Output text
    html.Div(id='out', style={'marginTop': '20px'})
])

@app.callback(
    Output('out', 'children'),
    Input('apply-btn', 'n_clicks'),
    State('threshold', 'value')
)
def apply(_, threshold):
    # Run only when the button is clicked
    if not _:
        raise dash.exceptions.PreventUpdate
    return f'✅ Applied threshold = {threshold}'

if __name__ == '__main__':
    app.run(debug=True)