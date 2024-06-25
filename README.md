# Alfabank test case

The main goal was to show how you can use the langchain libraries to create a simple web search agent.
Here is a quick start guide on how to use modules in your local environment:

## Requirements

Your machine must have Python version 3.11.4 installed.

## Setting Up Environment

1. First clone the repo to your local machine using:
```git clone <URL of Git Repo>```

2. Open terminal/command prompt and change your directory to the cloned repository by using
```cd <name_of_folder>```

3. The project uses various dependencies which are listed in `pyproject.toml`.
To install these dependencies, use the following command in terminal:
```
pip install poetry
poetry config virtualenvs.create true
poetry install
poetry shell
```
## Environment Configuration
1. You need to set up some environment variables before running the program. A sample .env.example file is provided in the repo.
Here are the steps to configure environment variables:
Rename .env.example to .env.
Replace <Your token> in OPENAI_API_KEY and LANGCHAIN_API_KEY fields with your actual tokens.

## Run the program
After setting up the environment and configuring variables, use the following commands to run agent_realization.py and graph_realization.py respectively:
```
python agent_realization.py
python graph_realization.py
```