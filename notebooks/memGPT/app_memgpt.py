from letta import create_client, LLMConfig, EmbeddingConfig
from letta import ChatMemory, EmbeddingConfig, LLMConfig, create_client
from letta.prompts import gpt_system

import streamlit as st
import pandas as pd
import os

# from running ollama serve
ollama_url = 'http://127.0.0.1:11434'
os.environ["OLLAMA_BASE_URL"] = ollama_url

llm_ollama = LLMConfig(
    # llama model versions: https://github.com/ollama/ollama
    model="llama3.2:1b", #"llama3.2", #ollama run llama3.2:1b
    model_endpoint_type="ollama",
    model_endpoint=ollama_url,
    context_window=16384
)
embedding_config = EmbeddingConfig.default_config(model_name="text-embedding-ada-002")

client = create_client()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]
if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = False  # Tracks if the conversation is active


def workflow_memory():
    with st.expander("**List Current Agents**"):
        if st.button("List Agents"):
            agent_states = []

            for agent_state in client.list_agents():
                agent_states.append({
                    "Agent Name": agent_state.name,
                    "Tools": agent_state.tools
                })
            st.table(pd.DataFrame(agent_states))

        if st.button("Delete Agents"):
            for agent_state in client.list_agents():
                client.delete_agent(agent_id=agent_state.id)

    with st.expander("**Create Agent**"):
        agent_name = st.text_input('Agent Name', value="Jarvis")
        agent_persona = st.text_input('Agent Persona', value="Helpful technical teacher")
        human_name = st.text_input('Human Name', value="Bobby")
        human_likes = st.text_input('Human Likes', value='Likes warm weather and pickleball')

        if st.button("Create Agent"):
            new_agent_state = client.create_agent(
                # agent's name (unique per-user, autogenerated if not provided)
                name=agent_name,
                # in-context memory representation with human/persona blocks
                memory= ChatMemory(
                    human=f"Name: {human_name}",
                    persona=agent_persona #"You are a helpful assistant that loves emojis"
                ),
                # LLM model & endpoint configuration
                llm_config=llm_ollama,
                # embedding model & endpoint configuration (cannot be changed)
                embedding_config=embedding_config,
                # system instructions for the agent (defaults to `memgpt_chat`)
                system=gpt_system.get_system_text("memgpt_chat"),
                # whether to include base letta tools (default: True)
                include_base_tools=True,
                # list of additional tools (by name) to add to the agent
                tools=[],
            )
            client.send_message(
                agent_id=new_agent_state.id,
                message = f"Save the information that '{human_name} likes {human_likes}' to archival",
                role = "user"
            )

    with st.expander("**Converse With Agent**"):

        # Start conversation button
        if st.button("Start Conversation"):
            st.session_state.conversation_active = True

        # Only run the conversation logic if the button is clicked
        if st.session_state.conversation_active:
            lookup = {agent_state.name: agent_state.id for agent_state in client.list_agents()}
            agent_name = st.selectbox('Select an agent', lookup.keys(), index=None)

            if agent_name:
                agent_active = client.get_agent(lookup.get(agent_name))
                st.write(agent_active.id)

                # Function to send a message to the LLM agent
                def get_agent_response(user_message):
                    try:
                        # Make the actual API call (blocking until response is ready)
                        response = client.send_message(
                            agent_id=agent_active.id,
                            role="user",
                            message=user_message
                        )
                        return response
                        #return response.messages  # Adjust based on API response format
                    except Exception as e:
                        return f"Error: {e}"


                # Display chat history
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

                # Get user input using st.chat_input
                if user_input := st.chat_input("Type your message"):
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    with st.chat_message("user"):
                        st.write(user_input)

                    # Create a placeholder for the agent's response
                    with st.chat_message("assistant"):
                        placeholder = st.empty()
                        placeholder.write("Thinking...")  # Show a typing indicator

                        # Fetch the agent's response
                        agent_response = get_agent_response(user_input)
                        st.write(agent_response)

                        # Update the chat history and display the response
                        st.session_state.messages.append({"role": "assistant", "content": agent_response})
                        placeholder.write(agent_response)


def app():
    st.title("Agents With Memory")
    task = st.sidebar.radio("Select a demo", ("Memory", "Tool") )

    if task == "Memory":
        workflow_memory()


if __name__ == "__main__":
    app()