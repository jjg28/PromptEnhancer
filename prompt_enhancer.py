import streamlit as st
from langchain.llms import OpenAIChat
from langchain import PromptTemplate, OpenAI, LLMChain
import openai
import os


# Set Streamlit page configuration
st.set_page_config(page_title="💬 Prompt Enhancer", layout="wide")


# Formatting for empty space above main area and sidebar
st.markdown(
    '''
    <style>
        .css-1544g2n {
            padding: 1rem 1rem 1.5rem;
        }

        .css-z5fcl4 {
            width: 100%;
            padding: 1rem 1rem 10rem;
            min-width: auto;
            max-width: initial;
        }
    </style>
    ''', unsafe_allow_html=True
)

# Titles and description
st.title("💬 Prompt Enhancer")
st.subheader("A tool for coming up with better prompts to input into GPT or other large language models")


# Creating sidebar
with st.sidebar:
    st.title("💡 How to use")

    # OpenAI API key input form
    with st.form("OpenAI API Key Input"):
        openai_api_key = st.text_input(label="🔑 OpenAI API Key", placeholder="Input your API key here")

        submitted = st.form_submit_button("Submit")
        if submitted:
            os.environ["OPENAI_API_KEY"] = openai_api_key
    
    # Instructions for using the tool
    st.write("""
    1. Input your OpenAI API key in the box above
    2. Input a prompt that you intend to input to GPT or any other LLM
    3. Receive 3 outputs with a description detailing reasoning for each output
    4. Select a prompt and input it into your choice of LLM
    """)
    
    st.write("---")
    st.title("ℹ️ About")
    st.write("""
    - This is a simple project I made in a couple of hours to familiarize myself with creating apps using the [OpenAI API](https://platform.openai.com/), [LangChain](https://python.langchain.com/en/latest/), and [Streamlit](https://streamlit.io/).
    - Here's a link to the [GitHub repository](https://github.com/MichaelElHage/PromptEnhancer).
    - If you're interested in my thoughts as I progressed with making this, as well as the problems I encountered, please check out my post on [Medium](medium).
    """)



# Template for prompt generation
template = """Prompt: {prompt}
Answer: Provide 3 differently worded prompts than the one above. The prompts that you provide are intended to be re-inputted into a large language model. Try to adhere to the integrity of the prompt inputted by the user as much as possible.

- Additionally, explain how each prompt relates to the original and quote the original.
- IMPORTANT >>>> Do not reword or change any text in quotations.
- Do not do any actions other than rewording or improving the language of the prompt.
- Do not create original prompts. All outputs should be inspired by the user's original prompt.
- Do not answer the prompts.
"""

prompt = PromptTemplate(template=template, input_variables=["prompt"])

# Prompt input form
with st.form("Prompt Input"):
    st.write("Input your prompt below")
    prompt_input = st.text_area(label="Prompt Input", placeholder="Input your prompt here", label_visibility="hidden")


    submitted = st.form_submit_button("Submit")
        # Check if the form has been submitted
    if submitted:
        # Create an instance of the OpenAIChat language model
        llm = OpenAIChat(model_name="gpt-3.5-turbo", temperature=0.6)
        
        # Create an instance of LLMChain with the OpenAIChat model and the prompt template
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        
        # Generate enhanced prompts using the inputted prompt
        result = llm_chain.run(prompt_input)
        
        # Display the result in the Streamlit app
        st.write(result)

