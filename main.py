import pygame
import conf
import loop

pygame.font.init()


pygame.init()
screen = pygame.display.set_mode(conf.SIZE_SCREEN)
clock = pygame.time.Clock()
running = True

base = loop.Loop(screen)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(conf.COLOR_BG)
    mouse_pos = pygame.mouse.get_pos()

    
    # RENDER GAME HERE
    base.loop()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60

pygame.quit()