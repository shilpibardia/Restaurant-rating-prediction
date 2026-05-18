import streamlit as st
from api_client import get_prediction

import pandas as pd
df = pd.read_csv("C:\\Users\\sambh\\Desktop\\restaurant_project\\Dataset .csv")

currency_options = sorted(df["Currency"].dropna().unique())

city_options = sorted(df["City"].dropna().unique())

cuisine_options = sorted(df["Cuisines"].dropna().unique())



country_mapping = (
    df[["Country Code"]]
    .drop_duplicates()
    .sort_values(by="Country Code")
    )

country_options = country_mapping["Country Code"].tolist()



# Page config
st.set_page_config(
    page_title="Restaurant Rating Predictor",
    page_icon="🍽️",
    layout="wide"
)


# Load custom css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Header
st.markdown("""
<div class='main-header'>
    <h1>🍽️ Restaurant Rating Predictor</h1>
    <p>Predict restaurant ratings using Machine Learning</p>
</div>
""", unsafe_allow_html=True)


# Layout
col1, col2 = st.columns(2)


with col1:
    st.subheader("📋 Restaurant Details")

    average_cost = st.number_input(
        "💵 Average Cost for Two",
        min_value=0,
        value=500
    )

    price_range = st.selectbox(
        "💰 Price Range",
        [1, 2, 3, 4]
    )

    votes = st.number_input(
        "🗳️ Votes",
        min_value=0,
        value=100
    )

    has_table_booking = st.selectbox(
        "🍽️ Table Booking",
        ["Yes", "No"]
    )

    has_online_delivery = st.selectbox(
        "🛵 Online Delivery",
        ["Yes", "No"]
    )

    switch_to_order_menu = st.selectbox(
    "🔄 Switch to Order Menu",
    ["Yes", "No"]
)

with col2:

    st.subheader("🌍 Additional Information")

    is_delivering_now = st.selectbox(
        "🚚 Delivering Now",
        ["Yes", "No"]
    )

    country_code = st.selectbox(
        "🌍 Country Code",
        country_options
    )

    currency = st.selectbox(
        "💰 Currency",
        currency_options
    )

    city = st.selectbox(
        "🏙️ City",
        city_options
    )

    cuisines = st.selectbox(
        "🍜 Cuisines",
        cuisine_options
    )

st.markdown("<br>", unsafe_allow_html=True)


if st.button("✨ Predict Rating"):

    data = {
        "Average_Cost_for_two": average_cost,
        "Price_range": price_range,
        "Votes": votes,
        "Has_Table_booking": has_table_booking,
        "Has_Online_delivery": has_online_delivery,
        "Is_delivering_now": is_delivering_now,
        "Switch_to_order_menu": switch_to_order_menu,
        "Country_Code": country_code,
        "Currency": currency,
        "City": city,
        "Cuisines": cuisines
    }

    with st.spinner("Predicting restaurant rating..."):
        result = get_prediction(data)

    if result:
        rating = result["predicted_rating"]

        st.markdown(f"""
        <div class='result-box'>
            <h2>⭐ Predicted Rating: {rating}</h2>
        </div>
        """, unsafe_allow_html=True)

        # if rating >= 4:
        #     st.success("Excellent Restaurant 🚀")
        # elif rating >= 3:
        #     st.info("Good Restaurant 👍")
        # else:
        #     st.warning("Needs Improvement 📉")
        if rating >= 4.5:
            st.success("🌟 Excellent Restaurant")
        elif rating >= 4:
            st.success("🔥 Highly Recommended")
        elif rating >= 3:
            st.info("👍 Good Restaurant")
        elif rating >= 2:
            st.warning("⚠️ Average Restaurant")
        else:
            st.error(" 📉 Needs Improvement ")

    else:
        st.error("API Connection Failed")