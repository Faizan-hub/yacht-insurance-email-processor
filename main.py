import os  # For accessing environment variables
import streamlit as st   # For creating the web application interface
from groq import Groq # Import the Groq library for LLM interactions

from helpers import parse_pdf_content, fill_missing_fields  # Custom modules
from llm_helper import process_email_content


# Cache the model and API keys to avoid reloading on each run
@st.cache_resource
def load_model():
    """
    Loads the Groq client and Google API credentials from environment variables.

    Returns:
        tuple: A tuple containing the Groq client, Google API key, and Custom Search Engine (CSE) ID.
    """
    # Retrieve API keys from environment variables
    groq_key = os.getenv("GROQ_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("CSE_ID")

    # Initialize the Groq client with the API key
    client = Groq(api_key=groq_key)

    return client, google_api_key, cse_id


def main():
    # Load model and API keys
    client, google_api_key, cse_id = load_model()

    # Set up the title of the Streamlit app
    st.title("Sample Yacht Insurance Inquiry Emails")

    # Description of the app's purpose
    """
    This app processes yacht insurance inquiry emails and, optionally, attached PDF documents.
    It extracts and completes relevant information for insurance purposes.
    """

    # Input field for entering email content
    email_content = st.text_area("Enter your email content here:", height=300)

    # File uploader for optional PDF attachments
    pdf_file = st.file_uploader("Upload a PDF (optional)", type=["pdf"])

    # Button to initiate processing of the input content
    if st.button("Submit"):
        # Variable to hold processed data
        response_data = None

        # Check if the user has entered any email content
        if email_content:
            try:
                # Process the email content with or without PDF content
                if pdf_file is not None:
                    # Parse and extract text from the uploaded PDF
                    pdf_content = parse_pdf_content(pdf_file)
                    # Process the email and PDF content together
                    response_data = process_email_content(client, email_content, pdf_content)
                else:
                    # Process only the email content if no PDF is provided
                    response_data = process_email_content(client, email_content)

                # Check if processing yielded any results
                if response_data:
                    # Fill in missing fields by fetching data from external sources (e.g., Google API)
                    filled_data = fill_missing_fields(client, google_api_key, cse_id, response_data)
                    # Display the completed data as JSON
                    st.json(filled_data)
                else:
                    # Show an error if processing failed due to format issues
                    st.error("Failed to process the email content. Please check the format.")
            except Exception as e:
                # Catch any exceptions and display an error message
                st.error(f"An error occurred while processing: {e}")
        else:
            # Warn the user if no email content was entered
            st.warning("Please enter the email content before submitting.")


# Run the main function to start the app
if __name__ == "__main__":
    main()
