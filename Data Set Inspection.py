import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = r"C:\Users\julia\Downloads\by_experiment_11.csv"
df = pd.read_csv(file_path)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Step 1: Visualize each sensor's data
sensor_types = df['sensor_type'].unique()
for sensor in sensor_types:
    sensor_data = df[df['sensor_type'] == sensor]
    plt.figure(figsize=(10, 4))
    sns.lineplot(data=sensor_data, x='timestamp', y='value')
    plt.title(f'Time Series of {sensor}')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.show()


# Step 2: Function to inject synthetic anomalies
def inject_anomalies(data, sensor_type, anomaly_type='spike', magnitude=3, anomaly_percentage=0.01):
    """
    Injects anomalies into the data for a specific sensor type.

    Parameters:
        data (pd.DataFrame): The dataframe containing the data.
        sensor_type (str): The sensor type to inject anomalies into.
        anomaly_type (str): The type of anomaly ('spike' or 'drop').
        magnitude (float): Number of standard deviations to add/subtract.
        anomaly_percentage (float): Proportion of points to turn into anomalies.

    Returns:
        pd.DataFrame: Dataframe with anomalies injected in the specified sensor type.
    """
    sensor_data = data[data['sensor_type'] == sensor_type].copy()
    num_anomalies = int(len(sensor_data) * anomaly_percentage)

    # Get mean and std for the specified sensor type
    mean_val = sensor_data['value'].mean()
    std_val = sensor_data['value'].std()

    # Randomly choose indices to inject anomalies
    anomaly_indices = np.random.choice(sensor_data.index, num_anomalies, replace=False)

    # Inject anomalies based on type
    for idx in anomaly_indices:
        if anomaly_type == 'spike':
            sensor_data.at[idx, 'value'] += magnitude * std_val  # Spike anomaly
        elif anomaly_type == 'drop':
            sensor_data.at[idx, 'value'] -= magnitude * std_val  # Drop anomaly

    # Merge with original data
    data.update(sensor_data)
    return data


# Step 3: Inject anomalies in relevant sensors
df_with_anomalies = df.copy()
df_with_anomalies = inject_anomalies(df_with_anomalies, 'temperature1', 'spike', magnitude=3, anomaly_percentage=0.02)
df_with_anomalies = inject_anomalies(df_with_anomalies, 'pressure', 'spike', magnitude=4, anomaly_percentage=0.01)
df_with_anomalies = inject_anomalies(df_with_anomalies, 'als', 'drop', magnitude=2, anomaly_percentage=0.02)

# Step 4: Visualize original vs anomalous data for selected sensors
for sensor in ['temperature1', 'pressure', 'als']:
    original_data = df[df['sensor_type'] == sensor]
    anomalous_data = df_with_anomalies[df_with_anomalies['sensor_type'] == sensor]
    plt.figure(figsize=(10, 4))
    sns.lineplot(data=original_data, x='timestamp', y='value', label='Original', linestyle="--")
    sns.lineplot(data=anomalous_data, x='timestamp', y='value', label='With Anomalies')
    plt.title(f'Anomaly Injection in {sensor}')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
