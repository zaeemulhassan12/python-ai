"""Lesson 2.1: Sweet Crumbs bot: fixed rules first, AI for everything else."""

from langchain.chat_models import init_chat_model

# Give the AI the real facts, or it will invent them
SYSTEM = """You are the friendly assistant of Sweet Crumbs bakery in Lahore.
Answer in 2 short lines.
Facts: open 10 AM to 10 PM, closed on Mondays. Chocolate cake Rs 1,800.
If you don't know something, say a staff member will help."""

# Create the model once, before the loop, so every question reuses it
llm = init_chat_model("llama3.2:1b", model_provider="ollama", temperature=0.3)

print("Sweet Crumbs Bot: Ask me anything. Type 'bye' to exit.")

while True:
    message = input("You: ").strip()

    # Rules first: free, instant and always correct
    if message.lower() == "bye":
        print("Bot: Goodbye!")
        break
    elif "refund" in message.lower():
        print("Bot: A manager will call you within 1 hour.")
    else:
        # Everything the rules cannot answer goes to the AI
        response = llm.invoke([
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": message},
        ])
        print(f"Bot: {response.text}")
        print(f"     ({response.usage_metadata['output_tokens']} tokens)")