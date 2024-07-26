import streamlit as st
from llm_chains import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory

def load_chain(chat_history):
    return load_normal_chain(chat_history)

def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""
def set_send_input():
    st.session_state.send_input = True
    clear_input_field()

def main():
    st.title("Multimodal Chat Local App")
    chat_container= st.container()

    if "send_input" not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ""

    chat_history = StreamlitChatMessageHistory(key="history")
    llm_chain = load_chain(chat_history)

    user_input = st.text_input("Escribe tu mensaje aqui", key="user_input", on_change=set_send_input)
    send_button= st.button("Enviar", key="send_button")

    if send_button or st.session_state.send_input:
        if st.session_state.user_question != "":
            #llm_response = "Esta es una respuesta del modelo LLM"

            with chat_container:
                st.chat_message("user").write(st.session_state.user_question)
                llm_response = llm_chain.run(st.session_state.user_question)
                #st.chat_message("ai").write(llm_response)
                st.session_state.user_question=""
                #st.chat_message("ai").write("dame respuesta")

    if chat_history.messages != []:
        st.write("Chat history")
        for message in chat_history.messages:
            st.chat_message(message.type).write(message.content)

if __name__ == "__main__":
    main()



