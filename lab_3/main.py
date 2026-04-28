
#cd "D:\AK\Лабораторные\2 курс\ППОИС\4 семестр\hangman_game"
 # coverage report -m
import pygame
import sys
import json
import random
import os
import time
from datetime import datetime

# Инициализация pygame
pygame.init()
pygame.mixer.init()

# Настройки окна
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Виселица - Hangman")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (40, 40, 40)
BLUE = (70, 130, 180)
LIGHT_BLUE = (100, 150, 200)
DARK_BLUE = (30, 80, 120)
RED = (255, 80, 80)
GREEN = (80, 255, 80)
YELLOW = (255, 255, 100)
ORANGE = (255, 200, 100)
GOLD = (255, 215, 0)

# Шрифты
try:
    font_title = pygame.font.Font('assets/fonts/arial.ttf', 64)
    font_menu = pygame.font.Font('assets/fonts/arial.ttf', 42)
    font_text = pygame.font.Font('assets/fonts/arial.ttf', 32)
    font_small = pygame.font.Font('assets/fonts/arial.ttf', 24)
    font_large = pygame.font.Font('assets/fonts/arial.ttf', 48)
except:
    font_title = pygame.font.SysFont('arial', 64, bold=True)
    font_menu = pygame.font.SysFont('arial', 42, bold=True)
    font_text = pygame.font.SysFont('arial', 32, bold=True)
    font_small = pygame.font.SysFont('arial', 24, bold=True)
    font_large = pygame.font.SysFont('arial', 48, bold=True)

# Русские слова
RUSSIAN_WORDS = {
    'easy': ['кот', 'дом', 'лес', 'сад', 'мир', 'день', 'ночь', 'хлеб', 'вода', 'огонь'],
    'medium': ['компьютер', 'программа', 'разработка', 'алгоритм', 'интернет', 'технология', 'система'],
    'hard': ['искусственный', 'интеллект', 'нейросеть', 'программирование', 'архитектура']
}


