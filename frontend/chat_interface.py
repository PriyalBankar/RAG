import streamlit as st
from .api_utils import get_api_response
from utilities.constants import DEFAULT_MODEL_NAME


def display_chat_interface():
    # Block chat if no documents are uploaded
    documents = st.session_state.get("documents", [])
    if not documents:
        st.warning("No documents found. Please upload a document in the sidebar.")
        return

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating response..."):
            # Ensure model is set, use default if not
            model = st.session_state.get("model", DEFAULT_MODEL_NAME)
            response = get_api_response(prompt, st.session_state.session_id, model)

            if response:
                st.session_state.session_id = response.get("session_id")
                st.session_state.messages.append(
                    {"role": "assistant", "content": response["answer"]}
                )

                with st.chat_message("assistant"):
                    st.markdown(response["answer"])

                    with st.expander("Details"):
                        st.subheader("Generated Answer")
                        st.code(response["answer"])
                        st.subheader("Model Used")
                        st.code(response["model"])
                        st.subheader("Session ID")
                        st.code(response["session_id"])
            else:
                st.error("Failed to get a response from the API. Please try again.")
