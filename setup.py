# It used to install a local package in my virtual envirnonment 
from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Abdoulfatah Abdillahi',
    author_email='aabdillahid@gmail.com',
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages()
)