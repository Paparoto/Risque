import pygame

background_colour = (234, 212, 252)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



screen.fill(background_colour)

pygame.display.flip()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
            running = False
