import unittest
import sys
import os
import json
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем только классы, которые не зависят от Pygame
from src.word_manager import WordManager
from src.player import Player
from src.scoreboard import Scoreboard
from src.timer import GameTimer


class TestWordManagerWorking(unittest.TestCase):
    def setUp(self):
        # Создаём временный JSON файл
        self.test_words = {
            "easy": ["кот", "дом", "лес"],
            "medium": ["компьютер", "программа"],
            "hard": ["искусственный"]
        }
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        json.dump(self.test_words, self.temp_file, ensure_ascii=False)
        self.temp_file.close()
        self.wm = WordManager(self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_words_loaded(self):
        """Проверка загрузки слов"""
        self.assertEqual(len(self.wm.words['easy']), 3)
        self.assertEqual(len(self.wm.words['medium']), 2)
        self.assertEqual(len(self.wm.words['hard']), 1)

    def test_get_random_word(self):
        """Получение случайного слова"""
        word = self.wm.get_random_word('easy')
        self.assertIn(word, ['кот', 'дом', 'лес'])

    def test_get_random_word_medium(self):
        word = self.wm.get_random_word('medium')
        self.assertIn(word, ['компьютер', 'программа'])

    def test_get_random_word_hard(self):
        word = self.wm.get_random_word('hard')
        self.assertEqual(word, 'искусственный')

    def test_get_random_word_no_difficulty(self):
        word = self.wm.get_random_word()
        self.assertIsNotNone(word)


class TestPlayerWorking(unittest.TestCase):
    def setUp(self):
        self.player = Player("Тестер")

    def test_name(self):
        self.assertEqual(self.player.name, "Тестер")

    def test_initial_score(self):
        self.assertEqual(self.player.score, 0)

    def test_initial_games_played(self):
        self.assertEqual(self.player.games_played, 0)

    def test_initial_games_won(self):
        self.assertEqual(self.player.games_won, 0)

    def test_win_game(self):
        self.player.win_game(100)
        self.assertEqual(self.player.games_played, 1)
        self.assertEqual(self.player.games_won, 1)
        self.assertEqual(self.player.score, 100)

    def test_lose_game(self):
        self.player.lose_game()
        self.assertEqual(self.player.games_played, 1)
        self.assertEqual(self.player.games_won, 0)

    def test_multiple_wins(self):
        self.player.win_game(50)
        self.player.win_game(30)
        self.assertEqual(self.player.games_played, 2)
        self.assertEqual(self.player.games_won, 2)
        self.assertEqual(self.player.score, 80)


class TestScoreboardWorking(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.close()
        self.sb = Scoreboard(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_score(self):
        result = self.sb.add_score("Игрок", 100, 5)
        self.assertTrue(result)
        self.assertEqual(len(self.sb.scores), 1)

    def test_add_multiple_scores(self):
        self.sb.add_score("A", 100, 5)
        self.sb.add_score("B", 50, 5)
        self.assertEqual(len(self.sb.scores), 2)

    def test_scores_are_sorted(self):
        self.sb.add_score("A", 50, 5)
        self.sb.add_score("B", 100, 5)
        self.sb.add_score("C", 75, 5)
        self.assertEqual(self.sb.scores[0]['score'], 100)
        self.assertEqual(self.sb.scores[1]['score'], 75)
        self.assertEqual(self.sb.scores[2]['score'], 50)

    def test_is_high_score_empty(self):
        self.assertTrue(self.sb.is_high_score(50))

    def test_is_high_score_true(self):
        for i in range(5):
            self.sb.add_score(f"P{i}", i * 10, 5)
        self.assertTrue(self.sb.is_high_score(100))

    def test_is_high_score_false(self):
        for i in range(10):
            self.sb.add_score(f"P{i}", 100 - i, 5)
        self.assertFalse(self.sb.is_high_score(1))

    def test_top_scores_limit(self):
        for i in range(20):
            self.sb.add_score(f"P{i}", i, 5)
        self.assertEqual(len(self.sb.scores), 10)


class TestTimerWorking(unittest.TestCase):
    def setUp(self):
        self.timer = GameTimer(60)

    def test_initial_time_limit(self):
        self.assertEqual(self.timer.time_limit, 60)

    def test_initial_enabled(self):
        self.assertTrue(self.timer.enabled)

    def test_start(self):
        self.timer.start()
        self.assertIsNotNone(self.timer.start_time)

    def test_get_remaining_before_start(self):
        self.assertEqual(self.timer.get_remaining(), 60)

    def test_reset(self):
        self.timer.start()
        self.timer.reset()
        self.assertIsNone(self.timer.start_time)

    def test_get_remaining_after_start(self):
        self.timer.start()
        import time
        time.sleep(0.1)
        remaining = self.timer.get_remaining()
        self.assertLess(remaining, 60)


if __name__ == '__main__':
    unittest.main()