# vision.py
import openai
from dotenv import load_dotenv
import os
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_price_info(image_path: str, site_name: str) -> str:
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that reads screenshots from {site_name} and identifies the lowest priced relevant product."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"This is a screenshot from {site_name} for a grocery product search. "
                            f"Please extract the **lowest priced item** with its **name and price** from this image. "
                            f"If prices are not clear or nothing is visible, say 'No data found'."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content.strip()
