import json

from metrics import check_faithfulness


with open("evaluation_dataset.json", "r") as file:
    dataset = json.load(file)


test_answers = {
    1: "Employees receive 24 annual vacation days.",
    2: "Vacation requests should be submitted five working days in advance.",
    3: "Employees can work remotely up to two days per week.",
    4: "Employees must change their password every 30 days.",
    5: "Employees must never share their passwords.",
    6: "I couldn't find this information in the available company policies."
}


for item in dataset:

    question_id = item["id"]

    context = item["expected_context"]

    answer = test_answers[question_id]

    faithful = check_faithfulness(
        answer,
        context
    )

    print("=" * 60)

    print("Question:")
    print(item["question"])

    print("\nContext:")
    print(context)

    print("\nGenerated answer:")
    print(answer)

    print("\nFaithful:", faithful)

