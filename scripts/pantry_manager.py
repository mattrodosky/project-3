from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import random

# Load model
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)

# Force CPU usage
device = "cpu"
model.to(device)

# **Bias Factors** - Helps force key ingredients higher
bias_factors = {
    "protein": 0.9,  # Steak, Chicken, Fish
    "vegetable": 0.6,  # Tomato, Carrot, Bell Pepper
    "herb": 0.4,  # Cilantro, Basil, Parsley
    "seasoning": 0.3,  # Salt, Pepper, Paprika
    "liquid": 0.2,  # Vinegar, Lemon Juice, Broth
    "neutral": 0.1,  # Water, Ice, Basic Items
}

# **Ingredient Type Mapping** (You can expand this!)
ingredient_types = {
    "steak": "protein",
    "chicken": "protein",
    "fish": "protein",
    "tomato": "vegetable",
    "cilantro": "herb",
    "basil": "herb",
    "paprika": "seasoning",
    "vinegar": "liquid",
    "water": "neutral",
}

# **Rescaling function** - Forces better spread between 0 and 1
def rescale(value):
    """
    Apply a stabilized sigmoid transformation to spread values evenly while avoiding 0.0 outputs.
    """
    scale_factor = 2.5  # Balanced spread without over-squishing values
    bias = 0.15  # Ensures small values don't round to zero

    tensor_value = torch.tensor(value * scale_factor, dtype=torch.float32)

    # Apply sigmoid transformation
    weight = 1 / (1 + torch.exp(-tensor_value)).item()

    # Adjust with bias to prevent zeros
    return round(max(weight, bias), 2)
# Assign ingredient weight
def get_ingredient_weight(ingredient):
    category = ingredient_types.get(ingredient.lower(), "neutral")  # Default to neutral if unknown
    bias = bias_factors.get(category, 0.1)  # Apply category-based bias

    prompt = (
        f"Rate the importance of {ingredient} in a recipe. "
        "A higher score (closer to 1.0) means it is essential (e.g., chicken in a chicken dish). "
        "A lower score (closer to 0.0) means it is optional or rarely the focus (e.g., parsley in a stew). "
        "Consider these examples:\n"
        "- Steak: 0.95 (Main protein)\n"
        "- Chicken: 0.9 (Main protein)\n"
        "- Tomato: 0.7 (Base ingredient)\n"
        "- Cilantro: 0.5 (Enhances flavor, not necessary)\n"
        "- Paprika: 0.3 (Adds flavor, but minor role)\n"
        "- Vinegar: 0.2 (Acidic enhancement)\n"
        "- Water: 0.1 (Always present, not a defining ingredient)\n"
        "Respond with just a single number between 0 and 1."
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model(**inputs).logits.squeeze().item()

    #Debugging raw out put print output
    raw_output = model.generate(**inputs, max_length=10)
    response = tokenizer.decode(raw_output[0], skip_special_tokens=True)
    print("Raw model output:", response)

    # **Apply Bias & Rescale**
    weight = rescale(output) * bias  

    # **Random Variation (Prevents clustering)**
    weight = round(weight + random.uniform(-0.05, 0.05), 2)

    return max(0.0, min(1.0, weight))  # Clamp between 0-1
