import ollama

response = ollama.chat(
    model="mistral",
    messages=[
        {"role": "user", "content": "Say hello in one short sentence."}
    ]
)

print(response["message"]["content"])
