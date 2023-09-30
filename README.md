В файле ModelQA.py содержиться интерфейс для создания и тестирования чат бота<br>
<br>В файле Trainning.py код для дообучения модели и преобразования входных данных (Обучался в Google Colab на GPU)<br>
<br>Файл Annoy_index и веса GPT модели необходимые для работы дообученной модели, необходимо скачать и вставить в файлы проекта, так как они превышает 100мб (git lfs не помог)
(https://drive.google.com/file/d/1gufxOUqmlSdKEqWSMUzflGKvj8OTdo2e/view?usp=sharing) - для ANNOY <br>
(https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1tdedCMoxcBLvx3OdVBnCFRDQZ4qeW_sY) для GPT
## Описание проекта
Данный проект представляет собой LLM чат-бота для обучения сотрудников компании Smart Consulting . Бот использует 2 модели SentenceTransformer и построенный на ее основе индекс Annoy для быстрого поиска наиболее подходящего ответа на заданный вопрос. А также ruDialoGPT-medim для формирования человеческих ответов. Такое решение помогает многократно улучшить масштабируемость и точность ответов

## Используемая модель
В данном проекте используется связь моделей SentenceTransformer с названием "all-MiniLM-L6-v2" и "tinkoff-ai/ruDialoGPT-small". Эти модели обучены на большом корпусе текстов и способны выделять семантические признаки из текстов, что позволяет использовать ее для задачи поиска наиболее подходящего ответа на заданный вопрос.

## Используемая метрика
Для измерения сходства между вопросами и ответами используется метрика cosine similarity, которая позволяет измерять косинус угла между векторами, полученными из текстов с помощью модели SentenceTransformer. Точность на данные их заданного датасета 0.95+.

## Функция сравнения
Для поиска наиболее подходящего ответа на заданный вопрос используется индекс Annoy, который строится на основе функции сравнения angular distance. Эта функция сравнения позволяет измерять угол между векторами и определять, насколько они близки друг к другу по смыслу.

## Используемые пакеты и библиотеки
<br>transformer
<br>annoy
<br>transformers[torch]
<br>sentence-transformers
<br>AnnoyIndex
<br>PyTorch
<br>Pandas
<br>from Sentence_transformers import SentenceTransformer, util
<br>Pickle

Обучение проводилось в Google Colab https://colab.research.google.com/drive/1K3xRY9uQWrjuLdSUF-B6nONKMar_m5YE?usp=sharing
<br>Модели на HuggingFace в открытом доступе<br>1)(https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
<br>2)(https://huggingface.co/tinkoff-ai/ruDialoGPT-small)
