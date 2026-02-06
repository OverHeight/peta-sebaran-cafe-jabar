import os
import leafmap.leafmap as leafmap

def pinPoint_processor(df, output_name="pinPoint"):
    out_dir = os.path.expanduser("./data/spatial")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Path untuk output
    out_shp = os.path.join(out_dir, f"{output_name}.shp")
    out_geojson = os.path.join(out_dir, f"{output_name}.geojson")

    # Simpan DataFrame sementara menjadi CSV
    temp_csv = os.path.join(out_dir, "temp_data.csv")
    df.to_csv(temp_csv, index=False)

    # Proses Konversi
    leafmap.csv_to_shp(temp_csv, out_shp)
    leafmap.csv_to_geojson(temp_csv, out_geojson)
    
    return out_shp, out_geojson