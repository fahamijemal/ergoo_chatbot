import requests
from django.conf import settings
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

def generate_text_with_gemini(prompt):
    """
    This function sends a prompt to the Google Gemini API and returns the response.
    If there is an error, it logs it and returns a default error message.
    """
    # Prepare the headers for the request, including the Authorization token
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",  # Authorization header using the Gemini API key from settings
        "Content-Type": "application/json"  # Setting the content type as JSON
    }

    # Prepare the payload data for the request
    data = {
        "contents": [{"parts": [{"text": prompt}]}]  # Format the prompt in the required structure
    }

    try:
        # Send a POST request to the Gemini API with the provided data and headers
        response = requests.post(settings.GEMINI_API_URL, headers=headers, json=data)

        # Raise an error if the response status code indicates failure
        response.raise_for_status()

        # Parse the response data from JSON
        response_data = response.json()

        # Log the full response from the Gemini API for debugging purposes
        logger.info(f"Gemini API response: {response_data}")

        # Return the 'response' field from the API's response if it exists, otherwise return a fallback message
        return response_data.get('response', "I couldn't understand that.")

    except requests.exceptions.RequestException as e:
        # Log any errors that occur during the request or response handling
        logger.error(f"Error with Google Gemini API: {str(e)}")
        
        # Return a default error message if an exception is raised
        return "Sorry, I couldn't get a response from the AI at the moment."
