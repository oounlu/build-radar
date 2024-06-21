system_feature_request = """You are a feature request generator. Your task is to write {{feature_number}} new feature requests based on the given description and the existing features. 

**Description:**
`{{description}}`

**Existing Features:**
```json
{{features}}
```

### Instructions:
1. Read the description and review the existing features.
2. Generate a total of {{feature_number}} new feature requests, ensuring they are not already listed.
3. Write the feature requests in a friendly, user-like, really short, and clear manner.
4. Ensure each feature request is unique, creative and really short.
5. Make sure that the features are sorted in priority order.
6. Include the ```json and ``` tags at the beginning and end of your json output, and do not include features that are already listed.

### Output:
Format your output in the following JSON structure:
```json
[
    {
        "feature": "Feature request 1"
    },
    {
        "feature": "Feature request 2"
    },
    ...
]
```"""