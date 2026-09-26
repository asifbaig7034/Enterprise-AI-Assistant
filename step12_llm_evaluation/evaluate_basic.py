import json

from metrics import keyword_overlap


with open("evaluation_dataset.json", "r") as file:
    dataset = json.load(file)


generated_answers = {
    1: "Employees get 24 vacation days every year.",
    2: "Vacation requests should be submitted at least five working days in advance.",
    3: "Employees can work remotely up to two days per week with manager approval.",
    4: "Employees must change their password every 90 days.",
    5: "Employees must never share their passwords.",
    6: "I couldn't find this information in the available company policies."
}


scores = []


for item in dataset:

    question_id = item["id"]

    expected = item["expected_answer"]
    generated = generated_answers[question_id]

    score = keyword_overlap(
        expected,
        generated
    )

    scores.append(score)

    print("=" * 60)
    print("Question:", item["question"])
    print("Expected:", expected)
    print("Generated:", generated)
    print("Keyword overlap:", round(score, 2))


average_score = sum(scores) / len(scores)


print("\n" + "=" * 60)
print("EVALUATION SUMMARY")
print("=" * 60)

print(
    "Average keyword overlap:",
    round(average_score, 2)
)
