import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback


def load_model_metrics(csv_file_path):
    """
    Đọc file CSV chứa metrics của các model

    Args:
        csv_file_path: Đường dẫn đến file CSV

    Returns:
        DataFrame: Dữ liệu metrics
    """
    try:
        df = pd.read_csv(csv_file_path)
        return df
    except Exception as e:
        print(f"Lỗi đọc file CSV: {e}")
        return None


def get_metrics_for_model_station(df, model_name, station_name):
    """
    Lấy metrics cho model và station cụ thể

    Args:
        df: DataFrame chứa dữ liệu
        model_name: Tên model
        station_name: Tên station

    Returns:
        dict: Metrics cho model và station đó
    """
    if df is None:
        return None

    # Filter data cho model và station cụ thể
    filtered_df = df[(df['Model'] == model_name) & (df['Station'] == station_name)]

    if filtered_df.empty:
        print(f"Không tìm thấy dữ liệu cho Model: {model_name}, Station: {station_name}")
        return None

    # Lấy row đầu tiên (giả sử mỗi model-station có 1 row)
    row = filtered_df.iloc[0]

    return {
        'mean': {
            'r2': row.get('R2 mean', 0),
            'mse': row.get('MSE mean', 0),
            'rmse': row.get('RMSE mean', 0),
            'mae': row.get('MAE mean', 0)
        },
        'max': {
            'r2': row.get('R2 max', 0),
            'mse': row.get('MSE max', 0),
            'rmse': row.get('RMSE max', 0),
            'mae': row.get('MAE max', 0)
        }
    }


def create_metric_card_item(value, label, color_class, border_class):
    """
    Tạo một item metric trong card
    """
    return dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{value:.3f}", className=f"{color_class} fw-bold mb-0"),
                html.P(label, className="text-muted small mb-0")
            ], className="text-center py-2")
        ], className=border_class)
    ], width=6)


def create_metrics_card(metrics_data, card_type="mean", card_title=None):
    """
    Tạo card hiển thị metrics (mean hoặc max)

    Args:
        metrics_data: Dict chứa metrics data
        card_type: "mean" hoặc "max"
        card_title: Tiêu đề card (optional)
    """
    if not metrics_data or card_type not in metrics_data:
        return create_empty_metrics_card(card_type)

    data = metrics_data[card_type]

    # Định nghĩa màu sắc và tiêu đề
    if card_type == "mean":
        header_color = "bg-success"
        default_title = "📊 Chỉ số đánh giá AT Mean"
    else:  # max
        header_color = "bg-info"
        default_title = "📊 Chỉ số đánh giá AT Max"

    title = card_title or default_title

    return dbc.Card([
        dbc.CardHeader([
            html.H5(title, className="mb-0 text-center")
        ], className=f"{header_color} text-white"),
        dbc.CardBody([
            dbc.Row([
                create_metric_card_item(data['r2'], "R² Score", "text-primary", "border-primary"),
                create_metric_card_item(data['mse'], "MSE", "text-info", "border-info"),
            ], className="mb-2"),
            dbc.Row([
                create_metric_card_item(data['mae'], "MAE", "text-warning", "border-warning"),
                create_metric_card_item(data['rmse'], "RMSE", "text-danger", "border-danger"),
            ])
        ], id=f"model-score-body-{card_type}")
    ], className="h-100")


def create_empty_metrics_card(card_type="mean"):
    """
    Tạo card rỗng khi không có dữ liệu
    """
    header_color = "bg-success" if card_type == "mean" else "bg-info"
    title = "📊 Chỉ số đánh giá AT Mean" if card_type == "mean" else "📊 Chỉ số đánh giá AT Max"

    return dbc.Card([
        dbc.CardHeader([
            html.H5(title, className="mb-0 text-center")
        ], className=f"{header_color} text-white"),
        dbc.CardBody([
            html.Div([
                html.H5("⚠️ Không có dữ liệu", className="text-muted text-center"),
                html.P("Vui lòng kiểm tra lại model và station", className="text-center small")
            ], className="py-4")
        ])
    ], className="h-100")


