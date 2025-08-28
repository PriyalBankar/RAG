import requests
import streamlit as st
from utilities.constants import API_BASE_URL


def get_api_response(question, session_id, model):
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"question": question, "model": model}
    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post(f"{API_BASE_URL}/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"API request failed with status code {response.status_code}: {response.text}"
            )
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None


def upload_document(file):
    print("Uploading file...")
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{API_BASE_URL}/upload-doc", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Failed to upload file. Error: {response.status_code} - {response.text}"
            )
            return None
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")
        return None


def list_documents():
    try:
        response = requests.get(f"{API_BASE_URL}/list-docs")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Failed to fetch document list. Error: {response.status_code} - {response.text}"
            )
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching the document list: {str(e)}")
        return []

