import folium
import pandas as pd
import numpy as np

# تحميل البيانات
df = pd.read_csv(r"C:\Users\96653\Downloads\recommendations.csv")

# حدود السعودية الجنوبية والشمالية
north = 28.5
south = 19.0

# عدد الصفوف
n = len(df)

# توليد Latitude عشوائي
latitudes = np.random.uniform(low=south, high=north, size=n)

# توليد Longitude بناءً على الميل لليسار
longitudes = []
for lat in latitudes:
    if lat >= 26:
        # شمال السعودية → ميل نحو الغرب
        lon = np.random.uniform(low=38.5, high=45.5)
    else:
        # جنوب السعودية → ميل نحو الشرق
        lon = np.random.uniform(low=41.5, high=50.5)
    longitudes.append(lon)

# تعيين الإحداثيات الجديدة
df["Latitude"] = latitudes
df["Longitude"] = longitudes
print(df['Soil_Type'].unique())
# إنشاء الخريطة
m = folium.Map(location=[df.iloc[0]["Latitude"], df.iloc[0]["Longitude"]],
               zoom_start=6,
               tiles="cartodb positron")

# إضافة النقاط على الخريطة
for _, row in df.iterrows():
    popup_text = f"""
    <b>Soil Type:</b> {row['Soil_Type']}<br>
    <b>Desertification:</b> {row['Desertification_Level']}<br>
    <b>NDVI:</b> {row['NDVI']}<br>
    <b>NDWI:</b> {row['NDWI']}<br>
    <b>LST Day:</b> {row['LST_Day']} K<br>
    <b>LST Night:</b> {row['LST_Night']} K<br><br>
    <b>🌱 Recommended Plant:</b><br>{row['Recommended_Plant']}
    """

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_text, max_width=400),
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(m)

# حفظ الخريطة
m.save(r"C:\Users\96653\Downloads\plant_recommendation_map.html")
print("✅ Map saved as 'plant_recommendation_map.html'")
