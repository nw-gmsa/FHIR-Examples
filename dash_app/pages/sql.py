import dash
from dash import html

dash.register_page(__name__, path="/sql")

print("Me")
layout = html.Div([
    html.H1('This is our SQL Reports page'),
    html.Div('This is our SQL based Reports page content.'),
])