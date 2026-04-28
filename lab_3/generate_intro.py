import pygame
import numpy as np
import imageio.v3 as iio
import os


def generate_intro_video(output_path='assets/videos/intro.mp4', duration=5, fps=30):
    pygame.init()

    width, height = 800, 600
    total_frames = duration * fps
    frames = []

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)

    try:
        font_large = pygame.font.Font('assets/fonts/arcade.ttf', 72)
        font_medium = pygame.font.Font('assets/fonts/arcade.ttf', 48)
        font_small = pygame.font.Font('assets/fonts/arcade.ttf', 24)
    except:
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)

    print(f"Generating {total_frames} frames...")

    for i in range(total_frames):
        surface = pygame.Surface((width, height))
        t = i / total_frames

        if t < 0.3:
            alpha = int(255 * (t / 0.3))
        else:
            alpha = 255

        surface.fill(BLACK)

        if t > 0.2:
            hangman_y = int(200 * min(1, (t - 0.2) / 0.3))
            pygame.draw.line(surface, WHITE, (300, 450), (300, 450 - hangman_y), 3)
            pygame.draw.line(surface, WHITE, (300, 450 - hangman_y), (350, 450 - hangman_y), 3)
            pygame.draw.line(surface, WHITE, (325, 450 - hangman_y), (325, 420), 3)

        if t > 0.1:
            title = font_large.render("HANGMAN", True, YELLOW)
            title_rect = title.get_rect(center=(400, 150))
            if t < 0.3:
                title.set_alpha(int(alpha))
            surface.blit(title, title_rect)

        if t > 0.2:
            subtitle = font_medium.render("The Classic Word Game", True, WHITE)
            subtitle_rect = subtitle.get_rect(center=(400, 220))
            surface.blit(subtitle, subtitle_rect)

        if t > 0.6:
            lab_info = font_small.render("Laboratory Work #3 - Hangman Game", True, (150, 150, 150))
            lab_rect = lab_info.get_rect(center=(400, 500))
            surface.blit(lab_info, lab_rect)

        if t > 0.8:
            pulse = 0.5 + 0.5 * np.sin(2 * np.pi * i / fps)
            instruction = font_small.render("Press SPACE or ENTER to start", True, RED)
            instruction.set_alpha(int(255 * pulse))
            instruction_rect = instruction.get_rect(center=(400, 550))
            surface.blit(instruction, instruction_rect)

        frame = pygame.surfarray.array3d(surface)
        frame = np.transpose(frame, (1, 0, 2))
        frames.append(frame)

        if i % 30 == 0:
            print(f"Frame {i}/{total_frames}")

    print("Saving video...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    iio.imwrite(output_path, frames, fps=fps, codec='libx264')
    print(f"Video saved to {output_path}")


if __name__ == "__main__":
    generate_intro_video()