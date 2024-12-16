from letta import ChatMemory, EmbeddingConfig, LLMConfig, create_client
from letta.schemas.memory import ChatMemory

import streamlit as st
import os

embedding_config = EmbeddingConfig.default_config(model_name="text-embedding-ada-002")
client = create_client()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]
if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = False  # Tracks if the conversation is active


# Function to send a message to the LLM agent
def get_agent_response(agent, user_message):
    try:
        # Make the actual API call (blocking until response is ready)
        response = client.send_message(
            agent_id=agent.id,
            role="user",
            message=user_message
        )
        return response
        # return response.messages  # Adjust based on API response format
    except Exception as e:
        return f"Error: {e}"


def chat(agent):
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
            agent_response = get_agent_response(agent, user_input)

            # Update the chat history and display the response
            st.session_state.messages.append({"role": "assistant", "content": agent_response})
            placeholder.write(agent_response)


def delete_agents():
    if st.button("Delete Agents"):
        for agent_state in client.list_agents():
            st.write(f"Deleting agent {agent_state.name}")
            client.delete_agent(agent_id=agent_state.id)


def get_agents():
    all_agents = []
    #if st.button(f"List Agents: {header}"):
    for agent_state in client.list_agents():
        all_agents.append({'name': agent_state.name, 'id': agent_state.id})

    return all_agents


def workflow_openai():
    os.environ['OPENAI_API_KEY'] = 'TBD'
    os.environ['OPENAI_PROJECT'] = 'TBD'

    with st.expander("**Create New Agent**"):
        import datetime
        agent_name = st.text_input('Agent Name', value="Jarvis")
        agent_name += "-" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        st.divider()
        st.write('Short Term Memory Modules')
        agent_persona = st.text_input('Agent:', value="You are a helpful assistant that loves emojis")

        human_name = st.text_input('User:', value="Bobby")

        if st.button(f'Create'):
            client.set_default_llm_config(LLMConfig.default_config("gpt-4o-mini"))
            client.set_default_embedding_config(EmbeddingConfig.default_config("text-embedding-ada-002"))

            new_agent = client.create_agent(
                name=agent_name,
                memory=ChatMemory(
                    human=f"My name is {human_name}.",  # refers to the human
                    persona=f"{agent_persona}"  # refers to the agent
                )
            )
            st.write(f'Created agent {new_agent.name}')
            if st.button('Show Memory Of New Agent'):
                memory_block_names = ['persona', 'human']
                memories = client.get_core_memory(new_agent.id)
                for b in memory_block_names:
                    st.write(memories.get_block(b))

    with st.expander("**List Agents**"):
        agents_read = get_agents()
        if agents_read:
            st.write(agents_read)

    with st.expander("**Converse With Agent**"):
        agent_ids = [a.get("id") for a in get_agents()]

        #agent_active_id = st.text_input('Please enter agent id:', value="")
        agent_active_id = st.selectbox("Please select an agent", agent_ids)

        if agent_active_id:
            agent_active = client.get_agent(agent_active_id)

            if st.button('**:blue[Show Short Term Memory]**'):
                memory_block_names = ['persona', 'human']
                memories_short = client.get_core_memory(agent_active.id)
                for b in memory_block_names:
                    st.write(b)
                    st.write(memories_short.get_block(b))

            if st.button('**:blue[Show Long Term Memory]**'):
                memories_long = client.get_archival_memory(agent_active.id)
                for l in memories_long:
                    st.write(l)

            st.divider()
            chat(agent_active)

    with st.expander("**Delete Agents**"):
        delete_agents()



def workflow_ollama():
    # from running ollama serve
    ollama_url = 'http://127.0.0.1:11434'
    os.environ["OLLAMA_BASE_URL"] = ollama_url
    return True


def app():
    st.title("Smart Agents, Smarter Memories")
    task = st.sidebar.radio("Select a LLM", ("OpenAI", "Ollama") )

    if task == "Ollama":
        workflow_ollama()
    elif task == "OpenAI":
        workflow_openai()


if __name__ == "__main__":
    app()
