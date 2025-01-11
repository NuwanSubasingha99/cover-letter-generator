import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import os
from chains import Chain
from cv_reader import read_cv
from utils import clean_text
from fpdf import FPDF
import base64


def save_cover_letter_as_pdf(content, file_name="Cover_Letter.pdf"):
    """Save the given content as a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content line by line to the PDF
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Save PDF to the file system
    pdf_output_path = os.path.join("generated_files", file_name)
    os.makedirs("generated_files", exist_ok=True)
    pdf.output(pdf_output_path)
    return pdf_output_path


def create_streamlit_app(llm, read_cv, clean_text):
    st.title("📧 Cover Letter Generator")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    url_input = st.text_input(
        "Enter a URL:",
        value=""

    )
    submit_button = st.button("Generate Cover Letter")

    file_path = None
    if uploaded_file is not None:
        # Display file details
        st.write("Filename:", uploaded_file.name)

        # Save the file to a temporary location
        temp_dir = "uploaded_files"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"File uploaded and saved to: {file_path}")

    if submit_button:
        if not file_path:
            st.error("Please upload a PDF file to proceed.")
            return

        if not url_input.strip():
            st.error("Please enter a valid URL.")
            return

        try:
            # Load job description from URL
            loader = WebBaseLoader([url_input])
            page_content = loader.load().pop().page_content
            job_data = clean_text(page_content)

            # Extract job details and CV data
            job = llm.extract_jobs(job_data)
            cv_data = read_cv(file_path=file_path)

            # Generate cover letter
            cover_letter = llm.write_cover_letter(job, cv_data)

            # Save the cover letter as a PDF
            pdf_file_path = save_cover_letter_as_pdf(cover_letter)

            # Display the cover letter preview
            st.write("### Cover Letter Preview:")
            st.text_area("Preview", cover_letter, height=300)

            # Provide a download button
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                download_link = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="Cover_Letter.pdf">Download Cover Letter</a>'
                st.markdown(download_link, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cover Letter Generator", page_icon="📧")
    create_streamlit_app(chain, read_cv, clean_text)
