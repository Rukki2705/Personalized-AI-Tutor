import streamlit as st
import json
import time
from rag_pipeline import generate_response
from quiz_assessment import generate_quiz

# Files to store performance metrics
METRICS_FILE = "scraped_data/performance_metrics.txt"
QUIZ_METRICS_FILE = "scraped_data/quiz_performance.txt"

# Function to log response time and accuracy for Q&A
def log_performance(query, response_time, accuracy_check):
    with open(METRICS_FILE, "a") as f:
        f.write(f"Query: {query}\n")
        f.write(f"Response Time: {response_time:.3f} seconds\n")
        f.write(f"Accuracy Check: {accuracy_check}\n")
        f.write("------------------------------------\n")

# Function to log quiz performance
def log_quiz_performance(subject, topic, score, total_questions, time_taken):
    with open(QUIZ_METRICS_FILE, "a") as f:
        f.write(f"Subject: {subject}\n")
        f.write(f"Topic: {topic}\n")
        f.write(f"Score: {score}/{total_questions}\n")
        f.write(f"Accuracy: {(score / total_questions) * 100:.2f}%\n")
        f.write(f"Time Taken: {time_taken:.2f} seconds\n")
        f.write(f"Quiz Completion: {'Completed' if score > 0 else 'Not Completed'}\n")
        f.write("------------------------------------\n")

# Available subjects
SUBJECTS = {
    "Mathematics": "math",
    "Physics": "physics",
    "Computer Science": "computer-science",
    "Biology": "biology",
    "Chemistry": "chemistry",
    "Electrical Engineering": "electrical-engineering",
    "Mechanical Engineering": "mechanical-engineering",
    "Economics": "economics",
    "Psychology": "psychology"
}

# Streamlit UI
def main():
    st.title("Personalized Learning Tutor")
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a feature", ["Question & Answer", "Quiz"])
    
    subject = st.sidebar.selectbox("Choose a subject", list(SUBJECTS.keys()))
    selected_subject = SUBJECTS[subject]

    if page == "Question & Answer":
        st.header(f"Ask a question about {subject}")
        user_query = st.text_input("Enter your question:")
        if st.button("Get Answer"):
            start_time = time.time()
            query_with_subject = f"{selected_subject}: {user_query}"
            answer = generate_response(query_with_subject)
            response_time = time.time() - start_time
            st.write("\n**AI Response:**\n", answer)
            
            # Log response time and accuracy
            accuracy_check = "Pending Manual Review"  # Placeholder for now
            log_performance(user_query, response_time, accuracy_check)
    
    elif page == "Quiz":
        st.header(f"Generate a Quiz on {subject}")
        topic = st.text_input("Enter a topic for the quiz:")
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=10, value=3, step=1)
        
        if st.button("Generate Quiz"):
            start_time = time.time()
            quiz_data = generate_quiz(f"{selected_subject}: {topic}", num_questions)
            quiz_generation_time = time.time() - start_time

            if quiz_data:
                st.session_state.quiz_data = quiz_data
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.quiz_start_time = time.time()
                st.session_state.show_quiz = True  

                # Log quiz generation time
                with open(QUIZ_METRICS_FILE, "a") as f:
                    f.write(f"Quiz Generated: {topic} ({subject})\n")
                    f.write(f"Generation Time: {quiz_generation_time:.3f} seconds\n")
                    f.write("------------------------------------\n")

        if "show_quiz" in st.session_state and st.session_state.show_quiz:
            quiz_data = st.session_state.quiz_data
            q_idx = st.session_state.current_question
            
            if q_idx < len(quiz_data['questions']):
                st.subheader(f"Question {q_idx + 1}: {quiz_data['questions'][q_idx]}")
                user_choice = st.radio("Choose an option:", quiz_data['options'][q_idx], index=None)

                if st.button("Submit Answer"):
                    correct_answer = quiz_data['correct_answers'][q_idx]
                    explanation = quiz_data['explanations'][q_idx]
                    if user_choice and user_choice.startswith(correct_answer):
                        st.success(f"✅ Correct! {explanation}")
                        st.session_state.score += 1
                    else:
                        st.error(f"❌ Incorrect. The correct answer was {correct_answer}. {explanation}")
                if st.button("Next Question"):
                    st.session_state.current_question += 1
            else:
                total_time = time.time() - st.session_state.quiz_start_time
                log_quiz_performance(subject, topic, st.session_state.score, num_questions, total_time)
                st.write(f"🎉 **Quiz Completed! Your Score: {st.session_state.score}/{num_questions}**")
                st.session_state.show_quiz = False  

if __name__ == "__main__":
    main()
