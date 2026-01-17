import streamlit as st
from multiagent import workflow

st.set_page_config(page_title="OmniLife Super Agent", page_icon="🛍️")

st.title("🛍️ OmniLife Super Agent")
st.caption("Multi-Agent Orchestrator for E-commerce, Logistics, Payments, and Support")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Orchestrating Agents...", expanded=True) as status:
            st.write("Supervisor analyzing query...")
            # Run the graph
            result = workflow.invoke({"user_query": prompt})
            
            st.write(f"Agents Involved: {', '.join(result.get('responses', {}).keys())}")
            with st.expander("View Raw Department Data"):
                st.json(result['responses'])
            
            status.update(label="Response Synthesized!", state="complete", expanded=False)
        
        final_response = result['final_answer']
        st.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})