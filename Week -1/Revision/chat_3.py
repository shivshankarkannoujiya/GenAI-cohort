from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
You are an AI Assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input analyze the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyze, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well as before giving final result.

Follow the steps in sequence that is "analyze", "think", "output", "validate" and finally "result"

Rules:
1. Follow the strict JSON format as per Output schema.
2. Always perform one step at a time and wait for next input.
3. Carefully analyze user query.

Output Format:
{{step: "string", content: "string"}}

Example:
Input: What is 2 + 2
Output: {{step: "analyze", content: "Alright! The user is interested in maths query and he is asking a basic arithmetic operation"}}
Output: {{step: "think", "content": "To performt he addition i must go from left to right and add all the operands"}}
Output: {{step: "output", "content": "4"}}
Output: {{step: "validate", "content": "seems like 4 is correct answer for 2 + 2"}}
Output: {{step: "result", "content": "2 + 2 = 4 and that is calculated by adding all numbers"}}
"""

result = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "what is 3 + 4 * 5"},
        # Assistant
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "analyze",
                    "content": "The user is asking to evaluate a mathematical expression: '3 + 4 * 5'. This involves arithmetic operations, specifically addition and multiplication. I need to apply the correct order of operations.",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "think",
                    "content": "To solve '3 + 4 * 5', I must follow the order of operations, commonly known as PEMDAS/BODMAS. This dictates that multiplication and division should be performed before addition and subtraction. Therefore, I will first calculate 4 * 5, and then add the result to 3. \n\nStep 1: Calculate 4 * 5.\nStep 2: Add 3 to the result from Step 1.",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps({"step": "output", "content": "23"}),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "validate",
                    "content": "Let's validate the output. Following the order of operations (PEMDAS/BODMAS), multiplication comes before addition. So, first calculate 4 * 5 = 20. Then, add 3 to 20, which is 3 + 20 = 23. The output '23' is consistent with this calculation.",
                }
            ),
        },
    ],
)

print(result.choices[0].message.content)
