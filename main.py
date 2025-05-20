import streamlit as st
from app.file_uploader import save_and_parse_uploaded_files
from app.query_engine import create_agent_with_multiple_dfs, run_query

st.set_page_config(page_title="CSV/Excel Chat Agent")

st.title("📊 Multi-File CSV/Excel Chat Agent")

uploaded_files = st.file_uploader("Upload your CSV or Excel files", accept_multiple_files=True, type=["csv", "xlsx"])

if uploaded_files:
    dfs = save_and_parse_uploaded_files(uploaded_files)
    st.success(f"{len(dfs)} file(s) uploaded and parsed.")

    agent = create_agent_with_multiple_dfs(dfs)

    st.subheader("💬 Ask a question about your data:")
    user_query = st.text_input("Type your question here")

    if st.button("Ask"):
        if user_query:
            with st.spinner("Analyzing..."):
                answer = run_query(agent, user_query)
                st.success("Answer:")
                st.write(answer)
        else:
            st.warning("Please enter a question.")
