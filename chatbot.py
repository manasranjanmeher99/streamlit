import streamlit as st
from ollama import Client

# Initialize Ollama client
client = Client(host="http://localhost:11434")

# Page configuration
st.set_page_config(
    page_title="Ollama ChatBot",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💬 Ollama ChatBot")
st.markdown("_Powered by Ollama and Streamlit_")

# Initialize chat history and sessions in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# Sidebar configuration
with st.sidebar:
    st.sidebar.title("💬 Chat")
    
    # New chat button
    if st.sidebar.button("➕ New Chat", use_container_width=True, key="new_chat"):
        # Save current chat to sessions if it has messages
        if st.session_state.messages:
            chat_title = st.session_state.messages[0]["content"][:30] + "..." if st.session_state.messages else "Untitled"
            st.session_state.chat_sessions.insert(0, {
                "id": len(st.session_state.chat_sessions),
                "title": chat_title,
                "messages": st.session_state.messages.copy()
            })
        st.session_state.messages = []
        st.session_state.current_session_id = None
        st.rerun()
    
    st.sidebar.divider()
    
    # Display previous chat sessions
    if st.session_state.chat_sessions:
        st.sidebar.markdown("**Previous Chats:**")
        for session in st.session_state.chat_sessions:
            if st.sidebar.button(
                f"📝 {session['title']}", 
                use_container_width=True, 
                key=f"session_{session['id']}"
            ):
                st.session_state.messages = session["messages"].copy()
                st.session_state.current_session_id = session["id"]
                st.rerun()
        st.sidebar.divider()
    
    st.header("⚙️ Configuration")
    
    # Model selection
    selected_model = "kimi-k2.5:cloud"
    st.markdown("**Model:** kimi-k2.5:cloud")
    
    st.sidebar.divider()
    
    # Clear chat history button at the bottom
    if st.sidebar.button("🗑️ Clear All Chats", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_sessions = []
        st.session_state.current_session_id = None
        st.rerun()

# Display chat history
st.subheader("Chat 💬")
chat_container = st.empty()

if st.session_state.messages:
    with chat_container.container():
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
else:
    chat_container.markdown("<div style='min-height:200px;'></div>", unsafe_allow_html=True)

# User input
st.subheader("Your Message")
user_input = st.chat_input(
    "Type your message here...",
    key="user_input"
)

# Process user input
if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Generate response from Ollama
    try:
        with st.spinner("🤖 Thinking..."):
            # Prepare messages for Ollama
            messages_for_ollama = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages
            ]
            
            # Call Ollama API
            response = client.chat(
                model=selected_model,
                messages=messages_for_ollama
            )
            
            assistant_message = response["message"]["content"]
            
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure Ollama is running on http://localhost:11434")
        # Remove the failed user message
        st.session_state.messages.pop()

# Footer
st.divider()
st.caption("� Select a model from the sidebar to get started!")
