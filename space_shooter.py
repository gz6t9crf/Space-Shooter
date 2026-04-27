import pgzrun
import pygame

# Globale Variablen
WIDTH = 1280
HEIGHT = 720

MOVE_SPEED= 5

background = None

# Charakter 
ship  = Actor("spaceships_001.png", anchor=("center","bottom"))
ship.midbottom  = (600,500)

meteors= [Actor("spacemeteors_001.png", topleft=(100, 100)), Actor("spacemeteors_002.png", topleft=(700, 200))]


def draw():
    global background

    if background is None:
        background = pygame.image.load("images/darkpurple.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    #Zeichen Hintergrund 
    screen.blit(background, (0, 0))
    
    # Zeichne Ship
    ship.draw()

    # Zeichne Meteoriten
    for meteor in meteors:
        meteor.draw()

def update():
    # x Geschwindigkeit berechnen (Bewegung links rechts)
    ship.vx = 0 
    if keyboard.left:
        ship.vx = -MOVE_SPEED
    elif keyboard.right:
        ship.vx = MOVE_SPEED


pgzrun.go()
