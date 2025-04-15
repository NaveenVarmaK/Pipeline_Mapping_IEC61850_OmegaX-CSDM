from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_from_disk
import torch

# 1. Load tokenizer
model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 2. Load model and apply LoRA again
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_8bit=True, device_map="auto")

lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)

# 3. Load the tokenized dataset from disk
tokenized_dataset = load_from_disk("Tokenized_rml_dataset")

# 4. Define training args and start training
training_args = TrainingArguments(
    output_dir="./mistral_rml_model",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    save_steps=500,
    logging_dir="./logs",
    learning_rate=2e-4,
    bf16=True,
    optim="adamw_torch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

trainer.train()
