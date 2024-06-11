from g4f.client import Client
from prompts import system_feature_request
import json

client = Client()


def generate_feature_request(description, features, feature_number):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": system_feature_request.replace("{{description}}", description).replace("{{feature_number}}", feature_number).replace("{{features}}", features)}],
    )

    output = response.choices[0].message.content.split("```json")[1].split("```")[0].strip()
    output = json.loads(output)

    return output
