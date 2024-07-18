from flask import Flask, request, render_template, jsonify, send_file
import fitz  # PyMuPDF
import os
import weaviate  # to communicate to the Weaviate instance
app = Flask(__name__)
client = weaviate.Client("http://localhost:8080")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def query():
    query = request.form['searched_data']
    response = (
    client.query
    .get("Pdfs", ["file_name", "chunk_position", "page_number", "chunk_text"])
    .with_near_text({"concepts": [query]})
    .with_additional(['certainty'])
    .do()
)
    print(response)
    return render_template('index.html', obj_info=response['data']['Get']['Pdfs'])

@app.route('/pdf/<path:filename>')
def get_pdf(filename):
    return send_file(filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, port=4000)
