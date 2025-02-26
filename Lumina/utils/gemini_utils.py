import google.generativeai as genai
import os

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Gemini API key not found.")
genai.configure(api_key=GOOGLE_API_KEY)

def gemini_text_extraction(pdf_path):
    """Extracts text from a PDF using Gemini API to handle encoding inconsistencies."""
    try:
        # Upload file to Gemini
        uploaded_file = genai.upload_file(path=pdf_path, display_name="Nepali PDF Document")
        print(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")

        # Use Gemini model
        model = genai.GenerativeModel(model_name="gemini-2.0-flash") 

        # Prompt for text extraction
        prompt = [
            {
                "parts": [
                    {"text": "Extract the full text content from this Nepali PDF document."},
                    {"file_data": {"mime_type": "application/pdf", "file_uri": uploaded_file.uri}}
                ]
            }
        ]

        # Get response from Gemini
        response = model.generate_content(prompt)

        return response.text if response else "No text extracted."

    except Exception as e:
        print(f"Error in gemini_text_extraction: {e}")
        return f"Error extracting text: {e}"

def generate_answer_with_llm(prompt):
    try:
        # Initialize Gemini model or another LLM as needed
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        # Construct the prompt parts for the LLM
        prompt_structure = [{"parts": [{"text": prompt}]}]
        response = model.generate_content(prompt_structure)
        return response.text if response else "No answer generated."
    except Exception as e:
        print(f"Error in generating answer: {e}")
        return f"Error generating answer: {e}"
