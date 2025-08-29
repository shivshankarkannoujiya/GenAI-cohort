import os
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
os.environ["HF_TOKEN"] = HF_TOKEN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "google/gemma-3-1b-it"

# pull/load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# print(tokenizer("hello, world!"))

input_conversation = [
    {"role": "user", "content": "which is best place to learn GenAI"},
    {"role": "assistant", "content": "The best place to learn GenAI is"}
]


# Tokenize user input
# Apply chat template into gemma model
input_tokens = tokenizer.apply_chat_template(
    conversation=input_conversation,
    # do not convert into numbers: give the raw string(depends on models)
    tokenize=False
)

# print(f"INPUT_TOKENS: {input_tokens}")


# Pull the model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16
).to(device)


# Check the model is working or not
input_prompt = "Which is the best place to learn GenAI?"
i_tokens = torch.tensor(tokenizer(input_prompt)[
                        "input_ids"]).unsqueeze(0).to(device)
output_tokens = model.generate(i_tokens)
print(f"OUTPUT_TOKENS: {output_tokens}")

# de-tokenize
decoed_tokens = tokenizer.batch_decode(output_tokens)
print(f"DECODED_TOKENS: {decoed_tokens}")
