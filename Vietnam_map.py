import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Đọc shapefile cấp tỉnh của Việt Nam
vietnam = gpd.read_file('.\gadm41_VNM_shp', layer='gadm41_VNM_1')

# Dữ liệu các điểm
stations = pd.DataFrame({
    'name': ['Nội Bài', 'Lạng Sơn', 'Lào Cai', 'Vinh', 'Phú Bài', 'Quy Nhơn', 'Tp.HCM', 'Cà Mau'],
    'lat': [21.2187, 21.8530, 22.4837, 18.6790, 16.4323, 13.7695, 10.8231, 9.1769],
    'lon': [105.8019, 106.7613, 103.9771, 105.6824, 107.5850, 109.2208, 106.6297, 105.1500],
    'region': ['Đồng bằng sông Hồng', 'Đông Bắc', 'Tây Bắc', 'Bắc Trung Bộ', 'Bắc Trung Bộ',
               'Duyên hải Nam Trung Bộ', 'Đông Nam Bộ', 'Đồng bằng sông Cửu Long']
})

# Mapping tỉnh thành với vùng
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

# Thêm cột region vào GeoDataFrame
vietnam['region'] = vietnam['NAME_1'].map(region_dict)

# Màu cho từng vùng
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

# Vẽ bản đồ
fig, ax = plt.subplots(figsize=(15, 20))

# Vẽ từng vùng với màu khác nhau
for region in colors.keys():
    region_data = vietnam[vietnam['region'] == region]
    if not region_data.empty:
        region_data.plot(ax=ax,
                         color=colors[region],
                         edgecolor='white',
                         linewidth=0.5,
                         label=region)

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

# Thêm các điểm đánh dấu
plt.scatter(stations['lon'], stations['lat'],
            c='#000000',
            s=150,
            marker='o',
            edgecolor='white',
            linewidth=1,
            label='Observation Stations')

# Thêm tên các trạm
for idx, row in stations.iterrows():
    plt.annotate(f"{row['name']}\n({row['region']})",
                 (row['lon'], row['lat']),
                 xytext=(10, 10),
                 textcoords='offset points',
                 fontsize=12, fontfamily='Times New Roman',
                 bbox=dict(facecolor='white', alpha=0.7))
plt.subplots_adjust(top=0.8)
plt.title('PHÂN BỐ KHÔNG GIAN CỦA CÁC TRẠM KHÍ TƯỢNG NGHIÊN CỨU', fontweight='bold', fontsize=18, fontfamily='Times New Roman')
ax.set_aspect('equal')
plt.axis('off')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.savefig('vietnam_regions_map.png',
            dpi=300,
            bbox_inches='tight')
plt.close()