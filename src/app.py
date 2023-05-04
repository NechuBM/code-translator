import streamlit as st
from streamlit_ace import st_ace
import openai
from utils import programming_languages, output_results, define_prompt, request

st.write(' ## Translate, explain and fix code with GPT')

_, psw_col2, _ = st.columns([1,2,1])
OPENAI_API_KEY = psw_col2.text_input('OpenAI API Key', type='password')

_, col2, col3, _ = st.columns(4)
model = col2.selectbox(
    'Model',
    ('gpt-3.5-turbo', 'gpt-4'))

action = col3.selectbox(
    'Action',
    ('translate', 'code_explanation', 'bug_fix'))

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
    r = request(model, prompt)

    if action == 'code_explanation':
        st.text_area(r)
    else:
        output_content = st_ace(
            value = r,
            language=output_langague,
            theme='dracula',
            readonly=True
        )