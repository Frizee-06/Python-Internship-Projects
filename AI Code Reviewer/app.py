import streamlit as st
import subprocess
import tempfile
import black
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze

# Page Setup
st.set_page_config(page_title="AI Code Reviewer", layout="wide")
st.title("AI Code Reviewer")

# Code Input
code_input = st.text_area("Paste your Python code here:", height=300)

# When Button is Clicked
if st.button("🔍 Analyze Code") and code_input.strip() != "":
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w+") as temp:
        temp.write(code_input)
        temp.flush()

        # Flake8 Style Report
        st.subheader("Flake8 Style Report")
        result = subprocess.run(["flake8", temp.name], capture_output=True, text=True)
        st.code(result.stdout or "No issues found!", language="text")

        # Black Formatter
        st.subheader("Black Formatting Suggestion")
        try:
            formatted_code = black.format_str(code_input, mode=black.Mode())
            st.code(formatted_code, language="python")
        except Exception as e:
            st.error(f"Black formatting failed: {e}")

        #  Radon Complexity Analysis  Fixed Version)
        st.subheader("Radon Complexity Analysis")
        try:
            blocks = cc_visit(code_input)
            if not blocks:
                st.info("No functions or classes found.")
            else:
                for block in blocks:
                    block_info={
                        "Name": block.name,
                        "Line No": block.lineno,
                        "End Line": getattr(block, "endline", "N/A"),
                        "Complexity": block.complexity,
                    }
                    st.json(block_info)
        except Exception as e:
            st.error(f"Radon error: {e}")

        # Maintainability Index
        st.subheader("Maintainability Index")
        try:
            mi_score = mi_visit(code_input, True)
            st.text(f"Maintainability Index Score: {mi_score}")
        except Exception as e:
            st.error(f"MI calculation error: {e}")

        # Raw Metrics
        st.subheader("Raw Metrics")
        try:
            raw = analyze(code_input)
            st.json(raw)
        except Exception as e:
            st.error(f"Raw metrics error: {e}")

        st.success("Code Review Complete!")