import google.generativeai as genai
import os
import streamlit as st

api_key=st.secrets["GEMINI_API_KEY]

genai.configure(api_key=api_key)

generation_config={
    "temperature":0.75,
    "top_p":0.95,
    "top_k":64,
    "max_output_tokens":8192,
}


safety_settings = [
    {
        "category":"HARM_CATEGORY_HARASSMENT",
        "threshold":"BLOCK_LOW_AND_ABOVE",
    },
    {
        "category":"HARM_CATEGORY_HATE_SPEECH",
        "threshold":"BLOCK_LOW_AND_ABOVE", 
    },
    {
        "category":"HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold":"BLOCK_LOW_AND_ABOVE",
    },
    {
        "category":"HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold":"BLOCK_LOW_AND_ABOVE"
    },

]

model=genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="""You are a technical support chatbot at TechNova Solutions, a software house.
                                  Your job is to assist and help TechNova Solutions' employees with technical issues they
                                  face during their office hours. 80% of our employees use Dell Latitude or 
                                 Dell XPS (Windows 11 Pro). The company issues Samsung Galaxy phones (Android 13) to 
                                 the employees. We have dual-screen setups for developers and we use HP LaserJet models
                                  on internal Wi-Fi. Lastly, we use Slack for team communication, Jira for 
                                 project management, and Microsoft 365 as our suite. You must assist employees  
                                 in a polite and respectful tone, and ensure troubleshooting instructions are clear, 
                                 concise, and to the point."""
)

history=[]

def chat_completion(user_input):
    chat_session=model.start_chat(
    history=history
    )
    response=chat_session.send_message(user_input)
    model_response=response.text
    st.write(model_response)
    history.append({"role":"user", "parts":[user_input]})
    history.append({"role":"model", "parts":[model_response]})
    

st.title("Technical Support Chatbot")

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue 
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input=st.chat_input("Type here...")

if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        response=chat_completion(user_input)
else:
    st.warning("No input was provided")




    


