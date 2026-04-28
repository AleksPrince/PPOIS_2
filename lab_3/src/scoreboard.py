import json
import os
from datetime import datetime


class Scoreboard:
    def __init__(self, filename='scores.json'):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_scores(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.scores, f, indent=4, ensure_ascii=False)

    def add_score(self, name, score, word_length):
        for record in self.scores:
            if record['name'] == name and record['score'] == score:
                return False

        self.scores.append({
            'name': name,
            'score': score,
            'word_length': word_length,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]

        self.save_scores()
        return True

    def is_high_score(self, score):
        if len(self.scores) < 10:
            return True
        min_score = min(s['score'] for s in self.scores)
        return score > min_score

    def get_top_scores(self, n=10):
        return self.scores[:n]