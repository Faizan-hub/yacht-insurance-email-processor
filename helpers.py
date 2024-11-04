# Library Imports
import fitz  # PyMuPDF for PDF processing
import requests  # For making HTTP requests, particularly to the Google Custom Search API and webpages
from bs4 import BeautifulSoup  # For parsing and cleaning HTML content
import re  # For regular expressions to clean text
from llm_helper import summarize_content  # Custom helper function to summarize content

# Function to parse text from PDF files
def parse_pdf_content(pdf_path):
    """
    Extracts text from each page of a PDF and returns it as a single string.

    Args:
        pdf_path (str): The file path of the PDF to read.

    Returns:
        str: The extracted text from the PDF or "N/A" if there was an issue reading the file.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
        text = "N/A"  # Return "N/A" if there's an issue reading the PDF
    return text

# Function to clean HTML content
def clean_text(html_text):
    """
    Cleans HTML content by removing tags and extra whitespace.

    Args:
        html_text (str): Raw HTML content to be cleaned.

    Returns:
        str: Cleaned text with HTML tags and extra whitespace removed.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    clean_text = soup.get_text(separator=" ", strip=True)
    return re.sub(r'\s+', ' ', clean_text)

# Performs a Google Custom Search query
def google_search(api_key, cse_id, query, char_limit=500):
    """
    Fetches the top 3 results from Google Custom Search and combines snippet and page content, limited by char_limit.

    Args:
        api_key (str): Google API key.
        cse_id (str): Custom Search Engine ID.
        query (str): Search query for Google Custom Search.
        char_limit (int): Character limit for the returned text.

    Returns:
        str: Concatenated text of search snippets and/or page content, trimmed to the character limit.
    """
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cse_id, "q": query, "num": 3}
    response = requests.get(search_url, params=params)
    search_results = response.json()

    try:
        # Concatenate snippets for additional context
        snippets = [item["snippet"] for item in search_results.get("items", [])]
        combined_snippet = " ".join(snippets)

        # Attempt to fetch the page content of the first result
        first_link = search_results["items"][0]["link"]
        page_text = fetch_page_content(first_link)

        # Combine snippet with fetched page content if available
        full_text = combined_snippet + " " + page_text if page_text else combined_snippet

        # Limit the result to the specified character limit
        return full_text[:char_limit] + "..." if len(full_text) > char_limit else full_text
    except (KeyError, IndexError):
        return "N/A"

# Fetch and clean the content from a webpage
def fetch_page_content(url):
    """
    Fetches and cleans text content from a given webpage URL.

    Args:
        url (str): The URL of the webpage to fetch content from.

    Returns:
        str: Cleaned text content from the webpage or an empty string if there was an error.
    """
    try:
        page_response = requests.get(url)
        soup = BeautifulSoup(page_response.text, "html.parser")
        page_text = soup.get_text(separator=" ", strip=True)
        clean_text = re.sub(r'\s+', ' ', page_text)  # Clean up extra whitespace
        return clean_text
    except requests.RequestException:
        return ""

# Search the web for missing data and fill fields using Google Custom Search API
def fill_missing_fields(client, api_key, cse_id, data):
    """
    Fills in missing fields in the data dictionary by searching the web for relevant information.

    Args:
        api_key (str): Google API key.
        cse_id (str): Custom Search Engine ID.
        data (dict): Dictionary with fields that may have missing ("N/A") values.

    Returns:
        dict: Data dictionary with missing fields filled in where possible.
    """
    missing_fields = {key: "N/A" for key, value in data.items() if value == "N/A"}
    for field in missing_fields.keys():
        search_query = f"{field} yacht insurance details"
        text = google_search(api_key, cse_id, search_query)
        data[field] = summarize_content(client, text)
    return data
