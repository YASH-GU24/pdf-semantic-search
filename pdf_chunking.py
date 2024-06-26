import fitz  # PyMuPDF
import math

def extract_chunks_from_pdf(pdf_file_path, chunk_size=1000):
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
            chunk_position = f"Characters {i}-{i + chunk_size}"
            
            chunk_data = {
                "page_number": page_number + 1,  # Pages are 1-indexed
                "text": chunk_text,
                "position": chunk_position
            }
            
            chunks.append(chunk_data)
    
    return chunks

# Example usage
pdf_file_path = "example.pdf"
chunks = extract_chunks_from_pdf(pdf_file_path)

for chunk in chunks:
    print(f"Page Number: {chunk['page_number']}")
    print(f"Chunk Position: {chunk['position']}")
    print(f"Text: {chunk['text'][:200]}...")  # Print first 200 characters
    print("\n---\n")
