import streamlit as st
from langchain.llms import OpenAIChat
from langchain import PromptTemplate, OpenAI, LLMChain
import openai
import os


st.set_page_config(page_title="💬 Prompt Enhancer", layout="wide")


# formatting for Empty space above main area and side bar

st.markdown(
    f'''
            <style>
                .css-1544g2n {{
                    padding: 1rem 1rem 1.5rem;
            }}

                .css-z5fcl4 {{
                    width: 100%;
                    padding: 1rem 1rem 10rem;
                    min-width: auto;
                    max-width: initial;
            }}
            </style>
    ''', unsafe_allow_html=True)

# titles and description
st.title("💬 Prompt Enhancer")
st.subheader(
    "A tool for coming up with better prompts to input into GPT or other Large Language Models")


# creating side bar
with st.sidebar:
    st.title("💡 How to use")

    with st.form("OpenAI API Key Input"):
        openai_api_key = st.text_input(label="🔑 OpenAI API Key",
                                       placeholder="Input your API key here")

        submitted = st.form_submit_button("Submit")
        if submitted:
            os.environ["OPENAI_API_KEY"] = openai_api_key
    st.write("""
    1. Input a prompt that you would intend to input to GPT or any other LLM
    2. Receive 3 outputs with a description detailing reasoning for output
    3. Select a prompt and input it into your choice of LLM
    """)
    st.write("---")
    st.title("ℹ️   About")
    st.write("""
    - This is just simple project I made in a couple hours to familiarize myself with creating apps with [OpenAI API](https://platform.openai.com/), [LangChain](https://python.langchain.com/en/latest/), and [Streamlit](https://streamlit.io/)

    - Here's a link to the [GitHub repository](https://github.com/MichaelElHage/PromptEnhancer)
    - If you're intersted in my thoughts as I progressed with making this as well as problems I encountered, please check out my post on [Medium](medium)!
    """)


template = """Prompt: {prompt}
Answer: Provide 3 differently worded prompts than the one inputted. the prompts that you provide is intended to be re-inputted into a large language model. Try to adhere to the integrity of the prompt inputted by the user as much as possible.

- Additionally explain how each prompt relates to the original and quote the original.
- IMPORTANT >>>> Do not reword or change any text in quotations.
- Do not do any actions other than rewording or improving the language of the prompt.
- Do not create original prompts. All outputs should be inspired by the user's original prompt.
- Do not answer the prompts.
    """

prompt = PromptTemplate(template=template, input_variables=["prompt"])

with st.form("Prompt Input"):
    st.write("Input your prompt below")
    prompt_input = st.text_area("", placeholder="Input your prompt here")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        llm = OpenAIChat(model_name="gpt-3.5-turbo", temperature=0.6)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        st.write(llm_chain.run(prompt_input))
