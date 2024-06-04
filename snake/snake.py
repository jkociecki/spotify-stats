import pygame
import random
import os
from PIL import Image
import numpy as np
import shutil

# Ustawienia gry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_BLOCK = 35
SNAKE_SPEED = 15

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)


def get_dominant_color(image_path):
    """
    Function to get the dominant color of an image.
    :param image_path: Path to the image
    :return: Dominant color as a tuple (R, G, B)
    """
    img = Image.open(image_path)
    img = img.resize((SNAKE_BLOCK, SNAKE_BLOCK))
    np_img = np.array(img)
    pixels = np_img.reshape(-1, 3)
    dominant_color = np.mean(pixels, axis=0)
    return tuple(dominant_color.astype(int))


def draw_snake(snake_list, snake_covers, screen):
    """
    Draw the snake on the screen.
    :param snake_list: List of snake segments
    :param snake_covers: List of covers for the snake segments
    :param screen: Pygame screen object
    """
    for idx, (x, y) in enumerate(snake_list):
        cover = snake_covers[idx] if idx < len(snake_covers) else BLACK
        if cover == BLACK:
            pygame.draw.rect(screen, BLACK, [x, y, SNAKE_BLOCK, SNAKE_BLOCK])
        else:
            screen.blit(cover, (x, y))


def load_images_and_sounds(num_tracks):
    """
     Load images and sounds for the tracks.
     :param num_tracks: Number of tracks
     :return: List of track data (cover, preview path, dominant color)
     """
    data = []
    for i in range(num_tracks):
        cover_path = f'covers/{i}.jpg'
        preview_path = f'previews/{i}.mp3'
        try:
            if not os.path.exists(cover_path):
                raise FileNotFoundError(f"Cover image not found: {cover_path}")
            if not os.path.exists(preview_path):
                raise FileNotFoundError(f"Preview MP3 not found: {preview_path}")
            cover = pygame.image.load(cover_path)
            cover = pygame.transform.scale(cover,
                                           (SNAKE_BLOCK, SNAKE_BLOCK))  # Skalowanie okładki do rozmiaru kostki węża
            dominant_color = get_dominant_color(cover_path)
            data.append((cover, preview_path, dominant_color))
        except Exception as e:
            print(f"Error loading track {i}: {e}")
            continue
    return data


def game(tracks_data):
    """
    Main game function.
    :param tracks_data: List of track data (cover, preview path, dominant color)
    """

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Eat This Playlist')

    clock = pygame.time.Clock()

    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 2) % SNAKE_BLOCK
    y1 = SCREEN_HEIGHT // 2 - (SCREEN_HEIGHT // 2) % SNAKE_BLOCK

    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_covers = []
    length_of_snake = 1

    foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
    foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK

    # tracks  queue
    random.shuffle(tracks_data)
    current_track_index = 0

    def load_track(index):
        global current_cover, current_preview_url, current_bg_color
        current_cover, current_preview_url, current_bg_color = tracks_data[index]
        try:
            pygame.mixer.music.load(current_preview_url)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error loading track {current_preview_url}: {e}")
            next_track()

    if len(tracks_data) > 0:
        load_track(current_track_index)

    def next_track():
        nonlocal current_track_index
        if current_track_index < len(tracks_data) - 1:
            current_track_index += 1
        else:
            current_track_index = 0
        load_track(current_track_index)

    while not game_over:
        while game_close:
            screen.fill(WHITE)
            font_style = pygame.font.SysFont(None, 50)
            message = font_style.render("You Lost! Press Q-Quit or C-Play Again", True, RED)
            screen.blit(message, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game(tracks_data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(current_bg_color)

        # Rysowanie jedzenia (okładki albumu)
        screen.blit(current_cover, (foodx, foody))

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_list, snake_covers, screen)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            length_of_snake += 1
            snake_covers.append(current_cover)  # Dodawanie zjedzonej okładki do listy
            next_track()

        clock.tick(SNAKE_SPEED)
    pygame.quit()
    pygame.mixer.quit()
    shutil.rmtree('covers', ignore_errors=True)
    shutil.rmtree('previews', ignore_errors=True)


def run():
    num_tracks = len([name for name in os.listdir('covers') if os.path.isfile(os.path.join('covers', name))])
    tracks_data = load_images_and_sounds(num_tracks)

    if len(tracks_data) > 0:
        # Uruchomienie gry
        game(tracks_data)
        pygame.mixer.quit()
        pygame.quit()
    else:
        print("No tracks loaded. Please check your files in the 'covers' and 'previews' directories.")
