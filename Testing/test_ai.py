import json
import typing_extensions as typing
import google.generativeai as genai

# Function to configure the AI model

with open('api.txt', 'r') as file:
    api_key = file.read().strip()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to check if data matches the schema
def check_schema(model, data, schema):
    class Recipe(typing.TypedDict):
        matched: bool
    prompt = f"Check if the given data matches the schema. Data: {json.dumps(data)}. Schema: {json.dumps(schema)}.\n"
    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[Recipe]
    ))
    return json.loads(response.text)

def main():
    # Example data and schema for testing
    data = {
        "email": "user@example.com",
        "password": "password123"
    }

    schema = {
        "email": "$string",
        "password": "$string"
    }

    # Check if the data matches the schema
    result = check_schema(model, data, schema)
    print(result[0]['matched'])

if __name__ == "__main__":
    main()
