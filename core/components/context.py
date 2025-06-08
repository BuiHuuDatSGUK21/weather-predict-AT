import dash
from dash import Dash, html, dash_table, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
from core.graphs import graph, graphs_predict
import plotly.graph_objects as go

context_style = {
    "background-color": "#EAEFEF",
    "height": "100vh",
}

row_style = {
    "background-color": "#EAEFEF"
}


def dashboard_layout():
    """Layout cho trang Dashboard"""
    return html.Div([
        dbc.Row([
            dcc.Tabs([
                dcc.Tab(label="Biểu đồ về không gian", value="space-plot",
                        selected_style={
                            "color": "black",
                            "border-bottom": "2px solid black",
                            "border-top": "white",
                            "border-left": "white",
                            "fontWeight": "600"},
                        style={
                            "background": "white",
                            "border": "none",
                        }),
                dcc.Tab(label="Biểu đồ về thời gian", value="time-plot",
                        selected_style={
                            "color": "black",
                            "border-bottom": "2px solid black",
                            "border-top": "white",
                            "border-left": "white",
                            "border-right": "white",
                            "fontWeight": "600"},
                        style={
                            "background": "white",
                            "border": "none",
                        })
            ], value="space-plot", id="tab-plot")
        ]),

        # Dashboard's Plots
        dbc.Container([

        ], fluid=True, id='dashboard-plot')

    ], className="m-2")


def predict_layout():
    """Layout cho trang dự đoán nhiệt độ cảm nhận với comparison charts"""
    return html.Div([
        # Header Section
        # dbc.Row([
        #     dbc.Col([
        #         html.H2("🌡️ Dự đoán Nhiệt độ Cảm nhận",
        #                 className="text-center mb-0 fw-bold text-primary"),
        #         html.P("Sử dụng AI để dự báo thời tiết 7 ngày tới",
        #                className="text-center text-muted mt-2")
        #     ])
        # ], className="bg-light rounded-3 p-4 mb-4 shadow-sm"),

        # Control Section
        dbc.Row([
            # Station & Model Selection
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Lựa chọn trạm và mô hình", className="mb-0 text-center")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        # Station Dropdown
                        html.Label("Chọn trạm khí tượng:", className="mb-2"),
                        dcc.Dropdown(
                            id='predict-station-dropdown',
                            options=[
                                {'label': 'Nội Bài', 'value': 'NoiBai'},
                                {'label': 'Lạng Sơn', 'value': 'LangSon'},
                                {'label': 'Lào Cai', 'value': 'LaoCai'},
                                {'label': 'Vinh', 'value': 'Vinh'},
                                {'label': 'Phú Bài', 'value': 'PhuBai'},
                                {'label': 'Quy Nhơn', 'value': 'QuyNhon'},
                                {'label': 'TP. Hồ Chí Minh', 'value': 'HCM'},
                                {'label': 'Cà Mau', 'value': 'CaMau'},
                            ],
                            value="HCM",
                            clearable=False,
                            className="mb-3"
                        ),

                        # Model Dropdown
                        html.Label("Chọn mô hình AI:", className=" mb-2"),
                        dcc.Dropdown(
                            id='predict-model-dropdown',
                            options=[
                                {'label': 'LSTM', 'value': 'LSTM'},
                                {'label': 'BiLSTM', 'value': 'BiLSTM'},
                                {'label': 'GCN + LSTM', 'value': 'GCN_LSTM'},
                                {'label': 'GCN + BiLSTM', 'value': 'GCN_BiLSTM'},
                                {'label': 'Cải tiến GCN + LSTM', 'value': 'Enhanced_GCN_LSTM'},
                                {'label': 'Cải tiến GCN + BiLSTM', 'value': 'Enhanced_GCN_BiLSTM'},
                            ],
                            value="LSTM",
                            clearable=False,
                        ),
                    ])
                ], className="h-100")
            ], width=6),

            # Model Performance Metrics
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Div(id='mean-card-container')
                    ], width=6),

                    dbc.Col([
                        html.Div(id='max-card-container')
                    ], width=6)
                ]),

            ], width=6),
        ], className="mb-4"),

        # 7-Day Forecast Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4("📅 Dự báo 7 ngày tới", className="mb-0 d-inline-block"),
                        ])
                    ], className="bg-gradient"),
                    dbc.CardBody([
                        # Loading spinner
                        dbc.Spinner([
                            html.Div(id='weather-forecast-section')
                        ], color="primary", type="grow"),
                    ], className="p-4")
                ], className="shadow")
            ], width=12)
        ], className="mb-4"),

        # ===== COMPARISON CHARTS SECTION =====
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("📈 So sánh Dự đoán vs Thực tế", className="mb-0")
                    ], className="bg-info text-white"),
                    dbc.CardBody([
                        # AT Mean Chart
                        dbc.Row([
                            dbc.Col([
                                html.H6("🌡️ Nhiệt độ cảm nhận trung bình", className="text-center mb-3"),
                                dcc.Graph(
                                    id='comparison-mean-chart',
                                    figure={
                                        'data': [],
                                        'layout': {
                                            'title': 'Đang tải biểu đồ AT Mean...',
                                            'height': 400
                                        }
                                    }
                                )
                            ], width=12)
                        ], className="mb-4"),

                        # AT Max Chart
                        dbc.Row([
                            dbc.Col([
                                html.H6("🔥 Nhiệt độ cảm nhận cực đại", className="text-center mb-3"),
                                dcc.Graph(
                                    id='comparison-max-chart',
                                    figure={
                                        'data': [],
                                        'layout': {
                                            'title': 'Đang tải biểu đồ AT Max...',
                                            'height': 400
                                        }
                                    }
                                )
                            ], width=12)
                        ])
                    ])
                ], className="shadow")
            ], width=12)
        ], className="mb-4"),

    ], className="p-4 bg-light min-vh-100")


