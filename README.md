
# Yacht Insurance Email Processor

This Streamlit application processes yacht insurance inquiry emails and, optionally, attached PDF documents. It extracts and completes relevant information required for insurance purposes using the Groq API for LLM interactions, along with the Google Custom Search API for additional data completion.

## Features
- Extracts essential information from email and PDF content related to yacht insurance.
- Completes missing data fields by searching the web for relevant information.
- Provides a concise and structured JSON output for easy data handling.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/yacht-insurance-email-processor.git
   cd yacht-insurance-email-processor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for API keys:
   ```bash
   export GROQ_API_KEY='your_groq_api_key'
   export GOOGLE_API_KEY='your_google_api_key'
   export CSE_ID='your_google_cse_id'
   ```

## File Structure

- `main.py`: The main file for running the Streamlit app, which handles user interactions and displays extracted data.
- `llm_helper.py`: Contains functions for interacting with the Groq API to extract and structure data from email and PDF content.
- `helpers.py`: Includes utility functions for PDF parsing, Google search integration, and webpage content retrieval.

## Usage

Run the application with Streamlit:
   ```bash
   streamlit run main.py
   ```

### Application Interface

- **Email Content**: Paste your yacht insurance inquiry email content here.
- **PDF Attachment**: Optionally upload a PDF document related to the inquiry.
- **Submit**: Click to process the input content and view the structured JSON output.

## Expected Output

The app outputs a JSON structure with the following fields:
   ```json
   {
     "Yacht Model": "",
     "Yacht Length": "",
     "Year of Manufacture": "",
     "Current Value/Purchase Price": "",
     "Current Location": "",
     "Intended Cruising Area": "",
     "Owner's Name": "",
     "Owner's Contact Information": "",
     "Owner's Boating Experience": "",
     "Previous Insurance Claims": "",
     "Additional Equipment": "",
     "Current Insurance Coverage": "",
     "Other": ""
   }
   ```

## Notes

- The app uses Google Custom Search API to fill in missing fields by searching the web.
- Make sure to set up the necessary environment variables before running the application.
