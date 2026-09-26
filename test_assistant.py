from app.main import ask_assistant


questions = [
    (
        "How many vacation days do employees receive?",
        "EMP001"
    ),

    (
        "Can employees work from home?",
        "EMP001"
    ),

    (
        "How often should I change my password?",
        "EMP001"
    ),

    (
        "How many vacation days do I have? My employee ID is EMP001.",
        "EMP001"
    ),

    (
        "How many vacation days do I have? My employee ID is EMP002.",
        "EMP001"
    ),

    (
        "What is the weather today?",
        "EMP001"
    )
]


for question, user_id in questions:

    print("\n" + "=" * 70)
    print("USER")
    print("=" * 70)

    print(question)

    result = ask_assistant(
        question,
        user_id
    )

    print("\nASSISTANT")
    print("=" * 70)

    print(result)
