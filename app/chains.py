import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `Company name`, `Company address`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):    
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_cover_letter(self, job, cv_data):
        prompt_cover_letter = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ## MY CV Details:
            {My_cv}

            ### INSTRUCTION:
            Your job is to write a cover letter to the compnay regarding the job mentioned above. 

            ### LETTER STRUCTURE:
            Sender and receiver addresses
            Introduction
            Body
            Closing

            (NO PREAMBLE):

            """
        )
        chain_email = prompt_cover_letter | self.llm
        res = chain_email.invoke({"job_description": str(job), "My_cv": cv_data})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))