def settings_layout():
    """Layout cho trang Cài đặt"""
    return html.Div([
        html.H2("Cài đặt", className="text-primary mb-4"),
        html.P("Cấu hình ứng dụng")
    ], className="p-4")


# ===== COMPARISON CHART FUNCTIONS =====

def create_comparison_chart(df, feature, forecast_horizon, station_name):
    """
    Tạo biểu đồ so sánh dữ liệu thực tế và dự đoán cho Dash
    """
    try:
        print("DEBUG: Creating comparison chart for {} at {}".format(feature, station_name))

        # Lấy date array cho station cụ thể
        date_array = get_date_array_for_station(station_name)

        # Tính toán forecast period
        forecast_start_index = 31 + forecast_horizon - 1
        if forecast_start_index < len(date_array):
            date_forecast_array = date_array[forecast_start_index:]
        else:
            date_forecast_array = date_array[-len(df):]  # Fallback: use last N dates

        # Đảm bảo length khớp với data
        min_length = min(len(date_forecast_array), len(df))
        date_forecast_array = date_forecast_array[:min_length]

        # Lấy dữ liệu real và predicted
        if feature == 'AT mean':
            real_data = df['Real_AT_mean'].iloc[:min_length]
            pred_data = df['Predicted_AT_mean'].iloc[:min_length]
            y_title = 'Nhiệt độ cảm nhận trung bình trong ngày (°C)'
            real_label = 'Nhiệt độ cảm nhận trung bình thực tế (°C)'
            pred_label = 'Nhiệt độ cảm nhận trung bình dự đoán (°C)'
            title_text = 'SO SÁNH DỮ LIỆU NHIỆT ĐỘ CẢM NHẬN TRUNG BÌNH TRONG NGÀY<br>THỰC TẾ VÀ DỰ ĐOÁN CỦA TRẠM {}'.format(
                station_name.upper())
        elif feature == 'AT max':
            real_data = df['Real_AT_max'].iloc[:min_length]
            pred_data = df['Predicted_AT_max'].iloc[:min_length]
            y_title = 'Nhiệt độ cảm nhận cực đại trong ngày (°C)'
            real_label = 'Nhiệt độ cảm nhận cực đại thực tế (°C)'
            pred_label = 'Nhiệt độ cảm nhận cực đại dự đoán (°C)'
            title_text = 'SO SÁNH DỮ LIỆU NHIỆT ĐỘ CẢM NHẬN CỰC ĐẠI TRONG NGÀY<br>THỰC TẾ VÀ DỰ ĐOÁN CỦA TRẠM {}'.format(
                station_name.upper())
        else:
            raise ValueError("Feature {} không được hỗ trợ".format(feature))

        # Tạo figure với Plotly
        fig = go.Figure()

        # Thêm đường thực tế
        fig.add_trace(go.Scatter(
            x=list(range(len(date_forecast_array))),
            y=list(real_data),
            mode='lines',
            name=real_label,
            line=dict(color='#1f77b4', width=2),
            customdata=date_forecast_array,
            hovertemplate='<b>%{fullData.name}</b><br>' +
                          'Ngày: %{customdata}<br>' +
                          'Giá trị: %{y:.2f}°C<extra></extra>'
        ))

        # Thêm đường dự đoán
        fig.add_trace(go.Scatter(
            x=list(range(len(date_forecast_array))),
            y=list(pred_data),
            mode='lines',
            name=pred_label,
            line=dict(color='#ff7f0e', width=2),
            customdata=date_forecast_array,
            hovertemplate='<b>%{fullData.name}</b><br>' +
                          'Ngày: %{customdata}<br>' +
                          'Giá trị: %{y:.2f}°C<extra></extra>'
        ))

        # Tạo tick labels cho trục x
        tick_step = max(1, len(date_forecast_array) // 10)
        tick_positions = list(range(0, len(date_forecast_array), tick_step))
        tick_labels = [date_forecast_array[i] for i in tick_positions]

        # Cập nhật layout
        fig.update_layout(
            title={
                'text': title_text,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'family': 'Times New Roman', 'size': 14, 'color': '#161b33'}
            },
            xaxis=dict(
                title='Ngày',
                tickfont=dict(family='Times New Roman', size=12),
                tickmode='array',
                tickvals=tick_positions,
                ticktext=tick_labels,
                tickangle=45,
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5
            ),
            yaxis=dict(
                title=y_title,
                tickfont=dict(family='Times New Roman', size=12),
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(family='Times New Roman', size=12)
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=80, r=60, t=100, b=120),
            height=400
        )

        # Ẩn border trên và phải
        fig.update_xaxes(showline=True, linewidth=1, linecolor='#161b33', mirror=False)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='#161b33', mirror=False)

        print("DEBUG: Comparison chart created successfully for {}".format(feature))
        return fig

    except Exception as e:
        print("ERROR in create_comparison_chart: {}".format(str(e)))
        import traceback
        traceback.print_exc()

        # Trả về biểu đồ trống nếu có lỗi
        fig = go.Figure()
        fig.update_layout(
            title="Lỗi khi tạo biểu đồ so sánh cho {}: {}".format(feature, str(e)),
            height=400
        )
        return fig


