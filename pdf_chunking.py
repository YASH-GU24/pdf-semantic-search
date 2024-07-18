import fitz  # PyMuPDF
import math

def extract_chunks_from_pdf(pdf_file_path, chunk_size=400):
    """
    Extracts text from a PDF file and splits it into smaller chunks.
    
    Args:
        pdf_file_path (str): Path to the PDF file.
        chunk_size (int): The size of each chunk in characters.
        
    Returns:
        List[dict]: A list of dictionaries, each containing a chunk of text and its metadata.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_file_path)
    chunks = []

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        text = page.get_text("text")
        
        # Split the text into smaller chunks
        for i in range(0, len(text), chunk_size):
            chunk_text = text[i:i + chunk_size]
            chunk_position = i  # Corrected chunk position
            
            chunk_data = {
                "page_number": page_number + 1,  # Pages are 1-indexed
                "chunk_text": chunk_text,
                "chunk_position": chunk_position
            }
            
            chunks.append(chunk_data)
    
    return chunks



