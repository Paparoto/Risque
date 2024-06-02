import socket
import threading
import pygame
import sys
import time

# from host import get_client_number

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Classe pour représenter un Cube
class Cube:
    def __init__(self, start_pos, end_pos, speed, attaquant, attaqué, couleur, cavalier):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.position = list(start_pos)
        self.speed = 2
        self.cavalier = pygame.image.load("asset/cavalier.png")
        self.cavalier_ennemi = pygame.image.load("asset/cavalier_ennemi.png")
        self.cavalier = pygame.transform.scale(self.cavalier, (80, 80))
        self.cavalier_ennemi = pygame.transform.scale(self.cavalier_ennemi, (80, 80))
        self.attaqué = attaqué
        self.attaquant = attaquant
        self.couleur = couleur
        self.troupes_cavalier = cavalier
        pygame.mixer.set_num_channels(2)
        self.cheval = pygame.mixer.Sound("asset/cheval.mp3")
        self.combat = pygame.mixer.Sound("asset/battle.mp3")
        self.canal_1 = pygame.mixer.Channel(0)
        self.canal_2 = pygame.mixer.Channel(1)
        self.cheval.set_volume(100)
        self.attaque = True

    def has_reached_destination(self):

        if self.position[0] == self.end_pos[0] and self.position[1] == self.end_pos[1]:
            if self.attaque:
                if self.attaquant.couleur != self.attaqué.couleur:

                    # time.sleep(10)
                    self.canal_2.play(self.combat)
                    self.attaqué.troupes -= self.troupes_cavalier
                    if self.attaqué.troupes < 0:
                        if self.attaquant.couleur == "red":
                            self.attaqué.couleur = "red"
                            self.attaqué.troupes = -self.attaqué.troupes
                        elif self.attaquant.couleur == "blue":
                            self.attaqué.couleur = "blue"
                            self.attaqué.troupes = -self.attaqué.troupes
                    self.attaque = False
                elif self.attaqué.couleur == self.attaquant.couleur and self.attaquant.nom in self.attaqué.liste_adjacents:
                    self.attaqué.troupes += self.troupes_cavalier
                    self.attaque = False
            return True
        return False

    def update(self):
        # Calculer le vecteur de déplacement
        direction = [self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1]]
        distance = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        if distance == 0:
            return

        # Normaliser le vecteur de direction
        direction[0] /= distance
        direction[1] /= distance

        # Déplacer le cube
        self.position[0] += direction[0] * self.speed
        self.position[1] += direction[1] * self.speed

        # Vérifier si le cube a atteint ou dépassé la position finale
        if (direction[0] > 0 and self.position[0] >= self.end_pos[0]) or \
                (direction[0] < 0 and self.position[0] <= self.end_pos[0]):
            self.position[0] = self.end_pos[0]

        if (direction[1] > 0 and self.position[1] >= self.end_pos[1]) or \
                (direction[1] < 0 and self.position[1] <= self.end_pos[1]):
            self.position[1] = self.end_pos[1]

    def draw(self, surface):
        if self.couleur == "red":
            surface.blit(self.cavalier, (self.position[0], self.position[1]))
        elif self.couleur == "blue":
            surface.blit(self.cavalier_ennemi, (self.position[0], self.position[1]))


# Liste pour stocker les cubes
cubes = []


def create_moving_cube(start_pos, end_pos, speed, attaquant, attaqué, couleur, cavalier):
    cube = Cube(start_pos, end_pos, speed, attaquant, attaqué, couleur, cavalier)
    cubes.append(cube)


