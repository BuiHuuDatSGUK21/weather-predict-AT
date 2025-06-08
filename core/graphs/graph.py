import os

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import geopandas as gpd
import json


def create_annual_trend_chart(feature, station_df, station_name, feature_name, unit):
    """
    Tạo biểu đồ xu hướng hàng năm cho Dash
    """
    try:
        df = station_df[station_name]

        mean_at = df.groupby('YEAR')[feature].mean()
        mean_at_max = df.groupby('YEAR')['AT max'].mean()
        years = np.arange(1992, 2025)

        fig = go.Figure()

        # Đường trung bình cho AT mean
        fig.add_trace(go.Scatter(
            x=years,
            y=mean_at,
            mode='lines+markers',
            name=f'Trung bình {feature_name[feature]} ({unit[feature]})',
            line=dict(color='#5D7F99', width=2),
            marker=dict(symbol='circle', size=6)
        ))

        # Thêm đường trung bình AT max
        atmax_feature = 'AT max'
        fig.add_trace(go.Scatter(
            x=years,
            y=mean_at_max,
            mode='lines+markers',
            name=f'Trung bình {feature_name[atmax_feature]} ({unit[atmax_feature]})',
            line=dict(color='#5D7F99', width=2),
            marker=dict(symbol='triangle-up', size=8)
        ))

        # Tính toán và thêm đường xu hướng cho feature chính
        z = np.polyfit(years, mean_at, 1)
        p = np.poly1d(z)
        trend_line = p(years)
        trend_value = f"{z[0] * 10:+.2f}"

        # Xu hướng tuyến tính
        fig.add_trace(go.Scatter(
            x=years,
            y=trend_line,
            mode='lines',
            name='Xu hướng tuyến tính',
            line=dict(color='#9d4edd', width=2.5, dash='solid')
        ))

        # Tính toán và thêm đường xu hướng cho AT max
        z_2 = np.polyfit(years, mean_at_max, 1)
        p_2 = np.poly1d(z_2)
        trend_line_2 = p_2(years)

        fig.add_trace(go.Scatter(
            x=years,
            y=trend_line_2,
            mode='lines',
            name='Xu hướng AT max',
            line=dict(color='#9d4edd', width=2.5, dash='solid'),
            showlegend=False
        ))

        # Thêm đường giá trị trung bình
        mean_value = np.mean(mean_at)
        fig.add_hline(
            y=mean_value,
            line_dash="dash",
            line_color="#cccccc",
            line_width=1.5,
            annotation_text=f'Trung bình nhiệt độ cảm nhận 1992-2024',
            annotation_position="top left"
        )

        mean_value_max = np.mean(mean_at_max)
        fig.add_hline(
            y=mean_value_max,
            line_dash="dash",
            line_color="#cccccc",
            line_width=1.5
        )

        # Cập nhật layout
        fig.update_layout(
            title={
                'text': f"BIẾN ĐỘNG THEO NĂM CỦA ĐẶC TRƯNG NHIỆT ĐỘ CẢM NHẬN<br>TẠI TRẠM KHÍ TƯỢNG {station_name.upper()}",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'family': 'Times New Roman', 'size': 16, 'color': '#161b33'}
            },
            xaxis=dict(
                title='Năm',
                tickfont=dict(family='Times New Roman', size=12),
                tickmode='array',
                tickvals=list(range(1992, 2025, 2)) + [2024],
                tickangle=45,
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5,
                zeroline=False
            ),
            yaxis=dict(
                title='Nhiệt độ cảm nhận (℃)',
                tickfont=dict(family='Times New Roman', size=12),
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5,
                zeroline=False
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(family='Times New Roman', size=12)
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=60, r=60, t=100, b=120)
        )

        # Ẩn border trên và phải
        fig.update_xaxes(showline=True, linewidth=1, linecolor='#161b33', mirror=False)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='#161b33', mirror=False)

        print(f"DEBUG: Chart created successfully for {station_name}")
        return fig

    except Exception as e:
        print(f"ERROR in create_annual_trend_chart: {str(e)}")
        import traceback
        traceback.print_exc()

        # Trả về biểu đồ trống với thông báo lỗi
        fig = go.Figure()
        fig.update_layout(
            title=f"Lỗi khi tạo biểu đồ cho {station_name}: {str(e)}",
            xaxis_title="Năm",
            yaxis_title="Nhiệt độ (°C)"
        )
        return fig


