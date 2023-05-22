import random
import pandas as pd

# 隨機生成100筆資料
data = []
for i in range(10):
    data.append([
        random.uniform(18, 30),   # 溫度
        random.uniform(20, 80),   # 濕度
        random.uniform(0, 2000),  # 光照強度
        random.uniform(400, 1500) # CO2濃度
    ])

# 將資料寫入pred.csv檔案
df = pd.DataFrame(data, columns=["Temperature", "Humidity", "Light", "CO2"])

numeric_cols = ["Light", "Temperature", "Humidity", "CO2"]
df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()

df.to_csv("pred.csv", index=False, header=True)