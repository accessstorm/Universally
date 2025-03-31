import google.generativeai as genai
from django.conf import settings
import json
import logging

# Configure the Gemini API client
try:
    genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
    # Initialize the model
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest') # Using model listed by list_models()
except AttributeError:
    logging.error("GOOGLE_AI_API_KEY not found in settings. Cannot configure Gemini.")
    model = None
except Exception as e:
    logging.error(f"Error configuring Gemini: {e}")
    model = None

def generate_quiz_questions(category, num_questions, question_type):
    """
    Generates quiz questions using the Gemini API based on the provided configuration.

    Args:
        category (str): The subject/category for the questions (e.g., 'python', 'django').
        num_questions (int): The number of questions to generate.
        question_type (str): The type of questions ('MCQ', 'MSQ', 'OPEN').

    Returns:
        list: A list of dictionaries, where each dictionary represents a question,
              or None if generation fails.
              Example for MCQ:
              [
                  {
                      "question": "What is the capital of France?",
                      "options": ["Berlin", "Madrid", "Paris", "Rome"],
                      "correct_answer": "Paris",
                      "type": "MCQ"
                  },
                  ...
              ]
              Example for OPEN:
               [
                  {
                      "question": "Explain the concept of closures in JavaScript.",
                      "type": "OPEN"
                  },
                  ...
              ]
    """
    if not model:
        logging.error("Gemini model not initialized. Cannot generate questions.")
        return None

    prompt = f"""
    Generate {num_questions} interview questions for the category '{category}'.
    The question type should be '{question_type}'.

    Format the output as a JSON list of objects.

    For '{question_type}' questions:
    - If MCQ (Multiple Choice Question): Each object must have keys "question" (string), "options" (list of 4 strings), and "correct_answer" (string - one of the options).
    - If MSQ (Multiple Select Question): Each object must have keys "question" (string), "options" (list of 4-6 strings), and "correct_answers" (list of strings - one or more of the options).
    - If OPEN (Open Ended): Each object must have a key "question" (string).

    Ensure the JSON is valid and contains exactly {num_questions} questions.
    Provide only the JSON list, no introductory text or explanations.

    Example for MCQ:
    [
      {{"question": "What keyword is used to define a function in Python?", "options": ["def", "fun", "define", "function"], "correct_answer": "def"}},
      ...
    ]

    Example for OPEN:
    [
      {{"question": "Describe the difference between a list and a tuple in Python."}},
      ...
    ]
    """

    try:
        response = model.generate_content(prompt)
        # Attempt to parse the response text as JSON
        # Clean potential markdown/formatting issues
        cleaned_response = response.text.strip().lstrip('```json').rstrip('```').strip()
        questions = json.loads(cleaned_response)

        # Basic validation
        if not isinstance(questions, list):
            raise ValueError("Generated content is not a JSON list.")
        if len(questions) != num_questions:
             logging.warning(f"Gemini generated {len(questions)} questions, expected {num_questions}. Using generated count.")
             # You might want to retry or handle this differently

        # Add the 'type' to each question dictionary for easier handling later
        for q in questions:
            q['type'] = question_type

        return questions

    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode Gemini response as JSON: {e}")
        logging.error(f"Raw response: {response.text}")
        return None
    except Exception as e:
        logging.error(f"Error generating questions with Gemini: {e}")
        # Log the prompt and response if possible and safe
        logging.debug(f"Prompt sent: {prompt}")
        if 'response' in locals():
             logging.debug(f"Response received: {response.text}")
        return None
