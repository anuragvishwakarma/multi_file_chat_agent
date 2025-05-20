import streamlit as st
from app.file_uploader import save_and_parse_uploaded_files
from app.query_engine import create_agent_with_multiple_dfs, run_query
from app.pdf_generator import create_pdf_report, generate_chart

# Set page config
st.set_page_config(page_title="CSV/Excel Chat Agent")

# App title
st.title("📊 Multi-File CSV/Excel Chat Agent")

# File uploader
uploaded_files = st.file_uploader("Upload your CSV or Excel files", accept_multiple_files=True, type=["csv", "xlsx"])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_files:
    # Save and parse files
    dfs = save_and_parse_uploaded_files(uploaded_files)
    st.success(f"{len(dfs)} file(s) uploaded and parsed.")

    # Create agent
    agent = create_agent_with_multiple_dfs(dfs)

    # Input box for user query
    st.subheader("🤖 Ask a question about your data:")
    user_query = st.text_input("Type your question here")

    # Handle question
    if st.button("Ask"):
        if user_query:
            with st.spinner("Analyzing..."):
                answer = run_query(agent, user_query)
                st.success("Answer:")
                st.write(answer)

                # Generate chart and PDF
                chart_paths = []
                for sheet, df in dfs.items():
                    if not df.select_dtypes(include="number").empty:
                        chart_file = f"{sheet}_chart.png"
                        generate_chart(df, chart_file)
                        chart_paths.append(chart_file)

                pdf_path = create_pdf_report(user_query, answer, dfs, chart_paths)
                st.success("PDF report generated!")

                # Save to session history
                st.session_state.chat_history.append({
                    "question": user_query,
                    "answer": answer,
                    "pdf_path": pdf_path
                })
        else:
            st.warning("Please enter a question.")

    # Show chat history
    st.markdown("### 💬 Chat History")
    for idx, chat in enumerate(st.session_state.chat_history):
        with st.expander(f"Q{idx+1}: {chat['question']}"):
            st.markdown(f"**Answer:** {chat['answer']}")
            with open(chat["pdf_path"], "rb") as f:
                st.download_button(f"📄 Download Report Q{idx+1}", f, file_name=f"report_q{idx+1}.pdf")

    # Manual download for latest report (optional)
    if st.button("📥 Download PDF Report"):
        if st.session_state.chat_history:
            latest_report = st.session_state.chat_history[-1]["pdf_path"]
            with open(latest_report, "rb") as f:
                st.download_button("Download Report", f, file_name="chat_report.pdf")
        else:
            st.warning("No report available yet.")
