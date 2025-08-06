import streamlit as st
import google.generativeai as genai

# --- API key ---
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# --- Configurations ---
generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

# --- Gemini Model ---
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="""
You are a technical support chatbot at TechNova Solutions, a software house.
Your job is to assist TechNova employees with technical issues during work hours.

80% of employees use Dell Latitude or Dell XPS (Windows 11 Pro).
Phones: Samsung Galaxy (Android 13).
Monitors: dual-screen setups for developers.
Printers: HP LaserJet on internal Wi-Fi.
Tools: Slack (chat), Jira (project mgmt), Microsoft 365.

Respond politely, clearly, and concisely.
"""
)

# --- Session state ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- LLM chat handler ---
def chat_completion(user_input):
    chat_session = model.start_chat(history=st.session_state.history)
    response = chat_session.send_message(user_input)
    model_response = response.text

    st.session_state.history.append({"role": "user", "parts": [user_input]})
    st.session_state.history.append({"role": "model", "parts": [model_response]})
    return model_response

# --- UI ---
st.title("TechNova IT Support Bot")

# Display conversation history
for turn in st.session_state.history:
    if turn["role"] == "user":
        with st.chat_message("user"):
            st.markdown(turn["parts"][0])
    elif turn["role"] == "model":
        with st.chat_message("assistant"):
            st.markdown(turn["parts"][0])

# Input box
user_input = st.chat_input("How can I help you?")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Typing..."):
        response = chat_completion(user_input)

    with st.chat_message("assistant"):
        st.markdown(response)




    



