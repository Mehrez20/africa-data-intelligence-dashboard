import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# ---------------------
# LOAD DATA
# ---------------------

data = pd.read_csv("data/tunisia_data.csv")

# ---------------------
# PREPARE DATA
# ---------------------

X = data[["year"]]
y = data["gdp"]

# ---------------------
# TRAIN MODEL
# ---------------------

model = LinearRegression()
model.fit(X, y)

# ---------------------
# FUTURE YEARS
# ---------------------

future_years = np.arange(2024, 2041).reshape(-1,1)

predictions = model.predict(future_years)

# ---------------------
# SAVE RESULTS
# ---------------------

pred_df = pd.DataFrame({
    "year": future_years.flatten(),
    "predicted_gdp": predictions
})

pred_df.to_csv("data/gdp_predictions.csv", index=False)

print("AI PREDICTIONS CREATED")