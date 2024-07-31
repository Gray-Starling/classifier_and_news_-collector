import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import joblib

def train():
    file_path = './data/processed/data.csv'
    df = pd.read_csv(file_path)

    train_val_data, test_data = train_test_split(df, test_size=0.1, random_state=42, stratify=df['category_encoded'])
    train_data, val_data = train_test_split(train_val_data, test_size=0.1, random_state=42, stratify=train_val_data['category_encoded'])

    # train_val_data, test_data = train_test_split(df, test_size=0.1, random_state=42, stratify=df['category_encoded'])
    # train_data, _ = train_test_split(train_val_data, train_size=0.1, random_state=42, stratify=train_val_data['category_encoded'])

    tfidf = TfidfVectorizer()

    X_train = tfidf.fit_transform(train_data['text'])
    y_train = train_data['category_encoded'].astype(int)

    param_grid_log_reg = {
    'penalty': ['l1', 'l2', None],
    'C': [0.01, 0.1, 1, 10, 100],
    'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
}

    log_reg = LogisticRegression(max_iter=2000)
    grid_search_log_reg = GridSearchCV(log_reg, param_grid_log_reg, refit=True, verbose=2, cv=3)

    grid_search_log_reg.fit(X_train, y_train)
    log_reg_best = grid_search_log_reg.best_estimator_

    param_grid_svm = {
    'C': [0.1, 1, 10, 100],
    'kernel': ['linear', 'rbf'],
    'gamma': [1, 0.1, 0.01],
}

    svm = SVC(probability=True, max_iter=2000)

    grid_search_svm = GridSearchCV(svm, param_grid_svm, refit=True, verbose=2, cv=3)

    grid_search_svm.fit(X_train, y_train)
    svm_best = grid_search_svm.best_estimator_

    param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [10, 20, 30],
    'criterion': ['gini', 'entropy']
}

    rf = RandomForestClassifier(random_state=42)
    grid_search_rf = GridSearchCV(rf, param_grid_rf, refit=True, verbose=2, cv=3)

    grid_search_rf.fit(X_train, y_train)
    rf_best = grid_search_rf.best_estimator_

    voting_clf = VotingClassifier(estimators=[
        ('log_reg', log_reg_best),
        ('svm', svm_best),
        ('rf', rf_best)
    ], voting='soft', weights=[1, 1, 1])

    voting_clf.fit(X_train, y_train)

    joblib.dump(voting_clf, './model/voting_classifier_model.pkl')
