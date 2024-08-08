import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

car_width = 50
car_height = 60
car_speed = 5

obstacle_width = 50
obstacle_height = 60
obstacle_speed = 5

car_image = pygame.image.load('car.png')

def game_loop():
    x = (screen_width * 0.45)
    y = (screen_height * 0.8)
    x_change = 0

    obstacle_start_x = random.randrange(0, screen_width)
    obstacle_start_y = -600
    obstacle_speed = 7
    obstacle_width = 100
    obstacle_height = 100

    clock = pygame.time.Clock()

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -car_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = car_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        screen.fill(white)

        pygame.draw.rect(screen, black, [obstacle_start_x, obstacle_start_y, obstacle_width, obstacle_height])
        obstacle_start_y += obstacle_speed

        screen.blit(car_image, (x, y))

        if x > screen_width - car_width or x < 0:
            game_exit = True

        if obstacle_start_y > screen_height:
            obstacle_start_y = 0 - obstacle_height
            obstacle_start_x = random.randrange(0, screen_width)

        if y < obstacle_start_y + obstacle_height:
            if x > obstacle_start_x and x < obstacle_start_x + obstacle_width or x + car_width > obstacle_start_x and x + car_width < obstacle_start_x + obstacle_width:
                game_exit = True

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

game_loop()
