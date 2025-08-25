import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")


def get_weather(city: str):
    return "32 degree celcius"


client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

system_prompt = """
You are an helpfull AI Assistant who is specialized in resolving user query.
You work on start, plan, action, observe mode.
for the given user query and available tool, plan the step by step execution, based on the planning select the relevent tool from the available tool. and based on the tool selection yu perform an action to call the tool. wait fot the observation and based on the observation resolve the user query.
 
Rules:
- Follow the output JSON Format.
- Always perform one step at a time and wait for the next input.
- Carefully analyze the user query

Output JSON Format:
{{
    "step": "string"
    "content": "string",
    "function": "The name of the function if the step is action"
    "input": "The input parameter for the function"
}}
 
 
Example:
User query: What is the weather of new york.
Output: {{"step": "start", "content": "The user is interested in weather data of new york" }}
Output: {{"step": "plan", "content": "From the available tool i should call the get_weather"}}
Output: {{"step": "action", "function": "get_weather", "input": "new york"}}
Output: {{"step": "Obsserve", "output": "12 degree celcius"}}
Output: {{"step": "output", "content": "The weather for the new york seems to  be 12 degree celcius"}}
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "what is the current weather of Lucknow"},
        {"role": "assistant", "content": json.dumps(

            {
                "step": "start",
                "content": "The user is interested in the current weather of Lucknow."
            }
        )},
        {"role": "assistant", "content": json.dumps(

            {
                "step": "plan",
                "content": "I should use a tool to get the current weather information for Lucknow. The `get_weather` tool seems appropriate for this task."
            }
        )},
        {"role": "assistant", "content": json.dumps(

            {
                "step": "action",
                "function": "get_weather",
                "input": "Lucknow"
            }
        )},
        {"role": "assistant", "content": json.dumps(

            {"step": "Obsserve", "output": "28 degrees Celsius, partly cloudy"}
        )},
    ]
)

result = response.choices[0].message.content
print(result)
