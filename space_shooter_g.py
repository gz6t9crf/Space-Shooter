import pgzrun
import pygame

# Globale Variablen
WIDTH = 1280
HEIGHT = 720

MOVE_SPEED= 5

background = None

# Charakter 
ship  = Actor("spaceships_007.png", anchor=("center","bottom"))
ship.midbottom  = (600,550)
ship.angle = 180  # Schiff umdrehen, damit es auf dem Kopf steht
meteors= [Actor("meteorbrown_big1.png", topleft=(100, 100)), Actor("meteorbrown_big2.png", topleft=(700, 200))]

# Schüsse
bullets = []

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

    # Zeichne Schüsse
    for bullet in bullets:
        bullet.draw()

def update():
    # x Geschwindigkeit berechnen (Bewegung links rechts)
    ship.vx = 0 
    if keyboard.left:
        ship.vx = -MOVE_SPEED
    elif keyboard.right:
        ship.vx = MOVE_SPEED

    # Schiff bewegen
    ship.x += ship.vx

    # Schüsse bewegen
    for bullet in bullets:
        bullet.y -= 10  # Schüsse nach oben bewegen

    # Schüsse entfernen, die den Bildschirm verlassen
    bullets[:] = [bullet for bullet in bullets if bullet.y > 0]

    # Schüsse abfeuern bei Leertaste
    if keyboard.space:
        bullet = Actor("effect_yellow.png", center=ship.center)  # Verwende gebe Funken als Bild für Schüssse
        bullet.y -= 20  # Etwas oberhalb des Schiffes starten
        bullets.append(bullet)

    #Kollision zwischen Schüssen und Meteoriten überprüfen
     

pgzrun.go()
