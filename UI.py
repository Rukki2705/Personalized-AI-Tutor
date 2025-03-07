import streamlit as st
import json
from rag_pipeline import generate_response
from quiz_assessment import generate_quiz

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
            query_with_subject = f"{selected_subject}: {user_query}"
            answer = generate_response(query_with_subject)
            st.write("\n**AI Response:**\n", answer)
    
    if page == "Quiz":
        st.header(f"Generate a Quiz on {subject}")
        topic = st.text_input("Enter a topic for the quiz:")
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=10, value=3, step=1)
    
        if st.button("Generate Quiz"):
            quiz_data = generate_quiz(f"{selected_subject}: {topic}", num_questions)
        
            if quiz_data:
                st.session_state.quiz_data = quiz_data
                st.session_state.current_question = 0
                st.session_state.score = 0  # ✅ Reset score when a new quiz starts
                st.session_state.show_explanation = False
                st.session_state.show_quiz = True  

        if "show_quiz" in st.session_state and st.session_state.show_quiz:
            quiz_data = st.session_state.quiz_data
            q_idx = st.session_state.current_question
        
            if q_idx < len(quiz_data['questions']):
                st.subheader(f"Question {q_idx + 1}: {quiz_data['questions'][q_idx]}")
                user_choice = st.radio("Choose an option:", quiz_data['options'][q_idx], index=None)

                if st.button("Submit Answer"):
                    correct_answer = quiz_data['correct_answers'][q_idx]
                    explanation = quiz_data['explanations'][q_idx]

                    if "submitted_answers" not in st.session_state:
                        st.session_state.submitted_answers = set()  # ✅ Track answered questions

                    if q_idx not in st.session_state.submitted_answers:
                        st.session_state.submitted_answers.add(q_idx)  # ✅ Prevent double scoring
                        if user_choice and user_choice.startswith(correct_answer):
                            st.success(f"✅ Correct! {explanation}")
                            st.session_state.score += 1
                        else:
                            st.error(f"❌ Incorrect. The correct answer was {correct_answer}. {explanation}")

                if st.button("Next Question"):
                    st.session_state.current_question += 1
                    st.session_state.show_explanation = False  # ✅ Reset explanation
                    st.session_state.submitted_answers.discard(q_idx)  # ✅ Remove answered flag

            else:
                st.write(f"🎉 **Quiz Completed! Your Score: {st.session_state.score}/{num_questions}**")
                st.session_state.show_quiz = False
                st.session_state.submitted_answers.clear()  # ✅ Clear tracking after quiz com

if __name__ == "__main__":
    main()
