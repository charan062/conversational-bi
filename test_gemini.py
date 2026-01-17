import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Generate content using supported model
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Say hello in one short sentence."
)

print(response.text)



