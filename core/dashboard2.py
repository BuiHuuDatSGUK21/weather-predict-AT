import random
from datetime import datetime, timedelta

import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Input, Output

# Khởi tạo ứng dụng Dash
app = dash.Dash(__name__)
app.title = "WeatherAI - Hệ thống Dự báo Thời tiết"

# Dữ liệu mô hình
weather_models = {
    'neural-network': {
        'name': 'Mạng Neural Nhân Tạo',
        'accuracy': 89.5,
        'description': 'Sử dụng deep learning để phân tích pattern thời tiết phức tạp',
        'features': ['Học sâu từ dữ liệu lịch sử', 'Xử lý dữ liệu phi tuyến tính', 'Độ chính xác cao'],
        'status': 'Hoạt động',
        'color': '#3B82F6'
    },
    'ensemble': {
        'name': 'Mô Hình Tổng Hợp',
        'accuracy': 92.1,
        'description': 'Kết hợp nhiều mô hình để đưa ra dự báo chính xác nhất',
        'features': ['Tổng hợp từ 5+ mô hình', 'Giảm thiểu sai số', 'Ổn định cao'],
        'status': 'Hoạt động',
        'color': '#10B981'
    },
    'statistical': {
        'name': 'Mô Hình Thống Kê',
        'accuracy': 85.3,
        'description': 'Dựa trên phân tích thống kê và xu hướng lịch sử',
        'features': ['Phân tích xu hướng', 'Mô hình ARIMA', 'Xử lý nhanh'],
        'status': 'Hoạt động',
        'color': '#8B5CF6'
    },
    'machine-learning': {
        'name': 'Học Máy Cổ Điển',
        'accuracy': 87.8,
        'description': 'Sử dụng các thuật toán Random Forest và SVM',
        'features': ['Random Forest', 'Support Vector Machine', 'Feature Engineering'],
        'status': 'Bảo trì',
        'color': '#F59E0B'
    }
}

# CSS tùy chỉnh
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Layout chính
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.Div([
                html.H1("🌤️ WeatherAI",
                        style={'color': '#1F2937', 'margin': '0', 'fontSize': '2rem', 'fontWeight': 'bold'}),
                html.P("Hệ thống dự báo thời tiết thông minh",
                       style={'color': '#6B7280', 'margin': '5px 0 0 0', 'fontSize': '0.9rem'})
            ], style={'flex': '1'}),

            html.Div([
                html.P(datetime.now().strftime("%A, %d/%m/%Y"),
                       style={'color': '#6B7280', 'margin': '0', 'fontSize': '0.9rem', 'textAlign': 'right'})
            ])
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'padding': '20px 0'
        })
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'color': 'white',
        'padding': '0 30px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }),

    # Navigation Tabs
    html.Div([
        dcc.Tabs(id="main-tabs", value='forecast', children=[
            dcc.Tab(label='🌡️ Dự Báo Thời Tiết', value='forecast',
                    style={'padding': '12px 24px', 'fontWeight': 'bold'},
                    selected_style={'backgroundColor': '#3B82F6', 'color': 'white', 'padding': '12px 24px',
                                    'fontWeight': 'bold'}),
            dcc.Tab(label='⚙️ Quản Lý Mô Hình', value='models',
                    style={'padding': '12px 24px', 'fontWeight': 'bold'},
                    selected_style={'backgroundColor': '#3B82F6', 'color': 'white', 'padding': '12px 24px',
                                    'fontWeight': 'bold'})
        ], style={'marginBottom': '20px'})
    ], style={'padding': '20px 30px 0 30px', 'backgroundColor': '#F9FAFB'}),

    # Nội dung chính
    html.Div(id='tab-content', style={'padding': '0 30px 30px 30px', 'backgroundColor': '#F9FAFB', 'minHeight': '80vh'})
])


# Callback cho tab navigation
@app.callback(Output('tab-content', 'children'),
              Input('main-tabs', 'value'))