def create_monthly_heatmap(station_name, station_df, feature):
    """
    Tạo biểu đồ heatmap cho xu hướng theo tháng
    """
    try:
        print(f"DEBUG: Creating heatmap for station: {station_name}, feature: {feature}")

        df = station_df[station_name].copy()

        conditions = [
            (df['YEAR'] >= 1992) & (df['YEAR'] <= 2002),
            (df['YEAR'] >= 2003) & (df['YEAR'] <= 2013),
            (df['YEAR'] >= 2014) & (df['YEAR'] <= 2018),
            (df['YEAR'] >= 2019) & (df['YEAR'] <= 2024),
        ]
        choices = ['1992 - 2002', '2003 - 2013', '2014 - 2018', '2019 - 2024']
        df['period'] = np.select(conditions, choices, default='Other')

        # Tính giá trị trung bình cho từng giai đoạn
        mean_at = df.groupby(['period', 'MONTH'])[feature].mean().unstack('MONTH')

        # Tính giá trị cho giai đoạn tổng
        total_df = df[(df['YEAR'] >= 1992) & (df['YEAR'] <= 2024)]
        mean_total = total_df.groupby('MONTH')[feature].mean()

        # Thêm giai đoạn tổng vào kết quả
        mean_at.loc['1992 - 2024'] = mean_total
        choices.append('1992 - 2024')
        mean_at = mean_at.reindex(choices)

        # Đổi thứ tự các hàng để '1992 - 2024' lên đầu
        choices = ['1992 - 2024'] + choices[:-1]
        mean_at = mean_at.reindex(choices)

        mean_at_values = mean_at.values

        # Tạo heatmap với Plotly
        fig = go.Figure(data=go.Heatmap(
            z=mean_at_values,
            x=[f'Tháng {i}' for i in range(1, 13)],
            y=choices,
            colorscale='RdYlBu_r',  # Tương tự coolwarm của matplotlib
            showscale=True,
            text=[[f'{val:.1f}' for val in row] for row in mean_at_values],
            texttemplate="%{text}",
            textfont={"family": "Times New Roman", "size": 12, "color": "black"},
            hoverongaps=False
        ))

        # Cập nhật layout
        title_text = ""
        if feature == 'AT mean':
            title_text = f'GIÁ TRỊ TRUNG BÌNH THÁNG<br>CỦA NHIỆT ĐỘ CẢM NHẬN TRUNG BÌNH TRONG NGÀY<br>TẠI TRẠM KHÍ TƯỢNG {station_name.upper()}'
        else:
            title_text = f'GIÁ TRỊ TRUNG BÌNH THÁNG<br>CỦA NHIỆT ĐỘ CẢM NHẬN CỰC ĐẠI TRONG NGÀY<br>TẠI TRẠM KHÍ TƯỢNG {station_name.upper()}'

        fig.update_layout(
            title={
                'text': title_text,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'family': 'Times New Roman', 'size': 14, 'color': '#161b33'}
            },
            xaxis=dict(
                title='Tháng',
                # titlefont=dict(family='Times New Roman', size=14, color='#161b33'),
                tickfont=dict(family='Times New Roman', size=12),
                side='bottom'
            ),
            yaxis=dict(
                title='Giai đoạn',
                # titlefont=dict(family='Times New Roman', size=14, color='#161b33'),
                tickfont=dict(family='Times New Roman', size=12),
                autorange='reversed',
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=100, r=100, t=120, b=80),
            height=400
        )

        print(f"DEBUG: Heatmap created successfully for {station_name}")
        return fig

    except Exception as e:
        print(f"ERROR in create_monthly_heatmap: {str(e)}")
        import traceback
        traceback.print_exc()

        # Trả về biểu đồ trống với thông báo lỗi
        fig = go.Figure()
        fig.update_layout(
            title=f"Lỗi khi tạo heatmap cho {station_name}: {str(e)}",
            xaxis_title="Tháng",
            yaxis_title="Giai đoạn"
        )
        return fig

def get_corr(station_df, feature):
    data = {
        'Nội Bài': list(station_df['Nội Bài'][feature]),
        'Lạng Sơn': list(station_df['Lạng Sơn'][feature]),
        'Lào Cai': list(station_df['Lào Cai'][feature]),
        'Vinh': list(station_df['Vinh'][feature]),
        'Phú Bài': list(station_df['Phú Bài'][feature]),
        'Quy Nhơn': list(station_df['Quy Nhơn'][feature]),
        'TPHCM': list(station_df['TPHCM'][feature]),
        'Cà Mau': list(station_df['Cà Mau'][feature]),
    }
    data = pd.DataFrame(data)
    corr = data.corr(method='pearson')

    return round(corr, 2)


