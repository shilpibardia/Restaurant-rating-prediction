import requests

API_URL = " https://restaurant-rating-prediction-tnae.onrender.com"


def get_prediction(data):

    try:
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            return response.json()

        print(response.text)
        return None

    except Exception as e:
        print("API ERROR:", e)
        return None
