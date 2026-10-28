"""Lesson 2.2: Sweet Crumbs bot with memory, using a list of messages."""

from langchain.chat_models import init_chat_model

MAX_MESSAGES = 6  # keep memory short so the chat stays fast and cheap

SYSTEM = """You are the friendly assistant of Sweet Crumbs bakery in Lahore.
Answer in 2 short lines.
Facts: open 10 AM to 10 PM, closed on Mondays. Chocolate cake Rs 1,800.
If you don't know something, say a staff member will help."""

llm = init_chat_model("llama3.2:1b", model_provider="ollama", temperature=0.3)

# Create the list once, before the loop, so it survives every turn
messages = [{"role": "system", "content": SYSTEM}]

print("Sweet Crumbs Bot: Ask me anything. Commands: /reset, bye")

while True:
    text = input("You: ").strip()

    if text.lower() == "bye":
        print("Bot: Goodbye!")
        break
    elif text.lower() == "/reset":
        messages = [messages[0]]  # forget the chat, keep the rules
        print("Bot: Memory cleared.")
    elif text == "":
        print("Bot: Please type a question.")
    else:
        messages.append({"role": "user", "content": text})

        # Trim old messages but always keep the system message first
        messages = [messages[0]] + messages[1:][-MAX_MESSAGES:]

        response = llm.invoke(messages)
        answer = response.text

        # Save the reply too, or the AI forgets what it said
        messages.append({"role": "assistant", "content": answer})

        print(f"Bot: {answer}")
        print(f"     (memory: {len(messages)} messages, {response.usage_metadata['input_tokens']} tokens sent)")