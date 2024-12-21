import pygame
from pygame import *
import sys
import os
import PyInstaller.hooks
#创建5个会移动的球
pygame.init()
size = (640,480)
screen = pygame.display.set_mode(size)
def load_transform(path):
    """返回80*80的图像"""
    img = pygame.image.load(path)
    img = pygame.transform.scale(img,(40,40))
    return img

def get_picture_num(path):
    return len(os.listdir(path))
clock = pygame.time.Clock()

shovel = load_transform('imgs\shovel.png')
is_shovel_mode = False
pygame.mouse.set_visible(False)


while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            is_shovel_mode = True
            pygame.mouse.set_visible(False)
        elif event.type == KEYUP and event.key == K_SPACE:
            is_shovel_mode = False
            pygame.mouse.set_visible(True)    
    screen.fill((0,0,0))
    if is_shovel_mode:
        mouse_x,mouse_y = pygame.mouse.get_pos()
        screen.blit(shovel,(mouse_x-shovel.get_rect()[2]//2,mouse_y-shovel.get_rect()[3]//2))
    # print(pygame.key.get_pressed())
    # print(pygame.K_SPACE)
    # screen.blit(shovel,(mouse_x-shovel.get_rect()[2]//2,mouse_y-shovel.get_rect()[3]//2))
    pygame.display.flip()
    clock.tick(100)
