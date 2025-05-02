import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.dates as mdates  # <-- Added

sns.set(style="whitegrid")

def generate_comparison_plots(data_path, output_pdf, sample_size=1000):
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip().str.lower()
    df['startdate'] = pd.to_datetime(df['startdate'], errors='coerce')
    df['enddate'] = pd.to_datetime(df['enddate'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['duration_sec'] = (df['enddate'] - df['startdate']).dt.total_seconds()
    df['hour'] = df['startdate'].dt.hour
    df['date'] = df['startdate'].dt.date
    df['person'] = df['person'].str.strip().astype(str)
    df = df.dropna(subset=['person'])

    sampled_df = pd.concat([ 
        group.sample(min(len(group), sample_size // 2)) 
        for _, group in df.groupby('person') 
    ])

    with PdfPages(output_pdf) as pdf:
        # 1. Line Plot: Value Over Time with year-only x-axis
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=sampled_df, x='startdate', y='value', hue='person')
        plt.title("Value Over Time by Person")
        plt.ylabel("Value")

        # Format x-axis to show only years
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.xticks(rotation=45)

        plt.legend(loc='upper left')
        pdf.savefig(); plt.close()

        # 2. Bar Plot: Total Value per Data Type (taller figure)
        plt.figure(figsize=(10, 12))
        sns.barplot(data=sampled_df, x='data_type', y='value', hue='person', estimator='sum', errorbar=None)
        plt.title("Total Value per Data Type by Person")
        plt.xticks(rotation=45)
        pdf.savefig(); plt.close()

        # 3. PCA Scatter Plot
        features_df = sampled_df[['value', 'duration_sec', 'hour']].dropna()
        if not features_df.empty:
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features_df)
            pca = PCA(n_components=2).fit_transform(features_scaled)
            plt.figure(figsize=(8, 6))
            plt.scatter(
                pca[:, 0], pca[:, 1],
                c=sampled_df.loc[features_df.index, 'person'].astype('category').cat.codes,
                cmap='viridis', alpha=0.5
            )
            plt.title("PCA of Features by Person")
            pdf.savefig(); plt.close()

# Run only downsampled version
generate_comparison_plots("data/downsampled.csv", "visualisations/downsampled_comparison.pdf", sample_size=10000)

print("Partial-data comparison generated.")
