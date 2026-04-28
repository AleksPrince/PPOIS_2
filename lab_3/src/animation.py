import pygame
import math


class Animation:
    @staticmethod
    def create_fade_animation(surface, duration=30):
        frames = []
        for i in range(duration):
            alpha = int(255 * (1 - i / duration))
            frame = surface.copy()
            frame.set_alpha(alpha)
            frames.append(frame)
        return frames

    @staticmethod
    def create_bounce_animation(rect, height=20, duration=30):
        frames = []
        original_y = rect.y

        for i in range(duration):
            offset = height * math.sin(2 * math.pi * i / duration)
            frame_rect = rect.copy()
            frame_rect.y = original_y - offset
            frames.append(frame_rect)

        return frames