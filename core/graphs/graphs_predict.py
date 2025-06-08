import dash
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback

def get_last_7_days_weather(csv_file_path, station_name=None):
    """
    Lấy dữ liệu thời tiết 7 ngày cuối cùng
    """
    try:
        # Đọc CSV
        df = pd.read_csv(csv_file_path)

        # Lọc theo trạm nếu có
        if station_name:
            df = df[df['NAME'] == station_name]


        # Sắp xếp theo YMD và lấy 7 ngày cuối
        last_7_days = df.tail(7)
        print(last_7_days)

        # Chọn các cột cần thiết
        weather_data = last_7_days[['YMD', 'NAME', 'YEAR', 'MONTH', 'DAY', 'TMP_2', 'AT mean', 'AT max']].copy()

        # Tạo thêm cột ngày trong tuần
        weather_data['DATE'] = pd.to_datetime(weather_data['YMD'])
        weather_data['WEEKDAY'] = weather_data['DATE'].dt.strftime('%A')  # Monday, Tuesday, etc.
        weather_data['DATE_STR'] = weather_data['DATE'].dt.strftime('%d/%m')  # 25/12

        print(f"Lấy được {len(weather_data)} ngày cho trạm {station_name}")
        return weather_data.to_dict('records')  # Trả về list of dictionaries

    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu: {e}")
        return []


def get_weather_icon(tmp_2, at_max):
    """
    Chọn icon thời tiết dựa trên nhiệt độ
    """
    if at_max >= 35:
        return "🌡️"  # Rất nóng
    elif tmp_2 >= 30:
        return "☀️"  # Nắng
    elif tmp_2 >= 25:
        return "⛅"  # Ít mây
    elif tmp_2 >= 20:
        return "☁️"  # Có mây
    else:
        return "🌨️"  # Lạnh

def create_weather_card(day_data, is_today=False):
    """
    Tạo một thẻ card cho một ngày
    """
    card_style = {
        'border': '2px solid #007bff' if is_today else '1px solid #ddd',
        'borderRadius': '10px',
        'padding': '15px',
        'margin': '5px',
        'backgroundColor': '#f8f9fa' if is_today else 'white',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
        'textAlign': 'center',
        'fontFamily': 'Times New Roman'
    }

    return html.Div([
        # Ngày và thứ
        html.H5(
            f"{day_data['WEEKDAY'][:3]}" if not is_today else "Hôm nay",
            style={'margin': '0', 'color': '#007bff' if is_today else '#333', 'fontSize': '14px'}
        ),
        html.P(
            day_data['DATE_STR'],
            style={'margin': '5px 0', 'fontSize': '12px', 'color': '#666'}
        ),

        # Icon thời tiết
        html.Div(
            get_weather_icon(day_data['TMP_2'], day_data['AT max']),
            style={'fontSize': '30px', 'margin': '10px 0'}
        ),

        # Nhiệt độ
        html.Div([
            html.Span(f"{day_data['AT max']:.0f}°",
                      style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#ff6b6b'}),
            html.Span(" / ", style={'margin': '0 3px', 'color': '#999'}),
            html.Span(f"{day_data['TMP_2']:.0f}°",
                      style={'fontSize': '14px', 'color': '#4ecdc4'})
        ], style={'margin': '10px 0'}),

        # Cảm nhận
        html.P(
            f"Cảm nhận: {day_data['AT mean']:.0f}°C",
            style={'margin': '5px 0', 'fontSize': '11px', 'color': '#888'}
        )
    ], style=card_style)


def create_7_day_forecast(csv_file_path, selected_station):
    """
    Tạo component dự báo 7 ngày
    """
    try:
        # Lấy dữ liệu 7 ngày
        weather_data = get_last_7_days_weather(csv_file_path, selected_station)

        if not weather_data:
            return html.Div("Không có dữ liệu thời tiết", style={'textAlign': 'center'})

        # Tạo cards cho 7 ngày
        cards = []
        for i, day_data in enumerate(weather_data):
            is_today = (i == len(weather_data) - 1)  # Ngày cuối cùng là "hôm nay"
            cards.append(create_weather_card(day_data, is_today))

        return html.Div([
            html.H3(
                f"Dự báo thời tiết 7 ngày - {selected_station}",
                style={
                    'textAlign': 'center',
                    'fontFamily': 'Times New Roman',
                    'marginBottom': '20px',
                    'color': '#333'
                }
            ),
            html.Div(
                cards,
                style={
                    'display': 'flex',
                    'flexWrap': 'wrap',
                    'justifyContent': 'center',
                    'gap': '10px'
                }
            )
        ])

    except Exception as e:
        return html.Div(f"Lỗi: {str(e)}", style={'color': 'red', 'textAlign': 'center'})

def create_enhanced_weather_card(day_data, is_today=False):
    """
    Version nâng cao với gradient và animation
    """
    gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if is_today else "white"
    text_color = "white" if is_today else "#333"

    return html.Div([
        # Content tương tự nhưng với style đẹp hơn
    ], style={
        'background': gradient,
        'color': text_color,
        'borderRadius': '15px',
        'padding': '20px',
        'margin': '10px',
        'boxShadow': '0 8px 25px rgba(0,0,0,0.15)',
        'transition': 'transform 0.3s ease',
        'cursor': 'pointer',
        'minWidth': '120px'
    })