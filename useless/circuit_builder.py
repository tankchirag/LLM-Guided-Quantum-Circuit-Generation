from openai import OpenAI
import os

print(os.getenv("OPENAI_API_KEY"))  # Should print your key

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resp = client.models.list()
print([m.id for m in resp.data])