def create_dual_metrics_cards(csv_file_path, model_name, station_name):
    """
    Tạo 2 card metrics (mean và max) từ dữ liệu CSV

    Args:
        csv_file_path: Đường dẫn file CSV
        model_name: Tên model
        station_name: Tên station

    Returns:
        dbc.Row: Container chứa 2 cards
    """
    # Load data từ CSV
    df = load_model_metrics(csv_file_path)

    # Lấy metrics cho model và station
    metrics_data = get_metrics_for_model_station(df, model_name, station_name)

    # Tạo 2 cards
    mean_card = create_metrics_card(metrics_data, "mean")
    max_card = create_metrics_card(metrics_data, "max")

    return dbc.Row([
        dbc.Col([mean_card], width=6),
        dbc.Col([max_card], width=6)
    ])


# Function để sử dụng trong Dash callback
def update_metrics_cards_from_csv(csv_file_path, selected_model, selected_station):
    """
    Function để sử dụng trong Dash callback
    Trả về 2 cards dựa trên selection
    """
    try:
        # Mapping tên model nếu cần
        model_mapping = {
            'LSTM': 'LSTM',
            'BiLSTM': 'BiLSTM',
            'GCN_LSTM': 'GCN_LSTM',
            'GCN_BiLSTM': 'GCN_BiLSTM',
            'Enhanced_GCN_LSTM': 'Enhanced_GCN_LSTM',
            'Enhanced_GCN_BiLSTM': 'Enhanced_GCN_BiLSTM'
        }

        # Mapping tên station nếu cần
        station_mapping = {
            "NoiBai": "NOI BAI",
            "LangSon": "LANG SON",
            "LaoCai": "LAO CAI",
            "Vinh": "VINH",
            "PhuBai": "PHU BAI",
            "QuyNhon": "QUY NHON",
            "HCM": "HCM",
            "CaMau": "CA MAU"
        }

        actual_model = model_mapping.get(selected_model, selected_model)
        actual_station = station_mapping.get(selected_station, selected_station)

        # Load và process data
        df = load_model_metrics(csv_file_path)
        metrics_data = get_metrics_for_model_station(df, actual_model, actual_station)

        # Tạo 2 cards riêng biệt
        mean_card = create_metrics_card(metrics_data, "mean")
        max_card = create_metrics_card(metrics_data, "max")

        return mean_card, max_card

    except Exception as e:
        print(f"Lỗi trong update_metrics_cards_from_csv: {e}")
        empty_mean = create_empty_metrics_card("mean")
        empty_max = create_empty_metrics_card("max")
        return empty_mean, empty_max


# Ví dụ cách sử dụng trong layout
def metrics_layout_example():
    """
    Ví dụ layout sử dụng metrics cards
    """
    return html.Div([
        # Model và Station selection
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='model-dropdown',
                    options=[
                        {'label': 'LSTM', 'value': 'LSTM'},
                        {'label': 'BiLSTM', 'value': 'BiLSTM'},
                        {'label': 'GCN + LSTM', 'value': 'GCN_LSTM'},
                    ],
                    value='LSTM'
                )
            ], width=6),
            dbc.Col([
                dcc.Dropdown(
                    id='station-dropdown',
                    options=[
                        {'label': 'TP.HCM', 'value': 'HCM'},
                        {'label': 'Nội Bài', 'value': 'NoiBai'},
                    ],
                    value='HCM'
                )
            ], width=6)
        ], className="mb-4"),

        # Metrics cards container
        html.Div(id='metrics-cards-container')
    ])


# Callback example
"""
@app.callback(
    Output('metrics-cards-container', 'children'),
    [Input('model-dropdown', 'value'),
     Input('station-dropdown', 'value')]
)
def update_metrics_display(selected_model, selected_station):
    csv_file_path = 'path/to/your/metrics.csv'
    return create_dual_metrics_cards(csv_file_path, selected_model, selected_station)
"""

# Hoặc nếu muốn return riêng từng card:
"""
@app.callback(
    [Output('mean-card-container', 'children'),
     Output('max-card-container', 'children')],
    [Input('model-dropdown', 'value'),
     Input('station-dropdown', 'value')]
)
def update_individual_cards(selected_model, selected_station):
    csv_file_path = 'path/to/your/metrics.csv'
    return update_metrics_cards_from_csv(csv_file_path, selected_model, selected_station)
"""