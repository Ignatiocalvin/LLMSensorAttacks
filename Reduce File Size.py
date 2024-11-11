import pandas as pd
import os

# Define file paths
input_file = r"C:\Users\julia\Downloads\by_experiment_11.csv"
output_file = r"C:\Users\julia\Downloads\by_experiment_11_reduced.csv"

# Desired size in bytes (500 MB)
target_size = 500 * 1024 * 1024  # 500 MB

# Read the original CSV file
df = pd.read_csv(input_file, low_memory=False)

# Calculate the approximate size of a single row
sample_size = 1000
sample = df.sample(n=sample_size)
row_size = sample.memory_usage(deep=True).sum() / sample_size

# Estimate the number of rows needed for a 500 MB file
num_rows = int(target_size / row_size)

# Sample the dataframe to match the target size
reduced_df = df.sample(n=min(num_rows, len(df)), random_state=42)

# Save the reduced dataframe to a new CSV file
reduced_df.to_csv(output_file, index=False)

# Check the file size
file_size = os.path.getsize(output_file)
print(f"Reduced file size: {file_size / (1024 * 1024):.2f} MB")
