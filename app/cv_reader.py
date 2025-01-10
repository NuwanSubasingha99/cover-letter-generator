from langchain.document_loaders import PyPDFLoader

def read_cv(file_path):
    """
            Reads a CV from a PDF file and returns its content.

            Parameters:
                file_path (str): The path to the PDF file.

            Returns:
                list: A list of documents representing the content of the PDF.
            """
    try:
        loader = PyPDFLoader(file_path)
        cv_data = loader.load()
        return cv_data
    except Exception as e:
        print(f"Error reading the CV: {e}")
        return None


