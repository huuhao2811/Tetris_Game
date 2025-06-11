import pygame, sys
from game import Game
from colors import Colors
pygame.init()
title_font = pygame.font.SysFont(None, 53)
score_surface = title_font.render("Score", True, (255, 255, 255))
next_surface = title_font.render("Next", True, (255, 255, 255))
game_over_surface = title_font.render("GAME OVER", True, (255, 0, 0))
score_rect = pygame.Rect(435, 80, 200, 80)  # Position for the score label
next_rect = pygame.Rect(435, 260, 200, 200)  # Position for the next piece label
dark_blue = (44,44,127)
screen = pygame.display.set_mode((660, 830))    
pygame.display.set_caption("Pygame Tetris")

clock = pygame.time.Clock()

game = Game()
AI_mode = True
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 20)  # Set a timer to trigger every second


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False 
                game.reset()
            if not AI_mode:
                if event.key == pygame.K_LEFT and not game.game_over:
                    game.move_left()  # Move the current block left
                if event.key == pygame.K_RIGHT and not game.game_over:
                    game.move_right()
                if event.key == pygame.K_DOWN and not game.game_over:
                    game.move_down()
                    game.update_score(0, 1)  
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()
        if event.type == GAME_UPDATE and not game.game_over:
            if AI_mode:
                col, rotation = game.get_best_move()
                game.apply_best_move(col, rotation)

    score_value_surface = title_font.render(str(game.score), True, (255, 255, 255))
    screen.fill(dark_blue)  # Fill the screen with dark blue color
    screen.blit(score_surface, (485, 20, 50, 50))  # Draw the score label
    screen.blit(next_surface, (485, 200, 50, 50))  # Draw the next piece label
    if game.game_over:
        screen.blit(game_over_surface, (430, 500, 50, 50))
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)  # Draw the score rectangle
    screen.blit(score_value_surface, score_value_surface.get_rect(center=(score_rect.centerx, score_rect.centery)))  # Draw the score value
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)  # Draw the next piece rectangle
    game.draw(screen)  # Draw the game elements

    pygame.display.update() 
    clock.tick(60)  # Limit the frame rate to 60 FPS