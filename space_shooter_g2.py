import pgzrun
import pygame
import random

# Globale Variablen
WIDTH = 1280
HEIGHT = 720
GRAVITY = 0.02

MOVE_SPEED= 10

background = None

# Charakter 
ship  = Actor("spaceships_007.png", anchor=("center","bottom"))
ship.midbottom  = (600,550)
ship.angle = 180  # Schiff umdrehen, damit es auf dem Kopf steht
# Erzeuge Meteoriten zufällig oben im Spielfeld
def spawn_meteor(image):
    meteor = Actor(image)
    meteor.x = random.randint(50, WIDTH - 50)
    meteor.y = random.randint(-120, 50)
    meteor.vy = 0
    return meteor

meteors = []
meteor1 = Actor("meteorbrown_big1.png", topleft=(100, 100))
meteor1.vy = 0
meteors.append(meteor1)

meteor2 = Actor("meteorbrown_big2.png", topleft=(700, 200))
meteor2.vy = 0
meteors.append(meteor2)

# Schüsse
bullets = []

# Metoer Spawn Timer
meteor_spawn_counter = 0
meteor_spawn_interval = 500 # Alle 500 Frames einen neune Meteor spwanen 

def draw():
    global background

    if background is None: 
        background = pygame.image.load("images/hintergund_3.jpg")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    #Zeichen Hintergrund 
    
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
    global meteor_spawn_counter

    meteor_spawn_counter += 1
    if meteor_spawn_counter >= meteor_spawn_interval:
        new_meteor= spawn_meteor( "meteorbrown_big1.png")
        meteors.append(new_meteor)
        meteor_spawn_counter = 0

    # x Geschwindigkeit berechnen (Bewegung links rechts)
    ship.vx = 0 
    if keyboard.left: 
        ship.vx = -MOVE_SPEED
    elif keyboard.right:
        ship.vx = MOVE_SPEED

    # Schiff bewegen
    ship.x += ship.vx
    #Raumschiff innerhalb des Bildschirmshalten
    ship.x = max(50, min(ship.x, WIDTH - 50))
    # y Geschwindigkeit meteoriden berechen und anwenden ( Bewegung oben unten)
    for meteor in meteors:
        # Gravitation hinzufügen
        meteor.vy += GRAVITY
        meteor.y += meteor.vy
    for bullet in bullets:
        bullet.y -= 10  # Schüsse nach oben bewegen

    # Kollision zwischen Schüssen und Meteoriten überprüfen
    for bullet in bullets[:]:  # Kopie der Liste, um während der Iteration zu entfernen
        for meteor in meteors[:]:  # Kopie der Liste
            if bullet.colliderect(meteor):
                meteors.remove(meteor)
                bullets.remove(bullet)
                break  # Ein Schuss kann nur einen Meteor treffen

    # Neue Meteoriten spawnen, wenn weniger als 2 vorhanden sind
    while len(meteors) < 2:
        new_meteor = spawn_meteor(random.choice(["meteorbrown_big1.png", "meteorbrown_big2.png"]))
        meteors.append(new_meteor)

    # Schüsse entfernen, die den Bildschirm verlassen
    bullets[:] = [bullet for bullet in bullets if bullet.y > 0]

    # Schüsse abfeuern bei Leertaste
    if keyboard.space:
        bullet = Actor("effect_yellow.png", center=ship.center)  # Verwende gebe Funken als Bild für Schüssse
        bullet.y -= 20  # Etwas oberhalb des Schiffes starten
        bullets.append(bullet)

    #Kollision zwischen Schüssen und Meteoriten überprüfen
     
        bullet = Actor("effect_yellow.png", center=ship.center)  # Verwende gelbes Effektbild als Schuss
        bullet.y -= 20  # Etwas oberhalb des Schiffes star        bullets.append(bullet)            

pgzrun.go()