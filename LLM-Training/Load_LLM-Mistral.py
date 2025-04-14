from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType
import torch
from huggingface_hub import login

# Login with your token (don't hardcode it in production)
login(token="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")

model_name = "mistralai/Mistral-7B-v0.1"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,  # Use float16 for faster GPU inference
    use_auth_token=True         # Correct argument for private model access
)

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    use_auth_token=True
)

config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, config)

print("Model loaded successfully with LoRA on GPU!")
