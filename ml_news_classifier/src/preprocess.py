import pandas as pd
import random
import re
import string
import nltk
import pymorphy3
from tqdm import tqdm

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.preprocessing import LabelEncoder

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
    
    def preprocess(text):
        result = regular_expression(text)
        result = tokenize(result)
        result = remove_stopwords(result)
        result = lemmatize(result)
        # print(f"Обработана строка {index}")
        return ' '.join(result)
    
    df['text'] = df['text'].progress_apply(preprocess)

    return df
    

def preprocess_data(file_path):
    tqdm.pandas()
    print("Считывание csv файла...")
    df = pd.read_csv(file_path)
    print("Удаление дубликатов...")
    df = del_duplicates(df)
    print("Удаление не нужных колонок...")
    df = del_columns(df)
    print("Преобразование категорий...")
    df = mapping_category(df)
    print("Преобразование категорий к числовому значению...")
    df = category_encoding(df)
    print("Удаление пустых строк...")
    df = del_empty(df)
    print("Преобразование текста к нижнему регистру...")
    df = to_lower_str(df)
    print("Удаление повторяющихся заголовков...")
    df = del_repeating_titles(df)
    print("Склеивание текста...")
    df = gluing_text(df)
    print("Предобработка текста...")
    df = preprocess_text(df)

    balanced_df = pd.DataFrame(columns=df.columns)

    df['word_count'] = df['text'].apply(lambda x: len(str(x).split()))
    avg_word_count = df['word_count'].mean()

    min_samples = df['category_name'].value_counts().min()

    category_word_counts = df.groupby('category_name')['word_count'].mean()

    # Функция для балансировки данных в каждой категории
    def balancing_samples(category_data):
        category_avg_word_count = category_data['word_count'].mean()

        # Если количество строк больше min_samples
        while len(category_data) > min_samples:
            if category_avg_word_count > avg_word_count:
                # Убираем самые длинные строки, пока среднее количество слов не станет <= avg_word_count
                category_data = category_data.drop(category_data['word_count'].idxmax())
            else:
                # Удаляем самые короткие строки, пока среднее количество слов не станет >= avg_word_count
                category_data = category_data.drop(category_data['word_count'].idxmin())

            # Пересчитываем среднее количество слов в категории после удаления строки
            category_avg_word_count = category_data['word_count'].mean()

        # Если количество строк меньше или равно min_samples, возвращаем данные как есть
        return category_data.reset_index(drop=True)

    for category in df["category_name"].unique():
        category_data = df[df["category_name"] == category].copy()
        print(f"Категория обработки: '{category}'")

        balanced_category_data = balancing_samples(category_data)

        balanced_df = pd.concat([balanced_df, balanced_category_data], ignore_index=True)

        print(f"Категория '{category}' сбалансирована. Количество строк после балансировки: {len(balanced_category_data)}")
        print()

    # print("Все категории обработаны и сбалансированы.")

    balanced_df.to_csv('./data/processed/data.csv', index=False)
    print("\nДанные получены, обработаны и сохранены")
