import json


input_file = "intent_dataset.jsonl"
output_file = "lora_dataset.jsonl"


with open(input_file, "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f]


converted = []

for record in records:

    converted.append(
        {
            "messages": [
                {
                    "role": "user",
                    "content": record["input"]
                },
                {
                    "role": "assistant",
                    "content": record["output"]
                }
            ]
        }
    )


with open(output_file, "w", encoding="utf-8") as f:

    for record in converted:
        f.write(json.dumps(record) + "\n")


print("Dataset conversion completed.")
print("Original examples:", len(records))
print("Converted examples:", len(converted))
print("Output file:", output_file)
