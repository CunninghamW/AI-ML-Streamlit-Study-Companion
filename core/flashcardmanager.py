import pandas as pd
import random
from flashcards import Flashcard


class FlashcardManager:
    def __init__(self, csv_path="CSV/SoftwareQuestions_preprocessed.csv"):
        self.csv_path = csv_path
        self.flashcards = []
        self.flashcard_map = {}
        self.df = pd.read_csv(csv_path, usecols=["Question Number", "Question", "Answer", "Category"])
        self.load_flashcards()
        
        
    # O(n)
    def load_flashcards(self):
        """
        Convert the DataFrame into flashcard objects. 
        
        """
        
        # loop through the df and pull out the columns we need
        for row in self.df.itertuples(index=False): # o(n)
            # create flashcard object from the raw data
            card = Flashcard( 
                id=row._1,
                question=row.Question,
                answer=row.Answer,
                category=row.Category
            )
            # store each card object into the self.flashcard list
            self.flashcards.append(card)
            # store the card ids into a dict/map for easy lookup with id o(1)
            self.flashcard_map[card.id] = card

    # O(1)
    def get_flashcard_by_id(self, id):
        return self.flashcard_map.get(id, None)

    # O(1)
    def get_random_flashcard(self):
        return random.choice(self.flashcards)

    # O(1)
    def get_flashcards_by_category(self, category):
        matching_category = []
        for card in self.flashcards:
            if card.category == category:
                matching_category.append(card)

        return matching_category

    # O(n)
    def all_categories(self):
        all_categories = set()
        for card in self.flashcards:
            all_categories.add(card.category)
        return all_categories