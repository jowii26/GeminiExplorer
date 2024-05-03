import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "my-project-421302"
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

#load model with config
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat()

#helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].contents.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
        "role": "user",
        "content": query
        }
    )

    st.session_state.messages.append(
        {
        "role": "model",
        "content": output
        }
    )

    st.title("Gemini Explorer")

    #initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #display and load to chat history
    for index, message in enumerate(st.session_state.messages):
        content = Content(
            role = message["role"],
            parts = [ Part.from_text(message["content"])]
        )

        if index != 0:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        chat.history.append(content)

        #for initial message start up
        if len(st.session_state.messages) == 0:
            initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive"
        llm_function(chat, initial_prompt)

        # for capture user input
        query = st.chat_input("Gemini Explorer")
        if query:
            with st.chat_message("user"):
                st.markdown(query)
            llm_function(chat, query)
