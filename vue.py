import tkinter
import modele

class VueModele:

    def __init__(self, modele):
        self.__BASE = 30
        self.__COULEURS = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'dark grey', 'black']
        self.__SUIVANT = 6
        self.__modele = modele
        self.__fen = tkinter.Tk()
        self.__can_terrain = tkinter.Canvas(self.__fen, width=self.__modele.get_largeur()*self.__BASE, height=self.__modele.get_hauteur()*self.__BASE)
        self.__can_terrain.grid(row=0, column=0)
        frame_droite = tkinter.Frame(self.__fen)
        self.__btn_quitter = tkinter.Button(frame_droite, text="quitter", command=self.__fen.destroy)
        self.__btn_quitter.grid(row=3, column=0)
        self.__lbl_score = tkinter.Label(frame_droite, text="Score : 0")
        self.__lbl_score.grid(row=2, column=0)
        self.__btn_start = tkinter.Button(frame_droite, text="commencer")
        self.__btn_start.grid(row=4, column=0)
        lbl_formeSuiv = tkinter.Label(frame_droite, text='Forme suivante :')
        lbl_formeSuiv.grid(row=0, column=0)
        self.__can_fsuivante = tkinter.Canvas(frame_droite, width=self.__SUIVANT*self.__BASE, height=self.__SUIVANT*self.__BASE)
        self.__can_fsuivante.grid(row=1, column=0)
        frame_droite.grid(row=0, column=1)
        self.dessiner_cases()
        self.dessiner_cases_suivantes()
        self.dessine_forme_suivante(modele.get_coords_suivante(), modele.get_couleur_suivante())

    def met_a_jour_score(self, val):
        self.__lbl_score['text'] = 'Score : '+str(val)

    def dessiner_cases(self):
        self.__les_cases = []
        for lig in range(self.__modele.get_hauteur()):
            ligne = []
            for col in range(self.__modele.get_largeur()):
                ligne.append(self.__can_terrain.create_rectangle(col*self.__BASE, lig*self.__BASE, (col+1)*self.__BASE-1, (lig+1)*self.__BASE-1, fill=self.__COULEURS[self.__modele.get_valeur(lig, col)], outline='grey'))
            self.__les_cases.append(ligne)

    def dessiner_cases_suivantes(self):
        self.__les_suivants = []
        for lig in range(self.__BASE):
            ligne = []
            for col in range(self.__BASE):
                ligne.append(self.__can_fsuivante.create_rectangle(col*self.__BASE, lig*self.__BASE, (col+1)*self.__BASE-1, (lig+1)*self.__BASE-1, fill='black', outline='grey'))
            self.__les_suivants.append(ligne)

    def fenetre(self):
        return self.__fen

    def dessine_case(self, lig, col, coul):
        if self.__can_terrain.itemconfigure(self.__les_cases[lig][col], 'fill') != coul:
            self.__can_terrain.itemconfigure(self.__les_cases[lig][col], fill=coul)

    def dessine_case_suivante(self, lig, col, coul):
        self.__can_fsuivante.itemconfigure(self.__les_suivants[lig][col], fill=coul)

    def nettoie_forme_suivante(self):
        for lig in range(self.__BASE):
            for col in range(self.__BASE):
                self.__can_fsuivante.itemconfigure(self.__les_suivants[lig][col], fill='black')

    def dessine_terrain(self):
        for lig in range(self.__modele.get_hauteur()):
            for col in range(self.__modele.get_largeur()):
                self.dessine_case(lig, col, self.__COULEURS[self.__modele.get_valeur(lig, col)])

    def dessine_forme(self, coords, couleur):
        for col,lig in coords:
            self.dessine_case(lig, col, self.__COULEURS[couleur])

    def dessine_forme_suivante(self, coords, couleur):
        self.nettoie_forme_suivante()
        for col,lig in coords:
            self.dessine_case_suivante(lig+2, col+2, self.__COULEURS[couleur])

    def setStartButtonCallback(self, cbk):
        self.__btn_start['command'] = cbk

    def setStartButtonLbl(self, lbl):
        self.__btn_start['text'] = lbl

    def setModel(self, modele):
        self.__modele = modele
