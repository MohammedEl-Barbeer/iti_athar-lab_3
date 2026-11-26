import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("AI_API_KEY"))
model = os.getenv("MODEL", os.getenv("AI_MODEL"))

# Price per 1 million tokens (USD)
INPUT_PRICE_PER_1M = 0.10
CACHED_INPUT_PRICE_PER_1M = 0.01
OUTPUT_PRICE_PER_1M = 0.50

prompts = [
    "What is Gemini in four short points.",
    "Compare WordPress and Laravel in three short points.",
]

total_tokens = 0
total_cost = 0.0

for i, prompt in enumerate(prompts, start=1):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    reply = response.choices[0].message.content
    usage = response.usage

    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    cached_tokens = 0
    if usage.prompt_tokens_details and usage.prompt_tokens_details.cached_tokens:
        cached_tokens = usage.prompt_tokens_details.cached_tokens

    uncached_input_tokens = input_tokens - cached_tokens

    cost = (
        (uncached_input_tokens / 1_000_000) * INPUT_PRICE_PER_1M
        + (cached_tokens / 1_000_000) * CACHED_INPUT_PRICE_PER_1M
        + (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_1M
    )

    total_tokens += usage.total_tokens
    total_cost += cost

    print(f"--- Request {i} ---")
    print(reply)
    print(
        f"Tokens -> Input: {input_tokens} (Cached: {cached_tokens}), "
        f"Output: {output_tokens}, Total: {usage.total_tokens}"
    )
    print(f"Cost   -> ${cost:.8f}\n")

print("=== Total Summary ===")
print(f"Total Tokens: {total_tokens}")
print(f"Total Cost:   ${total_cost:.8f}")