# Lingua AI - English Tutor

**Enhancing English proficiency through interactive conversations and advanced AI-driven feedback.**

## Project Overview

This project is an interactive English tutoring application built using Streamlit, Deepgram, and the Groq LLM model. It offers functionalities to practice English through conversations, improve vocabulary, and test grammar skills.

## Tech Stack

- **Language Models:** Groq LLM (Llama 3.1)
- **Speech Synthesis:** Deepgram
- **Framework:** Streamlit
- **Programming Language:** Python
- **Dependencies:** Managed via `requirements.txt`

## Installation Guide

### Create a Virtual Environment (Optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Install Dependencies

First, ensure that your virtual environment is activated. Then, run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```
### Configuration Setup

The application requires the following environment variables:

1. **GROQ_API_KEY**: Your API key for the Groq LLM model.
2. **DEEPGRAM_API_KEY**: Your API key for Deepgram's speech synthesis service.

#### Setting Up Environment Variables

1. Create a `.env` file in the root directory of the project.

2. Add your API keys to the `.env` file in the following format:

    ```plaintext
    GROQ_API_KEY=your_groq_api_key
    DEEPGRAM_API_KEY=your_deepgram_api_key
    ```

   Replace `your_groq_api_key` and `your_deepgram_api_key` with your actual API keys.

The `.env` file will be used to securely manage your API keys and other sensitive configurations.

### Usage

#### Run the Application

```bash
streamlit run app.py
```
### Choose an Option

- **Have a Conversation**: Practice English through formal or casual conversation.
  - **Formal**: Engage in a professional and academic manner.
  - **Casual**: Engage in a friendly and informal manner.

- **Improve Your Vocabulary**: Get assistance with vocabulary, including explanations, synonyms, and examples.

- **Test Your Grammar**: Complete grammar exercises tailored to your proficiency level.
  - **Expert**: Advanced level exercises.
  - **Intermediate**: Intermediate level exercises.
  - **Beginner**: Basic level exercises.

  ### Interact with the App

- **Enter your input** in the text area provided.
- **Click the "Submit" button** to receive responses and feedback based on your selected option.



