import json


input_file = "intent_dataset.jsonl"
output_file = "gpt2_dataset.jsonl"


with open(input_file, "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f]


with open(output_file, "w", encoding="utf-8") as f:

    for record in records:

        text = (
            "Question: "
            + record["input"]
            + "\nAnswer: "
            + record["output"]
        )

        f.write(
            json.dumps({"text": text})
            + "\n"
        )


print("GPT-2 dataset created.")
print("Examples:", len(records))
print("Output:", output_file)

