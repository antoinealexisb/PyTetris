import random

LES_FORMES = [[(-1,-1),(-1,0),(0,0),(1,0)], [(-1,1),(-1,0),(0,0),(1,0)], [(-1,-1),(0,-1),(0,0),(1,0)], [(-1,0),(0,0),(0,-1),(1,0)]]

class ModeleTetris:

    def __init__(self, larg=14, haut=20):
        self.__base = 4
        self.__haut = haut+self.__base
        self.__larg = larg
        self.__terrain = [[-2]*self.__larg]*self.__base + [[-1]*self.__larg]*(self.__haut-self.__base)
        self.__score = 0
        self.__terrain = []
        for i in range(self.__base):
            ligne = []
            for j in range(self.__larg):
                ligne.append(-2)
            self.__terrain.append(ligne)
        for i in range(self.__haut-self.__base):
            ligne = []
            for j in range(self.__larg):
                ligne.append(-1)
            self.__terrain.append(ligne)
        self.__forme = Forme(self)
        self.__suivante = Forme(self)
        

    def get_base(self):
        return self.__base

    def get_largeur(self):
        return self.__larg

    def get_hauteur(self):
        return self.__haut

    def get_valeur(self, l, c):
        return self.__terrain[l][c]

    def est_occupe(self, l, c):
        return self.get_valeur(l,c) >= 0

    def fini(self):
        for i in range(self.__larg) :
            if self.est_occupe(self.__base, i):
                return True
        return False

    def ajoute_forme(self):
        for col,lig in self.__forme.get_coords():
            self.__terrain[lig][col] = self.__forme.get_couleur()

    def forme_tombe(self):
        if self.__forme.tombe():
            return False
        self.ajoute_forme()
        self.supprime_lignes_completes()
        self.__forme = self.__suivante
        self.__suivante = Forme(self)
        return True

    def get_couleur_forme(self):
        return self.__forme.get_couleur()

    def get_couleur_suivante(self):
        return self.__suivante.get_couleur()

    def get_coords_forme(self):
        return self.__forme.get_coords()

    def get_coords_suivante(self):
        return self.__suivante.get_coords_relatives()

    def forme_a_gauche(self):
        self.__forme.a_gauche()

    def forme_a_droite(self):
        self.__forme.a_droite()

    def forme_tourne(self):
        self.__forme.tourne()

    def est_ligne_complete(self, lig):
        for val in self.__terrain[lig]:
            if val < 0:
                return False
        return True

    def supprime_ligne(self, lig):
        del self.__terrain[lig]
        self.__terrain.insert(self.__base, [-1]*self.__larg)

    def supprime_lignes_completes(self):
        for lig in range(self.__base, self.__haut):
            if self.est_ligne_complete(lig):
                self.supprime_ligne(lig)
                self.__score += 1

    def get_score(self):
        return self.__score


class Forme:

    def __init__(self, modele):
        self.__modele = modele
        n = random.randint(0, len(LES_FORMES)-1)
        self.__couleur = n
        self.__forme = LES_FORMES[n]
        self.__x0 = random.randint(2, self.__modele.get_largeur()-3)
        self.__y0 = 2

    def get_couleur(self):
        return self.__couleur

    def get_coords(self):
        coords = []
        for x,y in self.__forme:
            coords.append((x+self.__x0,y+self.__y0))
        return coords

    def get_coords_relatives(self):
        return self.__forme

    def collision(self):
        for col,lig in self.get_coords() :
            if lig == self.__modele.get_hauteur()-1:
                return True
            if self.__modele.est_occupe(lig+1, col):
                return True
        return False

    def tombe(self):
        if self.collision():
            return False
        self.__y0 += 1
        return True

    def position_valide(self):
        for col,lig in self.get_coords():
            if not(0 <= lig < self.__modele.get_hauteur()):
                return False
            if not(0 <= col < self.__modele.get_largeur()):
                return False
            if self.__modele.est_occupe(lig, col):
                return False
        return True

    def a_gauche(self):
        for col,lig in self.get_coords():
            if col == 0:
                return
        self.__x0 -= 1
        if not self.position_valide():
            self.__x0 += 1

    def a_droite(self):
        for col,lig in self.get_coords():
            if col == self.__modele.get_largeur()-1:
                return
        self.__x0 += 1
        if not self.position_valide():
            self.__x0 -= 1

    def tourne(self):
        forme_prec = self.__forme
        self.__forme = []
        for x,y in forme_prec:
            self.__forme.append((-y,x))
        if not self.position_valide():
            self.__forme = forme_prec
