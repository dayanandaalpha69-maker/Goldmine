import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app import (
    SUMMARY_MESSAGE_INTERVAL,
    SYSTEM_PROMPT,
    ask,
    create_model,
    prepare_messages,
    provider,
    summarize_messages,
)

st.set_page_config(
    page_title="Goldmine Chat",
    page_icon="G",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #f4f0e8;
    }
    [data-testid="stHeader"] {
        background: rgba(244, 240, 232, 0.85);
    }
    .hero {
        padding: 2.5rem 0 1.25rem;
        border-bottom: 1px solid #d8d0c4;
        margin-bottom: 1.5rem;
    }
    .eyebrow {
        color: #bd5b35;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .hero h1 {
        color: #17231f;
        font-family: Georgia, serif;
        font-size: 3rem;
        line-height: 1;
        margin: 0.35rem 0 0.6rem;
    }
    .hero p {
        color: #5b625e;
        font-size: 1rem;
        margin: 0;
    }
    [data-testid="stChatMessage"] {
        border: 1px solid #ded6ca;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        background: rgba(255, 253, 249, 0.72);
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #17231f;
        color: #fffdf9;
        border-color: #17231f;
    }
    [data-testid="stChatInput"] {
        padding-bottom: 1rem;
    }
    </style>
    <div class="hero">
        <div class="eyebrow">Goldmine / conversational AI</div>
        <h1>Ask better questions.</h1>
        <p>A focused chat workspace with compact memory and automatic summaries.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]
        st.session_state.pop("model_client", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]

if "model_client" not in st.session_state:
    try:
        st.session_state.model_client, st.session_state.model_name = create_model()
    except Exception as error:
        st.error(str(error))
        st.stop()

for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        continue
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(str(message.content))

question = st.chat_input("Send a message")
if question:
    st.session_state.messages.append(HumanMessage(content=question))
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ask(
                    st.session_state.model_client,
                    st.session_state.model_name,
                    prepare_messages(st.session_state.messages),
                )
                st.markdown(response)
                st.session_state.messages.append(AIMessage(content=response))

                conversation_message_count = sum(
                    not isinstance(message, SystemMessage)
                    for message in st.session_state.messages
                )
                if conversation_message_count % SUMMARY_MESSAGE_INTERVAL == 0:
                    st.session_state.messages = summarize_messages(
                        st.session_state.model_client,
                        st.session_state.model_name,
                        st.session_state.messages,
                    )
            except Exception as error:
                st.error(str(error))
                st.session_state.messages.pop()
