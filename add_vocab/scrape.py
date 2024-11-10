import requests
import json
import openai
from bs4 import BeautifulSoup
from requests_html import HTMLSession

# Function to fetch HTML content from the URL
def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    print("RESPONSE ", response.text)
    return response.text

# Function to extract <table> tags
def extract_tables(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    return [str(table) for table in tables]

# Function to clean up each <td> element, ignoring specific tags as needed
def clean_table_row(row, headers):
    cells = row.find_all('td')
    data = {}

    # Iterate through headers and cells
    for i, header in enumerate(headers):
        if i >= len(cells):
            data[header] = None  # If there aren't enough cells, set to None
            continue

        cell = cells[i]
        
        # For the first <td>, strip out <a> and <span> tags, keeping only the text
        if i == 0:
            text = ''.join(cell.stripped_strings)  # Get all text within <td> while ignoring tags like <a>, <span>
        
        # For the last <td>, specifically look for <bdi> content
        elif i == len(headers) - 1 and cell.find('bdi'):
            text = cell.find('bdi').get_text(strip=True)  # Get the text within <bdi> tag
        
        # Default case: get the text content directly
        else:
            text = cell.get_text(strip=True)
        
        data[header] = text

    return data

# Function to process each table and extract rows
def extract_table_data(table_html, headers):
    soup = BeautifulSoup(table_html, 'html.parser')
    rows = soup.find_all('tr')
    table_data = []

    # Iterate over rows and clean up data for each row
    for row in rows:
        row_data = clean_table_row(row, headers)
        if any(row_data.values()):  # Only add rows with non-empty values
            table_data.append(row_data)

    return table_data

if __name__ == "__main__":
    url = "https://www.chaiandconversation.com/speak-persian/how-greet-people-and-ask-how-theyre-doing"
    headers = ["Persian", "English", "Script"]

    # Fetch HTML content from the website
    html_content = fetch_html(url)
    
    # # Extract each table from the HTML
    # tables_html = extract_tables(html_content)

    # # Loop through each table and extract data using custom row processing
    # extracted_data = []
    # for table_html in tables_html:
    #     try:
    #         table_data = extract_table_data(table_html, headers)
    #         extracted_data.extend(table_data)  # Combine data if there are multiple tables
    #     except Exception as e:
    #         print(f"Error processing table: {e}")

    # Print the extracted data
    print("Extracted Table Data:", extracted_data)



