class Flashcard:
    def __init__(self, id, question, answer, category):
        self.id = id
        self.question = question
        self.answer = answer
        self.category = category

    def __repr__(self):
        return f"Flashcard({self.id}, {self.category}, {self.question})"
