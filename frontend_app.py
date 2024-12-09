import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Adjust if running on different host/port

st.title("AI Interviewer")

# Start session if not started
if "session_id" not in st.session_state:
    resp = requests.post(f"{API_URL}/start_session")
    data = resp.json()
    st.session_state.session_id = data["session_id"]
    st.session_state.history = [("AI", data["message"])]

for speaker, msg in st.session_state.history:
    if speaker == "AI":
        st.markdown(f"**{speaker}:** {msg}")
    else:
        st.markdown(f"**You:** {msg}")

with st.form("user_input_form", clear_on_submit=True):
    user_input = st.text_input("Your response or question:")
    
    # Create two columns for the buttons
    col1, col2 = st.columns([1, 1])  # Adjust proportions if needed
    with col1:
        submitted = st.form_submit_button("Submit")
    with col2:
        end_interview = st.form_submit_button("End Interview")
        
if submitted and user_input:
    resp = requests.post(
        f"{API_URL}/respond", 
        json={"session_id": st.session_state.session_id, "user_message": user_input}
    )
    data = resp.json()
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("AI", data["message"]))
    st.rerun()

if end_interview:
    requests.post(f"{API_URL}/end_session", json={"session_id": st.session_state.session_id})
    st.write("The interview session has ended. Thank you!")
    st.session_state.clear()
