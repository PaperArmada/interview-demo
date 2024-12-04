import streamlit as st
import pyperclip
import json

# Streamlit App
def main():
    st.title("JSON Response Navigator")
    st.write("Navigate through responses in a clean and aesthetically pleasing way.")

    # File uploader to upload JSON file
    uploaded_file = st.file_uploader("Upload a JSON file", type="json")
    if uploaded_file is not None:
        json_data = json.load(uploaded_file)
    else:
        st.warning("Please upload a JSON file to proceed.")
        return

    # Sidebar to select category
    category = st.sidebar.selectbox("Select a Category", list(json_data["responses"].keys()), on_change=lambda: st.session_state.update(index=0))
    
    # State to keep track of the current index
    if 'index' not in st.session_state:
        st.session_state['index'] = 0

    responses = json_data['responses'][category]
    total_responses = len(responses)

    # Display the current response
    st.markdown(f"### {category.capitalize()} Response {st.session_state['index'] + 1} of {total_responses}")
    response_text = responses[st.session_state['index']]['response']
    st.write(response_text)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous"):
            st.session_state['index'] = (st.session_state['index'] - 1) % total_responses
            st.rerun()
    with col2:
        # Copy to clipboard button
        if st.button("Copy Content"):
            pyperclip.copy(response_text)
            st.success('Text copied to clipboard.')
    with col3:
        if st.button("Next"):
            st.session_state['index'] = (st.session_state['index'] + 1) % total_responses
            st.rerun()

if __name__ == "__main__":
    main()
