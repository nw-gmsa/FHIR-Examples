
import dash
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc


# Initialize the Dash app (no longer need JupyterDash)
app = Dash(use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
    html.H4('Container should be above'),
])


if __name__ == '__main__':
    # Use app.run with jupyter_mode instead of JupyterDash's run_server
    app.run( port=8052)
