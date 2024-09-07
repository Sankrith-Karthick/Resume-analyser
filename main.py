from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import fitz  # PyMuPDF
import google.generativeai as genai
import io
import base64
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = doc.load_page(0)  # Load the first page

        pix = first_page.get_pixmap()  # Render page to image
        img_byte_arr = io.BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(img_byte_arr, format='JPEG')  # Save image to BytesIO
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app
st.set_page_config(page_title="Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded Successfully")

    submit1 = st.button("Tell me about the resume")
    submit3 = st.button("Percentage match")

    input_prompt1 = """You are an experienced HR with technical experience in the field of Data science, full stack, web development, big data engineering, devops, data mining. Your task is to review the provided resume against the job description for these profiles.
    Please share your professional experience on whether the candidate's profile aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job role."""

    input_prompt3 = """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, big data engineering, devops, data analyst, and deep ATS functionality. Your task is to evaluate the resume against the provided job description. First, the output should come as a percentage and then the keywords missing against the job description."""

    if submit1:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The response is ")
            st.write(response)
        else:
            st.write("Please upload the Resume")
    elif submit3:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The response is ")
            st.write(response)
        else:
            st.write("Please upload the Resume")
