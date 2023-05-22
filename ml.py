import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

# 讀取資料集
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

# 選擇特徵
features = ["Temperature", "Humidity", "Light", "CO2"]

# 準備訓練資料
X_train = train_df[features]
y_train = train_df['Occupancy']

# 準備測試資料
X_test = test_df[features]
y_test = test_df['Occupancy']

# 初始化四個演算法
linear_regression = LinearRegression()
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
svm = SVC()

# 訓練四個演算法
linear_regression.fit(X_train, y_train)
decision_tree.fit(X_train, y_train)
random_forest.fit(X_train, y_train)
svm.fit(X_train, y_train)

# 預測測試資料
y_pred_lr = linear_regression.predict(X_test)
y_pred_dt = decision_tree.predict(X_test)
y_pred_rf = random_forest.predict(X_test)
y_pred_svm = svm.predict(X_test)

# 計算四個演算法的準確率
accuracy_lr = accuracy_score(y_test, y_pred_lr.round())
accuracy_dt = accuracy_score(y_test, y_pred_dt)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
accuracy_svm = accuracy_score(y_test, y_pred_svm)

# 印出四個演算法的準確率
print('Linear Regression Accuracy:', accuracy_lr)
print('Decision Tree Accuracy:', accuracy_dt)
print('Random Forest Accuracy:', accuracy_rf)
print('SVM Accuracy:', accuracy_svm)

filename = 'random_forest_model.joblib'
joblib.dump(random_forest, filename)