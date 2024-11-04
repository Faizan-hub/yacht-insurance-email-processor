import re  # Regular expression
import json # Json Handling

import re  # Standard library imports
import json

# Function to interact with Groq API for data extraction from emails and PDFs
def process_email_content(client, email_content, pdf_content=None):
    """
    Extracts specific data points from email and PDF content related to a yacht insurance request.
    This function generates a JSON response with structured data fields and uses the Groq client for processing.

    Args:
        client (Groq): An instance of the Groq client initialized with an API key.
        email_content (str): The text content of the email to process.
        pdf_content (str, optional): The text content extracted from an optional PDF attachment. Defaults to None.

    Returns:
        dict: A dictionary containing the extracted data points in JSON format.
    """
    # Define the prompt to pass to the Groq API for structured data extraction
    prompt = f"""
        Extract the following data points from the email and PDF (if provided) related to a yacht insurance request.
        Respond *only* with a structured JSON object, including each field below. Fill any missing information with "N/A".

        {{
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
        }}

        Email Content:
        {email_content}

        PDF Content:
        {pdf_content if pdf_content else "N/A"}
    """

    # Send the prompt to the Groq API and retrieve the response
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-70b-versatile"
    )
    text = response.choices[0].message.content

    # Attempt to parse and return JSON data from the response
    try:
        json_text = re.search(r'\{.*\}', text, re.DOTALL).group()
        return json.loads(json_text)
    except (json.JSONDecodeError, AttributeError) as e:
        # Handle errors related to JSON parsing
        print("Failed to parse JSON:", e)
        return None


# Function to summarize content using Groq API for concise output
def summarize_content(client, content):
    """
    Generates a concise summary of the content related to a yacht insurance request.

    Args:
        client (Groq): An instance of the Groq client initialized with an API key.
        content (str): The text content (email and/or PDF) to summarize.

    Returns:
        str: A concise summary of the provided content.
    """
    # Define the prompt to create a concise 1-2 line summary of the content
    prompt = f"""
        Please summarize the following content related to a yacht insurance request in 1-2 lines. 
        Your response should be concise and only include complete and relevant information. 
        Remove any incomplete or excessive details, and do not include extraneous text.

        Content:
        {content}
    """

    # Send the prompt to the Groq API and retrieve the response
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-70b-versatile"
    )
    text = response.choices[0].message.content

    # Return the summarized text from the API response
    return text
