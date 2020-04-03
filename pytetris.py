import modele
import vue
import time

class Controleur:
    
    def __init__(self, modele):
        self.__tetris = modele
        self.__vue = vue.VueModele(modele)
        self.__vue.dessine_forme(modele.get_coords_forme(), modele.get_couleur_forme())
        self.__delai_init = 320
        self.__delai = self.__delai_init
        self.__fen = self.__vue.fenetre()
        self.__fen.bind("<Key-Left>", self.forme_a_gauche)
        self.__fen.bind("<Key-Right>", self.forme_a_droite)
        self.__fen.bind("<Key-Down>", self.forme_tombe)
        self.__fen.bind("<Key-Up>", self.forme_tourne)
        self.__vue.setStartButtonCallback(self.start)
        self.__on_pause = False
        self.__fen.mainloop()

    def start(self):
        self.__vue.setStartButtonLbl('pause')
        self.__vue.setStartButtonCallback(self.toggle_pause)
        self.joue()

    def joue(self):
        if not self.__tetris.fini() and not self.__on_pause:
            self.affichage()
            self.__job = self.__fen.after(self.__delai, self.joue)
            if self.__tetris.fini():
                self.__vue.setStartButtonLbl('recommencer')
                self.__vue.setStartButtonCallback(self.restart)

    def restart(self):
        self.__tetris = modele.ModeleTetris()
        self.__vue.setModel(self.__tetris)
        self.__vue.setStartButtonLbl('commencer')
        self.__vue.setStartButtonCallback(self.start)
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())

    def toggle_pause(self):
        if self.__on_pause :
            self.__on_pause = False
            self.__vue.setStartButtonLbl('pause')
            self.__job = self.__fen.after(0, self.joue)
        else:
            self.__fen.after_cancel(self.__job)
            self.__on_pause = True
            self.__vue.setStartButtonLbl('reprendre')

    def affichage(self):
        if self.__tetris.forme_tombe():
            self.__delai = self.__delai_init
            self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivante(), self.__tetris.get_couleur_suivante())
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())
        self.__vue.met_a_jour_score(self.__tetris.get_score())

    def forme_a_gauche(self, event):
        self.__tetris.forme_a_gauche()

    def forme_a_droite(self, event):
        self.__tetris.forme_a_droite()

    def forme_tombe(self, event):
        self.__delai = 100

    def forme_tourne(self, event):
        self.__tetris.forme_tourne()
        

if __name__ == "__main__":
    tetris = modele.ModeleTetris()
    ctrl = Controleur(tetris)
