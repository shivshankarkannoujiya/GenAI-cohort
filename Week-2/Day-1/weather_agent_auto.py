import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")


def get_weather(city: str):
    print("Tool called get_weather:", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"


available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as input and returns the current weather for the city"
    },
}

tools_description = "\n".join(
    [f"- {tool_name}: {tool_info['description']}" for tool_name,
        tool_info in available_tools.items()]
)

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

system_prompt = f"""
You are an helpfull AI Assistant who is specialized in resolving user query.
You work on start, plan, action, observe mode.
for the given user query and available tool, plan the step by step execution, based on the planning select the relevent tool from the available tool. and based on the tool selection yu perform an action to call the tool. wait fot the observation and based on the observation resolve the user query.

Rules:
- Follow the output JSON Format.
- Always perform one step at a time and wait for the next input.
- Carefully analyze the user query

Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

Available Tools:
{tools_description}

Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""

messages = [
    {"role": "system", "content": system_prompt},
]

while True:
    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append(
            {"role": "assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps(
                    {"step": "observe", "output": output}
                )})
                continue

        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break
