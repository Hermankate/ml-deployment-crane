
# import streamlit as st
# from PyPDF2 import PdfReader
# import pandas as pd
# import re
# import spacy
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import sys
# sys.modules["torch.classes"] = None

# # Load spaCy English model
# nlp = spacy.load("en_core_web_sm")

# # Function to extract text from PDF
# def extract_text_from_pdf(file):
#     pdf = PdfReader(file)
#     text = ""
#     for page in pdf.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + " "
#     return text.strip()

# # Function to extract candidate details using spaCy and regex
# def extract_candidate_details(text):
#     doc = nlp(text)
    
#     # Try to extract name using NER (take first PERSON entity found)
#     name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "Unknown")

#     # Extract email using regex
#     email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
#     email = email_match.group(0) if email_match else "Unknown"

#     # Extract phone number using regex (basic pattern)
#     phone_match = re.search(r'\+?\(?\d{2,4}\)?[-.\s]?\d{3}[-.\s]?\d{4,7}', text)
#     phone = phone_match.group(0) if phone_match else "Unknown"

#     return name, email, phone

# # Function to rank resumes based on job description
# def rank_resumes(job_description, resumes):
#     documents = [job_description] + resumes
#     vectorizer = TfidfVectorizer().fit_transform(documents)
#     vectors = vectorizer.toarray()

#     job_description_vector = vectors[0]
#     resume_vectors = vectors[1:]
#     cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()
    
#     return cosine_similarities

# # Streamlit app
# st.set_page_config(page_title="Resume Ranking System", layout="wide")
# st.title("📄 Resume Ranking System ")


# # File uploader
# st.header("📤 Upload Resume PDFs")
# uploaded_files = st.file_uploader("Upload PDF resumes", type=["pdf"], accept_multiple_files=True)

# # Job description input
# st.header("📌 Job Description")
# job_description = st.text_area("Enter the job description here...")


# if uploaded_files and job_description:
#     st.header("📊 Ranked Resumes")
    
#     resume_texts = []
#     candidate_info = []

#     for file in uploaded_files:
#         text = extract_text_from_pdf(file)
#         resume_texts.append(text)

#         name, email, phone = extract_candidate_details(text)
#         candidate_info.append({
#             "File Name": file.name,
#             "Name": name,
#             "Email": email,
#             "Contact": phone
#         })

#     # Rank resumes
#     scores = rank_resumes(job_description, resume_texts)

#     # Add scores to candidate info
#     for i in range(len(candidate_info)):
#         candidate_info[i]["Score"] = round(scores[i], 4)

#     # Convert to DataFrame
#     results_df = pd.DataFrame(candidate_info)
#     results_df = results_df.sort_values(by="Score", ascending=False).reset_index(drop=True)

#     # Display results
#     st.dataframe(results_df, use_container_width=True)


import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.modules["torch.classes"] = None

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text.strip()

# Function to extract candidate details using spaCy and regex
def extract_candidate_details(text):
    doc = nlp(text)
    
    # Try to extract name using NER (take first PERSON entity found)
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "Unknown")

    # Extract email using regex
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else "Unknown"

    # Extract phone number using regex (basic pattern)
    phone_match = re.search(r'\+?\(?\d{2,4}\)?[-.\s]?\d{3}[-.\s]?\d{4,7}', text)
    phone = phone_match.group(0) if phone_match else "Unknown"

    return name, email, phone

# Function to rank resumes based on job description
def rank_resumes(job_description, resumes):
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()
    
    return cosine_similarities

# Streamlit app
st.set_page_config(page_title="Resume Ranking System", layout="wide")
st.title("📄 Resume Ranking System ")

# File uploader
st.header("📤 Upload Resume PDFs")
uploaded_files = st.file_uploader("Upload PDF resumes", type=["pdf"], accept_multiple_files=True)

# Job description input
st.header("📌 Job Description")
job_description = st.text_area("Enter the job description here...")

if uploaded_files and job_description:
    resume_texts_dict = {}
    resume_texts_list = []
    candidate_info = []

    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        resume_texts_dict[file.name] = text
        resume_texts_list.append(text)
        
        name, email, phone = extract_candidate_details(text)
        candidate_info.append({
            "File Name": file.name,
            "Name": name,
            "Email": email,
            "Contact": phone
        })

    # Rank resumes
    scores = rank_resumes(job_description, resume_texts_list)

    # Add scores to candidate info
    for i in range(len(candidate_info)):
        candidate_info[i]["Score"] = round(scores[i], 4)

    # Convert to DataFrame and sort
    results_df = pd.DataFrame(candidate_info)
    results_df = results_df.sort_values(by="Score", ascending=False).reset_index(drop=True)

    # Display results
    st.dataframe(results_df, use_container_width=True)

    # Sidebar for resume preview
    with st.sidebar:
        st.header("🔍 Resume Preview")
        sorted_file_names = results_df["File Name"].tolist()
        selected_file = st.selectbox("Select resume to view:", sorted_file_names)

    # Display selected resume content
    # st.subheader(f"📑 Preview of {selected_file}")
    # preview_text = resume_texts_dict.get(selected_file, "Content not available")
    # st.text_area("Resume Content", value=preview_text, height=400, key="preview", disabled=True)


    # ... (keep all previous code the same until the preview section)

# Display selected resume content
    st.subheader(f"📑 Preview of {selected_file}")
    preview_text = resume_texts_dict.get(selected_file, "Content not available")

    # Create a styled preview container with white background
    st.markdown(
        f"""
        <div style="
            background-color: white;
            color: black;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #ddd;
            max-height: 400px;
            overflow-y: auto;
        ">
        <pre style="white-space: pre-wrap; font-family: sans-serif;">{preview_text}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )