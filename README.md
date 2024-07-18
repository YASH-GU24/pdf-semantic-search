# pdf-semantic-search

# Steps to run

1. Run weaviate Docker
```bash
docker-compose up -d
```
2. Make a virtual environment
```bash
pythom -m venv .venv
```
3. Activate virtual environment
```bash
source .venv/bin/activate
```
4. Install requirements
```bash
pip install -r requirements.txt
```
5. Add pdf to database
```bash
python add_data.py <-folder path->
```
6. Run the flask server
```bash
python server.py
```
Now navigate to http://127.0.0.1:4000 in your browser to access the application
