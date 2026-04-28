import pygame
import json
import sys
from .states import GameState
from .word_manager import WordManager
from .scoreboard import Scoreboard
from .timer import GameTimer
from .player import Player


class Game:
    def __init__(self):
        self.load_settings()
        self.init_pygame()
        self.init_components()
        self.load_assets()
        self.game_state = GameState.MENU
        self.running = True

    def load_settings(self):
        with open('config/settings.json', 'r', encoding='utf-8') as f:
            self.settings = json.load(f)

    def init_pygame(self):
        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode(
                (self.settings['screen']['width'],
                 self.settings['screen']['height'])
            )
        self.clock = pygame.time.Clock()

    def init_components(self):
        self.word_manager = WordManager()
        self.scoreboard = Scoreboard()
        self.timer = GameTimer(self.settings['game']['time_limit_mode'])
        self.player = Player()
        self.mistakes = 0
        self.guessed_letters = set()
        self.current_word = ""
        self.display_word = ""

    def load_assets(self):
        pygame.mixer.init()
        self.sounds = {}

        sound_files = {
            'background': 'assets/sounds/background.mp3',
            'correct': 'assets/sounds/correct.mp3',
            'wrong': 'assets/sounds/wrong.mp3',
            'game_over': 'assets/sounds/game_over.mp3'
        }

        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(self.settings['sound']['effects_volume'])
            except:
                print(f"Could not load sound: {path}")
                self.sounds[name] = None

        if self.sounds.get('background'):
            self.sounds['background'].set_volume(self.settings['sound']['background_volume'])
            self.sounds['background'].play(-1)

        try:
            self.font = pygame.font.Font('assets/fonts/arcade.ttf', 36)
            self.small_font = pygame.font.Font('assets/fonts/arcade.ttf', 24)
        except:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.QUIT
            elif event.type == pygame.KEYDOWN:
                self.handle_keypress(event)

    def handle_keypress(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game_state = GameState.MENU
        elif event.unicode.isalpha() and len(event.unicode) == 1:
            letter = event.unicode.lower()
            self.guess_letter(letter)

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)

        if letter in self.current_word:
            if self.sounds.get('correct'):
                self.sounds['correct'].play()
            self.update_display_word()

            if '_' not in self.display_word:
                self.game_over(True)
        else:
            if self.sounds.get('wrong'):
                self.sounds['wrong'].play()
            self.mistakes += 1

            if self.mistakes >= self.settings['game']['max_mistakes']:
                self.game_over(False)

    def update_display_word(self):
        self.display_word = ''.join([
            letter if letter in self.guessed_letters else '_'
            for letter in self.current_word
        ])

    def update(self):
        if self.timer.enabled and self.timer.get_remaining() <= 0:
            self.game_over(False)

    def game_over(self, won):
        if self.sounds.get('background'):
            self.sounds['background'].stop()

        if won:
            score = self.calculate_score()
            if self.scoreboard.is_high_score(score):
                self.show_high_score_dialog(score)
        else:
            if self.sounds.get('game_over'):
                self.sounds['game_over'].play()

        self.game_state = GameState.MENU
        self.reset_game()

    def reset_game(self):
        self.mistakes = 0
        self.guessed_letters = set()
        self.current_word = self.word_manager.get_random_word()
        self.display_word = '_' * len(self.current_word)
        self.timer.reset()
        if self.sounds.get('background'):
            self.sounds['background'].play(-1)

    def calculate_score(self):
        base_score = len(self.current_word) * 100
        time_bonus = max(0, self.timer.get_remaining()) * 10
        mistake_penalty = self.mistakes * 20
        return base_score + time_bonus - mistake_penalty

    def draw(self):
        self.screen.fill(self.settings['colors']['background'])
        self.draw_hangman()
        self.draw_word()
        self.draw_used_letters()
        self.draw_mistakes()
        if self.timer.enabled:
            self.draw_timer()
        pygame.display.flip()

    def draw_word(self):
        word_surface = self.font.render(
            ' '.join(self.display_word),
            True,
            self.settings['colors']['text']
        )
        word_rect = word_surface.get_rect(center=(400, 300))
        self.screen.blit(word_surface, word_rect)

    def draw_hangman(self):
        with open('config/hangman_stages.json', 'r', encoding='utf-8') as f:
            stages = json.load(f)['stages']

        stage = stages[min(self.mistakes, len(stages) - 1)]
        font = pygame.font.Font(None, 20)

        y_offset = 50
        for line in stage.split('\n'):
            text = font.render(line, True, self.settings['colors']['text'])
            self.screen.blit(text, (50, y_offset))
            y_offset += 20

    def draw_used_letters(self):
        letters = sorted(list(self.guessed_letters))
        letter_string = ' '.join(letters)
        text = self.small_font.render(
            f"Used letters: {letter_string}",
            True,
            self.settings['colors']['text']
        )
        self.screen.blit(text, (400, 400))

    def draw_mistakes(self):
        text = self.small_font.render(
            f"Mistakes: {self.mistakes}/{self.settings['game']['max_mistakes']}",
            True,
            self.settings['colors']['wrong'] if self.mistakes > 0 else self.settings['colors']['text']
        )
        self.screen.blit(text, (50, 450))

    def draw_timer(self):
        time_left = self.timer.get_remaining()
        color = (255, 0, 0) if time_left < 10 else self.settings['colors']['text']
        text = self.font.render(
            f"Time: {time_left}s",
            True,
            color
        )
        self.screen.blit(text, (650, 50))

    def show_scoreboard(self):
        self.screen.fill(self.settings['colors']['background'])

        title = self.font.render("TABLE OF RECORDS", True, self.settings['colors']['text'])
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)

        scores = self.scoreboard.get_top_scores()

        if not scores:
            text = self.small_font.render(
                "No records yet!",
                True,
                self.settings['colors']['text']
            )
            text_rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, text_rect)
        else:
            y_offset = 120
            for i, record in enumerate(scores, 1):
                record_text = f"{i}. {record['name']}: {record['score']} pts ({record['word_length']} letters)"
                text = self.small_font.render(record_text, True, self.settings['colors']['text'])
                self.screen.blit(text, (300, y_offset))
                y_offset += 30

        exit_text = self.small_font.render(
            "Press ESC to return to menu",
            True,
            self.settings['colors']['text']
        )
        self.screen.blit(exit_text, (250, 500))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.QUIT
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.MENU
                        waiting = False

    def show_help(self):
        self.screen.fill(self.settings['colors']['background'])

        title = self.font.render("HELP - HOW TO PLAY", True, self.settings['colors']['text'])
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)

        help_lines = [
            "HANGMAN GAME RULES:",
            "",
            "1. A random word is selected",
            "2. Guess letters one by one",
            "3. For each wrong guess, part of the hangman appears",
            "4. You have 6 mistakes maximum",
            "5. If you guess all letters - you win!",
            "",
            "TIME MODE:",
            "- You have 60 seconds to guess the word",
            "- Time bonus adds to your score",
            "",
            "CONTROLS:",
            "- Type letters on keyboard to guess",
            "- ESC - return to menu",
            "",
            "Press ESC to return"
        ]

        y_offset = 100
        for line in help_lines:
            if line.startswith("HANGMAN") or line.startswith("TIME") or line.startswith("CONTROLS"):
                text = pygame.font.Font(None, 28).render(line, True, (255, 255, 0))
            else:
                text = self.small_font.render(line, True, self.settings['colors']['text'])
            self.screen.blit(text, (200, y_offset))
            y_offset += 25

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.QUIT
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.MENU
                        waiting = False

    def show_high_score_dialog(self, score):
        self.screen.fill(self.settings['colors']['background'])

        congrats = self.font.render("CONGRATULATIONS!", True, (255, 215, 0))
        congrats_rect = congrats.get_rect(center=(400, 150))
        self.screen.blit(congrats, congrats_rect)

        score_text = pygame.font.Font(None, 36).render(
            f"New record: {score} points!",
            True,
            self.settings['colors']['text']
        )
        score_rect = score_text.get_rect(center=(400, 220))
        self.screen.blit(score_text, score_rect)

        prompt = pygame.font.Font(None, 32).render(
            "Enter your name:",
            True,
            self.settings['colors']['text']
        )
        prompt_rect = prompt.get_rect(center=(400, 300))
        self.screen.blit(prompt, prompt_rect)

        name = ""
        input_active = True
        cursor_visible = True
        cursor_timer = 0

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        self.scoreboard.add_score(name, score, len(self.current_word))
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        input_active = False
                    elif len(event.unicode) == 1 and event.unicode.isprintable():
                        if len(name) < 15:
                            name += event.unicode

            cursor_timer += 1
            if cursor_timer >= 30:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            self.screen.fill(self.settings['colors']['background'])
            self.screen.blit(congrats, congrats_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(prompt, prompt_rect)

            name_surface = pygame.font.Font(None, 36).render(name, True, (255, 255, 255))
            name_rect = name_surface.get_rect(center=(400, 350))
            self.screen.blit(name_surface, name_rect)

            if cursor_visible:
                cursor_x = name_rect.right + 5
                cursor_y = name_rect.top
                pygame.draw.line(
                    self.screen,
                    (255, 255, 255),
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + name_rect.height),
                    2
                )

            instr = pygame.font.Font(None, 24).render(
                "Press ENTER to save, ESC to cancel",
                True,
                (150, 150, 150)
            )
            instr_rect = instr.get_rect(center=(400, 450))
            self.screen.blit(instr, instr_rect)

            pygame.display.flip()