class Pays:
    def __init__(self, nom, liste_adjacents, rect, troupes: int, rendement: int, couleur, taille):
        self.etat = False
        self.taille = taille
        self.nom = nom
        self.liste_adjacents = liste_adjacents
        self.rect = rect
        self.troupes = troupes
        self.rendement = rendement
        if couleur == "blanc":
            self.couleur = "black"  # pour couleur police
        elif couleur == "rouge":
            self.couleur = "red"
        else:
            self.couleur = "blue"

        self.running = True

    def __str__(self):
        return self.nom

    def deplacement(self, autre_pays):
        if autre_pays not in self.liste_adjacents:
            return "impossible"
        elif autre_pays.couleur == self.couleur:
            autre_pays.troupes += self.troupes
            self.troupes = 0
        elif self.troupes < autre_pays.troupes:
            autre_pays.troupes -= self.troupes
            self.troupes = 0
        elif self.troupes > autre_pays.troupes:
            autre_pays.couleur = self.couleur
            autre_pays.troupes = self.troupes - autre_pays.troupes
            self.troupes = 0
        elif self.troupes == autre_pays.troupes:
            self.troupes = 0
            autre_pays.troupes = 0

    def augmenter_armee(self):
        if self.couleur == "black" or self.etat == True:
            pass
        else:
            self.etat = True
            while self.running:
                time.sleep(1)
                self.troupes += self.rendement

    def stop_augmenter_armee(self):
        self.running = False
        self.thread.join()


UK = Pays("UK", ("France", "Allemagne"), ((400, 250), (90, 80)), 100, 10, "rouge", 50)
France = Pays("France", ("UK", "Allemagne", "Italie", "Espagne"), ((430, 400), (165, 80)), 100, 10, "blanc", 50)
Espagne = Pays("Espagne", ("France"), ((260, 580), (180, 80)), 100, 10, "blanc", 50)
Allemagne = Pays("Allemagne", ("France", "Italie", "UK", "Autriche", "Pologne"), ((560, 300), (190, 70)), 100, 10,
                 "blanc", 45)
Italie = Pays("Italie", ("France", "Allemagne", "Autriche"), ((600, 460), (140, 70)), 100, 10, "blanc", 46)
Pologne = Pays("Pologne", ("Allemagne", "Autriche", "Ukraine", "Estonie"), ((780, 260), (165, 70)), 100, 10, "blanc",
               50)
Autriche = Pays("Autriche", ("Allemagne", "Grece", "Ukraine", "Serbie", "Italie", "Pologne"), ((760, 390), (170, 70)),
                100, 20, "blanc", 46)
Serbie = Pays("Serbie", ("Autriche", "Grece", "Ukraine", "Serbie", "Estonie", "Pologne"), ((940, 440), (140, 70)), 100,
              10, "blanc", 46)
Grece = Pays("Grece", ("Autriche", "Serbie", "Turquie"), ((920, 560), (150, 70)), 100, 10, "blanc", 50)
Estonie = Pays("Estonie", ("Pologne", "Russie", "Ukraine"), ((950, 200), (150, 70)), 100, 10, "blanc", 46)
Russie = Pays("Russie", ("Estonie", "Turquie", "Ukraine"), ((1200, 220), (185, 80)), 100, 10, "blanc", 60)
Ukraine = Pays("Ukraine", ("Estonie", "Serbie", "Pologne", "Russie", "Autriche"), ((1050, 355), (185, 70)), 100, 10,
               "blanc", 55)
Turquie = Pays("Turquie", ("Grece", "Russie"), ((1150, 640), (190, 85)), 100, 10, "bleu", 55)

liste = (UK, France, Espagne, Allemagne, Italie, Pologne, Autriche, Serbie, Grece, Estonie, Russie, Ukraine, Turquie)
liste_noms = (
    "UK", "France", "Espagne", "Allemagne", "Italie", "Pologne", "Autriche", "Serbie", "Grece", "Estonie", "Russie",
    "Ukraine", "Turquie")


