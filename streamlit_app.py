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
    # Menggunakan data dummy jika file belum diupload
    # Pastikan file csv memiliki kolom: nama, wilayah, lat, lon, dan sumber (opsional)
    try:
        df = pd.read_csv("./data/spatial/coffee_shop_jawa_barat_with_address.csv")
    except:
        # Data fallback jika file tidak ditemukan sama sekali
        data = {
            'nama': ['Starbucks', 'SPBU Dago', 'Tanpa Nama', 'Warung Makan'],
            'wilayah': ['Kota Bandung', 'Kota Bandung', 'Kabupaten Bandung', 'Sumedang'],
            'lat': [-6.894, -6.869, -6.8644, -6.892],
            'lon': [107.6055, 107.6209, 107.6279, 107.7641],
            'sumber': ['Google Maps', 'Google Maps', 'Manual', 'Survey']
        }
        df = pd.DataFrame(data)

# Pastikan kolom sumber ada untuk kebutuhan grafik
if 'sumber' not in df.columns:
    df['sumber'] = 'Data Internal'

# --- TAMPILAN UTAMA ---
st.title("☕ Dashboard Sebaran Café")

col_map, col_info = st.columns([2.5, 1])

with col_map:
    # Inisialisasi Map
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=11)
    
    # Tambah Marker
    for _, row in df.iterrows():
        folium.Marker(
            [row['lat'], row['lon']], 
            popup = f"Nama: {row['nama']}\nWilayah: {row['wilayah']}",
            icon=folium.Icon(color='orange', icon='coffee', prefix='fa')
        ).add_to(m)
    
    st_folium(m, width='100%', height=550)

with col_info:
    st.subheader("📊 Detail Data pie chart wilayah")
    st.metric("Total Titik", len(df))
    
    # --- TABS UNTUK PIE CHART ---
    tab_wilayah, tab_sumber = st.tabs(["📍 Wilayah", "ℹ️ Sumber"])

    with tab_wilayah:
        # Hitung data wilayah
        wilayah_counts = df['wilayah'].value_counts().reset_index()
        wilayah_counts.columns = ['Kategori', 'Jumlah']

        chart_wilayah = alt.Chart(wilayah_counts).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Jumlah", type="quantitative"),
            color=alt.Color(field="Kategori", type="nominal", legend=alt.Legend(orient="bottom", title=None)),
            tooltip=['Kategori', 'Jumlah']
        ).properties(height=350)
        
        st.altair_chart(chart_wilayah, use_container_width=True)

    with tab_sumber:
        # Hitung data sumber
        sumber_counts = df['sumber'].value_counts().reset_index()
        sumber_counts.columns = ['Kategori', 'Jumlah']

        chart_sumber = alt.Chart(sumber_counts).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Jumlah", type="quantitative"),
            color=alt.Color(field="Kategori", type="nominal", scale=alt.Scale(scheme='set2'), legend=alt.Legend(orient="bottom", title=None)),
            tooltip=['Kategori', 'Jumlah']
        ).properties(height=350)
        
        st.altair_chart(chart_sumber, use_container_width=True)

# === TABEL DATA (Update: alamat_asli diganti wilayah) ===
st.subheader("📋 Dataset Lokasi Café")  

# Menampilkan kolom wilayah menggantikan alamat_asli
st.dataframe(
    df[['nama', 'wilayah', 'lat', 'lon']],
    use_container_width=True,
    height=350
)