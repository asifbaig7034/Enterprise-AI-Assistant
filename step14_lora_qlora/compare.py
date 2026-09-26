from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


BASE_MODEL = "sshleifer/tiny-gpt2"
ADAPTER_PATH = "./lora_output"


tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token


# -----------------------------
# Base model
# -----------------------------

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL
)

base_model.eval()


# -----------------------------
# LoRA model
# -----------------------------

lora_base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL
)

lora_model = PeftModel.from_pretrained(
    lora_base_model,
    ADAPTER_PATH
)

lora_model.eval()


questions = [
    "How many vacation days do employees receive?",
    "Can employees work remotely?",
    "How often must employees change their password?",
    "How far in advance should vacation be requested?"
]


def generate_answer(model, question):

    prompt = (
        "Question: "
        + question
        + "\nAnswer:"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=20,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )


print("=" * 70)
print("BASE MODEL VS LoRA MODEL")
print("=" * 70)


for question in questions:

    base_answer = generate_answer(
        base_model,
        question
    )

    lora_answer = generate_answer(
        lora_model,
        question
    )

    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)
    print(question)

    print("\n--- BASE MODEL ---")
    print(base_answer)

    print("\n--- LoRA MODEL ---")
    print(lora_answer)