def get_comparison_data(model_name, station_name, forecast_horizon=7):
    """
    Lấy dữ liệu comparison cho model và station cụ thể
    Sử dụng cấu trúc thư mục thực tế của project
    """
    try:
        print("DEBUG: Loading comparison data for {} at {}".format(model_name, station_name))

        # Base path cho comparison data
        base_path = "../Data_compare/"

        # Mapping tên station sang format file
        station_file_mapping = {
            "NOI BAI": "NoiBai",
            "LANG SON": "LangSon",
            "LAO CAI": "LaoCai",
            "VINH": "Vinh",
            "PHU BAI": "PhuBai",
            "QUY NHON": "QuyNhon",
            "HCM": "TPHCM",
            "CA MAU": "CaMau"
        }

        station_file_name = station_file_mapping.get(station_name, "TPHCM")

        # Xác định model folder và file path
        if model_name == 'LSTM':
            # LSTM models
            model_folder = "LSTM/"
            csv_file_path = "{}{}Result_LSTM_1_{}.csv".format(base_path, model_folder, station_file_name)

        elif model_name == 'BiLSTM':
            # BiLSTM models
            model_folder = "BiLSTM/"
            csv_file_path = "{}{}Result_BiLSTM_1_{}.csv".format(base_path, model_folder, station_file_name)

        elif model_name == 'GCN_LSTM':
            # GCN_LSTM_baseline models - load both ATmean and ATmax files
            model_folder = "GCN_LSTM_baseline/"
            return load_gcn_comparison_data(base_path, model_folder, "GCN_LSTM_baseline", station_file_name)

        elif model_name == 'GCN_BiLSTM':
            # GCN_BiLSTM_baseline models
            model_folder = "GCN_BiLSTM_baseline/"
            return load_gcn_comparison_data(base_path, model_folder, "GCN_BiLSTM_baseline", station_file_name)

        elif model_name == 'Enhanced_GCN_LSTM':
            # GCN_LSTM_Attention models
            model_folder = "GCN_LSTM_Attention/"
            return load_gcn_comparison_data(base_path, model_folder, "GCN_LSTM_Attention", station_file_name)

        elif model_name == 'Enhanced_GCN_BiLSTM':
            # GCN_BiLSTM_Attention models
            model_folder = "GCN_BiLSTM_Attention/"
            return load_gcn_comparison_data(base_path, model_folder, "GCN_BiLSTM_Attention", station_file_name)

        else:
            print("Model {} không được hỗ trợ".format(model_name))
            return None

        print("Trying to load file: {}".format(csv_file_path))

        # Kiểm tra file tồn tại (cho LSTM/BiLSTM)
        import os
        if not os.path.exists(csv_file_path):
            print("File không tồn tại: {}".format(csv_file_path))
            return None

        # Load data
        df = pd.read_csv(csv_file_path)
        print("File loaded successfully. Shape: {}".format(df.shape))
        print("Columns: {}".format(list(df.columns)))

        # Xử lý columns cho LSTM/BiLSTM
        expected_cols = ['Real_AT_mean', 'Real_AT_max', 'Predicted_AT_mean', 'Predicted_AT_max']
        missing_cols = [col for col in expected_cols if col not in df.columns]

        if missing_cols:
            print("Thiếu columns: {} trong file {}".format(missing_cols, csv_file_path))
            print("Available columns: {}".format(list(df.columns)))

            # Thử tìm columns tương tự
            available_cols = list(df.columns)
            real_cols = [col for col in available_cols if 'real' in col.lower() or 'actual' in col.lower()]
            pred_cols = [col for col in available_cols if 'pred' in col.lower() or 'forecast' in col.lower()]

            print("Found real-like columns: {}".format(real_cols))
            print("Found pred-like columns: {}".format(pred_cols))

            if len(real_cols) >= 2 and len(pred_cols) >= 2:
                result_df = pd.DataFrame({
                    'Real_AT_mean': df[real_cols[0]],
                    'Real_AT_max': df[real_cols[1]] if len(real_cols) > 1 else df[real_cols[0]],
                    'Predicted_AT_mean': df[pred_cols[0]],
                    'Predicted_AT_max': df[pred_cols[1]] if len(pred_cols) > 1 else df[pred_cols[0]]
                })
                return result_df
            else:
                return None
        else:
            # Columns đầy đủ
            return df[expected_cols]

    except Exception as e:
        print("Error loading comparison data: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return None


def load_gcn_comparison_data(base_path, model_folder, model_name, station_file_name):
    """
    Load dữ liệu cho GCN models từ 2 file riêng biệt (ATmean và ATmax)
    """
    try:
        # Đường dẫn 2 files
        atmean_file = "{}{}Result_{}_1_ATmean_new.csv".format(base_path, model_folder, model_name)
        atmax_file = "{}{}Result_{}_1_ATmax_new.csv".format(base_path, model_folder, model_name)

        print("Loading GCN files:")
        print("  ATmean: {}".format(atmean_file))
        print("  ATmax: {}".format(atmax_file))

        import os

        # Kiểm tra files tồn tại
        if not os.path.exists(atmean_file):
            print("ATmean file không tồn tại: {}".format(atmean_file))
            return None

        if not os.path.exists(atmax_file):
            print("ATmax file không tồn tại: {}".format(atmax_file))
            return None

        # Load 2 files
        df_mean = pd.read_csv(atmean_file)
        df_max = pd.read_csv(atmax_file)

        print("ATmean file loaded. Shape: {}, Columns: {}".format(df_mean.shape, list(df_mean.columns)))
        print("ATmax file loaded. Shape: {}, Columns: {}".format(df_max.shape, list(df_max.columns)))

        # Tìm columns cho station cụ thể trong ATmean file
        available_cols_mean = list(df_mean.columns)
        available_cols_max = list(df_max.columns)

        # Pattern để tìm columns: Real_AT_[Station], Predicted_AT_[Station]
        real_mean_col = None
        pred_mean_col = None
        real_max_col = None
        pred_max_col = None

        # Tìm trong ATmean file
        for col in available_cols_mean:
            if 'real' in col.lower() and station_file_name.lower() in col.lower():
                real_mean_col = col
            elif ('pred' in col.lower() or 'forecast' in col.lower()) and station_file_name.lower() in col.lower():
                pred_mean_col = col

        # Tìm trong ATmax file
        for col in available_cols_max:
            if 'real' in col.lower() and station_file_name.lower() in col.lower():
                real_max_col = col
            elif ('pred' in col.lower() or 'forecast' in col.lower()) and station_file_name.lower() in col.lower():
                pred_max_col = col

        print("Found columns:")
        print("  Real ATmean: {}".format(real_mean_col))
        print("  Pred ATmean: {}".format(pred_mean_col))
        print("  Real ATmax: {}".format(real_max_col))
        print("  Pred ATmax: {}".format(pred_max_col))

        # Validate columns
        if not all([real_mean_col, pred_mean_col, real_max_col, pred_max_col]):
            print("Không tìm thấy đủ columns cho station {}".format(station_file_name))
            print("Available ATmean columns: {}".format(available_cols_mean))
            print("Available ATmax columns: {}".format(available_cols_max))

            # Fallback: sử dụng columns đầu tiên nếu có
            if len(available_cols_mean) >= 2 and len(available_cols_max) >= 2:
                # Giả sử columns 0,1 là real,pred cho mỗi file
                real_mean_col = available_cols_mean[0] if 'real' in available_cols_mean[0].lower() else \
                available_cols_mean[1]
                pred_mean_col = available_cols_mean[1] if 'pred' in available_cols_mean[1].lower() else \
                available_cols_mean[0]
                real_max_col = available_cols_max[0] if 'real' in available_cols_max[0].lower() else available_cols_max[
                    1]
                pred_max_col = available_cols_max[1] if 'pred' in available_cols_max[1].lower() else available_cols_max[
                    0]

                print("Using fallback columns:")
                print("  Real ATmean: {}".format(real_mean_col))
                print("  Pred ATmean: {}".format(pred_mean_col))
                print("  Real ATmax: {}".format(real_max_col))
                print("  Pred ATmax: {}".format(pred_max_col))
            else:
                return None

        # Đảm bảo cả 2 file có cùng số rows
        min_rows = min(len(df_mean), len(df_max))

        # Tạo DataFrame kết hợp
        result_df = pd.DataFrame({
            'Real_AT_mean': df_mean[real_mean_col].iloc[:min_rows],
            'Predicted_AT_mean': df_mean[pred_mean_col].iloc[:min_rows],
            'Real_AT_max': df_max[real_max_col].iloc[:min_rows],
            'Predicted_AT_max': df_max[pred_max_col].iloc[:min_rows]
        })

        print("Combined GCN data successfully. Final shape: {}".format(result_df.shape))
        return result_df

    except Exception as e:
        print("Error loading GCN comparison data: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return None

def get_date_array_for_station(station_name):
    """
    Lấy date array cho station cụ thể
    """
    try:
        # Mapping station sang file path
        station_file_mapping = {
            "NOI BAI": "../Data_AT_FilteredDate/NoiBai_FilteredDate.csv",
            "LANG SON": "../Data_AT_FilteredDate/LangSon_FilteredDate.csv",
            "LAO CAI": "../Data_AT_FilteredDate/LaoCai_FilteredDate.csv",
            "VINH": "../Data_AT_FilteredDate/Vinh_FilteredDate.csv",
            "PHU BAI": "../Data_AT_FilteredDate/PhuBai_FilteredDate.csv",
            "QUY NHON": "../Data_AT_FilteredDate/QuyNhon_FilteredDate.csv",
            "HCM": "../Data_AT_FilteredDate/TPHCM_FilteredDate.csv",
            "CA MAU": "../Data_AT_FilteredDate/CaMau_FilteredDate.csv"
        }

        csv_path = station_file_mapping.get(station_name, "../Data_AT_FilteredDate/NoiBai_FilteredDate.csv")

        df_data = pd.read_csv(csv_path)
        df_last_1177 = df_data.tail(1177)
        date_array = df_last_1177.apply(
            lambda row: "{:02d}/{:02d}/{}".format(int(row['DAY']), int(row['MONTH']), int(row['YEAR'])),
            axis=1
        ).tolist()

        return date_array

    except Exception as e:
        print("Error getting date array: {}".format(str(e)))
        # Return mock dates
        import datetime
        base_date = datetime.datetime(2020, 1, 1)
        return [(base_date + datetime.timedelta(days=i)).strftime("%d/%m/%Y") for i in range(100)]


def create_empty_comparison_chart(feature, station_name):
    """Tạo biểu đồ trống khi không có dữ liệu"""
    fig = go.Figure()
    fig.update_layout(
        title="Chưa có dữ liệu so sánh {} cho {}".format(feature, station_name),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        annotations=[
            dict(
                text="📊 Dữ liệu đang được tải...",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                xanchor='center', yanchor='middle',
                font=dict(size=16, color='gray')
            )
        ]
    )
    return fig


def register_callbacks(app):
    """Đăng ký tất cả callbacks"""

    # Main navigation callback
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def render_page_content(pathname):
        if pathname == '/':
            return dashboard_layout()
        elif pathname == '/predict':
            return predict_layout()
        elif pathname == '/settings':
            return settings_layout()
        else:
            return html.Div([
                html.H1("404 - Trang không tìm thấy", className="text-center"),
                html.P("Đường dẫn không tồn tại", className="text-center text-muted")
            ])

    @callback(
        Output('plot-space', 'children'),
        Input('station-dropdown', 'value')
    )
    def update_plot_space(selected_station):
        return html.Div([
            html.Img(src='/assets/vietnam_regions_map.png',
                     style={
                         'width': '100%',
                         'height': 'auto',
                         'object-fit': 'cover',
                         'object-position': 'center',
                         'display': 'block'
                     }
                     )
        ])

    @callback(
        Output("dashboard-plot", "children"),
        Input("tab-plot", "value")
    )
    def plot_type(selected_tab):
        if selected_tab == "space-plot":
            return space_plot_layout()
        elif selected_tab == "time-plot":
            return time_plot_layout()

    def heatmap_mean_layout():
        return dcc.Graph(figure=graph.update_chart("TPHCM", "corr_mean"))

    def heatmap_max_layout():
        return dcc.Graph(figure=graph.update_chart("TPHCM", "corr_max"))

    def geography_mean_layout():
        return html.Div([
            html.Img(src="../assets/temperature/atmean_geo.png")
        ])

    def geography_max_layout():
        return html.Div([
            html.Img(src="../assets/temperature/atmax_geo.png")
        ])

    def space_plot_layout():
        return html.Div([
            dbc.Row([
                # heatmap-mean plot
                dbc.Col([
                    heatmap_mean_layout()
                ], className="my-2", id="heatmap-mean-plot", width=6),

                # heatmap-max plot
                dbc.Col([
                    heatmap_max_layout()
                ], className="my-2", id="heatmap-max-plot", width=6)
            ], id="heatmap-plot"),

            dbc.Row([
                # georaphy-mean plot
                dbc.Col([
                    geography_mean_layout()
                ], className="my-2", id="geography-mean-plot", width=6),

                # geography-max plot
                dbc.Col([
                    geography_max_layout()
                ], className="my-2", id="geography-max-plot", width=6)
            ], id="geography-plot")
        ])

    @callback(
        Output("time-year-plot", "children"),
        Input("station-dropdown", "value")
    )
    def update_time_year_plot(selected_station):
        station_mapping = {
            "NoiBai": "Nội Bài",
            "LangSon": "Lạng Sơn",
            "LaoCai": "Lào Cai",
            "Vinh": "Vinh",
            "PhuBai": "Phú Bài",
            "QuyNhon": "Quy Nhơn",
            "HCM": "TPHCM",
            "CaMau": "Cà Mau"
        }

        actual_station_name = station_mapping.get(selected_station, "TPHCM")
        return dcc.Graph(figure=graph.update_chart(actual_station_name, "annual"), className="", style={"heigth": "20rem", "width": "50rem"})

    @callback(
        Output("time-monthly-mean-plot", "children"),
        Input("station-dropdown", "value")
    )
    def update_monthly_mean_layout(selected_station):
        station_mapping = {
            "NoiBai": "Nội Bài",
            "LangSon": "Lạng Sơn",
            "LaoCai": "Lào Cai",
            "Vinh": "Vinh",
            "PhuBai": "Phú Bài",
            "QuyNhon": "Quy Nhơn",
            "HCM": "TPHCM",
            "CaMau": "Cà Mau"
        }

        actual_station_name = station_mapping.get(selected_station, "TPHCM")
        return dcc.Graph(figure=graph.update_chart(actual_station_name, "monthly_mean"))

    @callback(
        Output("time-monthly-max-plot", "children"),
        Input("station-dropdown", "value")
    )
    def update_monthly_max_layout(selected_station):
        station_mapping = {
            "NoiBai": "Nội Bài",
            "LangSon": "Lạng Sơn",
            "LaoCai": "Lào Cai",
            "Vinh": "Vinh",
            "PhuBai": "Phú Bài",
            "QuyNhon": "Quy Nhơn",
            "HCM": "TPHCM",
            "CaMau": "Cà Mau"
        }

        actual_station_name = station_mapping.get(selected_station, "TPHCM")
        return dcc.Graph(figure=graph.update_chart(actual_station_name, "monthly_max"))

    def time_plot_layout():
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.H3("Lựa chọn trạm khí tượng", className="text-center"),
                    html.Div([
                        dcc.Dropdown(
                            options={
                                "NoiBai": "Trạm khí tượng Nội bài",
                                "LangSon": "Trạm khí tượng Lạng Sơn",
                                "LaoCai": "Trạm khí tượng Lào Cai",
                                "Vinh": "Trạm khí tượng Vinh",
                                "PhuBai": "Trạm khí tượng Phú Bài",
                                "QuyNhon": "Trạm khí tượng Quy Nhơn",
                                "HCM": "Trạm khí tượng Thành phố Hồ Chí Minh",
                                "CaMau": "Trạm khí tượng Cà Mau"
                            },
                            id="station-dropdown",
                            value="HCM",
                            clearable=False,

                        )
                    ])
                ], className="rounded-3 my-3 align-items-center justify-content-start", width=12),

                dbc.Row([
                    dbc.Col([
                        html.Div(id="time-monthly-mean-plot")
                    ], width=6),

                    dbc.Col([
                        html.Div(id="time-monthly-max-plot")
                    ], width=6)
                ]),

                dbc.Row([
                    html.Div(className="d-flex justify-content-center",id="time-year-plot")
                ], align="center", justify="center")
            ], className="rounded-3 my-1", style={"height": "120px"})
        ])

    # ===== MAIN PREDICTION CALLBACK WITH COMPARISON CHARTS =====
    @callback(
        [Output('weather-forecast-section', 'children'),
         Output('mean-card-container', 'children'),
         Output('max-card-container', 'children'),
         Output('comparison-mean-chart', 'figure'),  # ← THÊM COMPARISON CHARTS
         Output('comparison-max-chart', 'figure')],
        [Input('predict-station-dropdown', 'value'),
         Input('predict-model-dropdown', 'value')]
    )
    def update_prediction_dashboard_with_comparison(selected_station, selected_model):
        """
        Cập nhật tất cả components bao gồm comparison charts
        """
        try:
            # Mapping station names
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

            actual_station_name = station_mapping.get(selected_station, "HCM")
            print("Station: {}, Model: {}".format(actual_station_name, selected_model))

            # 1. Get CSV file path và tạo weather forecast
            csv_file_mapping = {
                "CA MAU": "../Data_AT_FilteredDate/CaMau_FilteredDate.csv",
                "LANG SON": "../Data_AT_FilteredDate/LangSon_FilteredDate.csv",
                "LAO CAI": "../Data_AT_FilteredDate/LaoCai_FilteredDate.csv",
                "PHU BAI": "../Data_AT_FilteredDate/PhuBai_FilteredDate.csv",
                "QUY NHON": "../Data_AT_FilteredDate/QuyNhon_FilteredDate.csv",
                "HCM": "../Data_AT_FilteredDate/TPHCM_FilteredDate.csv",
                "VINH": "../Data_AT_FilteredDate/Vinh_FilteredDate.csv",
                "NOI BAI": "../Data_AT_FilteredDate/NoiBai_FilteredDate.csv"
            }

            csv_file_path = csv_file_mapping.get(actual_station_name, "../Data_AT_FilteredDate/TPHCM_FilteredDate.csv")
            weather_forecast = graphs_predict.create_7_day_forecast(csv_file_path, actual_station_name)

            # 2. Load metrics từ CSV và tạo cards
            metrics_csv_path = "../DATA_Score/AT_ThucNghiemMoHinh.csv"
            mean_card, max_card = load_and_create_metrics_cards(
                metrics_csv_path,
                selected_model,
                actual_station_name
            )

            # 3. Tạo comparison charts
            comparison_data = get_comparison_data(selected_model, actual_station_name, forecast_horizon=7)

            if comparison_data is not None:
                mean_chart = create_comparison_chart(comparison_data, 'AT mean', 7, actual_station_name)
                max_chart = create_comparison_chart(comparison_data, 'AT max', 7, actual_station_name)
            else:
                mean_chart = create_empty_comparison_chart("AT mean", actual_station_name)
                max_chart = create_empty_comparison_chart("AT max", actual_station_name)

            return weather_forecast, mean_card, max_card, mean_chart, max_chart

        except Exception as e:
            print("Error in prediction dashboard: {}".format(str(e)))

            # Return empty states
            error_msg = html.Div([
                html.H5("⚠️ Có lỗi xảy ra", className="text-warning"),
                html.P("Chi tiết: {}".format(str(e)), className="text-muted small")
            ], className="text-center p-3")

            empty_mean_card = create_empty_metrics_card("mean")
            empty_max_card = create_empty_metrics_card("max")
            empty_mean_chart = create_empty_comparison_chart("AT mean", "Unknown")
            empty_max_chart = create_empty_comparison_chart("AT max", "Unknown")

            return error_msg, empty_mean_card, empty_max_card, empty_mean_chart, empty_max_chart

    # ===== METRICS FUNCTIONS (GIỮ NGUYÊN) =====
    def load_and_create_metrics_cards(csv_file_path, model_name, station_name):
        """Load metrics từ CSV và tạo 2 cards mean/max"""
        try:
            df = pd.read_csv(csv_file_path, dtype=str)

            model_mapping = {
                'LSTM': 'LSTM',
                'BiLSTM': 'BiLSTM',
                'GCN_LSTM': 'GCN - LSTM',
                'GCN_BiLSTM': 'GCN - BiLSTM',
                'Enhanced_GCN_LSTM': 'GCN - LSTM (Custom)',
                'Enhanced_GCN_BiLSTM': 'GCN - BiLSTM (Custom)'
            }

            actual_model = model_mapping.get(model_name, model_name)

            # Filter data cho model và station cụ thể
            model_filter = df['Model'].str.strip() == actual_model
            station_filter = df['Station'].str.strip() == station_name
            filtered_df = df[model_filter & station_filter]

            if filtered_df.empty:
                print("Không tìm thấy dữ liệu cho Model: {}, Station: {}".format(actual_model, station_name))
                return create_empty_metrics_card("mean"), create_empty_metrics_card("max")

            # Lấy row đầu tiên
            row = filtered_df.iloc[0]

            # Extract metrics data
            metrics_data = {
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

            # Tạo 2 cards
            mean_card = create_metrics_card(metrics_data, "mean", "📊 Chỉ số đánh giá AT Mean - {}".format(actual_model))
            max_card = create_metrics_card(metrics_data, "max", "📊 Chỉ số đánh giá AT Max - {}".format(actual_model))

            return mean_card, max_card

        except Exception as e:
            print("Lỗi load metrics từ CSV: {}".format(str(e)))
            return create_empty_metrics_card("mean"), create_empty_metrics_card("max")

    def create_metric_card_item(value, label, color_class, border_class):
        """Tạo một item metric trong card"""
        return dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("{}".format(value), className="{} fw-bold mb-0".format(color_class)),
                    html.P(label, className="text-muted small mb-0")
                ], className="text-center py-2")
            ], className=border_class)
        ], width=6)

    def create_metrics_card(metrics_data, card_type="mean", card_title=None):
        """Tạo card hiển thị metrics (mean hoặc max)"""
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
            ], className="{} text-white".format(header_color)),
            dbc.CardBody([
                dbc.Row([
                    create_metric_card_item(data['r2'], "R² Score", "text-primary", "border-primary"),
                    create_metric_card_item(data['mse'], "MSE", "text-info", "border-info"),
                ], className="mb-2"),
                dbc.Row([
                    create_metric_card_item(data['mae'], "MAE", "text-warning", "border-warning"),
                    create_metric_card_item(data['rmse'], "RMSE", "text-danger", "border-danger"),
                ])
            ], id="model-score-body-{}".format(card_type))
        ], className="h-100")

    def create_empty_metrics_card(card_type="mean"):
        """Tạo card rỗng khi không có dữ liệu"""
        header_color = "bg-success" if card_type == "mean" else "bg-info"
        title = "📊 Chỉ số đánh giá AT Mean" if card_type == "mean" else "📊 Chỉ số đánh giá AT Max"

        return dbc.Card([
            dbc.CardHeader([
                html.H5(title, className="mb-0 text-center")
            ], className="{} text-white".format(header_color)),
            dbc.CardBody([
                html.Div([
                    html.H5("⚠️ Không có dữ liệu", className="text-muted text-center"),
                    html.P("Vui lòng kiểm tra file CSV metrics", className="text-center small")
                ], className="py-4")
            ])
        ], className="h-100")