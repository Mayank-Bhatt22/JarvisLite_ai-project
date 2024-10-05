import os
import google.generativeai as genai

# If you want to store the key in the code directly (not recommended for security reasons):
GENAI_API_KEY = "YOUR_KEY"

# Alternatively, if the key is stored in an environment variable:
# GENAI_API_KEY = os.environ["GENAI_API_KEY"]

# Configure the API
genai.configure(api_key=GENAI_API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(
  history=[]
)

# Send a message to the model and get a response
response = chat_session.send_message("what is coding")

print(response.text)
