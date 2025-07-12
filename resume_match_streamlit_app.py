import streamlit as st
import fitz 
import ollama

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# Function to call Ollama (LLaMA2)
def analyze_resume(resume_text, job_text):
    prompt = f"""
Here is a resume:
---
{resume_text}
---

Here is a job description:
---
{job_text}
---

Based on the job description, provide:
1. Match score out of 100
2. List of matching skills
3. List of missing or weak areas
4. Suggestions to improve the resume
5. A custom cover letter tailored for the job
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Error from Ollama: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Resume Match Bot", layout="centered")
st.title("📄 Resume & Job Match Analyzer (Offline with Ollama)")

resume_file = st.file_uploader("📎 Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste the Job Description")

if resume_file and job_description:
    with st.spinner("Analyzing... please wait ⏳"):
        resume_text = extract_text_from_pdf(resume_file)
        if resume_text.startswith("Error"):
            st.error(resume_text)
        else:
            result = analyze_resume(resume_text, job_description)
            st.success("✅ Analysis Complete!")
            st.markdown(result)
