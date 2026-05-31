import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy import sparse

print("Downloading January 2023 data...")
url_jan = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
df_jan = pd.read_parquet(url_jan)

print("Downloading February 2023 data...")
url_feb = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-02.parquet"
df_feb = pd.read_parquet(url_feb)

# Q1
n_columns = df_jan.shape[1]
print(f"Q1: Number of columns in January data: {n_columns}")

# Q2
df_jan['duration'] = (df_jan['tpep_dropoff_datetime'] - df_jan['tpep_pickup_datetime']).dt.total_seconds() / 60
duration_std = df_jan['duration'].std()
print(f"Q2: Standard deviation of duration (minutes): {duration_std:.4f}")

# Q3
n_original = len(df_jan)
df_jan_filtered = df_jan[(df_jan['duration'] >= 1) & (df_jan['duration'] <= 60)]
n_filtered = len(df_jan_filtered)
fraction_remaining = n_filtered / n_original
print(f"Q3: Fraction of trips remaining after filtering outliers: {fraction_remaining:.4f}")

# Q4 - Use sparse matrices with DictVectorizer-style encoding
# PU and DO location IDs are encoded separately (PULocationID=1 is different from DOLocationID=1)
df = df_jan_filtered.copy()

pu_codes = df['PULocationID'].values.astype(np.int32)
do_codes = df['DOLocationID'].values.astype(np.int32)

# Offset DO codes so they don't overlap with PU codes
# PU codes: 1 to max_pu, DO codes: max_pu+1 to max_pu+max_do
max_pu = int(df['PULocationID'].max())
max_do = int(df['DOLocationID'].max())

# Add 1 to codes to leave index 0 unused (matches DictVectorizer behavior)
pu_indices = pu_codes  # Keep as-is (1-indexed)
do_indices = do_codes + max_pu + 1  # Offset to avoid overlap

n_features = max_pu + max_do + 2  # +2 for 0-index and offset
print(f"Creating sparse matrix: PU locations [{max_pu}], DO locations [{max_do}], total features: {n_features}")

indices = np.arange(len(df))
rows = np.concatenate([indices, indices])
cols = np.concatenate([pu_indices, do_indices])
data = np.ones(len(rows), dtype=np.float64)

X_train = sparse.csr_matrix((data, (rows, cols)), shape=(len(df), n_features))

dimensionality = X_train.shape[1]
print(f"Q4: Feature matrix dimensionality after one-hot encoding: {dimensionality}")

# Q5
y_train = df['duration'].values
print("Training LinearRegression model...")
lr = LinearRegression()
lr.fit(X_train, y_train)
y_train_pred = lr.predict(X_train)
rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
print(f"Q5: RMSE on training data: {rmse_train:.4f}")

# Q6 - Process February data
df_feb['duration'] = (df_feb['tpep_dropoff_datetime'] - df_feb['tpep_pickup_datetime']).dt.total_seconds() / 60
df_feb_filtered = df_feb[(df_feb['duration'] >= 1) & (df_feb['duration'] <= 60)]

feb_pu = df_feb_filtered['PULocationID'].values.astype(np.int32)
feb_do = df_feb_filtered['DOLocationID'].values.astype(np.int32)

# Apply same encoding
feb_pu_indices = feb_pu
feb_do_indices = feb_do + max_pu + 1

print(f"Creating sparse matrix for validation data...")
n_val = len(df_feb_filtered)
val_indices = np.arange(n_val)

val_rows = np.concatenate([val_indices, val_indices])
val_cols = np.concatenate([feb_pu_indices, feb_do_indices])
val_data = np.ones(len(val_rows), dtype=np.float64)

X_val = sparse.csr_matrix((val_data, (val_rows, val_cols)), shape=(n_val, n_features))

y_val = df_feb_filtered['duration'].values

print("Predicting on validation data...")
y_val_pred = lr.predict(X_val)
rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))
print(f"Q6: RMSE on validation (February) data: {rmse_val:.4f}")

print("\n=== SUMMARY ===")
print(f"Q1: {n_columns}")
print(f"Q2: {duration_std:.4f}")
print(f"Q3: {fraction_remaining:.4f}")
print(f"Q4: {dimensionality}")
print(f"Q5: {rmse_train:.4f}")
print(f"Q6: {rmse_val:.4f}")
