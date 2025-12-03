import OpenAI from 'openai';
import { ENV } from './config/env.js';
import readlineSync from 'readline-sync';

const client = new OpenAI({
    apiKey: ENV.GEMINI_API_KEY,
    baseURL: 'https://generativelanguage.googleapis.com/v1beta/openai',
});

function getWeatherDetails(city = '') {
    const lowerCaseCity = city.toLowerCase();

    if (lowerCaseCity === 'patiala') return `10°C`;
    if (lowerCaseCity === 'mohali') return `20°C`;
    if (lowerCaseCity === 'banglore') return `30°C`;
    if (lowerCaseCity === 'delhi') return `40°C`;
}

const TOOLS = {
    getWeatherDetails: getWeatherDetails,
};

const SYSTEM_PROMPT = `
    You are an AI Assistant with START, PLAN, ACTION, observation and Output States.
    Wait for the user prompt and first PLAN using available tools.
    After Plannig, take the action appropriate tools and wait for the Observation based on Action.
    Once you get the Observations, Return the response based on START prompt and Observations.


    Strictly follow the Json output format as in example

    AVAILABLE TOOLS:
    - function getWeatherDetails(city:String):String
    getWeatherDetails is a function that accept city name as string and return the weather details

    EXAMPLE:
    START
    {"type": "user", "user": "What is the sum of the weathers of the Patiala and Mohali?"}
    {"type": "plan", "plan": "I will call the getWeatherDetails for Patiala"}
    {"type": "action", "function": "getWeatherDetails", "input": "Patiala"}
    {"type": "observation", "observation": "10°C"}
    {"type": "plan", "plan": "I will call the getWeatherDetails for mohali"}
    {"type": "action", "function": "getWeatherDetails", "input": "mohali"}
    {"type": "observation", "observation": "30°C"}
    {"type": "output", "output": "Sum of weathers of Patiala and Mohali is: 40°C"}
`;

const messages = [{ role: 'system', content: SYSTEM_PROMPT }];

while (true) {
    const USER_QUERY = readlineSync.question('>> ');

    const user_query = {
        type: 'user',
        user: USER_QUERY,
    };

    messages.push({ role: 'user', content: JSON.stringify(user_query) });

    while (true) {
        const chat = await client.chat.completions.create({
            model: 'gemini-2.5-flash-live',
            messages: messages,
            response_format: { type: 'json_object' },
        });

        const result = chat.choices[0].message.content;
        messages.push({ role: 'assistant', content: result });

        const call = JSON.parse(result);

        if (call.type === 'output') {
            console.log(`🤖: ${call.output}`);
            break;
        } else if (call.type === 'action') {
            const fn = TOOLS[call.function];
            const observation = fn(call.input);
            const obs = { type: 'observation', observation: observation };
            messages.push({ role: 'developer', content: JSON.stringify(obs) });
        }
    }
}
