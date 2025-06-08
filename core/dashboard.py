from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from components import sidebar, context
from graphs import graph

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

container_style = {
    "background-color": "white",
    "color": "black",
}

#Website builder
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store'),  # Lưu trữ data session nếu cần

    html.Div([
        # Sidebar
        html.Div([
            sidebar.create_sidebar()
        ], className="col-2"),

        # Main content
        html.Div([
            html.Div(id='page-content')
        ], className="col-10")

    ], className="row")
], className="container-fluid", style=container_style)

# Register callbacks từ context
context.register_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)