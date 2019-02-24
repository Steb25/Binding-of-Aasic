from Classes import *
from Constantes import *

class MovableObject():

    def __init__(self,hitbox):
        self.hitbox = hitbox([Vector2(0,0),1,1])
        self.transform = self.hitbox.liste_param[0]     # Coordonnées du centre
        self.texture = None
        self.speed = 0

    def move(self,vector):
        self.transform.x += vector.x
        self.transform.y += vector.y


class Personnage():

    def __init__(self):
            global vitesseMax, taillePerso, frotement, proj_vitesse
            taillePerso = 32
            vitesseMax = 10
            frotement = 1
            proj_vitesse = 5
            self.transform = Vector2(320,240)
            self.speed = 2
            self.hitbox = hitbox([self.transform, taillePerso,taillePerso])
            self.vel = Vector2(0,0)
            self.hitWall = False


    def Show (self, fenetre):
       self.texture = pygame.image.load("Textures\Hero.png").convert_alpha()
       fenetre.blit(self.texture, (self.transform.x, self.transform.y))



    def collisionCheck(self,lvl):
        '''
        for block in AllWalls(lvl):
            if hit(self.hitbox,block.hitbox):
                distrep = distRepustion(block.hitbox,self.hitbox)
                teta = angle(block.hitbox,self.hitbox)

                self.transform.x += cos(teta)
                self.transform.y += sin(teta)

        '''
        repultionX,repultionY,nbContacts = 0,0,0

        for block in AllWalls(lvl):
            if hit(self.hitbox,block.hitbox):
                nbContacts+=1
                repultionX +=(self.hitbox.centre.x-block.hitbox.centre.x)/distance(self.hitbox,block.hitbox)
                repultionY +=(self.hitbox.centre.y-block.hitbox.centre.y)/distance(self.hitbox,block.hitbox)

        if not nbContacts==0:
            self.vel = Vector2(repultionX*5/nbContacts,repultionY*5/nbContacts)
            self.hitWall = True
        else:
            self.hitWall = False

        '''

        blockTest = hitbox([Vector2(100,100),32,32])

        if hit(self.hitbox,blockTest):
                self.vel.x =((self.hitbox.centre.x-blockTest.centre.x)/distance(self.hitbox,blockTest))
                self.vel.y =((self.hitbox.centre.y-blockTest.centre.y)/distance(self.hitbox,blockTest))
        '''

    def fire(self):
        vitesse = sqrt(self.vel.x**2 + self.vel.y**2)
        vecX = self.vel.x * self.proj_vitesse / vitesse
        vecY = self.vel.y * self.proj_vitesse / vitesse

        projectile.append(Projectile(self.transform,Vector2(vecX,vecY),None))

    def move(self,direction):
        if direction == 'up':
            self.vel.y -= self.speed
        elif direction == 'down':
            self.vel.y += self.speed
        elif direction == 'right':
            self.vel.x += self.speed
        elif direction == 'left':
            self.vel.x -= self.speed

    def update(self,lvl):

        self.collisionCheck(lvl)

        if self.vel.x > vitesseMax:
            self.vel.x = vitesseMax
        if self.vel.x < -vitesseMax:
            self.vel.x = -vitesseMax

        if self.vel.y > vitesseMax:
            self.vel.y = vitesseMax
        if self.vel.y < -vitesseMax:
            self.vel.y = -vitesseMax

        self.transform.x += self.vel.x
        self.transform.y += self.vel.y

        self.hitbox = hitbox([self.transform,taillePerso,taillePerso])

        if self.vel.x > 0:
            if self.vel.x <= frotement:
                self.vel.x = 0
            else:
                self.vel.x -= frotement
        elif self.vel.x < 0:
            if self.vel.x >= frotement:
                self.vel.x = 0
            else:
                self.vel.x += frotement

        if self.vel.y > 0:
            if self.vel.y <= frotement:
                self.vel.y = 0
            else:
                self.vel.y -= frotement
        elif self.vel.y < 0:
            if self.vel.y >= frotement:
                self.vel.y = 0
            else:
                self.vel.y += frotement

class Projectile():

    def show(self,fenetre):
        self.texture = pygame.image.load("Textures\roguelikeHoliday_transparent_solo.png").convert_alpha()
        fenetre.blit(self.texture, (self.transform.x, self.transform.y))

    def __init__(self,coord,vector,style):
        self.transform = coord
        self.direc = vector
        self.type = style
        self.hitbox = hitbox([self.transform,10,10])

    def collisionCheck(self):
        for block in AllWalls(lvl):
            if hit(self.hitbox,block.hitbox):
                del self

    def update(self):
        self.collisionCheck()
        self.transform.x += self.direc.x
        self.transform.y += self.direc.y