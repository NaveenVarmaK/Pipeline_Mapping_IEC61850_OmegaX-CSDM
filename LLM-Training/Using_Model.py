import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained("./results", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("./results")
model.eval()

# Load your CSV file
csv_path = "data.csv"  # <- update with your file path
df = pd.read_csv(csv_path)

# Convert CSV to string input format
csv_str = df.to_csv(index=False)

# Create the full input prompt
input_text = f"""File: {csv_path}
CSV Data:
{csv_str}

Generate RML representation from the IEC61850 dataset:"""

# Tokenize input
inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

# Generate output
with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=512)

# Decode and print
generated_rml = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated RML:\n", generated_rml)
