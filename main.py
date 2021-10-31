from SimCases.DistDisp import DistDisp
import pygame

# Initializing main window

width = 600
height = 600
dark_mode = False
pygame.init()
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
if dark_mode:
    background = (0, 0, 0)
    main_color = (255, 255, 255)
    rect_color = (100, 100, 100)
else:
    background = (255, 255, 255)
    main_color = (0, 0, 0)
    rect_color = (150, 150, 150)
window.fill(background)
pygame.display.set_caption('Point-particle Simulation Menu')

# Making loop function for main window


def loop():
    crashed = False
    while not crashed:
        for event in pygame.event.get():  # Event handling
            if event.type == pygame.QUIT:
                crashed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= pygame.mouse.get_pos()[0] <= 450 and 150 <= pygame.mouse.get_pos()[1]:
                    new_sim = DistDisp()
        font = pygame.font.SysFont('freesans', 20)
        pygame.draw.rect(window, background, (150, 150, 300, 100))
        text = font.render('Distance-Displacement', False, main_color)
        window.blit(text, (200, 185))
        pygame.draw.rect(window, rect_color, (150, 150, 300, 100))
        text = font.render('Distance-Displacement', False, main_color)
        window.blit(text, (200, 185))
        pygame.display.update()
        clock.tick(60)
    print('Thank you for using this GUI!')
    pygame.quit()
    quit()


try:
    loop()
except KeyboardInterrupt:
    print('Thank you for using this GUI!')
    
