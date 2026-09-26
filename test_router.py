from app.agents.router import classify_intent


questions = [
    "How many vacation days do employees receive?",
    "Can employees work from home?",
    "How often should I change my password?",
    "How many vacation days do I have? My employee ID is EMP001.",
    "What is the weather today?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION")
    print("=" * 60)
    print(question)

    result = classify_intent(question)

    print("\nROUTER RESULT:")
    print(result.model_dump())
