import json


REQUIRED_FIELDS = [
    "input",
    "output"
]


dataset = []


with open(
    "dataset.jsonl",
    "r",
    encoding="utf-8"
) as file:

    for line_number, line in enumerate(
        file,
        start=1
    ):

        line = line.strip()

        if not line:
            continue

        try:

            example = json.loads(line)

        except json.JSONDecodeError as error:

            print(
                f"[ERROR] Invalid JSON on line "
                f"{line_number}"
            )

            print(error)

            continue

        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if field not in example
        ]

        if missing_fields:

            print(
                f"[ERROR] Line {line_number} "
                f"is missing: {missing_fields}"
            )

            continue

        if not example["input"].strip():

            print(
                f"[ERROR] Empty input on line "
                f"{line_number}"
            )

            continue

        if not example["output"].strip():

            print(
                f"[ERROR] Empty output on line "
                f"{line_number}"
            )

            continue

        dataset.append(example)


print("=" * 60)
print("DATASET VALIDATION")
print("=" * 60)

print("Valid examples:", len(dataset))
print("Invalid examples:", 12 - len(dataset))

if len(dataset) == 12:

    print("\nDataset validation PASSED.")

else:

    print("\nDataset validation FAILED.")
