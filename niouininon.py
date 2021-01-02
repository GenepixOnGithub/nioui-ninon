import sys
import speech_recognition as sr
import pyttsx3
import random
from random import randint
import os
import requests
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from playsound import playsound


class NiOuiNiNonView(QWidget):
    def __init__(self):
        super().__init__()
        self.runs_count = 15
        voice_speed = 200 # vitesse de la parole
        self.current_run = 0
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("voice", "french")
        self.engine.setProperty("rate", voice_speed)
        # Init window
        self.init_window()      

    def init_window(self):
        self.setWindowTitle("GENEPIX Geolocalisation")
        self.setGeometry(300,300, 800,600)
        self.main_layout = QVBoxLayout()
        self.lbl_logo = QLabel(self)
        pixmap = QPixmap('img/genepix_niouininon.png')
        self.lbl_logo.setPixmap(pixmap)
        self.lbl_sentence = QLabel(self)
        self.lbl_sentence.setStyleSheet("color: #fff;")
        self.lbl_instructions = QLabel(self)
        self.lbl_instructions.setStyleSheet("color: #00ff00;")
        self.setStyleSheet("background-color: #222; color: #fff; font-weight: bold;")          
        self.btn_launch = QPushButton("Lancer le jeu")
        self.btn_launch.setStyleSheet("background-color: #00f2ec; color: #222; padding: 15px; border-radius: 3px;")
        self.main_layout.addWidget(self.lbl_logo)
        self.main_layout.addWidget(self.lbl_sentence)
        self.main_layout.addWidget(self.lbl_instructions)
        self.main_layout.addWidget(self.btn_launch)
        self.btn_launch.clicked.connect(self.launch_game)
        self.setLayout(self.main_layout)

    def get_sound(self):
        with sr.Microphone() as source:
            playsound('couin.mp3')
            self.lbl_instructions.setText("A toi de parler...")
            self.lbl_instructions.setStyleSheet("color: #00ff00")
            self.repaint()
            try:
                sound = self.r.listen(source)
                sound = self.r.recognize_google(sound, language="fr-FR")
                self.lbl_instructions.setText("Attends avant de parler...")
                self.repaint()
                if sound is None:
                    self.engine_say("Je n'ai pas bien compris, peux tu répéter?")
                    return self.get_sound()
                return sound
            except:
                self.engine_say("Je n'ai pas bien compris, peux tu répéter?")
                return self.get_sound()

    def engine_say(self, sentence):
        self.lbl_sentence.setText(sentence)
        self.lbl_instructions.setText("Attends avant de parler...")
        self.lbl_instructions.setStyleSheet("color: #ff0000;")
        self.repaint()
        self.engine.say(sentence)
        self.engine.runAndWait()

    def scrap_question(self):
        r = requests.get("https://www.jeu-de-soiree.fr/generateur/questions-indiscretes")
        html = r.text
        pos1 = html.find("<h2>")
        pos2 = html.find("</h2>")
        punch = html[pos1:pos2]
        punch = punch.replace("<h2>", "")
        punch = punch.replace("\"", "")
        punch = punch.split()
        question = " ".join(punch)
        return question  

    def launch_game(self):
        self.engine_say("Bienvenue, quel est ton prénom ?")
        prenom = self.get_sound()
        self.engine_say(f"Salut {prenom}, t'es chaud? C'est parti.")

        while(self.current_run <= self.runs_count):
            print(f"Run {self.current_run}")
            question = self.scrap_question()
            self.engine_say(question)
            reponse = self.get_sound()
            if reponse.find("oui") != -1 or reponse.find("non") != -1:
                self.engine_say(f"Déso, tu as perdu au tour numéro {str(self.runs_count + 1)} espèce de gros naze.")
                break
            self.current_run += 1
            # v += 30 # Pour accélérer le son de la voix 

        if self.current_run == self.runs_count:
            self.engine_say(f"Bravo {prenom} tu as gagné ! L'équipe de Génépix te félicite !")                  


myApp = QApplication(sys.argv)
window = NiOuiNiNonView()
window.show() 
myApp.exec_()
sys.exit(0)
