import json
import random
import os


class WordManager:
    def __init__(self, filename='config/words.json'):
        self.filename = filename
        self.words = self.load_words()
        self.current_difficulty = 'medium'

    def load_words(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "easy": ["cat", "dog", "sun", "car", "book"],
                "medium": ["python", "java", "ruby", "swift", "kotlin"],
                "hard": ["javascript", "typescript", "crocodile", "elephant"]
            }

    def get_random_word(self, difficulty=None):
        if difficulty is None:
            difficulty = self.current_difficulty

        if difficulty in self.words and self.words[difficulty]:
            return random.choice(self.words[difficulty]).lower()
        else:
            all_words = []
            for word_list in self.words.values():
                all_words.extend(word_list)
            return random.choice(all_words).lower() if all_words else "python"