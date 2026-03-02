import streamlit as st
import requests
import os

# Configuration
st.set_page_config(page_title="AI Code Reviewer", layout="wide")

# Get Backend URL from environment (provided by Railway)
# Fallback to localhost for local dev
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🛡️ AI Production Code Reviewer")
st.markdown("---")

with st.sidebar:
    st.header("Settings")
    language = st.selectbox("Select Language", ["python", "javascript", "go", "java", "cpp"])
    st.info(f"Connected to: {BACKEND_URL}")

code_content = st.text_area("Paste your code here...", height=400)

if st.button("Run Review", type="primary"):
    if not code_content:
        st.error("Please provide code to analyze.")
    else:
        with st.spinner("Analyzing code via Gemini API..."):
            try:
                payload = {"code": code_content, "language": language}
                response = requests.post(f"{BACKEND_URL}/review_code", json=payload)
                
                if response.status_code == 200:
                    res = response.json()
                    
                    # UI Layout for Results
                    st.success("Analysis Complete!")
                    st.metric("Overall Quality Score", f"{res['overall_score']}/100")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("🔒 Security")
                        for item in res['security_issues']:
                            st.error(item)
                    
                    with col2:
                        st.subheader("⚡ Performance")
                        for item in res['performance_issues']:
                            st.warning(item)
                            
                    with col3:
                        st.subheader("📝 Readability")
                        for item in res['readability_issues']:
                            st.info(item)
                else:
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")