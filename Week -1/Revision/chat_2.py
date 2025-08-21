from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
result = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "hey there" # zero shot prompting
        }
    ]
)

print(result.choices[0].message.content)