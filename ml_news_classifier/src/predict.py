import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd

def predict(text):
    voting_clf_loaded = joblib.load('./model/voting_classifier_model.pkl')

    file_path = './data/processed/data.csv'
    df = pd.read_csv(file_path)

    train_val_data, test_data = train_test_split(df, test_size=0.1, random_state=42, stratify=df['category_encoded'])
    train_data, _ = train_test_split(train_val_data, train_size=0.1, random_state=42, stratify=train_val_data['category_encoded'])

    tfidf = TfidfVectorizer()

    tfidf.fit(train_data['text'])


    X_new = tfidf.transform([text])

    predicted_category_encoded = voting_clf_loaded.predict(X_new)[0]

    category_map = pd.Series(df['category_name'].values, index=df['category_encoded'].values).to_dict()

    predicted_category_name = category_map.get(predicted_category_encoded, "Unknown")  # Get category name or "Unknown" if not found
    

    return predicted_category_name