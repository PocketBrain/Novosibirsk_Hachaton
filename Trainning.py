
from annoy import AnnoyIndex
import pandas as pd
from sentence_transformers import SentenceTransformer
import time
from tqdm import tqdm

MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
n_trees = 4048
max_corpus_size = 4000
top_k_hits = 5
annoy_index_path = 'Annoy_index'

def get_data():
    """Распаковка данных и перевод в формат CSV"""
    pd.read_excel('./train_dataset.xlsx').to_csv('QAdata', index=False)
    data = pd.read_csv('./QAdata')
    return list(data.QUESTION)


def new_data():
    """Загрузка данные на сайте (Дополнение датасета)"""
    pd.read_excel('train_dataset.xlsx').to_csv('QAdata', index=False)
    data = pd.read_csv('./QAdata')
    return list(data.QUESTION)


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper


@timing_decorator
def embedding():
    question = get_data()
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = []
    for q in tqdm(question, desc='Embedding'):
        embeddings.append(model.encode(q))
    #with open('model.pkl', 'wb') as f:
     #   pkl.dump(embeddings, f)
    return embeddings


@timing_decorator
def build_annoy_index(embeddings):
    annoy_index = AnnoyIndex(len(embeddings[0]), 'angular')
    for i, emb in tqdm(enumerate(embeddings), desc='Building index', total=len(embeddings)):
        annoy_index.add_item(i, emb)
    annoy_index.build(n_trees)
    annoy_index.save(annoy_index_path)
    return annoy_index


embeddings = embedding()
annoy_index = build_annoy_index(embeddings)