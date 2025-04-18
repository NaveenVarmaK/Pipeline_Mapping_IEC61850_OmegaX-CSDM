from transformers import AutoTokenizer
from datasets import load_dataset

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

if tokenizer.pad_token is None:
	tokenizer.pad_token = tokenizer.eos_token

dataset = load_dataset('json', data_files='../LLM-Training/Generated_Input_TrainingData/rml_instruction_data.jsonl', split='train')

def tokenize_function(examples):
	prompt =f"### Instruction:\n{examples['instruction']}\n\n### Input:\n{examples['input']}\n\n### Response:\n"
	response = examples["output"]
	
	prompt_ids = tokenizer(prompt, truncation=True, max_length=15000, padding='max_length')
	response_ids = tokenizer(response, truncation=True, max_length=20000, padding='max_length')

	input_ids= prompt_ids["input_ids"] + response_ids["input_ids"]
	attention_mask = prompt_ids["attention_mask"]+ response_ids["attention_mask"]
	labels = [-100] * len(prompt_ids["input_ids"]) + response_ids["input_ids"]


	return {
		"input_ids":input_ids,
		"attention_mask":attention_mask,
		"labels":labels,
	}

tokenized_dataset = dataset.map(tokenize_function, batched=False)

tokenized_dataset.save_to_disk("Tokenized_rml_dataset")

print(f"Dataset loaded and tokenized successfully")
