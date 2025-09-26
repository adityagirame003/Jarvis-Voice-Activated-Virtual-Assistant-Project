from openai import OpenAI
import os

# Use environment variable for API key
api_key = os.environ.get('OPENAI_API_KEY')

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Initialize the client
client = OpenAI(api_key=api_key)

def ask_question(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Akash."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    result = ask_question("What is coding?")
    print(result)
