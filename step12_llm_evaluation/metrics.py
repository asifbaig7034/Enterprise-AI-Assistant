def keyword_overlap(expected, generated):

    expected_words = set(
        expected.lower().replace(".", "").split()
    )

    generated_words = set(
        generated.lower().replace(".", "").split()
    )

    if not expected_words:
        return 0.0

    overlap = expected_words.intersection(
        generated_words
    )

    return len(overlap) / len(expected_words)


def contains_required_fact(
    generated,
    required_fact
):

    generated = generated.lower()
    required_fact = required_fact.lower()

    return required_fact in generated
def check_faithfulness(
    generated,
    context
):

    generated = generated.lower()
    context = context.lower()

    important_numbers = [
        word
        for word in generated.split()
        if any(char.isdigit() for char in word)
    ]

    for number in important_numbers:

        if number not in context:
            return False

    return True
def recall_at_k(
    retrieved_ids,
    relevant_ids,
    k
):

    top_k = retrieved_ids[:k]

    for document_id in relevant_ids:

        if document_id in top_k:
            return 1.0

    return 0.0
