import cartopy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import numpy as np
from scipy.interpolate import griddata
from matplotlib.patches import Circle
import matplotlib.patches as patches

'''
PHÂN TÍCH MỐI QUAN HỆ KHÔNG GIAN:
- Sự ảnh hưởng của vĩ độ lên các đặc trưng: TMP_2, DEW_2, RH, AT mean, AT max

- Sự tương quan giữa các trạm:
    + Tính sự tương quan giữa các trạm theo các đặc trưng: TMP_2, DEW_2, RH, AT mean, AT max
    + Tính tổng quát bằng cách đánh trọng số cho đặc trưng
    
- Phân tích rủi ro theo từng vùng: (Xem lại chi tiết đánh giá)
    
    
    
- PLOT 1: Sự ảnh hưởng của vĩ độ lên các đặc trưng
- PLOT 2: Sự tương quan giữa các trạm theo các đặc trưng
'''


# Mối liên hệ giữa vĩ độ ảnh hưởng dến nhiệt độ
def get_station_info(station_df):
    station_info = dict()
    for station, df in station_df.items():
        first_row = df.iloc[0]
        temp_dict = [first_row['LATITUDE'], first_row['LONGITUDE']]
        station_info[station] = temp_dict

    return station_info


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


def get_mean(station_df, feature):
    mean_feature_dict = dict()
    for station, df in station_df.items():
        mean_feature = df[feature].mean()
        mean_feature_dict[station] = mean_feature

    print(mean_feature_dict)
    return mean_feature_dict

def get_difference(station_df, feature_1, feature_2):
    result_dict = dict()
    for station, df in station_df.items():
        result_dict[station] = df[feature_1] - df[feature_2]
    print(result_dict)

def plot_2(station_df, feature, feature_name):
    plt.figure(figsize=(10, 8))

    corr_feature = get_corr(station_df, feature)
    sns.heatmap(data=corr_feature, annot=True, cmap='Blues')

    plt.xticks(fontfamily='Times New Roman', fontsize=14, rotation=45)
    plt.yticks(fontfamily='Times New Roman', fontsize=14, rotation=0)

    plt.title(f'TƯƠNG QUAN {feature_name[feature].upper()} \nGIỮA CÁC TRẠM KHÍ TƯỢNG',
              fontfamily='Times New Roman', fontsize=14, pad=20, fontweight='bold')
    plt.xlabel('Trạm khí tượng', fontfamily='Times New Roman', color='#0d0c1d', fontsize=14, fontweight='bold',
               labelpad=10)

    plt.tight_layout()
    plt.show()


