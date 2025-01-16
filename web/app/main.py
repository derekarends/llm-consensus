import asyncio
import logging
import sys
import streamlit as st

from uuid import uuid4
from agent import invoke_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
     handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def generate_new_id():
    st.session_state.id = str(uuid4())


async def handle_submit(session_id, text_input):
    response = await invoke_agent(session_id, text_input)
    return response


st.title("Consensus")

if "id" not in st.session_state:
    st.session_state.id = str(uuid4())

st.button("New Id", on_click=generate_new_id)
st.write(st.session_state.id)

with st.form("my_form"):
    text_input = st.text_input("Question")
    submitted = st.form_submit_button("Submit")
    if submitted:
        # st.write("text_input", settings.azure_openai_api_version)
        if not text_input:
            st.write("Please enter a question or command")
            st.stop()

        response = asyncio.run(handle_submit(st.session_state.id, text_input))
        st.write(response)
