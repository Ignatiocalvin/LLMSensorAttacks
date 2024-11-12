import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import load_model

def prepare_single_row(new_row, previous_data, window_size=60):
    # Combine the new row with previous data
    combined_data = pd.concat([previous_data.iloc[-59:], new_row], ignore_index=True)
    
    # Extract the features
    model_input = combined_data[['temperature2', 'pressure']].values
    
    # Reshape for model input (add batch dimension)
    model_input = model_input.reshape(1, window_size, 2)
    
    return model_input
def update_previous_data(previous_data, new_row):
    return pd.concat([previous_data.iloc[1:], new_row], ignore_index=True)

def predict_attack():
    df_with_attacks = pd.read_csv('process_dataset/temp_pressure_data_with_attacks.csv')
    df_last_100 = df_with_attacks.tail(100)
    scaler = MinMaxScaler()
    df_last_100[['temperature2', 'pressure']] = scaler.fit_transform(df_last_100[['temperature2', 'pressure']])
    previous_data = df_last_100.iloc[-59:]
    print(previous_data['temperature2'])
    # Example usage:
    # New row (already scaled) - replace with your actual new data
    new_row = pd.DataFrame({'temperature2': [10], 'pressure': [1020]})  # Example scaled values
    model_input = prepare_single_row(new_row, previous_data)
    model_path = 'trained_lstm_model.h5'  # Provide the correct path to your model .h5 file
    model = load_model(model_path)
    prediction = model.predict(model_input)
    attack_probability = prediction[0][0]
    is_attack = attack_probability > 0.5

    print(f"Attack probability: {attack_probability:.4f}")
    print(f"Is attack: {is_attack}")

    previous_data = update_previous_data(previous_data, new_row)
    print("Previous data updated for next prediction.")
    print(f"Shape of updated previous data: {previous_data.shape}")

def main():
    predict_attack()
    
if __name__ == "__main__":
    main()




