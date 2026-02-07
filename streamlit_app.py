import streamlit as st
import pandas as pd
import folium
import altair as alt
from streamlit_folium import st_folium
st.set_page_config(page_title="Peta Café Jabar", layout="wide")

with st.sidebar:
    st.title("⚙️ Pengaturan")
    uploaded_file = st.file_uploader("Unggah CSV Lokasi", type=['csv'])
    st.info("Pastikan CSV memiliki kolom: nama, wilayah, lat, lon, dan sumber.")
    process_btn = st.button("Proses Data")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("./data/spatial/coffee_shop_jawa_barat_with_address.csv")
    except:
        data = {
            'nama': ['Starbucks', 'SPBU Dago', 'Tanpa Nama', 'Warung Makan', 'Habenagen Coffeeshop', 'The Oldway Cafe', 'Kabut Salju', 'Cokotetra', 'YUTAKANA'],
            'wilayah': ['Kota Bandung', 'Kota Bandung', 'Kabupaten Bandung', 'Sumedang', 'Kota Bandung', 'Kota Bandung', 'Kota Bandung', 'Kota Bandung', 'Kota Bandung'],
            'lat': [-6.894, -6.869, -6.8644, -6.892, -6.9021, -6.907, -6.9183, -6.8785, -6.8835],
            'lon': [107.6055, 107.6209, 107.6279, 107.7641, 107.6041, 107.6231, 107.6143, 107.6168, 107.6147],
            'sumber': ['Google Maps', 'Google Maps', 'Manual', 'Survey', 'Google Maps', 'Google Maps', 'Google Maps', 'Google Maps', 'Google Maps']
        }
        df = pd.DataFrame(data)

if 'sumber' not in df.columns:
    df['sumber'] = 'Data Internal'


st.title("☕ Dashboard Sebaran Café Jawa Barat")
st.markdown("---")


col_map, col_table = st.columns([1.8, 1.2])

with col_map:
    st.subheader("Peta Sebaran Lokasi")
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=11)
    for _, row in df.iterrows():
        folium.Marker(
            [row['lat'], row['lon']], 
            popup = f"**{row['nama']}**<br>Wilayah: {row['wilayah']}",
            tooltip=row['nama'],
            icon=folium.Icon(color='orange', icon='coffee', prefix='fa')
        ).add_to(m)
    st_folium(m, width='100%', height=450)

with col_table:
    st.subheader("Dataset Lokasi Café")
    st.write(f"Menampilkan **{len(df)}** titik koordinat.")
    st.dataframe(
        df[['nama', 'wilayah', 'lat', 'lon']], 
        use_container_width=True,
        height=400
    )

st.markdown("---")


st.subheader("Analisis Distribusi Data")
col_pie1, col_pie2, col_bar = st.columns([1, 1, 1.5])

with col_pie1:
    # Pie Chart Wilayah
    wilayah_counts = df['wilayah'].value_counts().reset_index()
    wilayah_counts.columns = ['Wilayah', 'Jumlah']

    chart_wilayah = alt.Chart(wilayah_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Jumlah", type="quantitative"),
        color=alt.Color(field="Wilayah", type="nominal", legend=alt.Legend(orient="bottom", columns=1)),
        tooltip=['Wilayah', 'Jumlah']
    ).properties(height=350, title="Proporsi per Wilayah")
    st.altair_chart(chart_wilayah, use_container_width=True)

with col_pie2:
    # Pie Chart Sumber
    sumber_counts = df['sumber'].value_counts().reset_index()
    sumber_counts.columns = ['Sumber', 'Jumlah']

    chart_sumber = alt.Chart(sumber_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Jumlah", type="quantitative"),
        color=alt.Color(field="Sumber", type="nominal", scale=alt.Scale(scheme='pastel1'), legend=alt.Legend(orient="bottom")),
        tooltip=['Sumber', 'Jumlah']
    ).properties(height=350, title="Proporsi per Sumber")
    st.altair_chart(chart_sumber, use_container_width=True)

with col_bar:
    # Bar Chart Wilayah (Memperbaiki masalah 'undefined' sebelumnya)
    chart_bar = alt.Chart(wilayah_counts).mark_bar(
        color='#f97316', 
        cornerRadiusTopLeft=5, 
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X('Wilayah:N', sort='-y', title=None),
        y=alt.Y('Jumlah:Q', title='Jumlah Lokasi'),
        tooltip=['Wilayah', 'Jumlah']
    ).properties(height=350, title="Jumlah Café per Wilayah")
    
    st.altair_chart(chart_bar, use_container_width=True)