import openai
import json
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk import ne_chunk, pos_tag

import os
os.environ['NLTK_DATA'] = 'C:\\nltk_data'
nltk.data.path.append("C:\\nltk_data")
nltk.download('punkt', 'C:\\nltk_data')
nltk.download('averaged_perceptron_tagger', 'C:\\nltk_data')
nltk.download('maxent_ne_chunker', 'C:\\nltk_data')
nltk.download('words', 'C:\\nltk_data')

def load_book_chunks_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_book_chunks_to_json(chunks, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

def extract_keywords(chunk):
    words = word_tokenize(chunk)
    words = [word for word in words if word.isalpha()]
    words = [word for word in words if word not in stopwords.words('english')]
    fdist = FreqDist(words)
    keywords = [word for word, freq in fdist.most_common(10)]
    return ', '.join(keywords)

def extract_named_entities(chunk):
    words = word_tokenize(chunk)
    tagged = pos_tag(words)
    namedEnt = ne_chunk(tagged, binary=True)
    entities = []
    for subtree in namedEnt.subtrees(filter=lambda t: t.label() == 'NE'):
        entities.append(' '.join([child[0] for child in subtree.leaves()]))
    return ', '.join(entities)

if __name__ == '__main__':
    chunks = load_book_chunks_from_json('book_chunks_with_summaries.json')
    for chunk in chunks:
        keywords = extract_keywords(chunk['content'])
        named_entities = extract_named_entities(chunk['content'])
        chunk['keywords'] = keywords
        chunk['named_entities'] = named_entities

    save_book_chunks_to_json(chunks, 'book_chunks.json')
