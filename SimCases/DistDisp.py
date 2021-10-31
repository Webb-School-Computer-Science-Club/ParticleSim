"""
DistDisp.py
For helping visualize the similarites and differences between distance (a scalar) and displacement (a vector)
Distance and displacement units are arbitrary (2 pixels = 1 unit)
"""

import pygame
import math


class DistDisp:

    def __init__(self, width=600, height=600, dark_mode=False):

        pygame.init()  # Initializes pygame

        # Initializes sizing variables and pygame window

        self.width = width
        self.height = height
        self.x = int(self.width/2)
        self.y = int(self.height/2)
        self.x_start = int(self.width/2)
        self.y_start = int(self.height/2)
        self.x_prev = int(self.width/2)
        self.y_prev = int(self.height/2)
        self.dark_mode = dark_mode
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = 'Distance-Displacement Simulation'
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.go_back = False

        # Color initialization and circle

        self.background = (255, 255, 255)
        self.main_color = (0, 0, 0)
        if not dark_mode:
            self.circ_color = (150, 160, 180)
        else:
            self.main_color = (255, 255, 255)
            self.background = (0, 0, 0)
            self.circ_color = (50, 60, 80)
        self.window.fill(self.background)

        pygame.draw.circle(self.window, self.circ_color, (self.x, self.y), 10)  # Particle

        self.loop()  # Calls the loop function

    def loop(self):
        crashed = False
        mov_x = False
        neg_x = False
        mov_y = False
        neg_y = False
        inc_tot = 0
        ang = 0
        change_lis = []
        while not crashed:  # Main loop of GUI
            inc = [0, 0]
            for event in pygame.event.get():  # Event handling
                if event.type == pygame.QUIT:
                    crashed = True
                elif event.type == pygame.KEYDOWN:  # Moving the particle
                    if event.key == pygame.K_RIGHT:
                        mov_x = True
                        neg_x = False
                    elif event.key == pygame.K_LEFT:
                        mov_x = True
                        neg_x = True
                    elif event.key == pygame.K_UP:
                        mov_y = True
                        neg_y = False
                    elif event.key == pygame.K_DOWN:
                        mov_y = True
                        neg_y = True
                    elif event.key == pygame.K_e:  # Resets distance and displacement
                        for x, y, xx, yy in change_lis:
                            pygame.draw.line(self.window, self.background, (x, y), (xx, yy), 2)
                        pygame.draw.line(self.window, self.background, (self.x_start, self.y_start), (self.x, self.y), 4)
                        font = pygame.font.SysFont('freesans', 20)
                        text = font.render('Distance: ' + str(inc_tot / 2), False, self.background)
                        disp_text = font.render('Displacement: ' + str(round(math.sqrt((self.x - self.x_start) ** 2 +
                                                                            (self.y - self.y_start) ** 2) / 2,
                                                                             4)), False, self.background)
                        ang_text = font.render('Angle from horizontal: ' + str(round(ang, 4)), False, self.background)
                        self.window.blit(text, (5, 5))
                        self.window.blit(disp_text, (5, 30))
                        self.window.blit(ang_text, (250, 5))
                        self.x_start, self.y_start = self.x, self.y
                        change_lis = []
                        inc_tot = 0
                elif event.type == pygame.KEYUP:  # Stopping movement of particle
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        mov_y = False
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        mov_x = False

            # Erasing previously drawn text, circles, and lines

            pygame.draw.circle(self.window, self.background, (self.x, self.y), 10)
            font = pygame.font.SysFont('freesans', 20)
            text = font.render('Distance: ' + str(inc_tot/2), False, self.background)
            disp_text = font.render('Displacement: ' + str(round(math.sqrt((self.x - self.x_start)**2 +
                                                           (self.y - self.y_start)**2)/2, 4)), False, self.background)
            ang_text = font.render('Angle from horizontal: ' + str(round(ang, 4)), False, self.background)
            self.window.blit(text, (5, 5))
            self.window.blit(disp_text, (5, 30))
            self.window.blit(ang_text, (250, 5))
            self.x_prev, self.y_prev = self.x, self.y
            for x, y, xx, yy in change_lis:
                pygame.draw.line(self.window, self.background, (x, y), (xx, yy), 2)
            pygame.draw.line(self.window, self.background, (self.x_start, self.y_start), (self.x, self.y), 4)

            # Changing x and y-coords according to keyboard events

            if mov_x:
                if neg_x:
                    if self.x - 2 > 10:
                        self.x -= 2
                        inc[0] = 2
                else:
                    if self.x + 2 < self.width - 10:
                        self.x += 2
                        inc[0] = 2
            if mov_y:
                if neg_y:
                    if self.y + 2 < self.height - 10:
                        self.y += 2
                        inc[1] = 2
                else:
                    if self.y - 2 > 65:
                        self.y -= 2
                        inc[1] = 2

            # Getting angle

            try:
                ang = math.atan(((self.y_start - self.y)/(self.x - self.x_start))) * 180/math.pi
                if self.x - self.x_start < 0:
                    ang = ang + 180
                elif self.x - self.x_start > 0 and self.y_start - self.y < 0:
                    ang = ang + 360
            except ZeroDivisionError:
                if self.y - self.y_start == 0:
                    ang = 0
                elif self.y - self.y_start > 0:
                    ang = 270
                else:
                    ang = 90

            # Getting total path

            if self.x != self.x_prev or self.y != self.y_prev:
                change_lis.append([self.x_prev, self.y_prev, self.x, self.y])
            inc_tot = round(math.sqrt(inc[0] ** 2 + inc[1] ** 2) + inc_tot, 4)

            # Adding new text, circles, and lines

            text = font.render('Distance: ' + str(inc_tot/2), False, self.main_color)
            disp_text = font.render('Displacement: ' + str(round(math.sqrt((self.x - self.x_start) ** 2 +
                                                           (self.y - self.y_start) ** 2)/2, 4)), False, self.main_color)
            ang_text = font.render('Angle from horizontal: ' + str(round(ang, 4)), False, self.main_color)
            self.window.blit(text, (5, 5))
            self.window.blit(disp_text, (5, 30))
            self.window.blit(ang_text, (250, 5))
            for x, y, xx, yy in change_lis:
                pygame.draw.line(self.window, self.circ_color, (x, y), (xx, yy), 2)
            pygame.draw.line(self.window, self.main_color, (self.x_start, self.y_start), (self.x, self.y), 4)
            pygame.draw.circle(self.window, self.circ_color, (self.x, self.y), 10)
            pygame.display.update()
            self.clock.tick(60)
        self.end()

    def end(self):
        self.window.fill(self.background)
        print('Thanks for using this!')

