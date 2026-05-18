import pgzrun
import pygame
import random

# Globale Variablen
WIDTH = 1280
HEIGHT = 720
GRAVITY = 0.02

MOVE_SPEED= 10
SHIP_START_X = 600
SHIP_START_Y = 550

background = None

# Charakter 
ship  = Actor("spaceships_007.png", anchor=("center","bottom"))
ship.midbottom  = (SHIP_START_X, SHIP_START_Y)
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

# Leben
lives = 5

# Spielzustand
started = False
game_over = False

# Metoer Spawn Timer
meteor_spawn_counter = 0
meteor_spawn_interval = 500 # Alle 500 Frames einen neune Meteor spwanen 

def draw():
    global background

    if background is None: 
        background = pygame.image.load("images/hintergund_3.jpg")
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

    # Zeichne Lebensanzeige
    screen.draw.text(f"Leben: {lives}", (20, 20), color="white", fontsize=50)

    if not started:
        screen.draw.text("Drücke LEERTASTE, um zu starten", center=(WIDTH // 2, HEIGHT // 2), color="white", fontsize=60)
        screen.draw.text("Links/Rechts bewegen, Leertaste schießen", center=(WIDTH // 2, HEIGHT // 2 + 70), color="white", fontsize=40)

    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), color="red", fontsize=100)
        screen.draw.text("Drücke LEERTASTE, um neu zu starten", center=(WIDTH // 2, HEIGHT // 2 + 80), color="white", fontsize=40)


def update():
    global meteor_spawn_counter, lives, game_over

    if game_over or not started:
        return

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
        meteor.vy = meteor.vy + GRAVITY
        # y Bewegung ausführen
        meteor.y = meteor.y + meteor.vy

        # Meteor oben neu erscheinen lassen, wenn er unten aus dem Bildschirm fällt
        if meteor.top > HEIGHT:
            lives -= 1
            if lives <= 0:
                lives = 0
                game_over = True
            meteor.x = random.randint(50, WIDTH - 50)
            meteor.y = random.randint(-120, 50)
            meteor.vy = 0

        # Kollision mit dem Schiff: Leben abziehen und Meteor zurücksetzen
        if meteor.colliderect(ship):
            lives -= 1
            if lives <= 0:
                lives = 0
                game_over = True
            meteor.x = random.randint(50, WIDTH - 50)
            meteor.y = random.randint(-120, 50)
            meteor.vy = 0

    # Schüsse bewegen
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


def fire_bullet():
    bullet = Actor("effect_yellow.png", center=ship.center)
    bullet.y -= 20
    bullets.append(bullet)


def reset_game():
    global lives, game_over, started, meteors, bullets, meteor_spawn_counter, ship

    lives = 5
    game_over = False
    started = False
    bullets.clear()
    meteors.clear()
    meteor_spawn_counter = 0
    # Neu erzeuge das Schiff wie beim Programmstart und setze Position/Geschwindigkeit
    ship = Actor("spaceships_007.png", anchor=("center","bottom"))
    ship.midbottom = (SHIP_START_X, SHIP_START_Y)
    ship.x = SHIP_START_X
    ship.y = SHIP_START_Y
    ship.vx = 0
    ship.vy = 0
    ship.angle = 180

    meteors.append(spawn_meteor("meteorbrown_big1.png"))
    meteors.append(spawn_meteor("meteorbrown_big2.png"))


def on_key_down(key):
    global started, game_over

    if game_over and key == keys.SPACE:
        reset_game()
        started = True
        return

    if not started and key == keys.SPACE:
        started = True
        return

    if started and key == keys.SPACE:
        fire_bullet()

pgzrun.go()
