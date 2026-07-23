
import sys

print("Before pygame import")
print("sys.modules keys:", [k for k in sys.modules if 'numpy' in k or 'matplotlib' in k])

import pygame

print("After pygame import")
print("sys.modules keys:", [k for k in sys.modules if 'numpy' in k or 'matplotlib' in k])

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Test")
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Done")
