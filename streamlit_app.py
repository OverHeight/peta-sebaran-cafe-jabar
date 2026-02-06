import streamlit as st
import pandas as pd
import folium
import altair as alt
from streamlit_folium import st_folium


# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Peta Café Jabar", layout="wide")

# --- SIDEBAR & UPLOAD ---
with st.sidebar:
    st.title("Settings")
    uploaded_file = st.file_uploader("Upload CSV Lokasi", type=['csv'])
    process_btn = st.button("Generate Spatial Files")

# --- LOAD DATA ---
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Data dummy atau default
    df = pd.read_csv("./data/spatial/coffee_shop_jawa_barat_with_address.csv")

# --- TAMPILAN UTAMA ---
st.title("☕ Dashboard Sebaran Café")

col_map, col_info = st.columns([3, 1])

with col_map:
    # Inisialisasi Map
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=9)
    
    # Tambah Marker
    for _, row in df.iterrows():
        folium.Marker(
            [row['lat'], row['lon']], 
            popup = f"Nama   : {row['nama']}\nAlamat : {row['wilayah']}",
            icon=folium.Icon(color='orange', icon='coffee', prefix='fa')
        ).add_to(m)
    
    st_folium(m, width='100%', height='600')

    with col_info:
        st.subheader("Detail Data")
        st.write(f"Jumlah Titik: {len(df)}")

        # === TOGGLE BAR CHART ===
        show_top = st.toggle("Diagram Persentase Café Berdasarkan wilayah", value=True)

        location_count = (
            df['wilayah']
            .value_counts()
            .reset_index()
        )
        location_count.columns = ['Wilayah', 'Jumlah']


        if show_top:
            location_count = location_count.head(10)
            chart_title = "Wilayah Berdasarkan Jumlah Lokasi Café"
        else:
            chart_title = "Jumlah Lokasi Café per Wilayah"

        chart = (
            alt.Chart(location_count)
            .mark_bar(
                cornerRadiusTopLeft=6,
                cornerRadiusTopRight=6
            )
            .encode(
                x=alt.X(
                    'Nama Cafe:N',
                    sort='-y',
                    title=None
                ),
                y=alt.Y(
                    'Jumlah:Q',
                    title='Jumlah Lokasi'
                ),
                tooltip=[
                    alt.Tooltip('Nama Cafe:N', title='Café'),
                    alt.Tooltip('Jumlah:Q', title='Jumlah')
                ],
                color=alt.value('#f97316')
            )
            .properties(
                height=300,
                title=chart_title
            )
        )

        st.altair_chart(chart, use_container_width=True,
                        height=350)
        
    # === TABEL DATA ===
st.subheader("📋 Dataset Lokasi Café")  

st.dataframe(
    df[['nama', 'alamat_asli', 'lat', 'lon']],
    use_container_width=True,
    height=350
)
