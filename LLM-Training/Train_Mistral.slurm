#!/bin/bash
#SBATCH --job-name=mistral-train
#SBATCH --output=logs/mistral_%j.out
#SBATCH --error=logs/mistral_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G                        # Might want more memory for 7B model
#SBATCH --time=04:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=your.email@example.com

# Activate Conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate mistral-lora

# (Optional) Set HF token if needed
export HF_TOKEN="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"

# Run script
python Training_Mistral_LLM.py
