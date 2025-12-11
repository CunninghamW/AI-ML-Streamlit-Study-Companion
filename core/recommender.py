


class Recommender:
    def __init__(self, model_loader: ModelLoader):
        self.model_loader = model_loader


    def get_similar_questions(self, question_text, top_k=5):
        """
        Docstring for get_similar_questions
        
        Return the top_k questions most similar to the given question_text.
        uses the TF-IDF vectorizer and the KNN model from ModelLoader.
        """
        
        # ask the model loader to get similar questions
        all_similar = self.model_loader.find_similar(question_text)

        # return only the top_k results

        return all_similar[:top_k]