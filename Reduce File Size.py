import dask.dataframe as dd
import os

# Define file paths
input_file = r"C:\Users\julia\Downloads\by_experiment_11.csv"
output_file = r"C:\Users\julia\Downloads\by_experiment_11_reduced.csv"
temp_output = r"C:\Users\julia\Downloads\by_experiment_11_temp_reduced.csv"

# Desired size in bytes (500 MB)
target_size = 500 * 1024 * 1024  # 500 MB

# Read the CSV using Dask
print("Reading the CSV file using Dask...")
df = dd.read_csv(input_file, assume_missing=True)

# Initial sample fraction
sample_fraction = 0.1  # Start with a 10% sample
tolerance = 0.05  # Allowable tolerance (5%) for file size deviation
max_iterations = 5

for i in range(max_iterations):
    print(f"Iteration {i + 1}: Sampling with fraction {sample_fraction:.4f}...")
    # Sample the DataFrame
    sampled_df = df.sample(frac=sample_fraction, random_state=42)

    # Write the sampled data to a temporary CSV file
    print("Writing the sampled data to a temporary CSV file...")
    sampled_df.to_csv(temp_output, single_file=True, index=False)

    # Check the file size
    file_size = os.path.getsize(temp_output)
    print(f"Current file size: {file_size / (1024 * 1024):.2f} MB")

    # Check if the size is within the desired range
    if abs(file_size - target_size) <= target_size * tolerance:
        print("Target size achieved. Saving the final file...")
        os.rename(temp_output, output_file)
        break

    # Adjust the sampling fraction based on the observed size
    size_ratio = target_size / file_size
    sample_fraction *= size_ratio
    print(f"Adjusting sample fraction to {sample_fraction:.4f}...")

else:
    print("Max iterations reached. Saving the closest approximation...")
    os.rename(temp_output, output_file)

# Final file size check
final_size = os.path.getsize(output_file)
print(f"Final reduced file size: {final_size / (1024 * 1024):.2f} MB")