def create_corr_heatmap(station_df, feature, feature_name):
    try:
        corr_feature = get_corr(station_df, feature)

        # Định nghĩa thứ tự hiển thị từ Bắc xuống Nam
        station_order = [
            'Nội Bài', 'Lạng Sơn', 'Lào Cai',
            'Vinh', 'Phú Bài', 'Quy Nhơn',
            'TPHCM', 'Cà Mau'
        ]

        # Lọc chỉ những station có trong correlation matrix
        available_stations = [station for station in station_order if station in corr_feature.columns]

        # Sắp xếp lại correlation matrix theo thứ tự mong muốn
        corr_feature_sorted = corr_feature.loc[available_stations, available_stations]

        fig = go.Figure(data=go.Heatmap(
            z=corr_feature_sorted.values,
            x=corr_feature_sorted.columns,
            y=corr_feature_sorted.index,
            colorscale='Blues',
            showscale=True,
            text=[[f'{val:.2f}' for val in row] for row in corr_feature_sorted.values],
            texttemplate="%{text}",
            hoverongaps=False,
            zmin=-1,
            zmax=1
        ))

        fig.update_layout(
            title={
                'text': f'Ma trận tương quan <br>Các trạm khí tượng (Bắc - Nam)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'family': 'Times New Roman', 'size': 14, 'color': '#161b33'}
            },
            xaxis=dict(
                title='Trạm khí tượng',
                tickfont=dict(family='Times New Roman', size=12),
                side='bottom',
                tickangle=45
            ),
            yaxis=dict(
                title='Trạm khí tượng',
                tickfont=dict(family='Times New Roman', size=12),
                autorange='reversed'  # Thêm dòng này để đảo ngược trục y
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=120, r=100, t=120, b=100),
            height=500
        )
        return fig
    except Exception as e:
        print(f"ERROR in create_corr_heatmap: {str(e)}")
        fig = go.Figure()
        fig.update_layout(title="Lỗi khi tạo correlation heatmap")
        return fig



