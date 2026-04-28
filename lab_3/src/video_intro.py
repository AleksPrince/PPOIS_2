import pygame
import imageio.v3 as iio
import numpy as np
import os


class VideoIntro:
    def __init__(self, screen, video_path='assets/videos/intro.mp4'):
        self.screen = screen
        self.video_path = video_path
        self.frames = []
        self.current_frame = 0
        self.playing = False
        self.fps = 30
        self.clock = pygame.time.Clock()

    def load_video(self):
        try:
            if not os.path.exists(self.video_path):
                print(f"Video file not found: {self.video_path}")
                return False

            print(f"Loading video from: {self.video_path}")
            reader = iio.imiter(self.video_path, plugin="pyav")

            props = iio.improps(self.video_path)
            self.fps = int(props.get('fps', 30))

            frame_count = 0
            for frame in reader:
                if frame_count >= 300:
                    break

                frame_surface = self.numpy_to_surface(frame)
                frame_surface = pygame.transform.scale(
                    frame_surface,
                    self.screen.get_size()
                )

                self.frames.append(frame_surface)
                frame_count += 1

            print(f"Loaded {len(self.frames)} frames from video")
            return len(self.frames) > 0

        except Exception as e:
            print(f"Error loading video: {e}")
            return False

    def numpy_to_surface(self, frame):
        if len(frame.shape) == 3:
            if frame.shape[2] == 3:
                h, w, _ = frame.shape
                rgba_frame = np.zeros((h, w, 4), dtype=np.uint8)
                rgba_frame[:, :, :3] = frame
                rgba_frame[:, :, 3] = 255
                frame = rgba_frame

        surface = pygame.Surface((frame.shape[1], frame.shape[0]), pygame.SRCALPHA)
        pygame.pixelcopy.array_to_surface(surface, frame)

        return surface

    def play(self):
        if not self.frames:
            if not self.load_video():
                return False

        self.playing = True
        self.current_frame = 0

        while self.playing and self.current_frame < len(self.frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.playing = False
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False

            self.screen.blit(self.frames[self.current_frame], (0, 0))
            pygame.display.flip()

            self.current_frame += 1
            self.clock.tick(self.fps)

        return True

    def play_loop(self):
        if not self.frames:
            if not self.load_video():
                return False

        self.playing = True
        self.current_frame = 0

        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.playing = False
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False

            self.screen.blit(self.frames[self.current_frame], (0, 0))
            pygame.display.flip()

            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.current_frame = 0

            self.clock.tick(self.fps)

        return True