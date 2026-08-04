import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

print("=" * 60)
print("Groq Llama 3.3 Model Loaded Successfully!")
print("=" * 60)


def generate_response(prompt: str):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0

    )

    return response.choices[0].message.content


if __name__ == "__main__":

    prompt = input("Enter Prompt: ")

    result = generate_response(prompt)

    print("\nGroq Response:\n")

    print(result)