def plot_1(station_df, station_info, station_name, region_dict, feature, feature_name):
    colors = {
        'Tây Bắc': '#fee5d9',
        'Đông Bắc': '#fcae91',
        'Đồng bằng sông Hồng': '#fb6a4a',
        'Bắc Trung Bộ': '#de2d26',
        'Duyên hải Nam Trung Bộ': '#a50f15',
        'Tây Nguyên': '#808080',
        'Đông Nam Bộ': '#dd1c77',
        'Đồng bằng sông Cửu Long': '#756bb1'
    }

    vietnam = gpd.read_file('.\gadm41_VNM_shp', layer='gadm41_VNM_1')
    mean_feature_dict = get_mean(station_df, feature)
    stations = pd.DataFrame({
        'name': station_name,
        'lat': [station_info[name][0] for name in station_name],
        'lon': [station_info[name][1] for name in station_name],
        'region': ['Đồng bằng sông Hồng', 'Đông Bắc', 'Tây Bắc', 'Bắc Trung Bộ', 'Bắc Trung Bộ',
                   'Duyên hải Nam Trung Bộ', 'Đông Nam Bộ', 'Đồng bằng sông Cửu Long'],
        'feature_values': [mean_feature_dict[name] for name in station_name]
    })
    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations.lon, stations.lat),
        crs="EPSG:4326"
    )

    vietnam['region'] = vietnam['NAME_1'].map(region_dict)

    region_mean_values = {}
    for region in stations['region'].unique():
        region_stations = stations[stations['region'] == region]
        if not region_stations.empty:
            region_mean_values[region] = region_stations['feature_values'].mean()

    # Thêm giá trị trung bình vào GeoDataFrame của Vietnam
    vietnam['mean_feature'] = vietnam['region'].map(region_mean_values)

    # Tạo figure
    fig, ax = plt.subplots(figsize=(8, 8))

    vietnam.plot(ax=ax, color='lightgrey', edgecolor='white', linewidth=0.5)

    # Vẽ bản đồ với màu dựa trên giá trị trung bình của từng vùng
    if feature == 'RH':
        color_vietnam_plot = 'Reds'
    else:
        color_vietnam_plot = 'coolwarm'
    vietnam.plot(column='mean_feature',
                 ax=ax,
                 cmap=color_vietnam_plot,
                 edgecolor='white',
                 linewidth=0.5,
                 legend=True,
                 legend_kwds={
                              'orientation': 'vertical',  # Đổi sang định hướng dọc
                              'shrink': 0.8,  # Điều chỉnh kích thước
                              'pad': 0.02,  # Khoảng cách từ biểu đồ
                              'fraction': 0.03,  # Chiều rộng của colorbar
                              'aspect': 20,  # Tỉ lệ chiều cao/chiều rộng
                              })

    # THÊM QUẦN ĐẢO HOÀNG SA VÀ TRƯỜNG SA
    # Tọa độ quần đảo
    hoang_sa_lon, hoang_sa_lat = 112.0, 16.5  # Hoàng Sa
    truong_sa_lon, truong_sa_lat = 114.0, 10.0  # Trường Sa

    # Vẽ chấm nhỏ cho quần đảo (màu khác biệt với trạm khí tượng)
    ax.scatter(hoang_sa_lon, hoang_sa_lat,
               c='grey', s=30, marker='o',
               edgecolor='grey', linewidth=1.5,
               zorder=5, alpha=0.8)

    ax.scatter(truong_sa_lon, truong_sa_lat,
               c='grey', s=30, marker='o',
               edgecolor='grey', linewidth=1.5,
               zorder=5, alpha=0.8)

    # Ghi tên phía dưới chấm
    ax.annotate('Hoàng Sa',
                (hoang_sa_lon, hoang_sa_lat),
                xytext=(0, -15),  # Di chuyển xuống dưới 15 pixels
                textcoords='offset points',
                fontsize=10,
                fontfamily='Times New Roman',
                fontweight='bold',
                color='grey',
                ha='center',  # Căn giữa theo chiều ngang
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='grey',
                          boxstyle='round,pad=0.2', linewidth=1))

    ax.annotate('Trường Sa',
                (truong_sa_lon, truong_sa_lat),
                xytext=(0, -15),  # Di chuyển xuống dưới 15 pixels
                textcoords='offset points',
                fontsize=10,
                fontfamily='Times New Roman',
                fontweight='bold',
                color='grey',
                ha='center',  # Căn giữa theo chiều ngang
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='grey',
                          boxstyle='round,pad=0.2', linewidth=1))

    label_offsets = {
        'Lào Cai': (-60, 10),  # Di chuyển sang trái và lên trên
        'Lạng Sơn': (10, 15),  # Di chuyển sang phải và lên trên
        'Nội Bài': (30, -30)  # Di chuyển sang phải và xuống dưới
    }
    unit = {
        'TMP_2': '°C',
        'DEW_2': '°C',
        'RH': '%',
        'AT mean': '°C',
        'AT max': '°C'
    }
    # Thêm tên các trạm
    for idx, row in stations_gdf.iterrows():
        station_name = row['name']
        offset = label_offsets.get(station_name, (10, 5))
        if row['name'] == 'Quy Nhơn':
            plt.annotate(f"{row['name']}\n({row['feature_values']:.2f}{unit[feature]})",
                         (row['lon'], row['lat']),
                         xytext=offset,
                         textcoords='offset points',
                         fontsize=12,
                         fontfamily='Times New Roman',
                         bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'))
        else:
            plt.annotate(f"{row['name']}: ({row['feature_values']:.2f}{unit[feature]})",
                         (row['lon'], row['lat']),
                         xytext=offset,
                         textcoords='offset points',
                         fontsize=12,
                         fontfamily='Times New Roman',
                         bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'))

    scatter = ax.scatter(stations_gdf.lon, stations_gdf.lat,
                         c='green',
                         s=50,
                         marker='o',
                         edgecolor='green',
                         linewidth=1.5)

    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.gca().spines[['left', 'bottom']].set_color('#161b33')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(fontfamily='Times New Roman', fontsize=12)
    plt.yticks(fontfamily='Times New Roman', fontsize=12)
    plt.title(f"ẢNH HƯỞNG CỦA VĨ ĐỘ \nĐẾN {feature_name[feature].upper()} \nTẠI CÁC TRẠM KHÍ TƯỢNG",
        fontfamily='Times New Roman', fontsize=14, pad=20, fontweight='bold')

    plt.xlabel('Kinh độ', fontfamily='Times New Roman', color='#0d0c1d', fontsize=12, fontweight='bold')
    plt.ylabel('Vĩ độ', fontfamily='Times New Roman', color='#0d0c1d', fontsize=12, fontweight='bold')

    ax.set_aspect('equal')
    plt.subplots_adjust(left=0.038, bottom=0.062, right=0.824, top=0.895, wspace=0.2, hspace=0.2)
    # plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df_CaMau = pd.read_csv('../Data_AT_FilteredDate/CaMau_FilteredDate.csv')
    df_LangSon = pd.read_csv('../Data_AT_FilteredDate/LangSon_FilteredDate.csv')
    df_LaoCai = pd.read_csv('../Data_AT_FilteredDate/LaoCai_FilteredDate.csv')
    df_NoiBai = pd.read_csv('../Data_AT_FilteredDate/NoiBai_FilteredDate.csv')
    df_PhuBai = pd.read_csv('../Data_AT_FilteredDate/PhuBai_FilteredDate.csv')
    df_QuyNhon = pd.read_csv('../Data_AT_FilteredDate/QuyNhon_FilteredDate.csv')
    df_TPHCM = pd.read_csv('../Data_AT_FilteredDate/TPHCM_FilteredDate.csv')
    df_Vinh = pd.read_csv('../Data_AT_FilteredDate/Vinh_FilteredDate.csv')

    station_df = {
        'Cà Mau': df_CaMau,
        'Lạng Sơn': df_LangSon,
        'Lào Cai': df_LaoCai,
        'Nội Bài': df_NoiBai,
        'Phú Bài': df_PhuBai,
        'Quy Nhơn': df_QuyNhon,
        'TPHCM': df_TPHCM,
        'Vinh': df_Vinh
    }

    station_order = ['Nội Bài', 'Lạng Sơn', 'Lào Cai', 'Vinh', 'Phú Bài', 'Quy Nhơn', 'TPHCM', 'Cà Mau']

    station_info = get_station_info(station_df)
    print(station_info)

    feature_name = {
        'DEW_2': 'Điểm sương ở độ cao 2 mét',
        'TMP_2': 'Nhiệt độ ở độ cao 2 mét',
        'RH': 'Độ ẩm tương đối',
        'AT mean': 'Nhiệt độ cảm nhận trung bình trong ngày',
        'AT max': 'Nhiệt độ cảm nhận cực đại trong ngày'
    }

    region_dict = {
        # Tây Bắc
        'Sơn La': 'Tây Bắc', 'Điện Biên': 'Tây Bắc', 'Lai Châu': 'Tây Bắc',
        'Lào Cai': 'Tây Bắc', 'Yên Bái': 'Tây Bắc', 'Hoà Bình': 'Tây Bắc',

        # Đông Bắc
        'Lạng Sơn': 'Đông Bắc', 'Cao Bằng': 'Đông Bắc', 'Bắc Kạn': 'Đông Bắc',
        'Thái Nguyên': 'Đông Bắc', 'Quảng Ninh': 'Đông Bắc', 'Bắc Giang': 'Đông Bắc',
        'Phú Thọ': 'Đông Bắc', 'Tuyên Quang': 'Đông Bắc', 'Hà Giang': 'Đông Bắc',

        # Đồng bằng sông Hồng
        'Hà Nội': 'Đồng bằng sông Hồng', 'Hải Phòng': 'Đồng bằng sông Hồng',
        'Hải Dương': 'Đồng bằng sông Hồng', 'Hưng Yên': 'Đồng bằng sông Hồng',
        'Thái Bình': 'Đồng bằng sông Hồng', 'Hà Nam': 'Đồng bằng sông Hồng',
        'Nam Định': 'Đồng bằng sông Hồng', 'Ninh Bình': 'Đồng bằng sông Hồng',
        'Vĩnh Phúc': 'Đồng bằng sông Hồng', 'Bắc Ninh': 'Đồng bằng sông Hồng',

        # Bắc Trung Bộ
        'Thanh Hóa': 'Bắc Trung Bộ', 'Nghệ An': 'Bắc Trung Bộ',
        'Hà Tĩnh': 'Bắc Trung Bộ', 'Quảng Bình': 'Bắc Trung Bộ',
        'Quảng Trị': 'Bắc Trung Bộ', 'Thừa Thiên Huế': 'Bắc Trung Bộ',

        # Duyên hải Nam Trung Bộ
        'Đà Nẵng': 'Duyên hải Nam Trung Bộ', 'Quảng Nam': 'Duyên hải Nam Trung Bộ',
        'Quảng Ngãi': 'Duyên hải Nam Trung Bộ', 'Bình Định': 'Duyên hải Nam Trung Bộ',
        'Phú Yên': 'Duyên hải Nam Trung Bộ', 'Khánh Hòa': 'Duyên hải Nam Trung Bộ',
        'Ninh Thuận': 'Duyên hải Nam Trung Bộ', 'Bình Thuận': 'Duyên hải Nam Trung Bộ',

        # Tây Nguyên
        'Kon Tum': 'Tây Nguyên', 'Gia Lai': 'Tây Nguyên',
        'Đắk Lắk': 'Tây Nguyên', 'Đắk Nông': 'Tây Nguyên',
        'Lâm Đồng': 'Tây Nguyên',

        # Đông Nam Bộ
        'Bình Phước': 'Đông Nam Bộ', 'Tây Ninh': 'Đông Nam Bộ',
        'Bình Dương': 'Đông Nam Bộ', 'Đồng Nai': 'Đông Nam Bộ',
        'Bà Rịa - Vũng Tàu': 'Đông Nam Bộ', 'Hồ Chí Minh': 'Đông Nam Bộ',

        # Đồng bằng sông Cửu Long
        'Long An': 'Đồng bằng sông Cửu Long', 'Tiền Giang': 'Đồng bằng sông Cửu Long',
        'Bến Tre': 'Đồng bằng sông Cửu Long', 'Trà Vinh': 'Đồng bằng sông Cửu Long',
        'Vĩnh Long': 'Đồng bằng sông Cửu Long', 'Đồng Tháp': 'Đồng bằng sông Cửu Long',
        'An Giang': 'Đồng bằng sông Cửu Long', 'Kiên Giang': 'Đồng bằng sông Cửu Long',
        'Cần Thơ': 'Đồng bằng sông Cửu Long', 'Hậu Giang': 'Đồng bằng sông Cửu Long',
        'Sóc Trăng': 'Đồng bằng sông Cửu Long', 'Bạc Liêu': 'Đồng bằng sông Cửu Long',
        'Cà Mau': 'Đồng bằng sông Cửu Long'
    }

    plot_1(station_df, station_info, station_order, region_dict, 'TMP_2', feature_name)
    plot_1(station_df, station_info, station_order, region_dict, 'DEW_2', feature_name)
    plot_1(station_df, station_info, station_order, region_dict, 'RH', feature_name)
    plot_1(station_df, station_info, station_order, region_dict, 'AT mean', feature_name)
    plot_1(station_df, station_info, station_order, region_dict, 'AT max', feature_name)

    # plot_2(station_df, 'TMP_2', feature_name)
    # plot_2(station_df, 'DEW_2', feature_name)
    # plot_2(station_df, 'RH', feature_name)
    # plot_2(station_df, 'AT mean', feature_name)
    # plot_2(station_df, 'AT max', feature_name)

    exit()
