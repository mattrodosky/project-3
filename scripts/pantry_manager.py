# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# # Load TinyLlama model and tokenizer
# MODEL_NAME = "EleutherAI/gpt-neo-1.3B"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Ingredient importance prompt
# IMPORTANCE_PROMPT = """You are an expert chef and food scientist. 
# Assign an importance value between 0 and 1 to the following ingredient based on its role in cooking.
# More essential ingredients (like flour, eggs, salt) should have higher values.
# Less crucial or highly substitutable ingredients (like herbs or optional toppings) should have lower values.

# Ingredient: {ingredient}
# Importance (0-1): """

# def get_ingredient_weight(ingredient):
#     """Uses prompt engineering with TinyLlama to assign ingredient importance."""
#     prompt = IMPORTANCE_PROMPT.format(ingredient=ingredient)
    
#     # Tokenize input
#     inputs = tokenizer(prompt, return_tensors="pt").to(device)

#     # Generate response
#     with torch.no_grad():
#         output = model.generate(**inputs, max_new_tokens=10)

#     # Decode and extract number
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
    
#     # Extract numeric value
#     try:
#         weight = float(response.split("Importance (0-1):")[-1].strip())
#         weight = max(0, min(1, weight))  # Ensure between 0-1
#     except ValueError:
#         weight = 0.5  # Default fallback

#     return round(weight, 3)
