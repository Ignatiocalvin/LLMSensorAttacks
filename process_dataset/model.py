import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
import pandas as pd
# df_with_attacks = pd.read_csv('temp_pressure_data_with_attacks.csv')
df_with_attacks = pd.read_csv('process_dataset/temp_pressure_data_with_attacks.csv', nrows=100000)
df_with_attacks.to_csv('process_dataset/temp_pressure_data_with_attacks_subset.csv', index=False)

scaler = MinMaxScaler()
df_with_attacks[['temperature2', 'pressure']] = scaler.fit_transform(df_with_attacks[['temperature2', 'pressure']])
# Define X (features) and y (target)
X = df_with_attacks[['temperature2', 'pressure']].values
y = df_with_attacks['is_attacked'].values

# We create a sliding window over the time series data, e.g., using a window size of 60 (last 10 observations) - a minute
window_size = 60
X_windowed = []

for i in range(len(X) - window_size):
    X_windowed.append(X[i:i + window_size])

X_windowed = np.array(X_windowed)
y_windowed = y[window_size:]

X_train, X_test, y_train, y_test = train_test_split(X_windowed, y_windowed, test_size=0.2, random_state=42)
# Build the LSTM model
model = Sequential()
model.add(LSTM(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(1, activation='sigmoid'))  # Binary classification (attack or no attack)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_test, y_test))

# Make predictions


# test_loss, test_accuracy = model.evaluate(test_dataset)
# print(f'Test Loss: {test_loss}')
# print(f'Test Accuracy: {test_accuracy}')

model_file = 'trained_lstm_model.pkl'
model.save('trained_lstm_model.h5')  # Save model as an H5 file (more standard approach in Keras)
y_pred = (model.predict(X_test) > 0.5).astype(int)


print(f'Predictions (Sample): {y_pred[:5]}')
print(f'True Labels (Sample): {y_test[:5]}')
print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))