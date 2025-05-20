import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping

def gru_forecast(target, df, future_days, num_mc_simulations=100):
    df = df.copy()
    df['Datetime'] = pd.to_datetime(df['Date'])

    close_df = df[[target]]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_close = scaler.fit_transform(close_df)

    seq_len = 1
    X_train, y_train = [], []
    for i in range(seq_len, len(scaled_close)):
        X_train.append(scaled_close[i-seq_len:i])
        y_train.append(scaled_close[i])
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    model = Sequential([
        GRU(1000, return_sequences=True, input_shape=(seq_len, 1)),
        Dropout(0.26),
        GRU(200, return_sequences=True),
        Dropout(0.26),
        GRU(1000, return_sequences=False),
        Dropout(0.26),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=200, batch_size=32, verbose=0, callbacks=[EarlyStopping(patience=5)])

    future_mc_simulations = []
    for _ in range(num_mc_simulations):
        last_seq_mc = scaled_close[-seq_len:].reshape((1, seq_len, 1))
        future_prices = []
        for _ in range(future_days):
            pred = model.predict(last_seq_mc, verbose=0)
            future_prices.append(scaler.inverse_transform(pred)[0, 0])
            last_seq_mc = np.append(last_seq_mc[:, 1:, :], pred.reshape(1, 1, 1), axis=1)
        future_mc_simulations.append(future_prices)

    future_mc_simulations = np.array(future_mc_simulations)
    future_mc_avg = np.mean(future_mc_simulations, axis=0)

    return close_df[target].tolist(), future_mc_simulations.tolist(), future_mc_avg.tolist()
