import pandas as pd
import joblib

def predict_occupancy(pred_data):
    sample_df = pd.read_csv("datatraining.txt")
    sample_df = sample_df.drop(columns=["date", "HumidityRatio"])
    features = ["Temperature","Humidity","Light","CO2"]
    new_data = dict(zip(features,pred_data))
    df = pd.DataFrame(columns=features)
    df.loc[len(df)] = new_data
    df[features] = (df[features] - sample_df[features].mean()) / sample_df[features].std()
    print(df)
    # 載入模型
    model = joblib.load('random_forest_model.joblib')
    
    X_test = df[features]
    y_pred = model.predict(X_test)
    return y_pred[0]