import pygame, sys
from game import Game
pygame.init()
dark_blue = (44,44,127)
screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Pygame Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)  # Set a timer to trigger every second


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()  # Move the current block left
            if event.key == pygame.K_RIGHT:
                game.move_right()
            if event.key == pygame.K_DOWN:
                game.move_down()
            if event.key == pygame.K_UP:
                game.rotate()
        if event.type == GAME_UPDATE:
            game.move_down()

    screen.fill(dark_blue)  # Fill the screen with dark blue color
    game.draw(screen)  # Draw the game elements

    pygame.display.update() 
    clock.tick(60)  # Limit the frame rate to 60 FPS