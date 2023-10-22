import json

def split_book_into_chunks(file_name, chunk_size):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    chunks = ['\n'.join(chunk) for chunk in chunks]
    
    return chunks

def save_chunks_as_json(chunks, output_file_name):
    data = [{'index': i, 'content': chunk} for i, chunk in enumerate(chunks)]
    
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

chunks = split_book_into_chunks('book.txt', 50)
save_chunks_as_json(chunks, 'book_chunks.json')