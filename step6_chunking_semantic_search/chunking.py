document = """
Company Leave Policy

Employees receive 20 annual vacation days every calendar year.
Employees should submit vacation requests through their manager
at least five working days before the requested leave.

Remote Work Policy

Employees can work remotely two days per week with manager approval.
Employees must remain available during normal working hours.

Password Policy

Employees must change their company password every 90 days.
Passwords must contain uppercase letters, lowercase letters,
numbers, and special characters.
"""


def create_paragraph_chunks(text):
    paragraphs = text.strip().split("\n\n")

    chunks = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if paragraph:
            chunks.append(paragraph)

    return chunks


chunks = create_paragraph_chunks(document)


print("=" * 60)
print("PARAGRAPH CHUNKS")
print("=" * 60)

for i, chunk in enumerate(chunks, start=1):

    print(f"\n--- Chunk {i} ---")
    print(chunk)
    print("Characters:", len(chunk))