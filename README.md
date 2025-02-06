# Project_3
## Introduction
This application takes in ingredients from the user, and uses them to generate recipes
that can be made.
- Go to pantry to add in ingredients that you have on hand.
- Go to the stove to generate recipes based on what you have in the pantry.
- Go to the cookbooks to incorportate preferences and diets into the meals that you
want the application to go for.
- Go to computer to find flavor pairings based on what you have to create a smaller pantry
and use those to find a recipe based off of a narrower selection.

## Architecture
### Initial Application
Application uses a PySide front-end incorportated with "untrained" Gemini api calls to find
recipes in accordance with user desires. Gemini prompts use prompt engineering to
build the request based off of ingredients, diet, cuisine, and prefered ingredients.

### Refactored Application
Application uses a gradio frontside incorportated with a model trained off of 
[this dataset](AkashPS11/recipes_data_food.com). Receipes are normalized and cleaned
so that ingredients, quantities, and units become standardized. Taking this model, 
our application utilizes 
#### FINSISH WHEN APP ~DONE

## Setting up the Environment
[Install Conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html#)
in the command line, run:
```
conda env create -f environment.yml
```
## Initial - Requesting a Gemini API Key
(Copied from bookcamp spot)\
Before we get to building an AI-powered application, we will need to obtain an OpenAI API key.

1. Head over to the [Google developers website](https://ai.google.dev/gemini-api/docs/api-key) and register for a new account or log in to an existing one by first clicking the "Sign In" button in the top right of the page.

2. Once you're logged in you should be taken back to the developers page (or can use the link above to return there.) From that page, click "Get an API key".

3. You may be presented with the choices of using Google AI Studio or developing in your own environment. Choose to develop in your own environment by clicking "Get API key". Then read and respond to the legal notices and/or terms of service for the Gemini API.

4. You should be taken to the "API Keys" page. Click "Create API key" to generate an API key for developmental use. You will need to associate the API key with a development project. If you don't already have any projects to associate it with, choose "Create API key in new project.

5. After clicking creating the key you will be able to view and copy your key. This is the key we will use in our applications to make API calls to Gemini. You should be able to view the key again in the future if you need to, but it's still recommended that you record it somewhere securely for your own records.

6. Then, take the key that was generated and add it as a environmental varaible named GEMINI_API_KEY.

## Running
### Initial
1. Navigate to /project-3/scripts-old/ui in a CLI
2. run
```
conda activate meal-planner
python kitchen_ui.py
```
### Refactored
1. Navigate to /project-3 in a CLI
2. run
```
conda activate meal-planner
python app.py
```
3. Open [the local port operating](http://127.0.0.1:7860) or copy paste the url from the output.