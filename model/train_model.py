# train_model.py
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

product_lines = ['Motorcycles', 'Classic Cars', 'Trucks and Buses', 'Vintage Cars', 'Planes', 'Ships', 'Trains']
product_encoder = LabelEncoder()
product_encoder.fit(product_lines)

X_train = []
y_train = []

for q in range(1, 101):
    for p in range(20, 151):
        for m in range(1, 13):
            for product in product_lines:
                encoded = product_encoder.transform([product])[0]
                X_train.append([q, p, encoded, m])
                y_train.append(q * p + np.random.normal(0, 100))

model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Save model & encoder
joblib.dump(model, 'random_forest_sales.pkl')
joblib.dump(product_encoder, 'product_encoder.pkl')

print("Model saved.")