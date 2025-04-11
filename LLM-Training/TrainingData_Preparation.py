import os
import json
import tiktoken  # For counting tokens

# Set your file directories
csv_folder = "../LLM-Training/Input_Files/CSV_Files"
rml_folder = "../LLM-Training/Input_Files/RML_Files"
output_file = "../LLM-Training/Generated_Input_TrainingData/rml_instruction_data.jsonl"

# Instruction template
instruction_template = "Generate an RML mapping file based on the provided IEC 61850 CSV data."

# Initialize tokenizer (e.g., GPT-3.5)
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def count_tokens(text):
    return len(encoding.encode(text))


def create_training_sample(csv_content, rml_content, file_id):
    input_text = f"File: {file_id}\n\nCSV Data:\n{csv_content.strip()}"
    output_text = rml_content.strip()

    # Count tokens
    instruction_tokens = count_tokens(instruction_template)
    input_tokens = count_tokens(input_text)
    output_tokens = count_tokens(output_text)
    total_tokens = instruction_tokens + input_tokens + output_tokens

    # Print token stats to CLI
    print(f"Sample: {file_id}")
    print(f"  Input tokens: {input_tokens}")
    print(f"  Output tokens: {output_tokens}")
    print(f"  Total tokens: {total_tokens}\n")

    # Create sample
    return {
        "instruction": instruction_template,
        "input": input_text,
        "output": output_text,
        "token_count": total_tokens
    }


def get_file_id(filename):
    return os.path.splitext(filename)[0]


# Collect data pairs
samples = []
for filename in os.listdir(csv_folder):
    if not filename.endswith(".csv"):
        continue

    file_id = get_file_id(filename)
    csv_path = os.path.join(csv_folder, filename)

    # Match RML file by name
    for ext in [".ttl", ".jsonld"]:
        rml_path = os.path.join(rml_folder, file_id + ext)
        if os.path.exists(rml_path):
            csv_data = read_file(csv_path)
            rml_data = read_file(rml_path)
            sample = create_training_sample(csv_data, rml_data, file_id)
            samples.append(sample)
            break
    else:
        print(f"No RML file found for: {filename}")

# Save to JSONL
with open(output_file, "w", encoding='utf-8') as out:
    for sample in samples:
        out.write(json.dumps(sample, ensure_ascii=False) + "\n")

print(f"Saved {len(samples)} training samples to: {output_file}")
