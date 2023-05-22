import pandas as pd
import joblib

# 載入模型
model = joblib.load('random_forest_model.joblib')

features = ["Temperature", "Humidity", "Light", "CO2"]
pred_df = pd.read_csv('pred.csv')

X_test = pred_df[features]
print(X_test)

# 使用模型進行預測
y_pred = model.predict(X_test)

print(list(y_pred))