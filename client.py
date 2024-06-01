import socket
import threading
import pygame
import sys
import time


# from host import get_client_number


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


UK = Pays("UK", ("France", "Allemagne"), ((400, 250), (90, 80)), 100, 20, "rouge", 50)
France = Pays("France", ("UK", "Allemagne", "Italie", "Espagne"), ((430, 400), (165, 80)), 100, 25, "blanc", 40)
Espagne = Pays("Espagne", ("France"), ((260, 580), (180, 80)), 100, 25, "blanc", 40)
Allemagne = Pays("Allemagne", ("France", "Italie", "UK", "Autriche", "Pologne"), ((560, 300), (190, 70)), 100, 25,
                 "blanc", 35)
Italie = Pays("Italie", ("France", "Allemagn", "Autriche"), ((600, 460), (140, 70)), 100, 25, "blanc", 36)
Pologne = Pays("Pologne", ("Allemagne", "Autriche", "Ukraine", "Estonie"), ((780, 260), (165, 70)), 100, 25, "blanc",
               40)
Autriche = Pays("Autriche", ("Allemagne", "Grece", "Ukraine", "Serbie", "Italie", "Pologne"), ((760, 390), (170, 70)),
                100, 25, "blanc", 36)
Serbie = Pays("Serbie", ("Autriche", "Grece", "Ukraine", "Serbie", "Estonie", "Pologne"), ((940, 440), (140, 70)), 100,
              25, "blanc", 36)
Grece = Pays("Grece", ("Autriche", "Serbie", "Turquie"), ((920, 560), (150, 70)), 100, 25, "blanc", 40)
Estonie = Pays("Estonie", ("Pologne", "Russie", "Ukraine"), ((950, 200), (150, 70)), 100, 25, "blanc", 36)
Russie = Pays("Russie", ("Estonie", "Turquie", "Ukraine"), ((1200, 220), (185, 80)), 100, 25, "blanc", 50)
Ukraine = Pays("Ukraine", ("Estonie", "Serbie", "Pologne", "Russie", "Autriche"), ((1050, 355), (185, 70)), 100, 25,
               "blanc", 45)
Turquie = Pays("Turquie", ("Gece", "Russie"), ((1150, 640), (190, 85)), 100, 25, "bleu", 45)

liste = (UK, France, Espagne, Allemagne, Italie, Pologne, Autriche, Serbie, Grece, Estonie, Russie, Ukraine, Turquie)
liste_noms = (
    "UK", "France", "Espagne", "Allemagne", "Italie", "Pologne", "Autriche", "Serbie", "Grece", "Estonie", "Russie",
    "Ukraine", "Turquie")