class Client:
    def __init__(self, host, port):
        global numero
        self.start_boutton = pygame.Rect((450, 460), (650, 260))
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))
        self.message = []
        self.numero = 0
        self.pays_clique = ""
        self.class_pays_clique = ""
        self.V = False
        self.D = False
        self.attaque = False
        self.deplacement = False
        self.deplacement_adverse = False
        self.running = True
        self.jeu = False
        self.chargement=False
        self.input_text = ""
        self.cubes = cubes

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1620, 860))
        pygame.display.set_caption("Risque")
        self.font = pygame.font.Font(None, 30)
        self.cavalier = pygame.image.load("asset/cavalier.png")
        self.cavalier_ennemi = pygame.image.load("asset/cavalier_ennemi.png")
        self.fond = pygame.image.load('asset/Map.jpg')
        self.Menu_image = pygame.image.load('asset/Menu.jpg')
        self.Victoire_image = pygame.image.load('asset/Victoire.jpg')
        self.Defaite = pygame.image.load('asset/Defaite.jpg')
        self.fond = self.fond.convert()
        self.fond = pygame.transform.scale(self.fond, (1510, 780))
        self.cavalier = pygame.transform.scale(self.cavalier, (80, 80))
        self.cavalier_ennemi = pygame.transform.scale(self.cavalier_ennemi, (80, 80))

        pygame.mixer.music.load("asset/march-of-thousand-battles-123153.mp3")
        pygame.mixer.music.play(-1)

        pygame.mixer.set_num_channels(2)
        self.cheval = pygame.mixer.Sound("asset/cheval.mp3")
        self.combat = pygame.mixer.Sound("asset/battle.mp3")
        self.canal_1 = pygame.mixer.Channel(0)
        self.canal_2 = pygame.mixer.Channel(1)
        self.cheval.set_volume(100)

        self.Menu_image = self.Menu_image.convert()
        self.Menu_image = pygame.transform.scale(self.Menu_image, (1410, 750))
        self.Victoire_image = self.Victoire_image.convert()
        self.Victoire_image = pygame.transform.scale(self.Victoire_image, (1410, 750))
        self.Defaite = self.Defaite.convert()
        self.Defaite = pygame.transform.scale(self.Defaite, (1410, 750))

        self.thread_receive = threading.Thread(target=self.receive_messages)
        self.thread_receive.start()
        self.clock = pygame.time.Clock()
        self.mainloop()

    def receive_messages(self):
        while self.running:
            try:
                message = self.conn.recv(1024).decode("utf-8")
                if message == ("Vous etes client1"):
                    self.numero = "red"
                elif message == ("Vous etes client2"):
                    self.numero = "blue"
                elif message == ("start"):
                    self.jeu = True

                for i in range(len(liste_noms)):
                    for j in range(len(liste_noms)):
                        if message == (liste_noms[i] + "-" + liste_noms[j]):
                            self.message = (liste_noms[i] + "-" + liste_noms[j])
                            self.attaque = True
                        if message == (liste_noms[i] + "+" + liste_noms[j]):
                            self.message = (liste_noms[i] + "+" + liste_noms[j])
                            self.attaque = True
            except:
                self.running = False

    def mainloop(self):
        while self.running:

            if self.jeu:
                potentiellement_perdu_rouge = 0
                potentiellement_perdu_bleu = 0
                for pays in liste:
                    pays.thread = threading.Thread(target=pays.augmenter_armee)
                    pays.thread.start()

                    if pays.couleur == "red":
                        potentiellement_perdu_rouge += 1

                    if pays.couleur == "blue":
                        potentiellement_perdu_bleu += 1

                    if potentiellement_perdu_rouge == len(liste):
                        if self.numero == 'red':
                            self.V = True
                        elif self.numero == "blue":
                            self.D = True
                    if potentiellement_perdu_bleu == len(liste):
                        if self.numero == "blue":
                            self.V = True
                        elif self.numero == "red":
                            self.D = True

            for event in pygame.event.get():
                if self.jeu:
                    for pays in liste:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                pos = pygame.mouse.get_pos()

                                rect_pays = pygame.Rect(pays)

                                if rect_pays.collidepoint(pos):
                                    if self.deplacement == False:
                                        if self.pays_clique == "":
                                            if pays.couleur == self.numero:
                                                self.pays_clique = pays.nom
                                                self.class_pays_clique = pays

                                        else:
                                            if pays.couleur != self.numero and self.pays_clique in pays.liste_adjacents:
                                                # self.deplacement = True
                                                cavalier = self.class_pays_clique.troupes

                                                create_moving_cube(self.class_pays_clique.rect[0], pays.rect[0], 5,
                                                                   self.class_pays_clique, pays,
                                                                   self.class_pays_clique.couleur, cavalier)

                                                self.class_pays_clique.troupes = 0

                                                nom = pays.nom
                                                attaquant = self.pays_clique.encode("utf-8")
                                                attaqué = nom.encode("utf-8")
                                                attaque_log = attaquant + b"-" + attaqué
                                                self.conn.send(attaque_log)
                                                self.pays_clique = ""
                                            elif pays.couleur == self.numero and self.pays_clique in pays.liste_adjacents:
                                                cavalier = self.class_pays_clique.troupes
                                                create_moving_cube(self.class_pays_clique.rect[0], pays.rect[0], 5,
                                                                   self.class_pays_clique, pays,
                                                                   self.class_pays_clique.couleur, cavalier)

                                                self.class_pays_clique.troupes = 0
                                                nom = pays.nom
                                                defendu = nom.encode("utf-8")
                                                defenseur = self.pays_clique.encode("utf-8")
                                                defense_log = defenseur + b"+" + defendu
                                                self.conn.send(defense_log)
                                                self.pays_clique = ""

                if event.type == pygame.QUIT:
                    self.running = False
                    self.jeu = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()

                        rect_boutton = pygame.Rect(self.start_boutton)

                        if rect_boutton.collidepoint(pos):
                            if not self.jeu:
                                message = "pret"
                                message = message.encode("utf-8")
                                self.conn.send(message)
                                self.chargement=True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        message = "pret"
                        message = message.encode("utf-8")
                        self.conn.send(message)
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.jeu = False
                        pygame.quit()
                        sys.exit()
            if self.attaque:
                for i in range(len(liste_noms)):
                    for j in range(len(liste_noms)):
                        if self.message == (liste_noms[i] + "-" + liste_noms[j]):
                            cavalier = liste[i].troupes
                            create_moving_cube(liste[i].rect[0], liste[j].rect[0], 5,
                                               liste[i], liste[j],
                                               liste[i].couleur, cavalier)
                            liste[i].troupes = 0
                            self.attaque = False
                        if self.message == (liste_noms[i] + "+" + liste_noms[j]):
                            cavalier = liste[i].troupes
                            create_moving_cube(liste[i].rect[0], liste[j].rect[0], 5,
                                               liste[i], liste[j],
                                               liste[i].couleur, cavalier)
                            liste[i].troupes = 0
                            self.attaque = False

            def afficher(self, nom, couleur, rect, troupes, taille):
                position = rect[0]
                distance = rect[1]
                police = pygame.font.SysFont("PYHIERO", taille)
                police2 = pygame.font.SysFont("PYHIERO", 25)
                affiche_nom = police.render(nom, 1, couleur)
                affiche_troupes = police2.render(troupes, 1, couleur)
                self.screen.blit(affiche_nom, position)
                self.screen.blit(affiche_troupes, (position[0] + distance[0] / 2 - 38, position[1] + distance[1] / 2))

            if not self.jeu and not self.D and not self.V:
                self.screen.blit(self.Menu_image, (100, 60))
                if self.chargement:
                    police = pygame.font.SysFont("PYHIERO", 100)
                    message="En attente d'un deuxieme joeueur"
                    affichage = police.render(message, 1, "black")
                    self.screen.blit(affichage, (180, 730))
                # pygame.draw.rect(self.screen, "black", self.start_boutton, 10)

            if self.D:
                self.screen.blit(self.Defaite, (100, 60))
            if self.V:
                self.screen.blit(self.Victoire_image, (100, 60))

            if self.jeu and not self.D and not self.V:
                self.screen.blit(self.fond, (0, 0))
                police_team = pygame.font.SysFont("TXTLIB", 100)
                affichage_team = police_team.render(self.numero, 1, self.numero)
                self.screen.blit(affichage_team, (180, 80))

                police = pygame.font.SysFont("PYHIERO", 60)
                affichage = police.render(self.pays_clique, 1, self.numero)
                self.screen.blit(affichage, (180, 730))
                for pays in liste:
                    afficher(self, pays.nom, pays.couleur, pays.rect, str(pays.troupes), pays.taille)

                # pygame.draw.rect(self.screen, "black", pays.rect, 10)
            cubes = [cube for cube in self.cubes if not cube.has_reached_destination()]
            for cube in cubes:
                cube.update()
            for cube in cubes:
                cube.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    host = socket.gethostname()
    port = 50000
    Client(host, port)
