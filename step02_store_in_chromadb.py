import chromadb
from chromadb.config import Settings
import json

def load_book_chunks_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def store_book_chunks_in_chromadb(chunks, collection):
    for chunk in chunks:
        collection.add(documents=[chunk['content']], ids=[str(chunk['index'])])

if __name__ == '__main__':
    # instantiate ChromaDB
    persist_directory = "chromadb"
    chroma_client = chromadb.Client(Settings(persist_directory=persist_directory,chroma_db_impl="duckdb+parquet",))
    collection = chroma_client.get_or_create_collection(name="book")

    chunks = load_book_chunks_from_json('book_chunks.json')
    store_book_chunks_in_chromadb(chunks, collection)

    chroma_client.persist()