class Client:
    def __init__(self, host, port):
        global screen
        self.start_boutton=pygame.Rect((450, 460), (650, 260))
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))
        self.message = []
        self.numero = 0
        self.pays_clique = ""
        self.class_pays_clique = ""

        self.attaque = False

        self.running = True
        self.jeu = False
        self.input_text = ""

        pygame.init()
        self.screen = pygame.display.set_mode((1620, 860))
        pygame.display.set_caption("Client")
        self.font = pygame.font.Font(None, 30)
        self.fond = pygame.image.load('asset/Map.jpg')
        self.Menu_image=pygame.image.load('asset/Menu.jpg')
        self.Victoire_image=pygame.image.load('asset/Victoire.jpg')
        self.Defaite = pygame.image.load('asset/Defaite.jpg')
        self.fond = self.fond.convert()
        self.fond = pygame.transform.scale(self.fond, (1510, 780))

        self.Menu_image = self.Menu_image.convert()
        self.Menu_image = pygame.transform.scale(self.Menu_image, (1410, 750))
        self.Victoire_image = self.Victoire_image.convert()
        self.Victoire_image = pygame.transform.scale(self.Victoire_image, (1410, 750))
        self.Defaite = self.Defaite.convert()
        self.Defaite = pygame.transform.scale(self.Defaite, (1410, 750))

        self.thread_receive = threading.Thread(target=self.receive_messages)
        self.thread_receive.start()

        self.mainloop()

    def receive_messages(self):
        while self.running:
            try:
                message = self.conn.recv(1024).decode("utf-8")
                print(message)
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
                        if message==(liste_noms[i] + "+" + liste_noms[j]):
                            self.message=(liste_noms[i] + "+" + liste_noms[j])
                            self.attaque=True
            except:
                self.running = False

    def defence_adverse(self, defenseur, defendu):
        defendu.troupes += defenseur.troupes
        defenseur.troupes = 0

    def mainloop(self):
        while self.running:
            if self.jeu:
                for pays in liste:
                    pays.thread = threading.Thread(target=pays.augmenter_armee)
                    pays.thread.start()

            for event in pygame.event.get():
                if self.jeu:
                    for pays in liste:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                pos = pygame.mouse.get_pos()

                                rect_pays = pygame.Rect(pays)

                                if rect_pays.collidepoint(pos):
                                    if self.pays_clique == "":
                                        if pays.couleur == self.numero:
                                            self.pays_clique = pays.nom
                                            self.class_pays_clique = pays

                                    else:
                                        if pays.couleur != self.numero and self.pays_clique in pays.liste_adjacents:
                                            pays.troupes -= self.class_pays_clique.troupes
                                            if pays.troupes < 0:
                                                if self.class_pays_clique.couleur == "red":
                                                    pays.couleur = "red"
                                                    pays.troupes = -pays.troupes

                                                elif self.class_pays_clique.couleur == "blue":
                                                    pays.couleur = "blue"
                                                    pays.troupes = -pays.troupes

                                            self.class_pays_clique.troupes = 0

                                            nom = pays.nom
                                            attaquant = self.pays_clique.encode("utf-8")
                                            attaqué = nom.encode("utf-8")
                                            attaque_log = attaquant + b"-" + attaqué
                                            self.conn.send(attaque_log)
                                            self.pays_clique = ""
                                        elif pays.couleur == self.numero and self.pays_clique in pays.liste_adjacents:
                                            pays.troupes += self.class_pays_clique.troupes
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
                            message = "pret"
                            message = message.encode("utf-8")
                            self.conn.send(message)
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

                            liste[j].troupes -= liste[i].troupes
                            liste[i].troupes = 0
                            if liste[j].troupes < 0:
                                if self.numero == "red":
                                    liste[j].couleur = "blue"
                                elif self.numero == "blue":
                                    liste[j].couleur = "red"
                                liste[j].troupes = -liste[j].troupes

                                self.attaque = False
                        if self.message == (liste_noms[i] + "+" + liste_noms[j]):
                            liste[j].troupes+=liste[i].troupes
                            liste[i].troupes=0
                            self.attaque = False

            def afficher(self, nom, couleur, rect, troupes, taille):
                position = rect[0]
                distance = rect[1]
                police = pygame.font.SysFont("monospace", taille)
                police2 = pygame.font.SysFont("monospace", 25)
                affiche_nom = police.render(nom, 1, couleur)
                affiche_troupes = police2.render(troupes, 1, couleur)
                self.screen.blit(affiche_nom, position)
                self.screen.blit(affiche_troupes, (position[0] + distance[0] / 2 - 38, position[1] + distance[1] / 2))
            if not self.jeu:
                self.screen.blit(self.Menu_image, (100, 60))
                #pygame.draw.rect(self.screen, "black", self.start_boutton, 10)

            if self.jeu:
                self.screen.blit(self.fond, (0, 0))
                for pays in liste:
                    afficher(self, pays.nom, pays.couleur, pays.rect, str(pays.troupes), pays.taille)
                    # pygame.draw.rect(self.screen, "black", pays.rect, 10)

            pygame.display.flip()


if __name__ == "__main__":
    host = socket.gethostname()
    port = 50000
    Client(host, port)
