import sys
import json
from turtle import color
import maya.cmds as cmds

from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit,QCheckBox,
                               QPushButton,QMessageBox, QDialog)

def load_json_file(file_path):
    #Le open me permet d'ouvrir le fichier en mode lecture et de le lire avec l'encodage UTF-8 pour les accents.
     with open(file_path, "r", encoding="utf-8") as f:
        global data
        data = json.load(f) # -----> C:\Users\User\Desktop\NAD\Python\TP2\.vscode\rules.json
        return data


     

class MessageBoard(QWidget): #La class irrite de la class QWidget.
    def __init__(self): # Constructeur
        super().__init__() # Constructeur QWidget
        self.setWindowTitle("Outliner Organiser") # Titre de la fenetre
        self.setFixedSize(400, 200) # Taille de la fenetre
        self.create_ui()

    # Creation de l'interface utilisateur.
    def create_ui(self):
        print("create UI")
        layout = QVBoxLayout(self)
        label = QLabel("Json File Path") # Titre du label
        label.setFixedSize(400, 10) # Taille du label
        layout.addWidget(label)
       
        # Line edit pour le chemin du fichier JSON
        self.File_Path = QLineEdit()
        self.File_Path.setPlaceholderText("Copy here :") # Titre de la barre de recherche
        layout.addWidget(self.File_Path)

        # Bouton a check pour accepter pour activer les paramettre d'organisation du fichier JSON.
        
        # Application sur la selection seulement.
        self.selection_only = QCheckBox("Apply on selection only")
        layout.addWidget(self.selection_only)

        # Application de la couleur.
        self.colors = QCheckBox("Apply colors")
        layout.addWidget(self.colors)

        # Mettre en ordre.
        self.reorder = QCheckBox("Apply re-ordering")
        layout.addWidget(self.reorder)

        # Bouton pour lancer l'organisation du fichier JSON.
        self.organize_button = QPushButton("Organize")
        layout.addWidget(self.organize_button)
        self.organize_button.clicked.connect(self.organize)

  
       


 #---------------------------------------------- LES FONCTIONS PRINCIPALES -----------------------------------------#

    # Tri avec une selection seulement.
    def organize(self):
            
            cmds.undoInfo(openChunk=True, chunkName="Apply Color") # <--- J'ouvre un chunk pour que l'utilisateur puisse annuler l'action en une seule fois.
        
            # Le premier if regarde si selection_only est coche.
            if self.selection_only.isChecked():
                objects = cmds.ls(selection=True)
            else:
                objects = cmds.ls(assemblies=True)

            # Le deuxieme if regarde si colors est coche.
            if self.colors.isChecked():
                self.apply_color(objects)

            # Le troisieme if regarde si reorder est coche.
            if self.reorder.isChecked():
                self.apply_reordering(objects)

            cmds.undoInfo(closeChunk=True) # <--- Je ferme le chunk.      



    # ------------------------------------ FONCTION POUR APPLIQUER LES COULEURS ------------------------------------#
    def apply_color(self, objects):     
    #------------------------------------ BOUCLE DE VERIFICATIONS ------------------------------------#

        data = load_json_file(self.File_Path.text()) # Je speficifie le chemin du fichier JSON que je veux ouvrir et je le charge dans la variable data.

        for item in objects: # <--- JE regarde si l'objet existe dans la scene avant de lui appliquer une couleur.
            if cmds.objExists(item):   

                for prefix, color in data.items(): # <--- Je parcours le dictionnaire data pour recuperer les prefix et les couleurs associer a chaque prefix.
                    if item.startswith(prefix):
                        cmds.setAttr(item + ".useOutlinerColor", True) # <--- Active l'option de couleur dans l'outliner pour l'objet.
                        cmds.setAttr(item + ".outlinerColor", color[0], color[1], color[2]) # <--- Je recupere la couleur associer au prefix et je l'applique a l'objet.
             


    # ------------------------------------ FONCTION POUR ORDONNNER ------------------------------------#
    def apply_reordering(self, objects):

      
        data = load_json_file(self.File_Path.text())
        objects_to_reorder = [] # Creation d'une liste vide pour stocker les objets a reordonner.

        #------------------------------------ BOUCLE DE VERIFICATIONS ------------------------------------#
        
        # Boucle 1 : Identifier les objets à reordonner et les palcer dans une nouvelle liste a ordonner.
        for item in objects:

            for prefix in data:

                if item.startswith(prefix):
                    objects_to_reorder.append(item) # <--- J'ajoute l'objet a la liste des objets a reordonner.

        reordered_objects = sorted(objects_to_reorder) # <--- Fonction python pour creer une nouvelle list triee.

        for item in reversed(reordered_objects): # <--- Je parcours la liste des objets a reordonner dans l'ordre inverse pour que le dernier objet soit en haut de la liste.
            cmds.reorder(item, front=True) # <--- Maya commande pour deplacer l'objet en haut de la liste dans l'outliner.









def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()

