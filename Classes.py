from Constantes import *
from pygame.locals import *
import pygame
import random

class Vector2():
    '''
    créé un vecteur 2
    (peut paraître inutile mais sauve des vies)
    '''
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Room ():

    RoomCoordinate = Vector2(0,0)

    id_Room = 0
    type_Room = 0
    type_Opened = 0

    nbrLayers = 0
    layers = []

    layersBlock = []

    def __init__(self, fenetre):
        self.id_Room = 0
        self.type_Room = 0
        self.type_Opened = 0
        self.fenetre = fenetre

    def GenerateRoom (self, camera):
        for layer in self.layers:
            for structure in layer:
                num_ligne = 0
                layer1_block = []

                for ligne in structure:
                    #On parcourt les listes de lignes
                    num_case = 0
                    newLine = []

                    for sprite in ligne:
                        #On calcule la position réelle en pixels
                        num_case =  num_case + 1
                        if(sprite != []):
                            newBlock = Block(Vector2(num_case, num_ligne),int(sprite[0]))
                            newBlock.Show(self.fenetre, camera)
                            newLine.append(newBlock)


                    layer1_block.append(newLine)
                    num_ligne += 1

                self.layersBlock.append(layer1_block)


class Level ():

    Rooms = []

    def __init__(self, fichier, fen):
        self.fichier = fichier
        self.fenetre = fen

    def Generate (self, camera):

        Rooms = []

        #On ouvre le fichier
        fichiers = []
        with open(self.fichier, "r") as fichier:
            #On parcourt les lignes du fichier
            for ligne in fichier:
                fichiers.append(ligne.replace("\n", ''))
        for b in fichiers:
            with open(b, "r") as fichier:
                newRoom = Room(self.fenetre)
                i = 0
                j = 0 #compteur de lignes dans un layer
                h = 1 #compteur de layer
                structure_niveau = []
                for ligne in fichier:
                    i += 1
                    if(i <= 4):
                        # LA LIGNE 0 = Ligne qui dit le nbr de layer || 1 layer == 12x12
                        if(i == 1):
                            nbrLayer = ligne.replace('\n', '')
                            newRoom.nbrLayers = int(nbrLayer)
                            layer = []
                        elif(i == 2):
                            #LA LIGNE 2 = la ligne qui dit le type 1
                            newRoom.type_Room = int(ligne.replace('\n', ''))
                        elif(i == 3):
                            #LA LIGNE 3 = la ligne qui dit le type 1
                            newRoom.type_Opened = int(ligne.replace('\n', ''))
                    else:
                        if h <= newRoom.nbrLayers:
                            j += 1
                            ligne_niveau = []
                            #On parcourt les sprites (nomhres) contenus dans le fichier
                            for sprite in ligne:
                                case_niveau = []
                                if sprite != '\n' and sprite != '.':
                                    case_niveau.append(sprite)
                                elif sprite != '\n'and sprite == '.':
                                    a = ord(sprite)
                                    case_niveau.append(a)
                                #On ajoute la ligne à la liste du niveau
                                ligne_niveau.append(case_niveau)
                            structure_niveau.append(ligne_niveau)
                            #On sauvegarde cette structure
                            if(j == 12):
                                j = 0
                                layer.append(structure_niveau)
                                structure_niveau = []
                                h = h + 1
                newRoom.layers.append(layer)
                newRoom.GenerateRoom(camera)
                self.Rooms.append(newRoom)




    def Update (self, camera):
        for room in self.Rooms:
            for layersBlock in room.layersBlock:
                for ligne in layersBlock:
                    for b in ligne:
                        b.Show(self.fenetre, camera)

    def UpdateCollision (self):
            for room in self.Rooms:
                for layersBlock in room.layersBlock:
                    for ligne in layersBlock:
                        for b in ligne:
                            b.UpdateCollision()


def AllWalls(level):
    for room in level.Rooms:
            for layersBlock in room.layersBlock:
                for ligne in layersBlock:
                    for b in ligne:
                        if b.material == 1:
                            yield b

class VectorOperator ():

    def AddVectors (vectorA, vectorB):
        return Vector2(vectorA.x + vectorB.x, vectorA.y + vectorB.y)

    def SubtractVectors (vectorA, vectorB):
        return Vector2(vectorA.x - vectorB.x, vectorA.y - vectorB.y)

    def MulitplyVectors (vectorA, vectorB):
        return Vector2(vectorA.x * vectorB.x, vectorA.y * vectorB.y)

    def DivideVectors (vectorA, vectorB):
        if (vectorB != 0):
            return Vector2(vectorA.x / vectorB.x, vectorA.y / vectorB.y)

    def AddVectorsWithNumber (vectorA, nbre):
        return Vector2(vectorA.x + nbre, vectorA.y + nbre)

    def SubtractVectorsWithNumber (vectorA, nbre):
        return Vector2(vectorA.x - nbre, vectorA.y - nbre)

    def MulitplyVectorsWithNumber (vectorA, nbre):
        return Vector2(vectorA.x * nbre, vectorA.y * nbre)

    def DivideVectorsWithNumber (vectorA, nbre):
        if (nbre != 0):
            return Vector2(vectorA.x / nbre, vectorA.y / nbre)

