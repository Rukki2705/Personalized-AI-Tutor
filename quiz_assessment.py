import json
import random
from ollama import chat

# Dependencies required:
# pip install ollama

# Load the stored metadata containing course material references
DATA_DIR = "scraped_data"
METADATA_FILE = f"{DATA_DIR}/metadata.json"

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Function to generate quiz questions with explanations using Ollama
def generate_quiz(topic, num_questions=3):
    prompt = f"""
    Generate {num_questions * 2} multiple-choice quiz questions on {topic}.
    Ensure that:
    - Each question has exactly 4 options labeled A, B, C, and D.
    - The correct answer is a **single letter** (A, B, C, or D).
    - Options are returned as a **list of strings**, not a single string.
    - The explanation is **concise and clearly justifies the correct answer**.
    - Return the result **strictly in valid JSON format**, following this structure:
    
    {{
      "questions": ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5", "Question 6"],
      "options": [
         ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
         ["A) Option A", "B) Option B", "C) Option C", "D) Option D"],
         ["A) Answer A", "B) Answer B", "C) Answer C", "D) Answer D"]
      ],
      "correct_answers": ["A", "B", "C", "D", "A", "C"],
      "explanations": ["Explanation for Q1", "Explanation for Q2", "Explanation for Q3", "Explanation for Q4", "Explanation for Q5", "Explanation for Q6"]
    }}
    """
    response = chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    try:
        quiz_data = json.loads(response.message.content)
        # Randomly select the required number of questions
        selected_indices = random.sample(range(len(quiz_data['questions'])), num_questions)
        randomized_quiz = {
            "questions": [quiz_data['questions'][i] for i in selected_indices],
            "options": [quiz_data['options'][i] for i in selected_indices],
            "correct_answers": [quiz_data['correct_answers'][i] for i in selected_indices],
            "explanations": [quiz_data['explanations'][i] for i in selected_indices],
        }
        return randomized_quiz
    except (json.JSONDecodeError, AttributeError):
        print("Error: Unable to parse AI response into JSON. Please retry.")
        return None

# Function to conduct the quiz
def conduct_quiz(quiz_data):
    if not quiz_data or not all(k in quiz_data for k in ["questions", "options", "correct_answers", "explanations"]):
        print("Error: Invalid quiz data received. Please try again.")
        return
    
    score = 0
    
    for i, question in enumerate(quiz_data['questions']):
        print(f"\nQuestion {i+1}: {question}")
        for j, option in enumerate(quiz_data['options'][i]):
            print(f"{chr(65+j)}. {option}")
        
        user_answer = input("Your answer: ").strip().upper()
        correct_answer = quiz_data['correct_answers'][i].strip().upper()
        explanation = quiz_data['explanations'][i]
        
        if user_answer == correct_answer:
            print(f"Correct! {explanation}\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer was {correct_answer}. {explanation}\n")
    
    print(f"\nYour Final Score: {score}/{len(quiz_data['questions'])}")

if __name__ == "__main__":
    topic = input("Enter a topic for the quiz: ")
    quiz_data = generate_quiz(topic)
    conduct_quiz(quiz_data)
