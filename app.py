import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from googletrans import Translator
from dotenv import load_dotenv
import os

# ✅ Securely Fetch API Key from Streamlit Secrets
load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Streamlit UI Configuration
st.set_page_config(page_title="AI Travel Assistant", layout="wide")

# ✅ Banner Image with Styling
st.markdown(
    """
    <style>
        .banner-container { text-align: center; margin-bottom: 20px; }
        .banner-img { width: 100%; max-height: 250px; object-fit: cover; border-radius: 15px; }
    </style>
    <div class="banner-container">
        <img src="https://img.freepik.com/free-photo/view-travel-items-assortment-still-life_23-2149617645.jpg?t=st=1740675424~exp=1740679024~hmac=e186750047eacf608efc65a94d1c9abd5d9c6a39c046f2db926d56fc3e11cdc9&w=1380" class="banner-img">
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ Centered Title
st.markdown("<h1 style='text-align: center;'>🗺️✈︎ Destination Dynamo AI⁀જ✈︎</h1>", unsafe_allow_html=True)

# ✅ UI for User Input
col1, col2 = st.columns(2)

with col1:
    source_city = st.text_input("🛫 Departure City", placeholder="E.g., New Delhi")
    destination_city = st.text_input("📍Destination City", placeholder="E.g., Amsterdam")
    travel_date = st.date_input(".ೃ࿔ ✈︎ Travel Date")
    currency = st.selectbox("💲 Select Currency", ["USD", "INR", "EUR", "GBP", "JPY"])

with col2:
    preferred_mode = st.selectbox("🚗 Preferred Mode", ["Any", "Flight", "Train", "Bus", "Cab"])
    sort_by = st.radio("📊 Sort By", ["Price", "Duration"])
    language = st.selectbox("🌍 Select Language", ["English", "Spanish", "French", "German", "Hindi"])

# ✅ Language Code Mapping for Translation
language_codes = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
}

# ✅ Function to fetch AI-generated travel options
def get_travel_options(source, destination, mode, currency):
    system_prompt = SystemMessage(
        content="You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with estimated costs, duration, and relevant travel tips."
    )
    user_prompt = HumanMessage(
        content=f"I am traveling from {source} to {destination} in {currency}. Preferred mode: {mode}. Suggest travel options with estimated cost, duration, and important details."
    )

    # ✅ Initialize AI model
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

# ✅ Function to Translate Text
def translate_text(text, target_language):
    if target_language == "English":  # No need to translate if already in English
        return text

    translator = Translator()
    translated_text = translator.translate(text, dest=language_codes.get(target_language, "en")).text
    return translated_text

# ✅ Travel Option Fetching
if st.button("🔍 Find Travel Options"):
    if source_city.strip() and destination_city.strip():
        with st.spinner("🔄 Fetching best travel options..."):
            travel_info = get_travel_options(source_city, destination_city, preferred_mode, currency)
        
        st.success("✅ AI-Generated Travel Recommendations:")
        st.markdown(travel_info)

    else:
        st.warning("⚠️ Please enter both source and destination locations.")



# Footer Section
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;  /* Add this to stretch from left */
            right: 0; /* Add this to stretch from right */
            width: 100%; 
            text-align: center;
            padding: 10px;
            background-color: #f1f1f1;
            color: #333333;
            font-weight: bold;
            border-top: 2px solid #cccccc;
            z-index: 9999; /* Keeps it on top */
        }
    </style>
    <div class="footer">
        Created by Yashwanth 🚀
    </div>
    """,
    unsafe_allow_html=True
)
