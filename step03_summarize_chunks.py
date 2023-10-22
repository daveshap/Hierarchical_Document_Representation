import openai
import json

def load_book_chunks_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_book_chunks_to_json(chunks, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

def summarize_chunk(chunk, model="gpt-3.5-turbo-16k", temperature=0, max_tokens=200):
    conversation = [
        {'role': 'system', 'content': open_file('system_summary.txt')},
        {'role': 'user', 'content': chunk}
    ]
    response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    openai.api_key = open_file('key_openai.txt').strip()

    chunks = load_book_chunks_from_json('book_chunks.json')
    for chunk in chunks:
        summary = summarize_chunk(chunk['content'])
        print('\n\n\nSUMMARY:', summary)
        chunk['summary'] = summary

    save_book_chunks_to_json(chunks, 'book_chunks_with_summaries.json')