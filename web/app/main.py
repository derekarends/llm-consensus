from uuid import uuid4
import streamlit as st
import requests
from __init__ import settings
from  route_picker import execute 

st.title("Consensus")

if 'id' not in st.session_state:
    st.session_state.id = str(uuid4())

def generate_new_id():
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

        response = execute(st.session_state.id, text_input)
        st.write(response)


# uploaded_files = st.file_uploader(
#     "Choose a CSV file", accept_multiple_files=True
# )
# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)

# data = requests.get("'https://jsonplaceholder.typicode.com/todos/1'").json()

# st.write(data)

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache_data
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# # Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# # Notify the reader that the data was successfully loaded.
# data_load_state.text("Done! (using st.cache_data)")