# Tạo Dash app
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     html.H1("Biểu đồ xu hướng nhiệt độ cảm nhận theo năm",
#             style={'textAlign': 'center', 'fontFamily': 'Times New Roman', 'marginBottom': 30}),
#
#     html.Div([
#         html.Label("Chọn tên trạm:", style={'fontFamily': 'Times New Roman', 'fontSize': 14, 'fontWeight': 'bold'}),
#         dcc.Dropdown(
#             id='station-dropdown',
#             options=[
#                 {'label': 'Nội Bài', 'value': 'Nội Bài'},
#                 {'label': 'Lạng Sơn', 'value': 'Lạng Sơn'},
#                 {'label': 'Lào Cai', 'value': 'Lào Cai'},
#                 {'label': 'Vinh', 'value': 'Vinh'},
#                 {'label': 'Phú Bài', 'value': 'Phú Bài'},
#                 {'label': 'Quy Nhơn', 'value': 'Quy Nhơn'},
#                 {'label': 'TPHCM', 'value': 'TPHCM'},
#                 {'label': 'Cà Mau', 'value': 'Cà Mau'}
#             ],
#             value='Nội Bài',
#             style={'fontFamily': 'Times New Roman'}
#         )
#     ], style={'width': '300px', 'margin': '0 auto', 'marginBottom': 30}),
#
#     html.Div([
#         html.Label("Chọn loại biểu đồ:", style={'fontFamily': 'Times New Roman', 'fontSize': 14, 'fontWeight': 'bold'}),
#         dcc.RadioItems(
#             id='chart-type-radio',
#             options=[
#                 {'label': ' Xu hướng theo năm', 'value': 'annual'},
#                 {'label': ' Heatmap theo tháng (AT mean)', 'value': 'monthly_mean'},
#                 {'label': ' Heatmap theo tháng (AT max)', 'value': 'monthly_max'},
#                 {'label': 'Heatmap tương quan (AT mean)', 'value': 'corr_mean'},
#                 {'label': 'Heatmap tương quan (AT max)', 'value': 'corr_max'},
#                 {'label': 'Vietnam map (AT mean)', 'value': 'lat_mean'},
#                 {'label': 'Vietnam map (AT max)', 'value': 'lat_max'}
#             ],
#             value='annual',
#             style={'fontFamily': 'Times New Roman', 'fontSize': 12},
#             labelStyle={'display': 'block', 'marginBottom': '5px'}
#         )
#     ], style={'width': '300px', 'display': 'inline-block', 'verticalAlign': 'top'}),
#
#     dcc.Graph(id='annual-trend-chart')
# ])


# @callback(
#     Output('annual-trend-chart', 'figure'),
#     [Input('station-dropdown', 'value'),
#      Input('chart-type-radio', 'value')]
# )
def update_chart(selected_station, chart_type):
    """
    Callback để cập nhật biểu đồ khi chọn trạm hoặc loại biểu đồ khác
    """
    print(f"DEBUG: Selected station: {selected_station}, Chart type: {chart_type}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"File location: {os.path.abspath(__file__)}")

    # Test đường dẫn
    test_path = '../Data_AT_FilteredDate/CaMau_FilteredDate.csv'
    print(f"Trying to access: {os.path.abspath(test_path)}")
    print(f"File exists: {os.path.exists(test_path)}")
    try:
        # Đọc dữ liệu từ các file CSV
        df_CaMau = pd.read_csv('../Data_AT_FilteredDate/CaMau_FilteredDate.csv')
        df_LangSon = pd.read_csv('../Data_AT_FilteredDate/LangSon_FilteredDate.csv')
        df_LaoCai = pd.read_csv('../Data_AT_FilteredDate/LaoCai_FilteredDate.csv')
        df_NoiBai = pd.read_csv('../Data_AT_FilteredDate/NoiBai_FilteredDate.csv')
        df_PhuBai = pd.read_csv('../Data_AT_FilteredDate/PhuBai_FilteredDate.csv')
        df_QuyNhon = pd.read_csv('../Data_AT_FilteredDate/QuyNhon_FilteredDate.csv')
        df_TPHCM = pd.read_csv('../Data_AT_FilteredDate/TPHCM_FilteredDate.csv')
        df_Vinh = pd.read_csv('../Data_AT_FilteredDate/Vinh_FilteredDate.csv')

        # Tạo dictionary cho station_df
        station_df = {
            'Nội Bài': df_NoiBai,
            'Lạng Sơn': df_LangSon,
            'Lào Cai': df_LaoCai,
            'Vinh': df_Vinh,
            'Phú Bài': df_PhuBai,
            'Quy Nhơn': df_QuyNhon,
            'TPHCM': df_TPHCM,
            'Cà Mau': df_CaMau,
        }

        # Kiểm tra xem selected_station có trong dictionary không
        if selected_station not in station_df:
            print(f"ERROR: Station '{selected_station}' not found in station_df")
            print(f"Available stations: {list(station_df.keys())}")
            selected_station = 'Nội Bài'  # Fallback to default

        # Định nghĩa feature_name và unit
        feature_name = {
            'AT mean': 'nhiệt độ cảm nhận trung bình trong ngày',
            'AT max': 'nhiệt độ cảm nhận cực đại trong ngày'
        }

        unit = {
            'AT mean': '°C',
            'AT max': '°C'
        }

        print(f"DEBUG: Creating {chart_type} chart for {selected_station}")

        # Tạo biểu đồ tương ứng với loại được chọn
        if chart_type == 'annual':
            fig = create_annual_trend_chart('AT mean', station_df, selected_station, feature_name, unit)
        elif chart_type == 'monthly_mean':
            fig = create_monthly_heatmap(selected_station, station_df, 'AT mean')
        elif chart_type == 'monthly_max':
            fig = create_monthly_heatmap(selected_station, station_df, 'AT max')
        elif chart_type == 'corr_mean':
            fig = create_corr_heatmap(station_df, 'AT mean', feature_name)
        elif chart_type == 'corr_max':
            fig = create_corr_heatmap(station_df, 'AT max', feature_name)
        # elif chart_type == 'lat_mean':
        #     station_order = ['Nội Bài', 'Lạng Sơn', 'Lào Cai', 'Vinh', 'Phú Bài', 'Quy Nhơn', 'TPHCM', 'Cà Mau']
        #     fig = create_vietnam_choropleth_with_local_geojson(station_df, station_info, station_order, 'AT mean', feature_name)
        else:
            # Default fallback
            fig = create_annual_trend_chart('AT mean', station_df, selected_station, feature_name, unit)

        print(f"DEBUG: Chart created successfully for {selected_station}, type: {chart_type}")
        return fig

    except Exception as e:
        print(f"ERROR in update_chart: {str(e)}")
        import traceback
        traceback.print_exc()

        # Trả về biểu đồ trống nếu có lỗi
        fig = go.Figure()
        fig.update_layout(
            title="Lỗi khi tải dữ liệu",
            xaxis_title="",
            yaxis_title=""
        )
        return fig

# if __name__ == '__main__':
#     app.run(debug=True)