def render_tab_content(active_tab):
    if active_tab == 'forecast':
        return forecast_layout()
    elif active_tab == 'models':
        return models_layout()


def forecast_layout():
    return html.Div([
        # Header section
        html.Div([
            html.H2("🌤️ Dự Báo Thời Tiết", style={'color': '#1F2937', 'marginBottom': '10px'}),
            html.P("Dự báo chính xác với công nghệ AI tiên tiến", style={'color': '#6B7280'})
        ], style={
            'background': 'linear-gradient(135deg, #3B82F6, #1D4ED8)',
            'color': 'white',
            'padding': '30px',
            'borderRadius': '12px',
            'marginBottom': '20px'
        }),

        # Controls
        html.Div([
            html.Div([
                html.Label("⚙️ Chọn Mô Hình Dự Báo:",
                           style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.Dropdown(
                    id='model-selector',
                    options=[
                        {'label': f"{model['name']} (Độ chính xác: {model['accuracy']}%)", 'value': key}
                        for key, model in weather_models.items() if model['status'] == 'Hoạt động'
                    ],
                    value='neural-network',
                    style={'marginBottom': '20px'}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.Label("📅 Chọn Ngày Dự Báo:",
                           style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.DatePickerSingle(
                    id='date-picker',
                    date=datetime.now().date(),
                    display_format='DD/MM/YYYY',
                    style={'marginBottom': '20px'}
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'backgroundColor': 'white',
            'padding': '25px',
            'borderRadius': '12px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
            'marginBottom': '20px'
        }),

        # Kết quả dự báo
        html.Div(id='forecast-results')
    ])


def models_layout():
    return html.Div([
        # Header section
        html.Div([
            html.H2("⚙️ Quản Lý Mô Hình Dự Báo", style={'color': '#1F2937', 'marginBottom': '10px'}),
            html.P("Quản lý và theo dõi hiệu suất các mô hình AI dự báo thời tiết", style={'color': '#6B7280'})
        ], style={
            'background': 'linear-gradient(135deg, #8B5CF6, #7C3AED)',
            'color': 'white',
            'padding': '30px',
            'borderRadius': '12px',
            'marginBottom': '20px'
        }),

        # Model cards
        html.Div([
            html.Div([
                create_model_card(key, model) for key, model in weather_models.items()
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))',
                'gap': '20px'
            })
        ])
    ])


def create_model_card(model_id, model_data):
    status_color = '#10B981' if model_data['status'] == 'Hoạt động' else '#F59E0B'

    return html.Div([
        # Header với icon và tên
        html.Div([
            html.Div([
                html.H3(model_data['name'], style={'margin': '0', 'color': '#1F2937', 'fontSize': '1.2rem'}),
                html.Span(model_data['status'], style={
                    'backgroundColor': status_color,
                    'color': 'white',
                    'padding': '4px 12px',
                    'borderRadius': '20px',
                    'fontSize': '0.8rem',
                    'fontWeight': 'bold'
                })
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                      'marginBottom': '15px'}),

            html.Div([
                html.Span(f"{model_data['accuracy']}%", style={
                    'fontSize': '2rem',
                    'fontWeight': 'bold',
                    'color': model_data['color']
                }),
                html.Div("Độ chính xác", style={'fontSize': '0.9rem', 'color': '#6B7280'})
            ], style={'textAlign': 'right'})
        ]),

        # Mô tả
        html.P(model_data['description'], style={'color': '#6B7280', 'marginBottom': '15px'}),

        # Tính năng
        html.Div([
            html.H4("Tính năng chính:", style={'fontSize': '1rem', 'marginBottom': '10px', 'color': '#1F2937'}),
            html.Ul([
                html.Li(feature, style={'marginBottom': '5px', 'color': '#6B7280'})
                for feature in model_data['features']
            ])
        ]),

        # Footer
        html.Hr(style={'margin': '15px 0', 'border': 'none', 'borderTop': '1px solid #E5E7EB'}),
        html.Div([
            html.Span("Cập nhật lần cuối:", style={'color': '#6B7280', 'fontSize': '0.9rem'}),
            html.Span("2 giờ trước",
                      style={'color': '#1F2937', 'fontSize': '0.9rem', 'fontWeight': 'bold', 'float': 'right'})
        ])

    ], style={
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'border': f'2px solid {model_data["color"]}',
        'transition': 'transform 0.2s',
    })


# Callback cho kết quả dự báo
@app.callback(
    Output('forecast-results', 'children'),
    [Input('model-selector', 'value'),
     Input('date-picker', 'date')]
)
def update_forecast(selected_model, selected_date):
    if not selected_model or not selected_date:
        return html.Div("Vui lòng chọn mô hình và ngày để xem dự báo.")

    # Tạo dữ liệu dự báo mẫu
    forecast_data = generate_forecast_data(selected_model, selected_date)
    model_info = weather_models[selected_model]

    return html.Div([
        # Main forecast card
        html.Div([
            html.Div([
                # Left side - Main weather info
                html.Div([
                    html.H3(f"Dự Báo Cho {datetime.strptime(selected_date, '%Y-%m-%d').strftime('%d/%m/%Y')}",
                            style={'marginBottom': '5px', 'color': '#1F2937'}),
                    html.P(f"Mô hình: {model_info['name']}", style={'color': '#6B7280', 'fontSize': '0.9rem'}),

                    # Weather icon and temperature
                    html.Div([
                        html.Div([
                            html.Span(get_weather_icon(forecast_data['condition']),
                                      style={'fontSize': '4rem', 'marginBottom': '10px', 'display': 'block'}),
                            html.Span(f"{forecast_data['temperature']}°C",
                                      style={'fontSize': '3rem', 'fontWeight': 'bold', 'color': '#1F2937'}),
                            html.Div(get_condition_text(forecast_data['condition']),
                                     style={'fontSize': '1.2rem', 'color': '#6B7280', 'marginTop': '10px'})
                        ], style={'textAlign': 'center'})
                    ], style={
                        'background': 'linear-gradient(135deg, #EBF4FF, #E0E7FF)',
                        'padding': '30px',
                        'borderRadius': '12px',
                        'margin': '20px 0'
                    })
                ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                # Right side - Model info and confidence
                html.Div([
                    html.Div([
                        html.H4("📊 Thông Tin Mô Hình", style={'marginBottom': '15px', 'color': '#1F2937'}),
                        html.P(f"Độ chính xác: {model_info['accuracy']}%", style={'marginBottom': '8px'}),
                        html.P(f"Trạng thái: {model_info['status']}", style={'marginBottom': '8px'}),
                        html.Div([
                            html.Span("Độ tin cậy: ", style={'color': '#6B7280'}),
                            html.Span(f"{forecast_data['confidence']}%",
                                      style={'fontSize': '1.5rem', 'fontWeight': 'bold', 'color': '#10B981'})
                        ])
                    ], style={
                        'backgroundColor': '#F9FAFB',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'marginBottom': '20px'
                    }),

                    # 7-day trend
                    html.Div([
                        html.H4("📈 Xu Hướng 7 Ngày", style={'marginBottom': '15px', 'color': '#1F2937'}),
                        create_7day_trend()
                    ], style={
                        'backgroundColor': '#F9FAFB',
                        'padding': '20px',
                        'borderRadius': '8px'
                    })
                ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
            ]),

            # Weather details grid
            html.Div([
                create_weather_detail("💧", "Độ ẩm", f"{forecast_data['humidity']}%", "#3B82F6"),
                create_weather_detail("💨", "Gió", f"{forecast_data['wind_speed']} km/h", "#10B981"),
                create_weather_detail("🌧️", "Mưa", f"{forecast_data['precipitation']}%", "#8B5CF6"),
                create_weather_detail("👁️", "Tầm nhìn", f"{forecast_data['visibility']} km", "#F59E0B")
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
                'gap': '15px',
                'marginTop': '20px',
                'clear': 'both'
            }),

            # Chart
            html.Div([
                dcc.Graph(figure=create_forecast_chart(selected_model, selected_date))
            ], style={'marginTop': '20px'})

        ], style={
            'backgroundColor': 'white',
            'padding': '30px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
        })
    ])


def generate_forecast_data(model, date):
    """Tạo dữ liệu dự báo mẫu"""
    base_temp = 25 + np.sin(pd.to_datetime(date).dayofyear / 365 * 2 * np.pi) * 8
    accuracy = weather_models[model]['accuracy']

    return {
        'temperature': int(base_temp + random.uniform(-4, 4)),
        'humidity': int(60 + random.uniform(0, 30)),
        'wind_speed': int(5 + random.uniform(0, 15)),
        'precipitation': int(random.uniform(0, 80)),
        'visibility': int(8 + random.uniform(0, 7)),
        'condition': random.choice(['sunny', 'cloudy', 'rainy', 'partly-cloudy']),
        'confidence': int(accuracy + random.uniform(-10, 10))
    }


def get_weather_icon(condition):
    icons = {
        'sunny': '☀️',
        'cloudy': '☁️',
        'rainy': '🌧️',
        'partly-cloudy': '⛅'
    }
    return icons.get(condition, '☀️')


def get_condition_text(condition):
    conditions = {
        'sunny': 'Nắng',
        'cloudy': 'Nhiều mây',
        'rainy': 'Mưa',
        'partly-cloudy': 'Ít mây'
    }
    return conditions.get(condition, 'Nắng')


def create_weather_detail(icon, label, value, color):
    return html.Div([
        html.Div(icon, style={'fontSize': '1.5rem', 'marginBottom': '8px'}),
        html.Div(label, style={'fontSize': '0.9rem', 'color': '#6B7280', 'marginBottom': '5px'}),
        html.Div(value, style={'fontSize': '1.2rem', 'fontWeight': 'bold', 'color': color})
    ], style={
        'backgroundColor': '#F9FAFB',
        'padding': '20px',
        'borderRadius': '8px',
        'textAlign': 'center',
        'border': f'2px solid {color}20'
    })


def create_7day_trend():
    trend_items = []
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        temp = 25 + np.sin(i * 0.5) * 5 + random.uniform(-3, 3)
        trend_items.append(
            html.Div([
                html.Span(date.strftime("%a %d"), style={'color': '#6B7280', 'fontSize': '0.8rem'}),
                html.Div([
                    html.Span("☀️", style={'marginRight': '5px'}),
                    html.Span(f"{int(temp)}°C", style={'fontWeight': 'bold'})
                ])
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'marginBottom': '8px',
                'padding': '5px 0'
            })
        )
    return html.Div(trend_items)


def create_forecast_chart(model, date):
    """Tạo biểu đồ dự báo nhiệt độ 24 giờ"""
    hours = [f"{i:02d}:00" for i in range(24)]
    base_temp = 25 + np.sin(pd.to_datetime(date).dayofyear / 365 * 2 * np.pi) * 8
    temperatures = [base_temp + 5 * np.sin(i * np.pi / 12) + random.uniform(-2, 2) for i in range(24)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=temperatures,
        mode='lines+markers',
        name='Nhiệt độ dự báo',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=6),
        hovertemplate='<b>%{x}</b><br>Nhiệt độ: %{y:.1f}°C<extra></extra>'
    ))

    fig.update_layout(
        title=f'Dự Báo Nhiệt Độ 24 Giờ - {weather_models[model]["name"]}',
        xaxis_title='Giờ',
        yaxis_title='Nhiệt độ (°C)',
        hovermode='x unified',
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

    return fig


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)