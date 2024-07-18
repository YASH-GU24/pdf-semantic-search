import weaviate  # to communicate to the Weaviate instance
import warnings
import os
import argparse
from pdf_chunking import extract_chunks_from_pdf

warnings.filterwarnings("ignore")

# setting up client
client = weaviate.Client("http://localhost:8080")

SCHEMA_NAME = "Pdfs"

def get_schemas():
    return [schema["class"] for schema in client.schema.get()["classes"]]

schema = {
      "class": SCHEMA_NAME,
      "description": "A class called Pdf",
      "moduleConfig": {
        "text2vec-transformers": {
          "vectorizeClassName": True
        }
      },
      "properties": [
        {
          "dataType": [
            "text"
          ],
          "description": "The name of the file",
          "moduleConfig": {
            "text2vec-transformers": {
              "skip": True,
              "vectorizePropertyName": False
            }
          },
          "name": "file_name"
        },
        {
          "dataType": [
            "number"
          ],
          "description": "The page number of the pdf",
          "moduleConfig": {
            "text2vec-transformers": {
              "skip": True,
              "vectorizePropertyName": False
            }
          },
          "name": "page_number"
        },
        {
          "dataType": [
            "text"
          ],
          "description": "The text of the chunk",
          "moduleConfig": {
            "text2vec-transformers": {
              "skip": False,
              "vectorizePropertyName": True
            }
          },
          "name": "chunk_text"
        },
        {
          "dataType": [
            "number"
          ],
          "description": "The position of the chunk",
          "moduleConfig": {
            "text2vec-transformers": {
              "skip": False,
              "vectorizePropertyName": True
            }
          },
          "name": "chunk_position"
        },
      ],
      "vectorizer": "text2vec-transformers"
    }

if SCHEMA_NAME not in get_schemas():
    client.schema.create_class(schema)
    print("Schema successfully added")
else:
    client.schema.delete_class(SCHEMA_NAME)
    client.schema.create_class(schema)
    print("Schema successfully added")

client.batch.configure(
  batch_size=10, 
  # dynamically update the `batch_size` based on import speed
  dynamic=True,
  timeout_retries=3,
)

def add_data_to_weaviate(chunks, filename):
  for data in chunks:
    data_object = {
        'file_name': str(filename),
        'page_number': int(data['page_number']),
        'chunk_text': str(data['chunk_text']),
        'chunk_position': int(data['chunk_position']),
    }

    try:
        client.batch.add_data_object(data_object, "Pdfs")
        print("object added")
    except BaseException as error:
        print("Import Failed at: ", data_object) 
        print("An exception occurred: {}".format(error))
        # Stop the import on error

  client.batch.flush()

def iterate_pdfs(folder_path):
    # Check if the provided path is a directory
    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} is not a valid directory.")
        return

    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is a PDF
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            chunks = extract_chunks_from_pdf(pdf_path)
            add_data_to_weaviate(chunks, filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process PDFs and add to Weaviate.')
    parser.add_argument('folder_path', type=str, help='The path to the folder containing PDFs')
    
    args = parser.parse_args()
    iterate_pdfs(args.folder_path)
