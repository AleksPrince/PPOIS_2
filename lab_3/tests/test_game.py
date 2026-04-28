import unittest
import sys
import os
import json
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.word_manager import WordManager
from src.player import Player
from src.scoreboard import Scoreboard
from src.timer import GameTimer


class TestWordManager(unittest.TestCase):
    def setUp(self):
        # Создаём временный JSON файл
        self.test_data = {
            "easy": ["кот", "дом"],
            "medium": ["компьютер"],
            "hard": ["искусственный"]
        }
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        self.wm = WordManager(self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_load_words(self):
        """Проверка загрузки слов"""
        self.assertEqual(len(self.wm.words), 3)

    def test_get_random_word_easy(self):
        """Получение лёгкого слова"""
        word = self.wm.get_random_word('easy')
        self.assertIn(word, ['кот', 'дом'])

    def test_get_random_word_medium(self):
        """Получение среднего слова"""
        word = self.wm.get_random_word('medium')
        self.assertEqual(word, 'компьютер')

    def test_get_random_word_default(self):
        """Получение слова без параметра"""
        word = self.wm.get_random_word()
        self.assertIsNotNone(word)

    def test_get_random_word_invalid(self):
        """Неверная сложность"""
        word = self.wm.get_random_word('invalid')
        self.assertIsNotNone(word)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Тестер")

    def test_initialization(self):
        """Проверка инициализации"""
        self.assertEqual(self.player.name, "Тестер")
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.games_played, 0)
        self.assertEqual(self.player.games_won, 0)

    def test_win_game(self):
        """Победа в игре"""
        self.player.win_game(100)
        self.assertEqual(self.player.games_played, 1)
        self.assertEqual(self.player.games_won, 1)
        self.assertEqual(self.player.score, 100)

    def test_lose_game(self):
        """Поражение в игре"""
        self.player.lose_game()
        self.assertEqual(self.player.games_played, 1)
        self.assertEqual(self.player.games_won, 0)

    def test_multiple_games(self):
        """Несколько игр"""
        self.player.win_game(50)
        self.player.win_game(30)
        self.player.lose_game()
        self.assertEqual(self.player.games_played, 3)
        self.assertEqual(self.player.games_won, 2)
        self.assertEqual(self.player.score, 80)


class TestScoreboard(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.close()
        self.sb = Scoreboard(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_score(self):
        """Добавление рекорда"""
        result = self.sb.add_score("Игрок", 100, 5)
        self.assertTrue(result)
        self.assertEqual(len(self.sb.scores), 1)

    def test_is_high_score_empty(self):
        """Проверка рекорда в пустой таблице"""
        self.assertTrue(self.sb.is_high_score(50))

    def test_is_high_score_true(self):
        """Проверка рекорда - да"""
        for i in range(5):
            self.sb.add_score(f"P{i}", i * 10, 5)
        self.assertTrue(self.sb.is_high_score(100))

    def test_is_high_score_false(self):
        """Проверка рекорда - нет"""
        for i in range(10):
            self.sb.add_score(f"P{i}", 100 - i, 5)
        self.assertFalse(self.sb.is_high_score(1))

    def test_top_scores_limit(self):
        """Ограничение на 10 рекордов"""
        for i in range(20):
            self.sb.add_score(f"P{i}", i, 5)
        self.assertEqual(len(self.sb.scores), 10)

    def test_scores_sorted(self):
        """Проверка сортировки"""
        self.sb.add_score("A", 50, 5)
        self.sb.add_score("B", 100, 5)
        self.sb.add_score("C", 75, 5)
        self.assertEqual(self.sb.scores[0]['score'], 100)
        self.assertEqual(self.sb.scores[1]['score'], 75)
        self.assertEqual(self.sb.scores[2]['score'], 50)


class TestGameTimer(unittest.TestCase):
    def setUp(self):
        self.timer = GameTimer(60)

    def test_initialization(self):
        """Инициализация"""
        self.assertEqual(self.timer.time_limit, 60)
        self.assertTrue(self.timer.enabled)

    def test_start(self):
        """Запуск"""
        self.timer.start()
        self.assertIsNotNone(self.timer.start_time)

    def test_get_remaining_before_start(self):
        """Остаток до старта"""
        self.assertEqual(self.timer.get_remaining(), 60)

    def test_reset(self):
        """Сброс"""
        self.timer.start()
        self.timer.reset()
        self.assertIsNone(self.timer.start_time)

    def test_time_left_decreases(self):
        """Время уменьшается"""
        self.timer.start()
        import time
        time.sleep(0.5)
        remaining = self.timer.get_remaining()
        self.assertLess(remaining, 60)


if __name__ == '__main__':
    unittest.main()