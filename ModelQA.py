
"""
Установить!
pip install transformer
pip install annoy
pip install transformers[torch]
pip install -U sentence-transformers
"""
from annoy import AnnoyIndex
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import pickle as pkl
import torch
from transformers import GPT2Tokenizer

# Загрузка SBERT модели
data = pd.read_csv('QAdata')
question = list(data.QUESTION)
answer = list(data.ANSWER)
#sbert_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
sbert_model = SentenceTransformer("modelbert.pt")
with open('model.pkl', 'rb') as f:
    sbert_embeddings = pkl.load(f)
annoy_index = AnnoyIndex(len(sbert_embeddings[0]), 'angular')
annoy_index.load('Annoy_index')
sbert_embeddings = [torch.tensor(embedding) for embedding in sbert_embeddings]

# Загрузка GPT-3 модели
DEVICE = torch.device('cpu')
modelgpt = torch.load('modelgpt1234.pt', map_location=torch.device('cpu'))
modelgpt.eval()
#model_name_or_path = "tinkoff-ai/ruDialoGPT-medium"
tokenizer = GPT2Tokenizer.from_pretrained('modelgpt1234.pt')


def generate_gpt_response(question, model, tokenizer):
    input_ids = tokenizer.encode(question, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = model.generate(input_ids,
                             do_sample=True,
                             num_beams=3,
                             temperature=1.5,
                             top_p=1,
                             top_k=0,
                             max_length=150)
    generated_text = list(map(tokenizer.decode, out))[0]
    last_period_index = generated_text.rfind('.')
    if last_period_index != -1:
        generated_text = generated_text[:last_period_index + 1]
    input_ids2 = tokenizer.encode(question, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = model.generate(input_ids2,
                             do_sample=True,
                             num_beams=3,
                             temperature=1.5,
                             top_p=1,
                             top_k=0,
                             max_length=150)
    generated_text2 = list(map(tokenizer.decode, out))[0]
    last_period_index = generated_text2.rfind('.')
    if last_period_index != -1:
        generated_text2 = generated_text2[:last_period_index + 1]
    result = [generated_text, generated_text2]
    return result


def question_response(sbert_embeddings, inp_question):
    top_k_hits = 3
    question_embedding = sbert_model.encode(inp_question)

    corpus_ids, scores = annoy_index.get_nns_by_vector(question_embedding, top_k_hits, include_distances=True)
    hits = [{'corpus_id': id, 'score': 1 - ((score ** 2) / 2)} for id, score in zip(corpus_ids, scores)]
    hits_above_threshold = [hit for hit in hits if hit['score'] > 0.8]

    if hits_above_threshold:
        print("Возможные ответы на ваш вопрос:")
        for hit in hits_above_threshold:
            print("\t{:.3f}\t{}".format(hit['score'], question[hit['corpus_id']]))

        # Семантический поиск с SBERT
        correct_hits = util.semantic_search(question_embedding, sbert_embeddings, top_k=top_k_hits)[0]
        correct_hits_ids = [hit['corpus_id'] for hit in correct_hits]

        return answer[correct_hits_ids[0]]
    else:
        print("К сожалению, мы не поняли ваш вопрос. Возможно, вы имели в виду один из следующих вопросов:")
        for hit in hits[:3]:
            print("\t{}".format(question[hit['corpus_id']]))
        return "Не понятен вопрос"


if __name__ == '__main__':
    while True:
        try:
            inp_question = input("Введите ваш вопрос: ")
            print("Быстрый ответ")
            #вывод обычной модели (убрать принты)
            print(question_response(sbert_embeddings, inp_question))
            print("Ответ от GPT требует времени...")
            # вывод gpt модели (убрать принты)
            print(generate_gpt_response(inp_question, modelgpt, tokenizer))
        except KeyboardInterrupt:
            print('Пока!')
            break