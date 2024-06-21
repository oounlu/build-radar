from gradio_client import Client
from prompts import system_feature_request
import json
import random

client = Client("Qwen/Qwen2-72B-Instruct")


def generate_feature_request(description, features, feature_number):
    response = client.predict(
        api_name="/model_chat",
        query=system_feature_request.replace("{{description}}", description).replace("{{feature_number}}", feature_number).replace("{{features}}", features),
    )[1][0][-1]
    try:
        output = response.replace("```json", "```").replace("```\njson", "```")
        output = output.split("```")[1].split("```")[0].strip()
        output = json.loads(output)

        upvotes = random.sample(range(1, 50), len(output))
        sorted_upvotes = sorted(upvotes, reverse=True)

        for index, feature in enumerate(output):
            feature.update({"upvotes": sorted_upvotes[index]})

        return output
    except:
        print(response)
        return []
