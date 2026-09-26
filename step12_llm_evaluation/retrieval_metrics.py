from metrics import recall_at_k


tests = [
    {
        "question": "How many vacation days?",
        "retrieved": [
            "chunk_1",
            "chunk_4",
            "chunk_3",
            "chunk_8",
            "chunk_10"
        ],
        "relevant": ["chunk_3"]
    },
    {
        "question": "How often must passwords change?",
        "retrieved": [
            "chunk_1",
            "chunk_2",
            "chunk_5",
            "chunk_6",
            "chunk_7"
        ],
        "relevant": ["chunk_9"]
    }
]


for test in tests:

    score = recall_at_k(
        test["retrieved"],
        test["relevant"],
        5
    )

    print("=" * 60)
    print("Question:", test["question"])
    print("Recall@5:", score)

