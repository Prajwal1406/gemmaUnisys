import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig, GemmaTokenizer
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

model_id = "Prajwal3009/gemma2bunisys"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_id,
                                             quantization_config=bnb_config,
                                             device_map={"":0},
                                             token=HF_TOKEN)


@st.cache(allow_output_mutation=True)
def generate_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=1000)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


st.title("Gemma Chatbot")
st.write("Welcome to Gemma Chatbot! Ask me anything about Unisys.")

user_input = st.text_input("You:", "")
if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        response = generate_response(user_input)
        st.text_area("Gemma:", value=response, height=200, max_chars=None, key=None)

