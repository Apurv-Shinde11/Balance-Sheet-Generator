import streamlit as st
from main import run_pipeline  # We will slightly refactor main.py

st.set_page_config(page_title="Automated Balance Sheet Generator")

st.title("📊 Automated Balance Sheet Generator")

ticker = st.text_input("Enter Company Ticker (e.g., AAPL, RELIANCE.NS)")

if st.button("Generate Balance Sheet"):

    if ticker:
        with st.spinner("Generating balance sheet..."):
            try:
                output_file = run_pipeline(ticker.strip().upper())
                st.success("Balance Sheet Generated Successfully!")

                with open(output_file, "r", encoding="utf-8") as f:
                    html_content = f.read()

                st.components.v1.html(html_content, height=800, scrolling=True)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a ticker symbol.")