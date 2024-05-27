# All the code will be here 
import os 
import json
import pandas as pd 
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# importing necessary packages packages from Langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain 
from langchain.chains import SequentialChain


# load environment variable from the .env file 
load_dotenv()

# Access the environment variables
KEY=os.getenv("OPENAI_API_KEY")

#OpenAI API 
llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-4-turbo", temperature=0.3)

# Input prompt Template 
template=""""
Text:{text}
You are expert MCQ maker. Given the above text, it is your job to \ create a quiz of 
{number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be confirming the text as well. 
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \ 
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

#Input prompt 
quiz_generation_prompt = PromptTemplate(
    input_variables=["text","number", "subject","tone","response_json"],
    template=template
)

quiz_chain =LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

# Evaluate the quiz
template2="""
You are an expert english grammarian and writer. Given a multiple choice quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity 
if the quiz is not at per with the cognitive and analytics abilities of the students,\
update the quiz questions which needs to be changed the tone such that it perfectly fits the students
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
# Second prompt 
quiz_evaluate_prompt = PromptTemplate(input_variables=["subject", " quiz"], template=template2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluate_prompt, output_key="review", verbose=True)

# Object sequential chain 
generate_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text","number", "subject","tone","response_json", ],
                                          output_variables=["quiz", "review"], verbose=True)

