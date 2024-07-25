import pandas as pd
import requests
import os
import random
import re
import string
import nltk
import pymorphy3

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.preprocessing import LabelEncoder

from config import NEWS_DATA_API


# Ссылка на файл
link = NEWS_DATA_API
file_path = "data/source/news_dataset.csv"


async def download_data():
    # Проверка, существует ли файл
    if os.path.exists(file_path):
        print(f"Файл уже существует: {file_path}")
    else:
        # Попытка загрузить файл
        try:
            response = await requests.get(link)
            response.raise_for_status()  # Проверка успешности запроса
        except Exception as e:
            print("Что-то пошло не так при попытке загрузить файл:", e)
            raise e

        # Если запрос успешен, сохранить файл
        if response.ok:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Файл загружен и сохранен в {file_path}")
        else:
            print("Не удалось загрузить файл. Статус код:", response.status_code)
            raise ValueError("Не удалось загрузить файл")


def del_duplicates(df):
    df = df.drop_duplicates(subset=["article_link"])
    return df


def del_columns(df):
    df = df.drop("news_source_name", axis=1).drop("news_source_link", axis=1).drop(
        "category_link", axis=1).drop("article_date", axis=1).drop("article_link", axis=1)
    return df


def mapping_category(df):
    category_for_mapping = {
        "Политика": "Новости и Политика",
        "Россия": "Новости и Политика",
        "Мир": "Новости и Политика",
        "Бывший СССР": "Новости и Политика",
        "Силовые структуры": "Новости и Политика",
        "Экономика": "Экономика и Финансы",
        "Бизнес": "Экономика и Финансы",
        "Финансы": "Экономика и Финансы",
        "Технологии и медиа": "Технологии и Наука",
        "Наука и техника": "Технологии и Наука",
        "Интернет и СМИ": "Технологии и Наука",
        "Общество": "Культура и Общество",
        "Культура": "Культура и Общество",
        "Ценности": "Культура и Общество",
        "Спорт": "Спорт и Путешествия",
        "Путешествия": "Спорт и Путешествия",
        "Из жизни": "Здоровье и Образ жизни",
        "Среда обитания": "Здоровье и Образ жизни",
        "Забота о себе": "Здоровье и Образ жизни",
        "В мире": "Новости и Политика",
        "Происшествия": "Новости и Политика",
        "Армия": "Новости и Политика",
        "Наука": "Технологии и Наука",
        "Религия": "Культура и Общество",
        "Технологии": "Технологии и Наука",
        "Авто": "Новости и Политика",
        "Стиль": "Здоровье и Образ жизни"
    }

    df["category_name"] = df["category_name"].map(category_for_mapping)
    return df


def category_encoding(df):
    label_encoder = LabelEncoder()
    df["category_encoded"] = label_encoder.fit_transform(df["category_name"])

    return df


def del_empty(df):
    null_title_count = df['article_title'].isna()
    null_text_count = df['article_text'].isna()

    if null_title_count.sum():
        df.dropna(subset=["article_title"], inplace=True)

    if null_text_count.sum():
        df.dropna(subset=["article_text"], inplace=True)

    return df


def to_lower_str(df):
    df["article_title"] = df["article_title"].str.lower()
    df["article_text"] = df["article_text"].str.lower()

    return df


def del_repeating_titles(df):
    def replace_title(row):
        count = row["article_text"].count(row["article_title"])
        if count > 0:
            return ""
        else:
            return row["article_title"]

    df["article_title"] = df.apply(replace_title, axis=1)

    return df


def gluing_text(df):
    df['text'] = df['article_title'] + " " + df['article_text']
    df.drop(columns=['article_title', 'article_text'], inplace=True)

    return df


def preprocess_text(df):
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('omw-1.4')
    additional_stopwords = {'риа'}
    stop_words = set(stopwords.words('russian')).union(additional_stopwords)
    morph = pymorphy3.MorphAnalyzer()

    def regular_expression(text):
        return re.sub(r'\[.*?\]|https?://\S+|www\.\S+|<.*?>+|[%s]' % re.escape(string.punctuation), '', str(text))
    
    def tokenize(text):
        return word_tokenize(text)

    def remove_stopwords(tokens):
        return [word for word in tokens if word.lower() not in stop_words]

    def lemmatize(tokens):
        return [morph.parse(word)[0].normal_form for word in tokens]
    
    def preprocess_text(text):
        result = regular_expression(text)
        result = tokenize(result)
        result = remove_stopwords(result)
        result = lemmatize(result)
        return ' '.join(result)
    
    df['text'] = df['text'].apply(preprocess_text)

    return df
    

async def preprocess_data():
    try:
        await download_data()
    except Exception as e:
        print("Что-то пошло не так:", e)

    df = pd.read_csv(file_path)
    df = del_duplicates(df)
    df = del_columns(df)
    df = mapping_category(df)
    df = category_encoding(df)
    df = del_empty(df)
    df = to_lower_str(df)
    df = del_repeating_titles(df)
    df = gluing_text(df)
    df = preprocess_text(df)

    def random_text(count):
        for num in range(1, count+1):
            rand_int = random.randint(1, len(df))
            print(df['text'].iloc[rand_int])
            print("-"*30)

    random_text(1)
