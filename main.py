import pygame
import conf
import loop

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


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
    screen.blit(my_font.render(str(mouse_pos[0]) + ' ' + str(mouse_pos[1]), False, (0, 0, 0)), (50,0))

    
    # RENDER GAME HERE
    base.loop()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60

pygame.quit()