import pygame
from .states import GameState


class Menu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.selected_option = 0
        self.options = [
            "START GAME",
            "SCOREBOARD",
            "HELP",
            "QUIT"
        ]
        self.font = pygame.font.Font(None, 48)
        self.next_state = GameState.MENU

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = GameState.QUIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def select_option(self):
        if self.selected_option == 0:
            self.next_state = GameState.PLAYING
        elif self.selected_option == 1:
            self.next_state = GameState.SCOREBOARD
        elif self.selected_option == 2:
            self.next_state = GameState.HELP
        elif self.selected_option == 3:
            self.next_state = GameState.QUIT

    def draw(self):
        self.screen.fill(self.settings['colors']['background'])

        for i, option in enumerate(self.options):
            color = self.settings['colors']['button_hover'] if i == self.selected_option else self.settings['colors'][
                'button']
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, 200 + i * 60))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def get_next_state(self):
        return self.next_state