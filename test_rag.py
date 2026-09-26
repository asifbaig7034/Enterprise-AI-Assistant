from app.rag.retriever import retrieve_context
from app.rag.generator import generate_grounded_answer


question = "How many vacation days do employees receive?"


context = retrieve_context(question)


print("\n" + "=" * 60)
print("RETRIEVED CONTEXT")
print("=" * 60)
print(context)


answer = generate_grounded_answer(
    question,
    context
)


print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)
print(answer)
