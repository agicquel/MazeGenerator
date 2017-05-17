# importation de la lib graphique
from tkinter import *
# importation de la lib pour générer un nombre aléat
from random import randint
import time

# Création d'une fenêtre, base de l'interface
fenetre = Tk()
fenetre.title('Interface')

# Création d'un LabelFrame ayant comme titre: "Projet ISN : Labyrinthe"
# Fonction permettant l'agrandissement auto du LabelFrame
LF1 = LabelFrame(fenetre, text="Projet ISN : Labyrinthe", padx=5, pady=5, bg="white")
LF1.pack(fill="both", expand="yes")

# Ajout Frame -> Affichage du labyrinthe
Frame1 = Frame(LF1, relief=GROOVE, bg="white")
Frame1.pack(side=LEFT, padx=50, pady=0)
canvas = Canvas(Frame1, width=512, height=512, bg="ivory")
canvas.pack(side=BOTTOM, padx=0, pady=0)
Label1 = Label(Frame1,text="Affichage du labyrinthe", bg="gold")
Label1.pack()

# Ajout Frame -> Contient la Génération et la résolution du labyrinthe
Frame2 = Frame(LF1, relief=GROOVE, bg="white")
Frame2.pack(side=RIGHT, padx=50, pady=0)

class Cellule (object):
    # Classe Cellule pour chaque case du damier

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.couleur = "black"
        self.carre = canvas.create_rectangle(x*size, y*size, (x+1)*size, (y+1)*size, fill=self.couleur, outline=self.couleur)
        self.valeur = 0 # 0 = jamais été atteinte; 1=doite; 2=gauche; 3=haut; 4=bas

    def change_couleur(self, nvl_couleur):
        self.couleur = nvl_couleur
        canvas.itemconfig(self.carre, fill=self.couleur, outline=self.couleur) # changer couleur

