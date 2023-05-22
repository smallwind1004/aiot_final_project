import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv("datatraining.txt")

# # 刪除不需要的欄位
df = df.drop(columns=["date", "HumidityRatio"])

# # 將日期時間轉換成時間戳記
# df["timestamp"] = pd.to_datetime(df["date"]).astype(int) // 10**9
# df = df.drop(columns=["date"])

# # 資料標準化
numeric_cols = ["Temperature", "Humidity", "Light", "CO2"]
df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()

# # 將資料集分成訓練集和測試集
train_df = df.sample(frac=0.8, random_state=1)
test_df = df.drop(train_df.index)

# # 儲存處理好的資料
train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)