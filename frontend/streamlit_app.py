import streamlit as st
from .sidebar import display_sidebar
from .chat_interface import display_chat_interface
from .api_utils import list_documents, upload_document
from utilities.constants import DEFAULT_MODEL_NAME, SUPPORTED_EXTENSIONS_WITHOUT_DOT

st.title("Langchain RAG Chatbot")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL_NAME

# Ensure documents list exists on first load
if "documents" not in st.session_state:
    st.session_state.documents = list_documents()

# Sidebar for listing/management only
display_sidebar()

# Main-page uploader and gating
documents = st.session_state.get("documents", [])

if not documents:
    st.subheader("Upload a document to get started")
    uploaded_file = st.file_uploader(
        "Choose a file", type=SUPPORTED_EXTENSIONS_WITHOUT_DOT, key="main_uploader"
    )
    if uploaded_file is not None:
        if st.button("Upload", key="main_upload_btn"):
            with st.spinner("Uploading..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.success(
                        f"File '{uploaded_file.name}' uploaded successfully (ID {upload_response['file_id']})."
                    )
                    st.session_state.documents = list_documents()
                else:
                    st.error("Failed to upload the file. Please try again.")
    st.info("Please upload a document to start chatting.")
else:
    # Show optional uploader even when docs exist
    with st.expander("Upload another document"):
        extra_file = st.file_uploader(
            "Choose a file", type=SUPPORTED_EXTENSIONS_WITHOUT_DOT, key="extra_uploader"
        )
        if extra_file is not None:
            if st.button("Upload", key="extra_upload_btn"):
                with st.spinner("Uploading..."):
                    upload_response = upload_document(extra_file)
                    if upload_response:
                        st.success(
                            f"File '{extra_file.name}' uploaded successfully (ID {upload_response['file_id']})."
                        )
                        st.session_state.documents = list_documents()
                    else:
                        st.error("Failed to upload the file. Please try again.")

    # Display the chat interface
    display_chat_interface()
