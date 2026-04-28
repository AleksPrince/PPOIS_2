import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем все тесты
from tests.test_game import *
from tests.test_game_core import *

if __name__ == '__main__':
    unittest.main()