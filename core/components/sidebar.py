import dash
from dash import html, dcc, Input, Output, callback
from core.components import context
import dash_bootstrap_components as dbc
from dash import page_registry, page_container

sidebar_style = {
    "background-color": "white",
    "padding": "20px",
    "height": "100vh",
    'border-right': '2px solid #dee2e6',
    "position": "sticky",
    "top": "0"
}


def create_sidebar():
    """Tạo component sidebar"""
    return html.Div([
        # Header thông tin sinh viên
        html.Div([
            html.H5("Thông tin nhóm", className="text-center mb-3"),
            html.Hr(),
            html.P("Huỳnh Thị Tuyết Ngọc", className="mb-1"),
            html.Small("3121411147", className="text-muted d-block mb-2"),
            html.P("Bùi Hữu Đạt", className="mb-1"),
            html.Small("3121411048", className="text-muted d-block"),
        ], className="text-center py-3"),

        html.Hr(),

        # Navigation menu
        html.Div([
            dbc.Nav([
                dbc.NavItem(
                    dbc.NavLink(
                        [html.I(className="fas fa-chart-line me-2"), "Dashboard"],
                        href="/",
                        active="exact",
                        id="nav-dashboard",
                        className="mb-2",
                        style={
                            'whiteSpace': 'normal',  # ⭐ Cho phép wrap
                            'wordWrap': 'break-word',  # ⭐ Break từ dài
                            'fontSize': '14px',
                            'padding': '8px 12px',
                            'borderRadius': '6px'
                        }
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        [html.I(className="fas fa-crystal-ball me-2"), "Dự đoán"],
                        href="/predict",
                        active="exact",
                        id="nav-predict",
                        className="mb-2",
                        style={
                            'whiteSpace': 'normal',  # ⭐ Cho phép wrap
                            'wordWrap': 'break-word',  # ⭐ Break từ dài
                            'fontSize': '14px',
                            'padding': '8px 12px',
                            'borderRadius': '6px'
                        }
                    )
                ),

            ], vertical=True, pills=True)
        ])
    ], style=sidebar_style, className="")


def get_active_nav():
    """Hàm helper để xác định nav nào đang active"""
    return {
        '/': 'nav-dashboard',
        '/predict': 'nav-predict',
        '/settings': 'nav-settings'
    }