class Block():
    #Coord = fictif
    #Transform = real position
    import pygame

    #__init__
    def __init__(self, gridCoord, materialType):
        '''
        gridCoord = Vector2(x,y)
        materialType = |. = empty
                       |0 = floor1
                       |1 = wall1
        '''
        self.coord = Vector2(5000, 5000)
        self.transform = Vector2(5000, 5000)
        self.texture = None

        #Convert coord to transform
        self.coord = gridCoord
        self.transform = Vector2(self.coord.x*32,self.coord.y*32)
       # self.UpdateTransform(self.coord)
        self.material = materialType
        self.addMaterial(materialType)

        self.hitbox = hitbox([self.transform,32,32])

    def addMaterial (self, matType):
        if (matType == 0):
            self.texture = pygame.image.load("Textures\Floor1.png").convert_alpha()
        elif (matType == 1):
            a = random.randint(1,4)
            if a == 1:
                self.texture = pygame.image.load("Textures\Wall1.png").convert_alpha()
            elif a == 2:
                self.texture = pygame.image.load("Textures\Wall2.png").convert_alpha()
            elif a == 3:
                self.texture = pygame.image.load("Textures\Wall3.png").convert_alpha()
            elif a == 4:
                self.texture = pygame.image.load("Textures\Wall4.png").convert_alpha()
        elif (matType == 46):
            self.texture = pygame.image.load("Textures\Empty.png").convert_alpha()

    def UpdateTransform (self, coord2, camera):
        self.transform.x = 32 * coord2.x + camera.transform.x
        self.transform.y = 32 * coord2.y + camera.transform.y

    def UpdateCollision (self):
        self.hitbox = hitbox([self.transform,32,32])


    def Show (self, fenetre, camera):
        self.UpdateTransform(self.coord, camera)
        fenetre.blit(self.texture, (self.transform.x, self.transform.y))

class Camera ():

    transform = Vector2(64*2,64*2)
    speed = 8.0
    offsetX = 320
    offsetY = 240
    def __init__(self):
        self.speed = self.speed

    def follow (self, target):
        self.transform.x = target.x + self.offsetX
        self.transform.y = target.y + self.offsetY

    def Move (self, direction):
        self.transform.x = direction.x * self.speed
        self.transform.y = direction.y * self.speed



class hitbox():
    def __init__(self,liste_param):
        '''
        liste_param : list
            rectangle --> [centre,longueurGauche-Droite,longueurHaut-Bas]
        '''
        self.centre = liste_param[0]
        # Céation des sommets
        self.sommets = []

        listePeuImportante = [[-1,-1],[-1,1],[1,-1],[1,1]]
                                #[[h-g],[h-d],[b-g],[b-d]]
        for i in listePeuImportante :
            x = liste_param[1] * i[0] / 2 + self.centre.x
            y = liste_param[2] * i[1] / 2 + self.centre.y
            self.sommets.append(Vector2(x,y))

        self.maxX = self.sommets[3].x
        self.maxY = self.sommets[3].y
        self.minX = self.sommets[0].x
        self.minY = self.sommets[0].y

    def Move(self,vector):
        for i in range(len(self.sommets)):
            self.sommets[i] = Vector2(self.sommets[i].x+vector.x,self.sommets[i].y+vector.y)

        self.centre = Vector2(self.centre.x+vector.x,self.centre.y+vector.y)

def distance(hb1,hb2):
    return sqrt((hb1.centre.x-hb2.centre.x)**2+(hb1.centre.y-hb2.centre.y)**2)

def angle(hb1,hb2):
    return acos((hb2.centre.x - hb1.centre.x)/distance(hb1,hb2))

def distRepustion(hb1,hb2):
    teta = angle(hb1,hb2)

    if pi/4 <teta< 3*pi/4 or 5*pi/4 <teta< 7*pi/4:
        x = cos(teta) * 32
    else:
        x = sin(teta) * 32

    return sqrt(1024+x**2)

def hit(hitbox1,hitbox2):
    '''
    permet de savoir si des hitbox se touchent
    '''
    critere = [True for i in range(4)]
    for point in hitbox2.sommets:
        listePos = [point.y>hitbox1.maxY,point.y<hitbox1.minY,point.x>hitbox1.maxX,point.x<hitbox1.minX]   #[dessus,dessous,droite,gauche]
        critere = [critere[i] and listePos[i] for i in range(4)]

    result = critere[0] or critere[1] or critere[2] or critere[3]
    return not result