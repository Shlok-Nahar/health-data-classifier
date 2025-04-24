import pandas as pd
from sklearn.utils import resample

# Load the raw data
df = pd.read_csv("rawData/raw_data.csv")
df['startDate'] = pd.to_datetime(df['startDate'])
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df = df.dropna(subset=['value'])

# Function to match date range for sampling
def sample_by_date_range(df_source, df_target, n_samples):
    min_date, max_date = df_target['startDate'].min(), df_target['startDate'].max()
    df_filtered = df_source[(df_source['startDate'] >= min_date) & (df_source['startDate'] <= max_date)]

    if len(df_filtered) >= n_samples:
        return df_filtered.sample(n=n_samples, random_state=42)
    else:
        return resample(df_filtered, replace=True, n_samples=n_samples, random_state=42)

# Containers for processed data
downsampled_data = []
upsampled_data = []
midway_data = []

downsample_counts = {'shlok': 0, 'akhil': 0}
upsample_counts = {'shlok': 0, 'akhil': 0}
midway_counts = {'shlok': 0, 'akhil': 0}

# Group by data_type
for data_type in df['data_type'].unique():
    shlok_df = df[(df['person'] == 'shlok') & (df['data_type'] == data_type)]
    akhil_df = df[(df['person'] == 'akhil') & (df['data_type'] == data_type)]

    n_shlok = len(shlok_df)
    n_akhil = len(akhil_df)

    if n_shlok == 0 or n_akhil == 0:
        continue

    # --- Downsample ---
    akhil_down = sample_by_date_range(akhil_df, shlok_df, n_shlok)
    downsampled_data.append(pd.concat([shlok_df, akhil_down], ignore_index=True))
    downsample_counts['shlok'] += len(shlok_df)
    downsample_counts['akhil'] += len(akhil_down)

    # --- Upsample ---
    shlok_upsampled = resample(
        shlok_df,
        replace=True,
        n_samples=n_akhil,
        random_state=42
    )
    upsampled_data.append(pd.concat([shlok_upsampled, akhil_df], ignore_index=True))
    upsample_counts['shlok'] += len(shlok_upsampled)
    upsample_counts['akhil'] += len(akhil_df)

    # --- Midway ---
    mid_count = (n_shlok + n_akhil) // 2
    akhil_mid = sample_by_date_range(akhil_df, shlok_df, mid_count)
    shlok_mid = resample(
        shlok_df,
        replace=True,
        n_samples=mid_count,
        random_state=42
    )
    midway_data.append(pd.concat([shlok_mid, akhil_mid], ignore_index=True))
    midway_counts['shlok'] += len(shlok_mid)
    midway_counts['akhil'] += len(akhil_mid)

# Save the output files
pd.concat(downsampled_data, ignore_index=True).to_csv("data/downsampled.csv", index=False)
pd.concat(upsampled_data, ignore_index=True).to_csv("data/upsampled.csv", index=False)
pd.concat(midway_data, ignore_index=True).to_csv("data/midway.csv", index=False)

# Print summaries
print(f"Exported {downsample_counts['shlok']} records to 'data/downsampled.csv' with person='shlok'.")
print(f"Exported {downsample_counts['akhil']} records to 'data/downsampled.csv' with person='akhil'.")
print(f"Exported {upsample_counts['shlok']} records to 'data/upsampled.csv' with person='shlok'.")
print(f"Exported {upsample_counts['akhil']} records to 'data/upsampled.csv' with person='akhil'.")
print(f"Exported {midway_counts['shlok']} records to 'data/midway.csv' with person='shlok'.")
print(f"Exported {midway_counts['akhil']} records to 'data/midway.csv' with person='akhil'.")
