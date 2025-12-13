import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class ModelLoader:
    def __init__(self, csv_path="CSV/SoftwareQuestions_preprocessed.csv"):
        self.csv_path = csv_path

        self.model_dir = "models"

        self._ensure_model_dir()
        self.df = pd.read_csv(self.csv_path)

        self.vectorizer = None
        self.question_vectors = None
        self.knn_model = None

        self.load_or_train_models()
        

    def _ensure_model_dir(self):
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    def load_or_train_models(self):
        # set the file paths for saved models
        tfidf_path = f"{self.model_dir}/tfidf_vectorizer.pkl"
        vectors_path = f"{self.model_dir}/question_vectors.pkl"
        knn_path = f"{self.model_dir}/knn_model.pkl"

        # if the model already exists, load them instead of retraining
        if os.path.exists(tfidf_path) and os.path.exists(vectors_path):
            self.vectorizer = joblib.load(tfidf_path)
            self.question_vectors = joblib.load(vectors_path)

        else:
            # train TF-IDF on all questions
            self.vectorizer = TfidfVectorizer(max_features=5000)
            self.question_vectors = self.vectorizer.fit_transform(self.df["Question"]) #fit_transform converts questions to numerical values
            
            # save the vectorizer and vectors for use
            joblib.dump(self.vectorizer, tfidf_path)
            joblib.dump(self.question_vectors, vectors_path)

        # if the model exists then load it
        if os.path.exists(knn_path):
            self.knn_model = joblib.load(knn_path)
        
        else:
            # train NearestNeighbor on all TF-IDF vectors
            self.knn_model = NearestNeighbors(n_neighbors=5, metric="cosine")
            self.knn_model.fit(self.question_vectors)
            
            # save the trained KNN
            joblib.dump(self.knn_model, knn_path)

    def vectorize_question(self, question):
        return self.vectorizer.transform([question])

    def get_knn_model(self):
        return self.knn_model
    
    def find_similar(self, user_question):
        # convert the user question into TF-IDF vector
        user_vec = self.vectorize_question(user_question)

        # Get nearest neighbors
        distances, indices = self.knn_model.kneighbors(user_vec)

        # Return the actual question texts 
        similar_questions = [self.df["Question"].iloc[i] for i in indices[0]]
        return similar_questions
