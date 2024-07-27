import streamlit as st
import io
import os
from deepgram import DeepgramClient, SpeakOptions
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']
deepgram_api_key = os.environ['DEEPGRAM_API_KEY']
llm = ChatGroq(temperature=0, model_name="llama-3.1-70b-Versatile")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: var(--background-color);
        padding: 20px;
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 30px;
    }
    .sidebar .sidebar-content {
        background-color: var(--sidebar-background-color);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .textarea {
        height: 150px;
        border: 1px solid #cccccc;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        background-color: var(--input-background-color);
        color: var(--text-color);
    }
    .label, .label-bold {
        font-size: 18px;
        font-weight: bold;
        color: var(--label-color);
    }
    .success, .info, .error {
        margin: 20px 0;
        padding: 10px;
        border-radius: 5px;
    }
    .success {
        background-color: #e6ffed;
        color: #155724;
    }
    .info {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .error {
        background-color: #f8d7da;
        color: #721c24;
    }
    .footer {
        text-align: center;
        padding: 10px;
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333333;
        color: white;
        font-size: 14px;
    }
    </style>
    <style id="theme-styles">
    </style>
""", unsafe_allow_html=True)

def text_to_speech(transcript):
    try:
        deepgram = DeepgramClient()
        speak_options = {"text": transcript}
        options = SpeakOptions(
            model="aura-stella-en",
            encoding="linear16",
            container="wav"
        )
        response = deepgram.speak.v("1").stream(speak_options, options)
        return response.stream.getvalue()
    except Exception as e:
        st.error(f"Exception: {e}")
        return None

def get_response(question, prompt):
    prompt_template = PromptTemplate(
        input_variables=["question", "history"],
        template=prompt + "{history}\nHuman: {question}",
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.invoke({"question": question, "history": "\n".join(st.session_state.conversation_history)})
    response = result["text"]
    st.session_state.conversation_history.append(f"Human: {question}")
    st.session_state.conversation_history.append(f"Assistant: {response}")
    return response

def get_conversation_response(question, prompt):
    prompt_template = PromptTemplate(
        input_variables=["question", "history"],
        template=prompt + "{history}\nHuman: {question}",
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.invoke({"question": question, "history": "\n".join(st.session_state.conversation_history)})
    response_content = result["text"]

    if "Review:" in response_content:
        response_parts = response_content.split('Review:')
        conversation_response = response_parts[0].strip()
        review = 'Review:'.join(response_parts[1:]).strip()
    else:
        conversation_response = response_content.strip()
        review = None

    st.session_state.conversation_history.append(f"Human: {question}")
    st.session_state.conversation_history.append(f"Assistant: {response_content}")

    return conversation_response, review

def main():
    st.markdown('<div class="title">English Tutor</div>', unsafe_allow_html=True)

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""

    option = st.sidebar.selectbox("Select an option:", ["Have a Conversation", "Improve Your Vocabulary", "Test Your Grammar"])

    if "prev_option" not in st.session_state:
        st.session_state.prev_option = option
    elif st.session_state.prev_option != option:
        st.session_state.conversation_history = []
        st.session_state.prev_option = option

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Additional Options")
    theme = st.sidebar.radio("Choose a theme:", ["Light", "Dark"])
    st.sidebar.markdown("### Progress")
    progress = st.sidebar.progress(0)
    if theme == "Dark":
        st.markdown("""
            <style>
            .main { color: white; background-color: #333; }
            .label-bold { color: #ffffff; }
            .textarea { color: #ffffff; background-color: #444; }
            .wide-textarea { color: #ffffff; background-color: #444; }
            .success { background-color: #2e2e2e; color: #d4edda; }
            .info { background-color: #2e2e2e; color: #d1ecf1; }
            .error { background-color: #2e2e2e; color: #f8d7da; }
            .footer { background-color: #111; color: #ffffff; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .main { color: black; background-color: #f9f9f9; }
            .label-bold { color: #333333; }
            .textarea { color: black; background-color: #ffffff; }
            .wide-textarea { color: black; background-color: #ffffff; }
            .success { background-color: #e6ffed; color: #155724; }
            .info { background-color: #d1ecf1; color: #0c5460; }
            .error { background-color: #f8d7da; color: #721c24; }
            .footer { background-color: #e0e0e0; color: #333; }
            </style>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if option == "Have a Conversation":
            st.markdown('<p class="label-bold">Conversation Style:</p>', unsafe_allow_html=True)
            conversation_style = st.selectbox("", ["Formal", "Casual"], key="conversation_style")
        if option == "Test Your Grammar":
            st.markdown('<p class="label-bold">What is your level in English:</p>', unsafe_allow_html=True)
            user_level = st.selectbox("", ["Expert", "Intermediate", "Beginner"], key="user_level")

    with col2:
        st.markdown('<p class="label-bold">Start the chat:</p>', unsafe_allow_html=True)
        st.session_state.chat_input = st.text_area("", st.session_state.chat_input, height=150)

    if st.button("Submit"):
        question = st.session_state.chat_input

        progress.progress(50)

        if len(st.session_state.conversation_history) > 10:
            st.session_state.conversation_history = st.session_state.conversation_history[-10:]

        if option == "Have a Conversation":
            if conversation_style == "Formal":
                prompt = "You are an English tutor in disguise having a formal conversation with an Indian student who is around the age of 50. Respond to their questions or statements in a professional and academic manner. Always keep the conversation going. Instead of asking them what they want to talk about, suggest topics (make sure these topics are friendly to Indians and also someone who is around 50 years old) and start talking about them to motivate the user to get into a conversation and try to get them to talk to you by initiating the conversation, but below your response to the conversation put a review of what the user said and if they used good English or what could have been a better way to say it."
            else:
                prompt = "You are an English tutor in disguise having a casual conversation with an Indian student who is around the age of 50. Respond to their questions or statements in a friendly and casual manner. Always keep the conversation going. Instead of asking them what they want to talk about, suggest topics (make sure these topics are friendly to Indians and also someone who is around 50 years old) and start talking about them to motivate the user to get into a conversation and try to get them to talk to you by initiating the conversation, but below your response to the conversation put a review of what the user said and if they used good English or what could have been a better way to say it."

            response, review = get_conversation_response(question, prompt)
            progress.progress(75)

            audio_bytes = text_to_speech(response)
            if audio_bytes:
                audio_file = io.BytesIO(audio_bytes)
                st.audio(audio_file, format='audio/wav')

            st.success(f"Tutor's response: {response}")
            if review:
                st.info(review)

        elif option == "Improve Your Vocabulary":
            prompt = "You are an English tutor in disguise helping an Indian student who is around the age of 50 improve their vocabulary. Provide detailed explanations and examples like synonyms and similar words to what the student asks."
            response = get_response(question, prompt)
            progress.progress(75)
            st.success(f"Tutor's response: {response}")

        else:
            prompt = f"You are an English tutor in disguise helping an Indian student who is around the age of 50 by testing their grammar. Give them exercises according to their level which is {user_level}, like fill in the blanks to complete these sentences, or change the tense of this sentence and then provide them with a review and help them get better."
            response = get_response(question, prompt)
            progress.progress(75)
            st.success(f"Tutor's response: {response}")

        progress.progress(100)

    st.markdown('<div class="footer">© 2024 English Tutor. All rights reserved.</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
