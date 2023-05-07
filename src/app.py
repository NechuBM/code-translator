import streamlit as st
from streamlit_ace import st_ace
import openai
from utils import programming_languages, output_results, define_prompt, request, action_details, model_details

st.write(' ## Translate, explain and fix code with GPT')

_, psw_col2, _ = st.columns([1,2,1])
OPENAI_API_KEY = psw_col2.text_input('OpenAI API Key', type='password')

_, col2, col3, _ = st.columns(4)
model = col2.selectbox(
    'Model',
    ('GPT-3.5', 'GPT-4'))

action = col3.selectbox(
    'Action',
    ('Explain', 'Translate', 'Fix'))

st.write('\n')
st.write('\n')

input_language = st.selectbox(
    'Input',
    programming_languages)

code_content = st_ace(
    placeholder="Input your code",
    language=input_language,
    theme='dracula',
    auto_update=True,
    value = "")

output_langague = st.selectbox(
    'Ouput',
    options=output_results[action])

if st.button('Run'):
    openai.api_key = OPENAI_API_KEY
    prompt = define_prompt(action, input_language, code_content, output_langague)
    try:
        r = request(model_details[model], prompt)

        if action == 'Explain':
            st.text_area(r)
        else:
            output_content = st_ace(
                value = r,
                language=output_langague,
                theme='dracula',
                readonly=True
            )
    except Exception as e:
        if e.error["code"] == 'invalid_api_key':
            st.warning('Invalid API key provided \
                       \nLearn how to get the API key at https://www.youtube.com/watch?v=F0nnsrcvrsc&t=1543s \
                       \nFind your API key at https://platform.openai.com/account/api-keys')

        elif e.error["type"] == "invalid_request_error":
            st.warning('No API Key provided \
                       \nLearn how to get the API key at https://www.youtube.com/watch?v=F0nnsrcvrsc&t=1543s \
                       \nFind your API key at https://platform.openai.com/account/api-keys')