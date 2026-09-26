prompts = {
    "short": "Explain RAG.",
    
    "medium": """
    You are an experienced machine learning instructor.
    Explain Retrieval-Augmented Generation to a beginner.
    Use simple English and give one example.
    """,

    "long": """
    You are an experienced machine learning instructor
    with extensive knowledge of artificial intelligence,
    natural language processing, large language models,
    retrieval-augmented generation, vector databases,
    embeddings, semantic search, and production AI systems.

    Explain Retrieval-Augmented Generation to a beginner
    who understands Python but has never worked with LLMs.

    Explain what RAG is, why it is needed, how retrieval
    works, how embeddings are used, how vector databases
    are involved, and how the retrieved information is
    provided to the language model.

    Use simple English and provide a practical example.
    """
}

for name, prompt in prompts.items():
    print("=" * 60)
    print(name.upper())
    print("=" * 60)

    print("Characters:", len(prompt))
    print("Words:", len(prompt.split()))
    print()