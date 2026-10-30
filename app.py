
import streamlit as st
import os
import time
from google import genai

# Page configuration
st.set_page_config(
    page_title="AI Question Paper Generator",
    page_icon="📝",
    layout="centered"
)

# Application heading
st.title("📝 AI Question Paper Generator")
st.write("Generate customized college question papers using Gemini AI.")

# Get API key securely
api_key = None

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is missing. Configure GEMINI_API_KEY in Streamlit secrets.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# User inputs
st.subheader("Enter Examination Details")

subject = st.text_input("Subject Name")

topics = st.text_area(
    "Enter Topics (separate topics with commas)"
)

difficulty = st.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

number_of_questions = st.number_input(
    "Number of Questions",
    min_value=1,
    max_value=50,
    value=5
)

question_type = st.selectbox(
    "Select Question Type",
    ["MCQ", "Short Answer", "Long Answer", "Mixed Questions"]
)

# Generate button
if st.button("Generate Question Paper"):

    if not subject.strip() or not topics.strip():
        st.warning("Please enter both subject and topics.")

    else:

        if question_type == "MCQ":
            type_instruction = """
            Generate only MCQs.
            Give exactly four options (A, B, C, D).
            Include one correct answer per question.
            """

        elif question_type == "Short Answer":
            type_instruction = """
            Generate only short-answer questions
            with brief answers in the answer key.
            """

        elif question_type == "Long Answer":
            type_instruction = """
            Generate only long-answer questions
            with detailed answers in the answer key.
            """

        else:
            type_instruction = """
            Generate a mixture of MCQs, short-answer
            and long-answer questions.
            """

        prompt = f"""
        You are an experienced college examination paper setter.

        Generate a professional question paper.

        Subject: {subject}
        Topics: {topics}
        Difficulty: {difficulty}
        Number of Questions: {number_of_questions}
        Question Type: {question_type}

        Instructions:
        1. Generate exactly {number_of_questions} questions.
        2. Cover the provided topics.
        3. Use clear academic language.
        4. Assign marks to each question.
        5. Display the total marks.
        6. Avoid repeated questions.
        7. Provide a separate answer key.
        8. Ensure answers match the questions.

        Question type instructions:
        {type_instruction}

        Format the paper with an examination heading,
        instructions, numbered questions, marks,
        total marks and a separate answer key.
        """

        with st.spinner("Gemini is generating your question paper..."):

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                    if response.text:
                        st.session_state["paper"] = response.text
                        break

                    st.warning("Gemini returned an empty response.")

                except Exception as e:
                    if attempt < 2:
                        time.sleep(10)
                    else:
                        st.error("Unable to generate the paper. Please try again.")
                        st.caption(str(e))

        # Display generated paper
        if st.session_state.get("paper"):
            st.success("Question paper generated successfully!")

            st.markdown(st.session_state["paper"])

            # Download question paper
            st.download_button(
                label="Download Question Paper",
                data=st.session_state["paper"],
                file_name="question_paper.txt",
                mime="text/plain"
            )

st.divider()
st.caption("AI Question Paper Generator | Powered by Gemini API")
