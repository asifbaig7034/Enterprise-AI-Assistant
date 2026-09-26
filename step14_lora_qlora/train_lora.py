from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer


MODEL_NAME = "sshleifer/tiny-gpt2"

DATASET_FILE = "gpt2_dataset.jsonl"

OUTPUT_DIR = "./lora_output"


print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

dataset = load_dataset(
    "json",
    data_files=DATASET_FILE,
    split="train"
)

print(dataset)
print("Number of examples:", len(dataset))


print("\n" + "=" * 60)
print("LOADING TOKENIZER")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# GPT-2 does not have a padding token by default.
tokenizer.pad_token = tokenizer.eos_token

print("Tokenizer loaded.")


print("\n" + "=" * 60)
print("LOADING MODEL")
print("=" * 60)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

model.config.pad_token_id = tokenizer.pad_token_id

print("Model loaded.")


print("\n" + "=" * 60)
print("CONFIGURING LoRA")
print("=" * 60)

peft_config = LoraConfig(
    r=4,
    lora_alpha=8,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["c_attn"]
)

print("LoRA configuration created.")


print("\n" + "=" * 60)
print("TRAINING")
print("=" * 60)

training_args = SFTConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    learning_rate=2e-4,
    logging_steps=1,
    save_strategy="epoch",
    report_to="none",
    use_cpu=True,
    bf16=False,
    fp16=False,
    dataset_text_field="text",
    max_length=128
)


trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    processing_class=tokenizer,
    peft_config=peft_config
)


trainer.train()


print("\n" + "=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)

trainer.save_model(OUTPUT_DIR)

print("LoRA adapter saved to:", OUTPUT_DIR)