class Chronometre (object):

    def __init__(self):
        self.initial_clock = time.time()
        self.clock = 0

    def chronometrer(self):
        # seconde écoulé
        self.clock = time.time() - self.initial_clock
        minute = str(int(self.clock // 60))
        seconde = str(int(self.clock % 60))
        return (minute + " min " + seconde + " sec")


class Labyrinthe (object):

    def __init__(self):
        self.liste = []
        self.resolu = False

    def creation(self):
        # creation du damier, contenu dans une liste
        # vide la liste au cas ou elle n'est pas vierge
        self.liste[:] = []
        # On recupere la taille voulu d'apres le SpinBox
        self.cote = int(SB.get())
        self.size = 512/self.cote
        i = 0
        o = 0

        while i<self.cote:
            while o<self.cote:
                case = Cellule(o, i, self.size)
                self.liste.append(case)
                o = o+1
            i = i+1
            o = 0

    def generation(self):

        # on recreer le damier en noir
        self.creation()
        clock = Chronometre()

        # Le point de départ (à peu pres au milieu)
        pos = int(len(self.liste)/2-self.cote/2)
        self.liste[pos].valeur = -1
        self.liste[pos].change_couleur("red")

        # definition des variables necessaires
        fin = True
        orientation = []

        while fin:

            canvas.update_idletasks()
            # un petit delay si on veut (en sec)
            time.sleep(0.000005)
            # On update le Chronometre
            genClockLabel1.configure(text=clock.chronometrer())

            # on regarde les chemins possibles
            if self.liste[pos + 2].valeur == 0 and self.liste[pos + 2].x != self.cote and self.liste[pos + 2].x != 0:
                orientation.append("droite")
            if self.liste[pos - 2].valeur == 0 and self.liste[pos - 2].x != self.cote and self.liste[pos - 2].x != 0:
                orientation.append("gauche")
            if self.liste[pos + (2*self.cote)].valeur == 0 and self.liste[pos + (2*self.cote)].y <= (self.cote-2) and self.liste[pos + (2*self.cote)].y >= 0:
                orientation.append("haut")
            if self.liste[pos - (2*self.cote)].valeur == 0 and self.liste[pos - (2*self.cote)].y <= (self.cote-2) and self.liste[pos - (2*self.cote)].y >= 0:
                orientation.append("bas")

            # on en choisis un possible aleatoirement si possible
            if len(orientation) != 0:
                alea = randint(0,len(orientation))
                alea -= 1
                # puis on deplace le curseur
                if orientation[alea] == "droite":
                    pos += 2
                    self.liste[pos].valeur = 1
                    self.liste[pos-1].change_couleur("white")
                if orientation[alea] == "gauche":
                    pos -= 2
                    self.liste[pos].valeur = 2
                    self.liste[pos+1].change_couleur("white")
                if orientation[alea] == "haut":
                    pos += (2*self.cote)
                    self.liste[pos].valeur = 3
                    self.liste[pos-self.cote].change_couleur("white")
                if orientation[alea] == "bas":
                    pos -= (2*self.cote)
                    self.liste[pos].valeur = 4
                    self.liste[pos+self.cote].change_couleur("white")
                # on colorie en blanc la case
                self.liste[pos].change_couleur("white")

            # Sinon on recule
            else:
                if self.liste[pos].valeur == 1:
                    pos -= 2
                if self.liste[pos].valeur == 2:
                    pos += 2
                if self.liste[pos].valeur == 3:
                    pos -= (2*self.cote)
                if self.liste[pos].valeur == 4:
                    pos += (2*self.cote)

            # si on retourne a la case de depart et que toute les issues sont decouvertes
            if self.liste[pos].valeur == -1 and len(orientation) == 0:
                fin  = False

            orientation[:] = [] # vide la liste

        # on trouve un point de sortie aleatoirement qui est
        # sur une case blache et sur les 10 premieres lignes du labyrinthe
        sortie = 0
        while self.liste[sortie].couleur in "black":
            sortie = randint(self.cote,self.cote*10)
        self.liste[sortie].valeur = -2
        self.liste[sortie].change_couleur("red")

        # lorsqu'un un labyrinthe est généré, il est de base pas résolu
        self.resolu = False

        # on rafraichi l'écran
        canvas.update_idletasks()

    def resolution(self):

        # On remet toutes les cases à la valeur 0 et colorie la case initial en vert
        i = 0
        pos = 0
        pos_fin = 0
        while i < (self.cote*self.cote):
            if self.liste[i].valeur == -2:
                pos_fin = i
            if self.liste[i].valeur == -1:
                pos = i
            else:
                self.liste[i].valeur = 0
            i+=1

        # on commence la résolution si ce n'est pas deja fait
        fin = False
        if self.resolu == False:
            fin = True
        orientation = "aucune"
        clock = Chronometre()

        while fin:

            canvas.update_idletasks()
            # un petit delay si on veut (en sec)
            time.sleep(0.000005)
            # On update le Chronometre
            resClockLabel1.configure(text=clock.chronometrer())

            # on regarde les chemins possibles
            orientation = "aucune"
            if self.liste[pos + 1].valeur == 0 and (self.liste[pos+1].couleur in "black") == False:
                orientation = "droite"
            if self.liste[pos - 1].valeur == 0 and (self.liste[pos-1].couleur in "black") == False:
                orientation = "gauche"
            if self.liste[pos + self.cote].valeur == 0 and (self.liste[pos + self.cote].couleur in "black") == False:
                orientation = "haut"
            if self.liste[pos - self.cote].valeur == 0 and (self.liste[pos - self.cote].couleur in "black") == False:
                orientation = "bas"

            # Si un chemin est possible
            if orientation != "aucune":
                # puis on deplace le curseur
                if orientation == "droite":
                    pos += 1
                    self.liste[pos].valeur = 1
                if orientation == "gauche":
                    pos -= 1
                    self.liste[pos].valeur = 2
                if orientation == "haut":
                    pos += self.cote
                    self.liste[pos].valeur = 3
                if orientation == "bas":
                    pos -= self.cote
                    self.liste[pos].valeur = 4
                # on colorie en blanc la case
                self.liste[pos].change_couleur("green")

            # sinon on recule en recoloriant les cases en blanc
            else:
                self.liste[pos].change_couleur("white")
                if self.liste[pos].valeur == 1:
                    pos -= 1
                elif self.liste[pos].valeur == 2:
                    pos += 1
                elif self.liste[pos].valeur == 3:
                    pos -= self.cote
                elif self.liste[pos].valeur == 4:
                    pos += self.cote
                else:
                    self.liste[pos].change_couleur("white")

            # si on trouve la sortie (val = -2)
            if pos == pos_fin:
                self.liste[pos].change_couleur("red")
                fin  = False

        # on declare le labyrinthe comme resolu
        self.resolu = True

# on declare le projet, de classe Labyrinthe
projet = Labyrinthe()

# Ajout d'une FrameLabel et d'un Bouton-> Gestion de la génération
LF2 = LabelFrame(Frame2, text="Gestion de la génération", padx=64, pady=64, bg="white")
LF2.pack(side=TOP,fill="both", expand="yes")
# Bouton de la génération
bouton = Button(LF2, text="Génération", command=projet.generation, bg="white")
bouton.pack(side=TOP, pady=16)
# La SpinBox pour choisir la taille du labyrinthe
SB_label = Label(LF2, text="Taille en pixel du coté du Labyrinthe")
SB_label.pack(side=TOP)
SB = Spinbox(LF2, values=(32, 64, 128, 256, 512))
SB.pack(side=TOP, pady=(0, 16))

# Ajout d'une FrameLabel et d'un Bouton-> Gestion de la résolution
LF3 = LabelFrame(Frame2, text="Gestion de la résolution", padx=64, pady=64, bg="white")
LF3.pack(side=BOTTOM, fill="both", expand="yes")
bouton = Button(LF3, text="Résolution", command=projet.resolution, bg="white")
bouton.pack(pady=16)

# Les chronometres
genClockLabel1 = Label(LF2, text="0 min 0 sec")
genClockLabel1.pack(side=BOTTOM)
genClockLabel2 = Label(LF2, text="Temps écoulé")
genClockLabel2.pack(side=BOTTOM)

resClockLabel1 = Label(LF3, text="0 min 0 sec")
resClockLabel1.pack(side=BOTTOM)
resClockLabel2 = Label(LF3, text="Temps écoulé")
resClockLabel2.pack(side=BOTTOM)

# Démarrage boucle Tkinter
fenetre.mainloop()
