import pandas as pd
import time
from geopy.geocoders import Nominatim

INPUT_CSV = "data/raw/coffee_shop_jawa_barat_clean.csv"
OUTPUT_CSV = "data/spatial/coffee_shop_jawa_barat_with_address.csv"

geolocator = Nominatim(user_agent="cafe_sebaran_jabar")

def reverse_geocode(lat, lon):
    try:
        location = geolocator.reverse(
            (lat, lon),
            language="id",
            timeout=10
        )
        return location.address if location else ""
    except Exception as e:
        print(f"Error at ({lat}, {lon}): {e}")
        return ""

def main():
    df = pd.read_csv(INPUT_CSV)

    df["alamat_asli"] = ""

    total = len(df)
    print(f"Reverse geocoding {total} data \n")

    for i, row in df.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        address = reverse_geocode(lat, lon)
        df.at[i, "alamat_asli"] = address

        if (i + 1) % 10 == 0 or i == 0:
            print(f"Progress: {i + 1}/{total}")

        # rate limit soalnya nomatim ngasih batas 1 request per detik
        time.sleep(1) 
        
    print("Saved to:", OUTPUT_CSV)

    df.to_csv(OUTPUT_CSV, index=False)


if __name__ == "__main__":
    main()
