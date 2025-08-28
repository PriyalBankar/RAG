import streamlit as st
from .api_utils import upload_document, list_documents
from utilities.constants import DEFAULT_MODEL_NAME


def display_sidebar():
    # Sidebar: Model Selection
    st.sidebar.header("Selected Model")
    # Set the model in session state if not already set
    if "model" not in st.session_state:
        st.session_state.model = DEFAULT_MODEL_NAME
    st.sidebar.text(st.session_state.model)

    # Sidebar: List Documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(
                f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})"
            )

    # Delete UI removed for simplicity; can be re-enabled if needed
