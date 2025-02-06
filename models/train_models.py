import torch
from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
import os

# Define save path inside Hugging Face Spaces
save_path = "./model_output/"
os.makedirs(save_path, exist_ok=True)

# Load T5 tokenizer and model
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)

def fine_tune_model(dataset_path, output_dir):
    """Fine-tunes T5-base on the given dataset."""
    
    # Load dataset
    dataset = load_dataset("json", data_files=dataset_path)["train"]
    
    # Tokenization function
    def tokenize_data(batch):
        return tokenizer(batch["prompt"], text_target=batch["completion"], padding="max_length", truncation=True, max_length=512)
    
    # Tokenize dataset
    tokenized_dataset = dataset.map(tokenize_data, batched=True)
    
    # Split into train/test
    train_test = tokenized_dataset.train_test_split(test_size=0.1)
    train_data, test_data = train_test["train"], train_test["test"]
    
    # Load model
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    
    # Training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir=save_path + "logs",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        gradient_accumulation_steps=4,
        learning_rate=3e-5,
        weight_decay=0.01,
        save_total_limit=2,
        num_train_epochs=3,
        predict_with_generate=True,
        fp16=torch.cuda.is_available(),  # Use mixed precision if available
        report_to="none"  # Disable logging to external services
    )
    
    # Initialize Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=test_data,
        tokenizer=tokenizer,
        data_collator=data_collator
    )
    
    # Train the model
    trainer.train()
    
    # Save fine-tuned model
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model fine-tuning complete! Saved at {output_dir}")

# Fine-tune Model 1: Ingredient-to-Recipe Names
fine_tune_model("ingredients_to_recipe_names.json", save_path + "t5_recipe_names_model")

# Fine-tune Model 2: Recipe Names-to-Instructions
fine_tune_model("recipe_names_to_instructions.json", save_path + "t5_recipe_instructions_model")