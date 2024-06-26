import weaviate  # to communicate to the Weaviate instance
import warnings

warnings.filterwarnings("ignore")

# setting up client
client = weaviate.Client("http://localhost:8080")

SCHEMA_NAME = "Pdf"

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
          "description": "The id of the chunk",
          "moduleConfig": {
            "text2vec-transformers": {
              "skip": True,
              "vectorizePropertyName": False
            }
          },
          "name": "chunk_id"
        },
        {
          "dataType": [
            "text"
          ],
          "description": "The id of the file",
          "moduleConfig": {
            "text2vec-transformers": {
              "skip": True,
              "vectorizePropertyName": False
            }
          },
          "name": "file_id"
        },
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
    print("Schema succefully added")
else:
    print("Schema already present")