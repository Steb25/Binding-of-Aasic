import pygame
from Constantes import *

pygame.init()

#Ouverture de la fenêtre Pygame

fenetre = pygame.display.set_mode((640, 480))

#BOUCLE INFINIE
Start()

continuer = 1

lvl = Level("Level1.txt", fenetre)
lvl.Generate(camera)

perso = Personnage()

lastcam = Vector2(0,0)

while continuer:
    clock = pygame.time.Clock()
    clock.tick(60)
    #Rafraîchissement de l'écran
    fenetre.fill((0,0,0))
    lvl.Update(camera)
    perso.update(lvl)
    #rectangle=pygame.draw.rect(fenetre,(0,0,0),pygame.Rect(100 , 100, 32, 32),1)
    directionVector = Vector2(0,0)

    keysPressed = pygame.key.get_pressed()
    if keysPressed[pygame.K_ESCAPE]:
        continuer = 0
    if keysPressed[pygame.K_LEFT]:
        directionVector.x += 1.0
        perso.move("left")
    if keysPressed[pygame.K_RIGHT]:
        directionVector.x -= 1.0
        perso.move("right")
    if keysPressed[pygame.K_DOWN]:
        directionVector.y -= 1.0
        perso.move("down")
    if keysPressed[pygame.K_UP]:
        directionVector.y += 1.0
        perso.move("up")

    #Liste des Events à gérer
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

    perso.Show(fenetre)

    if(perso.hitWall is not True):
        camera.transform = VectorOperator.AddVectors(camera.transform, VectorOperator.MulitplyVectorsWithNumber(directionVector, camera.speed))

    if(camera.transform != lastcam):
        lvl.UpdateCollision()
        lastcam = camera.transform
    pygame.display.flip()


