from openai import OpenAI
import json
import sys
from typing import List, Dict, Optional

def analyze_html_structure(headers: List[str], example_entry: List[str], html_content: str) -> Optional[Dict]:
    """
    Analyze HTML content and extract vocabulary terms based on provided headers and example entry.
    
    Args:
        headers: List of header names for vocabulary fields
        example_entry: Example entry provided by the user for mapping headers correctly
        html_content: HTML content to analyze
        
    Returns:
        Dictionary containing vocabulary data or None if analysis fails
    """
    
    # Format the headers and example entry as JSON
    formatted_example = json.dumps([{headers[i]: example_entry[i] for i in range(len(headers))}], ensure_ascii=False, indent=4)
    formatted_headers = json.dumps(headers, ensure_ascii=False)
    
    system_prompt = f"""You are an HTML analyzer. Your task is to extract vocabulary terms from the provided HTML content.
    The data should be returned as a JSON object with the following headers: {formatted_headers}.
    
    To help you understand the structure, here is an example of the correct format for the first entry, based on the provided headers:
    
    Example Entry:
    {formatted_example}
    
    Ensure the output follows this structure exactly.

    Return the data in this JSON format:
    {{
        "vocabulary": [
            {{
                {', '.join(f'"{header}": "example"' for header in headers)}
            }}
        ],
        "metadata": {{
            "total_entries": 0,
            "headers": {formatted_headers}
        }}
    }}

    Rules:
    1. Extract only raw text (ignore audio, formatting)
    2. Ensure each entry has all fields, in the correct order
    3. Preserve exact spelling and characters as shown in the HTML content
    4. Use the first example to ensure correct field mapping and formatting
    """

    user_prompt = f"Extract vocabulary terms from this HTML using these headers: {headers}\n\nHTML content:\n{html_content}"

    try:
        # Create OpenAI client
        client = OpenAI()
        
        # Get response from GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}  # Enforce JSON response
        )
        
        # Extract and parse JSON response
        response_content = response.choices[0].message.content
        parsed_data = json.loads(response_content)
        # Validate JSON structure
        validate_response(parsed_data, headers)
        
        return parsed_data

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response: {e}")
        return None
    except ValueError as e:
        print(f"Error: Validation failed: {e}")
        return None
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return None

def validate_response(data: Dict, expected_headers: List[str]) -> None:
    """
    Validate the structure and content of the API response.
    
    Args:
        data: Parsed JSON data to validate
        expected_headers: List of expected header fields
        
    Raises:
        ValueError: If validation fails
    """
    # Check required top-level keys
    if not all(key in data for key in ["vocabulary", "metadata"]):
        raise ValueError("Missing required top-level keys")
    
    # Validate metadata
    if not all(key in data["metadata"] for key in ["total_entries", "headers"]):
        raise ValueError("Missing required metadata fields")
    
    # Validate vocabulary entries
    if not data["vocabulary"]:
        raise ValueError("No vocabulary entries found")
    
    # Check all entries have all required fields
    expected_fields = [header for header in expected_headers]
    for entry in data["vocabulary"]:
        missing_fields = [field for field in expected_fields if field not in entry]
        if missing_fields:
            raise ValueError(f"Missing fields in entry: {missing_fields}")
        
        # Validate no empty values
        empty_fields = [field for field, value in entry.items() if not value.strip()]
        if empty_fields:
            raise ValueError(f"Empty values found in fields: {empty_fields}")

def get_vocab(headers: List[str], example_entry: Dict[str, str], html_content: str) -> Optional[Dict]:
    """
    Get vocabulary data from user input.
    
    Args:
        headers: List of headers for the vocabulary terms.
        example_entry: Example entry for each header.
        html_content: HTML content to analyze.
    
    Returns:
        Dictionary containing vocabulary data or None if process fails
    """
    try:
        if not html_content:
            print("Error: No HTML content provided")
            return None
            
        if not headers:
            print("Error: No headers provided")
            return None

        # Run analysis and return results
        result = analyze_html_structure(headers, example_entry, html_content)
        
        if result:
            print(f"\nSuccessfully extracted {len(result['vocabulary'])} vocabulary entries")
            return result
        
        return None

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
