from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import pandas as pd
import torch

# Load model
base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", device_map="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
model = PeftModel.from_pretrained(base_model, "./results/checkpoint-3")
model.eval()

# Load CSV
csv_path = "../LLM-Training/Examples/Test_Meteosta_New_dataset.csv"
df = pd.read_csv(csv_path)
csv_str = df.to_csv(index=False)

# Create input
input_text = f"""### Instruction:
Generate an RML mapping file based on the provided IEC 61850 CSV data.

### Input:
# File: {csv_path}
# CSV Data:
{csv_str}

### Output:
"""

inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

# # Generate
# with torch.no_grad():
#     output = model.generate(**inputs, max_new_tokens=10000)

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=5000,           # Increase to get longer output
        temperature=0.7,               # Controls randomness
        top_p=0.95,                    # Nucleus sampling
        repetition_penalty=1.2,        # Penalize repetition
        do_sample=True,               # Enables sampling
        pad_token_id=tokenizer.eos_token_id  # Avoid warning
    )

generated_rml = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated RML:\n", generated_rml)

with open("generated_rml_output.txt", "w") as f:
    f.write(generated_rml)
