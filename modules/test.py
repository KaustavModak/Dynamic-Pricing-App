import pandas as pd

# Load the full metadata CSV
file_path = '../../data/full_retail_meta_dataset.csv'
df = pd.read_csv(file_path)

# Filter out the target row
df = df[
    ~(
        (df["product_name"] == "Organic Amla Juice 500ml") &
        (df["category"] == "health drinks") &
        (df["location_zone"] == "Tier-2") &
        (df["state"] == "Maharashtra")
    )
]

# Save the updated CSV
df.to_csv(file_path, index=False)
print("✅ Row deleted and file saved.")
