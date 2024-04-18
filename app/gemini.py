import json
from django.conf import settings
import google.generativeai as genai
import logging

log = logging.getLogger('app')


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]
        # SYSTEM_PROMPT = """
        #                 Summarize the given text to create a concise summary suitable for a LinkedIn post. \
        #                 Additionally, categorize the content into one of the following flags: 'news', 'information', or 'other'.\
        #                 Return the result in JSON format with the following structure:
        #                     {
        #                         'text': < summary > ,
        #                         'flag': < flag >
        #                     }
        #                 """
        character_limit = 280
        SYSTEM_PROMPT = f"""
**Task:** Summarize the given text for a LinkedIn audience and categorize its content.

**Input:**

* Text: A string containing the text to be summarized.

**Output:**

A JSON object with the following keys:

* `text`: (string) A concise summary suitable for a LinkedIn post, limited to a character count of {character_limit} (e.g., 280 characters).
* `flag`: (string) Category of the content, one of the following:
    * `news`: If the content reports on current events.
    * `information`: If the content provides general knowledge or educational value.
    * `other`: If the content doesn't fit into the "news" or "information" categories (e.g., opinions, stories).

**Additional Considerations:**

* Maintain a neutral and objective tone in the summary. 
* Avoid including personal opinions or biases.
* Focus on the key takeaways of the original text.
* Use clear and concise language suitable for a broad LinkedIn audience.
"""
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            system_instruction=[SYSTEM_PROMPT],
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

    def generate_completion(self, message):
        conversation = self.model.start_chat()
        try:
            conversation.send_message(message)
            log.debug(f'Gemini request sucessfull')
            response = conversation.last.text
            cleaned_data_string = response.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned_data_string)
        except Exception as e:
            log.debug(f'Error Gemini: {str(e)}')
            return None
