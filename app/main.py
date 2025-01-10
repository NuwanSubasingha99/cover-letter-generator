import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from cv_reader import read_cv
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cover Letter Generator")
    url_input = st.text_input("Enter a URL:", value="https://hcmcloud.dialog.lk/CareerPortal/Advert?id=4298&schema=bEopnWmcv9llMiBG3zygOw%3D%3D")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, read_cv, clean_text)

