import sys
import json
import maya.cmds as cmds

from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit,QCheckBox,
                               QPushButton,QMessageBox, QDialog)

def load_json_file(file_path):
    #Le open me permet d'ouvrir le fichier en mode lecture et de le lire avec l'encodage UTF-8 pour les accents.
     with open(file_path, "r", encoding="utf-8") as f:
        global data
        data = json.load(f)
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

        # Application sur la selection seulement.
        self.colors = QCheckBox("Apply colors")
        layout.addWidget(self.colors)

        # Application sur la selection seulement.
        self.reorder = QCheckBox("Apply re-ordering")
        layout.addWidget(self.reorder)

        # Bouton pour lancer l'organisation du fichier JSON.
        self.organize_button = QPushButton("Organize")
        layout.addWidget(self.organize_button)
        self.organize_button.clicked.connect(apply_color)

       


#------------------------------------ Fonction principale ------------------------------------#

 # Tri avec une selection seulement.

# Appliquer une couleur sur les elements selectionner en rapport avec le Key.
def apply_color(self):
   


    selected_objects = cmds.ls(selection=True)


    for item in selected_objects:
        if cmds.objExists(item):   

       
            cmds.setAttr(item + ".useOutlinerColor", True)
            cmds.setAttr(item + ".outlinerColor", 1, 0, 0)  # Rouge

         
           
        else:
            return False

           
        
       
# appliquer un re-ordering sur les elements selectionner en ordre croissant.



def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()