class HangmanGame:
    def __init__(self):
        self.state = 'menu'
        self.selected_option = 0
        self.menu_options = ['НАЧАТЬ ИГРУ', 'РЕЖИМ ВРЕМЕНИ', 'ТАБЛИЦА РЕКОРДОВ', 'СПРАВКА', 'ВЫХОД']

        # Игровые переменные
        self.current_word = ""
        self.display_word = ""
        self.guessed_letters = set()
        self.mistakes = 0
        self.max_mistakes = 6
        self.game_won = False
        self.score = 0
        self.correct_guesses_count = 0

        # Таймер
        self.time_mode = False
        self.time_left = 60
        self.start_time = None
        self.time_bonus = 0

        # Изображения
        self.hangman_images = self.load_hangman_images()
        self.background_image = self.load_background()

        # Таблица рекордов
        self.scores = self.load_scores()

        # Музыка
        self.music_playing = False
        self.current_music_type = None
        self.menu_music = None
        self.game_music = None
        self.sounds = {}
        self.load_music()

        # Выбор слова
        self.select_word()

        # Анимация
        self.animation_frame = 0
        self.pulse_direction = 1
        self.pulse_value = 0

    def draw_text_with_shadow(self, text, font, color, x, y, center=True, right_aligned=False):
        """Отрисовка текста с тенью для лучшей видимости"""
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()

        if center:
            text_rect.center = (x, y)
        elif right_aligned:
            text_rect.right = x
            text_rect.top = y
        else:
            text_rect.topleft = (x, y)

        # Тень
        shadow_surf = font.render(text, True, BLACK)
        shadow_rect = shadow_surf.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        elif right_aligned:
            shadow_rect.right = x + 2
            shadow_rect.top = y + 2
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        screen.blit(shadow_surf, shadow_rect)
        screen.blit(text_surf, text_rect)

    def load_music(self):
        """Загрузка музыки и звуков"""
        try:
            if os.path.exists('assets/sounds/menu_music.mp3'):
                self.menu_music = 'assets/sounds/menu_music.mp3'
                print("Загружена музыка меню")
            elif os.path.exists('assets/sounds/menu_music.ogg'):
                self.menu_music = 'assets/sounds/menu_music.ogg'
                print("Загружена музыка меню")
            else:
                self.menu_music = None

            if os.path.exists('assets/sounds/game_music.mp3'):
                self.game_music = 'assets/sounds/game_music.mp3'
                print("Загружена музыка игры")
            elif os.path.exists('assets/sounds/background.mp3'):
                self.game_music = 'assets/sounds/background.mp3'
                print("Загружена музыка игры")
            else:
                self.game_music = None
        except:
            self.menu_music = None
            self.game_music = None

        self.sounds = {}
        for sound in ['correct', 'wrong', 'win', 'lose', 'click']:
            try:
                path = f'assets/sounds/{sound}.wav'
                if os.path.exists(path):
                    self.sounds[sound] = pygame.mixer.Sound(path)
                    self.sounds[sound].set_volume(0.7)
            except:
                self.sounds[sound] = None

    def start_music(self, music_type='game'):
        try:
            if self.music_playing and self.current_music_type == music_type:
                return
            pygame.mixer.music.stop()
            music_file = self.menu_music if music_type == 'menu' else self.game_music
            if music_file and os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.music_playing = True
                self.current_music_type = music_type
        except:
            pass

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except:
            pass

    def play_sound(self, sound_name):
        try:
            if sound_name in self.sounds and self.sounds[sound_name]:
                self.sounds[sound_name].play()
        except:
            pass

    # В функции load_hangman_images измените масштаб
    def load_hangman_images(self):
        images = []
        for i in range(7):
            try:
                img_path = f'assets/images/hangman_{i}.png'
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)
                    # Увеличим размер до 400x400
                    img = pygame.transform.scale(img, (400, 400))
                    images.append(img)
                else:
                    images.append(self.create_hangman_placeholder(i))
            except:
                images.append(self.create_hangman_placeholder(i))
        return images

    def create_hangman_placeholder(self, stage):
        surf = pygame.Surface((300, 300), pygame.SRCALPHA)
        surf.fill((50, 50, 50, 100))

        pygame.draw.rect(surf, WHITE, (50, 250, 200, 10))
        pygame.draw.rect(surf, WHITE, (120, 50, 10, 200))
        pygame.draw.rect(surf, WHITE, (120, 50, 100, 10))
        pygame.draw.line(surf, WHITE, (220, 50), (220, 80), 5)

        if stage >= 1:
            pygame.draw.circle(surf, WHITE, (220, 110), 25, 2)
        if stage >= 2:
            pygame.draw.line(surf, WHITE, (220, 135), (220, 200), 3)
        if stage >= 3:
            pygame.draw.line(surf, WHITE, (220, 150), (190, 180), 3)
        if stage >= 4:
            pygame.draw.line(surf, WHITE, (220, 150), (250, 180), 3)
        if stage >= 5:
            pygame.draw.line(surf, WHITE, (220, 200), (190, 240), 3)
        if stage >= 6:
            pygame.draw.line(surf, WHITE, (220, 200), (250, 240), 3)

        return surf

    def load_background(self):
        """Загрузка фонового изображения с принудительным растяжением"""
        try:
            # Пробуем загрузить PNG
            if os.path.exists('assets/images/background.png'):
                img = pygame.image.load('assets/images/background.png')
                # Принудительно растягиваем до размера окна
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"Фон загружен! Размер: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                return img
            # Пробуем загрузить JPG
            elif os.path.exists('assets/images/background.jpg'):
                img = pygame.image.load('assets/images/background.jpg')
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"Фон загружен! Размер: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                return img
            else:
                print("Файл фона не найден!")
                return None
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            return None

    def load_scores(self):
        try:
            if os.path.exists('scores.json'):
                with open('scores.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []

    def save_scores(self):
        try:
            with open('scores.json', 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, ensure_ascii=False, indent=2)
        except:
            pass

    def add_score(self, name, score):
        self.scores.append({
            'name': name[:14],
            'score': score,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'word': self.current_word,
            'time_mode': self.time_mode
        })
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()

    def select_word(self):
        all_words = []
        for words in RUSSIAN_WORDS.values():
            all_words.extend(words)
        self.current_word = random.choice(all_words)
        self.display_word = '_' * len(self.current_word)

    def guess_letter(self, letter):
        if letter in self.guessed_letters or self.game_won:
            return
        if self.time_mode and self.time_left <= 0:
            return

        self.guessed_letters.add(letter)

        if letter in self.current_word:
            self.play_sound('correct')
            self.correct_guesses_count += 1
            self.score += 5
            self.update_display_word()
            if '_' not in self.display_word:
                self.game_won = True
                self.end_game()
        else:
            self.play_sound('wrong')
            self.mistakes += 1
            if self.mistakes >= self.max_mistakes:
                self.end_game()

    def update_display_word(self):
        display = []
        for letter in self.current_word:
            if letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append('_')
        self.display_word = ' '.join(display)

    def update_timer(self):
        if self.time_mode and self.start_time and not self.game_won and self.mistakes < self.max_mistakes:
            elapsed = int(time.time() - self.start_time)
            self.time_left = max(0, 60 - elapsed)
            self.time_bonus = self.time_left
            if self.time_left <= 0:
                self.end_game()

    def calculate_score(self):
        base_score = self.correct_guesses_count * 5
        word_bonus = len(self.current_word) * 2
        time_bonus = self.time_bonus if self.time_mode else 0
        total = base_score + word_bonus + time_bonus
        if self.correct_guesses_count == 0:
            total = 0
        return total

    def end_game(self):
        self.game_won = '_' not in self.display_word
        if self.time_mode and self.time_left <= 0 and self.correct_guesses_count == 0:
            self.game_won = False
        if self.mistakes >= self.max_mistakes and not self.game_won:
            self.game_won = False

        final_score = self.calculate_score()

        if self.game_won:
            self.play_sound('win')
        else:
            self.play_sound('lose')
        self.stop_music()

        is_record = False
        if self.game_won:
            if len(self.scores) < 10:
                is_record = True
            elif final_score > self.scores[-1]['score']:
                is_record = True

        if is_record:
            self.show_high_score_dialog(final_score)
        else:
            self.state = 'game_over'

    def show_high_score_dialog(self, score):
        name = ""
        input_active = True
        cursor_visible = True
        cursor_timer = 0

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        self.add_score(name, score)
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        input_active = False
                    elif len(event.unicode) == 1 and event.unicode.isprintable():
                        if len(name) < 14:
                            name += event.unicode

            if self.background_image:
                screen.blit(self.background_image, (0, 0))
            else:
                screen.fill(DARK_GRAY)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            self.draw_text_with_shadow("НОВЫЙ РЕКОРД!", font_large, GOLD, SCREEN_WIDTH // 2, 150)
            self.draw_text_with_shadow(f"Очки: {score}", font_text, YELLOW, SCREEN_WIDTH // 2, 230)
            self.draw_text_with_shadow(f"Слово: {self.current_word}", font_small, GRAY, SCREEN_WIDTH // 2, 280)
            self.draw_text_with_shadow("Введите ваше имя (до 14 символов):", font_text, WHITE, SCREEN_WIDTH // 2, 370)

            name_surface = font_text.render(name, True, WHITE)
            name_rect = name_surface.get_rect(center=(SCREEN_WIDTH // 2, 430))
            screen.blit(name_surface, name_rect)

            char_count = font_small.render(f"{len(name)}/14", True, GRAY if len(name) < 14 else RED)
            char_count_rect = char_count.get_rect(center=(SCREEN_WIDTH // 2 + 150, 430))
            screen.blit(char_count, char_count_rect)

            cursor_timer += 1
            if cursor_timer >= 30:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            if cursor_visible:
                cursor_x = name_rect.right + 5
                cursor_y = name_rect.top
                pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + name_rect.height), 2)

            self.draw_text_with_shadow("ENTER - сохранить, ESC - отмена", font_small, GRAY, SCREEN_WIDTH // 2, 520)
            pygame.display.flip()
            clock.tick(60)

        self.state = 'scoreboard'

    def reset_game(self):
        self.select_word()
        self.guessed_letters.clear()
        self.mistakes = 0
        self.game_won = False
        self.score = 0
        self.correct_guesses_count = 0
        self.time_bonus = 0
        self.update_display_word()

        if self.time_mode:
            self.start_time = time.time()
            self.time_left = 60

        self.start_music('game')

    def draw_button(self, text, x, y, width, height, color, hover=False):
        if hover:
            pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
            pygame.draw.rect(screen, WHITE, (x, y, width, height), 3, border_radius=10)
        else:
            pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
            pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height), 2, border_radius=10)
        self.draw_text_with_shadow(text, font_small, WHITE, x + width // 2, y + height // 2, center=True)

    def draw_menu(self):
        """Отрисовка меню - без перекрытия фона"""
        self.start_music('menu')

        # Просто рисуем фон
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(DARK_GRAY)

        # Убираем overlay - он тоже перекрывает фон!
        # (было: overlay = pygame.Surface...)

        # Всё остальное рисуем прямо поверх фона
        self.animation_frame += 1
        self.pulse_value += self.pulse_direction

        if self.pulse_value >= 55:
            self.pulse_direction = -1
        elif self.pulse_value <= 0:
            self.pulse_direction = 1

        red_value = min(255, max(0, 200 + self.pulse_value))

        self.draw_text_with_shadow("ВИСЕЛИЦА", font_title, (red_value, 200 + self.pulse_value // 2, 0),
                                   SCREEN_WIDTH // 2, 120)
        self.draw_text_with_shadow("Классическая игра в слова", font_small, GRAY, SCREEN_WIDTH // 2, 180)

        menu_x = SCREEN_WIDTH // 2 - 200
        menu_y = 250
        button_height = 50
        button_spacing = 70

        self.menu_buttons = []
        for i, option in enumerate(self.menu_options):
            btn_rect = pygame.Rect(menu_x, menu_y + i * button_spacing, 400, button_height)
            self.menu_buttons.append(btn_rect)
            hover = btn_rect.collidepoint(pygame.mouse.get_pos())
            color = LIGHT_BLUE if i == self.selected_option or hover else DARK_BLUE
            self.draw_button(option, btn_rect.x, btn_rect.y, btn_rect.width, btn_rect.height, color, hover)

        if self.scores:
            best = self.scores[0]
            self.draw_text_with_shadow(f"Лучший: {best['name']} - {best['score']} очков", font_small, GOLD,
                                       SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        pygame.display.flip()

    def draw_playing(self):
        """Отрисовка игрового процесса - без перекрытия фона"""

        # Сначала рисуем ТВОЙ фон на весь экран
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(DARK_GRAY)

        # Убираем чёрную панель! Вместо неё просто рисуем текст поверх фона
        # (без дополнительного прямоугольника)

        # Левый верхний угол - очки и буквы (прямо на фоне)
        self.draw_text_with_shadow(f"Очки: {self.score}", font_text, GOLD, 25, 20, center=False)
        self.draw_text_with_shadow(f"Правильных букв: {self.correct_guesses_count}", font_small, GREEN, 25, 65,
                                   center=False)

        if self.time_mode:
            self.update_timer()
            timer_color = RED if self.time_left < 10 else YELLOW
            self.draw_text_with_shadow(f"Время: {self.time_left}с", font_text, timer_color, SCREEN_WIDTH - 25, 20,
                                       center=False, right_aligned=True)
            if self.time_left > 0:
                self.draw_text_with_shadow(f"Бонус: +{self.time_bonus}", font_small, GREEN, SCREEN_WIDTH - 25, 65,
                                           center=False, right_aligned=True)

        self.draw_text_with_shadow(f"Ошибки: {self.mistakes}/{self.max_mistakes}", font_small, RED, SCREEN_WIDTH - 25,
                                   100, center=False, right_aligned=True)

        # Виселица
        img_idx = min(self.mistakes, len(self.hangman_images) - 1)
        if img_idx < len(self.hangman_images):
            screen.blit(self.hangman_images[img_idx], (80, 200))

        # Слово
        self.draw_text_with_shadow(self.display_word, font_large, YELLOW, SCREEN_WIDTH // 2 - 50, 500)

        if self.guessed_letters:
            letters = sorted(list(self.guessed_letters))
            self.draw_text_with_shadow(f"Использованные буквы: {', '.join(letters)}", font_small, LIGHT_GRAY,
                                       SCREEN_WIDTH // 2 - 50, 560)

        self.draw_text_with_shadow("Нажмите любую букву для отгадывания | ESC - меню", font_small, WHITE,
                                   SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

        if self.game_won:
            self.draw_game_over_message(True)
        elif self.mistakes >= self.max_mistakes:
            self.draw_game_over_message(False)
        elif self.time_mode and self.time_left <= 0:
            self.draw_game_over_message(False)

        pygame.display.flip()

    def draw_game_over_message(self, won):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        if won and self.game_won:
            msg = "ПОБЕДА!"
            color = GREEN
            final_score = self.calculate_score()
            score_text = f"Итоговые очки: {final_score}"
        else:
            msg = f"ПОРАЖЕНИЕ! Загаданное слово: {self.current_word}"
            color = RED
            score_text = f"Ваши очки: {self.calculate_score()}"

        self.draw_text_with_shadow(msg, font_large, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        self.draw_text_with_shadow(score_text, font_text, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.draw_text_with_shadow("Нажмите ESC для продолжения", font_small, WHITE, SCREEN_WIDTH // 2,
                                   SCREEN_HEIGHT // 2 + 50)

    def draw_scoreboard(self):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(DARK_GRAY)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        self.draw_text_with_shadow("ТАБЛИЦА РЕКОРДОВ", font_large, GOLD, SCREEN_WIDTH // 2, 60)

        # Кнопка возврата
        back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        back_hover = back_btn.collidepoint(mouse_pos)
        self.draw_button("НАЗАД", back_btn.x, back_btn.y, back_btn.width, back_btn.height, BLUE, back_hover)
        self.scoreboard_back_button = back_btn

        if not self.scores:
            self.draw_text_with_shadow("Пока нет рекордов!", font_text, WHITE, SCREEN_WIDTH // 2, 300)
        else:
            headers = ["#", "Имя", "Очки", "Слово", "Дата"]
            header_x = [50, 170, 370, 580, 840]

            for i, header in enumerate(headers):
                self.draw_text_with_shadow(header, font_small, YELLOW, header_x[i], 120, center=False)

            y_offset = 160
            for i, record in enumerate(self.scores[:10], 1):
                self.draw_text_with_shadow(str(i), font_small, GOLD if i == 1 else WHITE, header_x[0], y_offset,
                                           center=False)
                name = record['name'][:12]
                if len(record['name']) > 12:
                    name = name[:10] + '…'
                self.draw_text_with_shadow(name, font_small, WHITE, header_x[1], y_offset, center=False)
                self.draw_text_with_shadow(str(record['score']), font_small, GOLD if i == 1 else WHITE, header_x[2],
                                           y_offset, center=False)
                word = record['word'][:14]
                if len(record['word']) > 14:
                    word = word[:12] + '…'
                self.draw_text_with_shadow(word, font_small, LIGHT_GRAY, header_x[3], y_offset, center=False)
                date = record['date'][:10] if len(record['date']) >= 10 else record['date']
                self.draw_text_with_shadow(date, font_small, GRAY, header_x[4], y_offset, center=False)
                y_offset += 35

        pygame.display.flip()

    def draw_help(self):
        """Отрисовка справки"""
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(DARK_GRAY)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        self.draw_text_with_shadow("СПРАВКА", font_large, GOLD, SCREEN_WIDTH // 2, 35)

        help_text = [
            "ПРАВИЛА:",
            "  • Компьютер загадывает случайное русское слово",
            "  • Нажимайте буквы на клавиатуре, чтобы отгадывать",
            "  • За правильную букву +5 очков",
            "  • За неправильную букву очки не снимаются",
            "  • 6 попыток, чтобы отгадать слово",
            "",
            "ПОДСЧЕТ ОЧКОВ:",
            "  • Правильная буква: +5 очков",
            "  • Бонус за длину слова: +2 очка за букву",
            "  • Режим времени: +1 очко за секунду",
            "  • Если не отгадано ни одной буквы - 0 очков",
            "",
            "УПРАВЛЕНИЕ:",
            "  • Буквы А-Я: отгадывание буквы",
            "  • ESC: возврат в меню",
            "  • Мышь: нажатие на кнопки",
            "",
            "РЕЖИМЫ:",
            "  • Обычный режим: классическая игра",
            "  • Режим времени: 60 секунд"
        ]

        y_offset = 80
        for line in help_text:
            if line.startswith("ПРАВИЛА:") or line.startswith("ПОДСЧЕТ ОЧКОВ:") or \
                    line.startswith("УПРАВЛЕНИЕ:") or line.startswith("РЕЖИМЫ:"):
                self.draw_text_with_shadow(line, font_text, YELLOW, 80, y_offset, center=False)
                y_offset += 30
            elif line:
                self.draw_text_with_shadow(line, font_small, WHITE, 100, y_offset, center=False)
                y_offset += 24
            else:
                y_offset += 12
                continue

        # Две пустые строки перед пожеланием
        y_offset += 30

        # Пожелание зелёным цветом
        self.draw_text_with_shadow("Удачи и приятной игры!", font_text, GREEN, SCREEN_WIDTH // 2, y_offset, center=True)
        y_offset += 40

        # Кнопка возврата
        back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 65, 200, 45)
        mouse_pos = pygame.mouse.get_pos()
        back_hover = back_btn.collidepoint(mouse_pos)
        self.draw_button("НАЗАД", back_btn.x, back_btn.y, back_btn.width, back_btn.height, BLUE, back_hover)
        self.help_back_button = back_btn

        pygame.display.flip()

    def draw_game_over(self):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(DARK_GRAY)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        final_score = self.calculate_score()

        if self.game_won:
            self.draw_text_with_shadow("ПОБЕДА!", font_large, GREEN, SCREEN_WIDTH // 2, 150)
            self.draw_text_with_shadow(f"Вы отгадали слово: {self.current_word}", font_text, WHITE, SCREEN_WIDTH // 2,
                                       250)
        else:
            self.draw_text_with_shadow("ИГРА ОКОНЧЕНА", font_large, RED, SCREEN_WIDTH // 2, 150)
            self.draw_text_with_shadow(f"Загаданное слово: {self.current_word}", font_text, WHITE, SCREEN_WIDTH // 2,
                                       250)

        self.draw_text_with_shadow(f"Итоговые очки: {final_score}", font_large, GOLD, SCREEN_WIDTH // 2, 350)

        stats = [
            f"Правильных букв: {self.correct_guesses_count}",
            f"Ошибок: {self.mistakes}",
            f"Длина слова: {len(self.current_word)}"
        ]

        y_offset = 450
        for stat in stats:
            if stat:
                self.draw_text_with_shadow(stat, font_small, GRAY, SCREEN_WIDTH // 2, y_offset)
                y_offset += 35

        # Кнопки
        mouse_pos = pygame.mouse.get_pos()

        play_btn = pygame.Rect(SCREEN_WIDTH // 2 - 210, 560, 200, 50)
        menu_btn = pygame.Rect(SCREEN_WIDTH // 2 + 10, 560, 200, 50)

        play_hover = play_btn.collidepoint(mouse_pos)
        menu_hover = menu_btn.collidepoint(mouse_pos)

        self.draw_button("ИГРАТЬ СНОВА", play_btn.x, play_btn.y, play_btn.width, play_btn.height, GREEN, play_hover)
        self.draw_button("ГЛАВНОЕ МЕНЮ", menu_btn.x, menu_btn.y, menu_btn.width, menu_btn.height, BLUE, menu_hover)

        self.game_over_buttons = [play_btn, menu_btn]

        pygame.display.flip()

    def handle_menu_events(self, event):
        # Обработка мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, btn_rect in enumerate(self.menu_buttons):
                if btn_rect.collidepoint(mouse_pos):
                    self.play_sound('click')
                    if i == 0:
                        self.time_mode = False
                        self.reset_game()
                        self.state = 'playing'
                    elif i == 1:
                        self.time_mode = True
                        self.reset_game()
                        self.state = 'playing'
                    elif i == 2:
                        self.state = 'scoreboard'
                    elif i == 3:
                        self.state = 'help'
                    elif i == 4:
                        return False
                    return True

        # Обработка клавиатуры
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                self.play_sound('click')
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                self.play_sound('click')
            elif event.key == pygame.K_RETURN:
                self.play_sound('click')
                if self.selected_option == 0:
                    self.time_mode = False
                    self.reset_game()
                    self.state = 'playing'
                elif self.selected_option == 1:
                    self.time_mode = True
                    self.reset_game()
                    self.state = 'playing'
                elif self.selected_option == 2:
                    self.state = 'scoreboard'
                elif self.selected_option == 3:
                    self.state = 'help'
                elif self.selected_option == 4:
                    return False
        return True

    def handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = 'menu'
                return True
            elif not self.game_won and self.mistakes < self.max_mistakes:
                letter = event.unicode.lower()
                if letter and ('а' <= letter <= 'я' or letter == 'ё'):
                    self.guess_letter(letter)
        return True

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.state == 'menu':
                    running = self.handle_menu_events(event)
                elif self.state == 'playing':
                    self.handle_playing_events(event)
                elif self.state == 'scoreboard':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if hasattr(self, 'scoreboard_back_button'):
                            if self.scoreboard_back_button.collidepoint(event.pos):
                                self.play_sound('click')
                                self.state = 'menu'
                elif self.state == 'help':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if hasattr(self, 'help_back_button'):
                            if self.help_back_button.collidepoint(event.pos):
                                self.play_sound('click')
                                self.state = 'menu'
                elif self.state == 'game_over':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if hasattr(self, 'game_over_buttons'):
                            if self.game_over_buttons[0].collidepoint(event.pos):
                                self.play_sound('click')
                                self.reset_game()
                                self.state = 'playing'
                            elif self.game_over_buttons[1].collidepoint(event.pos):
                                self.play_sound('click')
                                self.state = 'menu'

            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'playing':
                self.draw_playing()
            elif self.state == 'scoreboard':
                self.draw_scoreboard()
            elif self.state == 'help':
                self.draw_help()
            elif self.state == 'game_over':
                self.draw_game_over()

            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = HangmanGame()
    game.run()