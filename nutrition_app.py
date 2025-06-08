import streamlit as st
import requests
import pandas as pd

# App title
st.title("🥗 Nutrition Info Finder")
st.info("Track nutritional information of food items using Edamam API")

# Hardcoded Edamam API credentials
EDAMAM_APP_ID = "e8c59bcf"
EDAMAM_APP_KEY = "2c13922a0b69c5661b825c6939407a82"
BASE_URL = "https://api.edamam.com/api/food-database/v2/parser"

# Function to get food data
def get_food_data(food_name):
    params = {
        "ingr": food_name,
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "parsed" in data and data["parsed"]:
            food = data["parsed"][0]["food"]
        elif "hints" in data and data["hints"]:
            food = data["hints"][0]["food"]
        else:
            return None
        return {
            "label": food.get("label"),
            "category": food.get("category"),
            "nutrients": food.get("nutrients", {})
        }
    else:
        print("API Error:", response.status_code, response.text)
        return None

# Sidebar input
st.sidebar.title("Nutrition Tracker")
food_item = st.sidebar.text_input("Enter a food item:", value="banana")
num_nutrients = st.sidebar.slider("Nutrients to display:", 3, 10, 5)
show_map = st.sidebar.checkbox("Show nutrition hotspots map")

# Main logic
if st.sidebar.button("Get Nutrition Info"):
    if not food_item.strip():
        st.error("Please enter a valid food item.")
    else:
        with st.spinner("Fetching nutrition info..."):
            data = get_food_data(food_item)
            if not data:
                st.warning("Sorry, no data found for this food item.")
            else:
                st.success(f"Nutritional info for: {data['label']}")
                st.markdown(f"**Category**: {data['category']}")

                nutrients = dict(list(data["nutrients"].items())[:num_nutrients])
                nutrients_df = pd.DataFrame(nutrients.items(), columns=["Nutrient", "Value"])
                st.dataframe(nutrients_df)

                st.bar_chart(nutrients_df.set_index("Nutrient"))

                # Show map if checkbox checked
                if show_map:
                    st.subheader("Nutrition Hotspots Map Example")
                    # Example coordinates, replace with your own data as needed
                    locations = pd.DataFrame({
                        'lat': [40.7128, 34.0522, 41.8781],
                        'lon': [-74.0060, -118.2437, -87.6298],
                        'name': ['New York', 'Los Angeles', 'Chicago']
                    })
                    st.map(locations)
else:
    st.markdown("""
    ## How to use:
    1. Enter a food item in the sidebar (e.g., `apple`, `chicken`)
    2. Select how many nutrient values to show
    3. Check the box if you want to see a nutrition hotspots map
    4. Click "Get Nutrition Info"
    """)

    st.subheader("Try these examples:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("🍌 Banana", disabled=True)
    with col2:
        st.button("🍗 Chicken", disabled=True)
    with col3:
        st.button("🍞 Bread", disabled=True)

st.markdown("---")
