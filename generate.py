from g4f.client import Client
from prompts import system_feature_request
import json
import g4f

client = Client()


def generate_feature_request(description, features, feature_number):
    for _ in range(8):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": system_feature_request.replace("{{description}}", description).replace("{{feature_number}}", feature_number).replace("{{features}}", features)}],
        )
        try:
            output = response.choices[0].message.content.split("```json")[1].split("```")[0].strip()
            output = json.loads(output)
            return output
        except:
            print(f"Try #{_} failed")
            continue
