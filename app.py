from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import uvicorn


# Load model
model = joblib.load("restaurant_rating_pipeline.joblib")
feature_meta = joblib.load("feature_meta.joblib")

app = FastAPI(title="Restaurant Rating Prediction API")

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RestaurantInput(BaseModel):
    Average_Cost_for_two: float
    Price_range: int
    Votes: int
    Has_Table_booking: str
    Has_Online_delivery: str
    Is_delivering_now: str
    Switch_to_order_menu: str
    Country_Code: int
    Currency: str
    City: str
    Cuisines: str

@app.get("/")
def home():
    return {
        "message": "Restaurant Rating Prediction API Running"
    }


@app.post("/predict")
def predict(data: RestaurantInput):

    input_dict = {
        "Average Cost for two": [data.Average_Cost_for_two],
        "Price range": [data.Price_range],
        "Votes": [data.Votes],
        "Has Table booking": [data.Has_Table_booking],
        "Has Online delivery": [data.Has_Online_delivery],
        "Is delivering now": [data.Is_delivering_now],
        "Switch to order menu": [data.Switch_to_order_menu],
        "Country Code": [data.Country_Code],
        "Currency": [data.Currency],
        "City": [data.City],
        "Cuisines": [data.Cuisines]
    }

    df = pd.DataFrame(input_dict)

    # Feature engineering
    df['Log_Votes'] = df['Votes'].apply(lambda x: __import__('numpy').log1p(x))

    prediction = model.predict(df)[0]

    prediction = round(float(prediction), 2)

    return {
        "predicted_rating": prediction
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)