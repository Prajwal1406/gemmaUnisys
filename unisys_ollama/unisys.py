from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="ls__a6ef969716ef4689a2bdd5ec8c635a8d"
LANGCHAIN_PROJECT="Unisys Query Assistant"


prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful unisys query assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)


st.title('Unisys Query Assistant')
input_text=st.text_input("Ask About unisys")


llm=Ollama(model="prajwal3009/gemmauni")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))
