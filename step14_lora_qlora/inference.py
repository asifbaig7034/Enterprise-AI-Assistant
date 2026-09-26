from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


BASE_MODEL = "sshleifer/tiny-gpt2"
ADAPTER_PATH = "./lora_output"


print("=" * 60)
print("LOADING TOKENIZER")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL
)

tokenizer.pad_token = tokenizer.eos_token


print("\n" + "=" * 60)
print("LOADING BASE MODEL")
print("=" * 60)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL
)


print("\n" + "=" * 60)
print("LOADING LoRA ADAPTER")
print("=" * 60)

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH
)

model.eval()

print("LoRA adapter loaded successfully.")


questions = [
    "How many annual leave days are available?",
    "Can employees work from home?",
    "How frequently should passwords be changed?",
    "When should I request vacation?"
]


for question in questions:

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
        max_new_tokens=40,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    generated_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    print("\n" + "=" * 60)
    print("QUESTION")
    print("=" * 60)
    print(question)

    print("\n" + "=" * 60)
    print("MODEL OUTPUT")
    print("=" * 60)
    print(generated_text)
