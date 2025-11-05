import streamlit as st
import boto3
from botocore.exceptions import ClientError
import json
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt

# Streamlit UI
st.title("Bedrock Chat Application")

# Sidebar for configurations
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox("Select LLM Model", ["anthropic.claude-3-haiku-20240307-v1:0", "anthropic.claude-3-5-sonnet-20240620-v1:0"])
kb_id = st.sidebar.text_input("Knowledge Base ID", "your-knowledge-base-id")
temperature = st.sidebar.select_slider("Temperature", [i/10 for i in range(0,11)],1)
top_p = st.sidebar.select_slider("Top_P", [i/1000 for i in range(0,1001)], 1)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    sources_output = ""
    if valid_prompt(prompt, model_id):
        kb_response = query_knowledge_base(prompt, kb_id)
        if kb_response:
            answer = kb_response['output']['text']
            citations = kb_response.get('citations', [])

            sources_output += "\n\n**Sources:**\n"
            if not citations:
                sources_output += "No sources found for this answer."
            else:
                unique_sources = set()
                for citation in citations:
                    retrieved_reference = citation.get('retrievedReference', {})
                    location = retrieved_reference.get('location', {})
                    s3_location = location.get('s3Location', {})
                    uri = s3_location.get('uri')
                    if uri:
                        unique_sources.add(uri)
                for i, source_uri in enumerate(unique_sources):
                    file_name = source_uri.split('/')[-1]
                    sources_output += f"[{i+1}] {file_name}\n"

            response = f"{answer}{sources_output}"
        else:
            response = "No response from knowledge base."
    else:
        response = "I can only answer questions about heavy machinery. Please ask a relevant question."

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})