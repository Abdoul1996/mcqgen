import os 
import json
import pandas as pd 
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st 
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


# loading json file 
file_path = os.path.join(os.path.dirname(__file__), 'Response.json')
with open(file_path, 'r') as file:
    RESPONSE_JSON = json.load(file)


# creating a title for the app 
st.title("MCQs Creator Application with LangChain 🦜️🔗 ")

# create form using st.form 
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert subject", max_chars=20)
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="simple")
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                # Count tokens and the cost of API call 
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error occurred during MCQ generation.")
            else:
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total cost: {cb.total_cost}")
                
                if isinstance(response, dict):
                    quiz = response.get("quiz")
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index += 1
                            st.table(df)
                            # Display the review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)