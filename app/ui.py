import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

# On fait une classe qui dérive de QMainWindow, ca sera notre
# fenetre général du logiciel
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):

        # on oublie pas d'appeler l'init de la classe parent ( QMainWindow ! )
        super(MainWindow, self).__init__(parent=parent)

        # on set un titre à la fenetre
        self.setWindowTitle("mp3 reader")
        self.setWindowIcon(QIcon("audio.png"))
        
        # on créer on objet QMediaPlayer, c'est dans cette objet qu'on va ajouter
        # les musiques qu'on veut lire, c'est aussi avec lui qu'on va faire .play(),
        # .stop() et .pause() de la musique
        self.media_player = QMediaPlayer()

        # on fait le layout général de la fenetre ( comment seront agencer les widgets )
        # on fait aussi un QWidget de base qui sera utilisé comme central widget par
        # la fenetre, c'est a ce widget là qu'on va assigner le layout général
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignTop) # on peut décider d'un alignement ( top, left, right ...)
        central_layout.setSpacing(5)        
        central_widget = QWidget()

        # on fait un autre layout, cette fois ci horizontal pour pouvoir mettre de fauche a droit:
        # un label "Fichier: ", un line edit qui servira de chemin vers le mp3 qu'on veut lire
        # et un button qui va ouvrir un explorateur de fichier pour aller piquer le mp3
        # on ajoute donc ces widgets là au input_layout et non pas au layout general ( central_layout )
        input_layout = QHBoxLayout()
        input_layout.setAlignment(Qt.AlignLeft)
        input_label = QLabel("Dossier:")
        input_layout.addWidget(input_label)

        self.file_path_input = QLineEdit()
        self.file_path_input.returnPressed.connect(self.returned_pressed_folder)
        input_layout.addWidget(self.file_path_input)

        self.pick_folder_btn = QPushButton("")
        self.pick_folder_btn.setIcon(QIcon("file.png"))
        self.pick_folder_btn.setIconSize(QSize(32, 32))
        self.pick_folder_btn.clicked.connect(self.pick_folder)
        input_layout.addWidget(self.pick_folder_btn)

        # on ajoute le input layout au central_layout comme si c'était un widget
        central_layout.addLayout(input_layout)

        # idem, on fait un autre horizontal layout pour les buttons start stop et play
        button_layout = QHBoxLayout()

        # creation du button
        self.play_btn = QPushButton("Play")

        # ajouter une icon au button, attention, le chemin est pas complet ici car le
        # fichier .png est dans le même dosseier que le fichier python, donc ca marche,
        # autrement on aurait du mettre le chemin en entier.
        self.play_btn.setIcon(QIcon("play.png"))
        # on peut donner une taille à notre icon
        self.play_btn.setIconSize(QSize(32, 32))

        # ici on bind le signal "j'ai cliqué sur le button" a une method de la QMainWindow qu'on a
        # fait, ici play_file(), quand le button sera cliqué, cette méthod s'executera
        self.play_btn.clicked.connect(self.play_file)
        button_layout.addWidget(self.play_btn)

        # idem pour les autres buttons, avec des methods bindées différentes
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_file)
        self.pause_btn.setIcon(QIcon("pause.png"))
        self.pause_btn.setIconSize(QSize(32, 32))
        button_layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_file)
        self.stop_btn.setIcon(QIcon("stop.png"))
        self.stop_btn.setIconSize(QSize(32, 32))
        button_layout.addWidget(self.stop_btn)
        
        self.slider_volume = QSlider()
        self.slider_volume.setMinimum(0)
        self.slider_volume.setMaximum(100)
        self.slider_volume.setValue(20)
        self.media_player.setVolume(20)
        self.slider_volume.valueChanged.connect(self.set_volume)
        button_layout.addWidget(self.slider_volume)

        self.volume_label = QLabel("20")
        button_layout.addWidget(self.volume_label)

        self.mp3_picker = FilePicker()
        button_layout.addWidget(self.mp3_picker)

        # idem, on ajoute le button layout au central layout
        central_layout.addLayout(button_layout)

        # on set central_layout au central widget et on dit a la windows
        # d'utiliser ce widget en tant que central widget
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def set_volume(self, volume):

        self.media_player.setVolume(volume)
        self.volume_label.setText(str(volume))

    def play_file(self):
        
        # method executée quand on presse le button play, d'abord, on vérifie que le
        # media player n'est pas déjà en train de lire une musique, pour cela, on vérifie 
        # sont était "state" en anglais, si il n'est PAS ( if NOT) en train de jouer, alors
        # on prend le chemin du fichier mp3 qu'on veut lire depuis le QLineEdit qu'on a rajouter
        # plus tôt dans le code, on peut récupérer son contenu avec la method .text()

        if not self.media_player.state() == self.media_player.PlayingState:
            
            # on récupère le contenu de la QLineEdit
            file_path = self.file_path_input.text() + os.sep + self.mp3_picker.get_selected_mp3()

            # on vérifie que c'est un fichier qui existe:
            if os.path.exists(file_path):

                # on ajoute la musique au média player pour qu'il puisse la jouer
                self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

                # on lance la musique
                self.media_player.play()

    def stop_file(self):

        # avant de stopper le fichier, on vérifie bien qu'il était en train de lire la musique
        if self.media_player.state() == self.media_player.PlayingState:
            self.media_player.stop()

    def pause_file(self):

        # Si le media player est en train de lire une musique, on l'a met en pause
        if self.media_player.state() == self.media_player.PlayingState:
            self.media_player.pause()

        # sinon si le media player est déjà en pause, on relance la musique avec play()
        elif self.media_player.state() == self.media_player.PausedState:
            self.media_player.play()

    def pick_folder(self):

        my_dir = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",)
        
        self.file_path_input.setText(my_dir)
        self._set_items(my_dir)

    def returned_pressed_folder(self):

        my_dir = self.file_path_input.text()
        self._set_items(my_dir)
        
    def _set_items(self, my_dir):

        self.mp3_picker.set_items(my_dir)

class FilePicker(QWidget):

    def __init__(self, parent=None):
        
        super(FilePicker, self).__init__(parent=parent)

        main_layout = QVBoxLayout()

        self.mp3_list = QListWidget()
        main_layout.addWidget(self.mp3_list)

        self.setLayout(main_layout)

    def set_items(self, folder = None):
        
        self.mp3_list.clear()

        if os.path.exists(folder):

            elements = os.listdir(folder)

            for e in elements:
                
                e_full_path = folder + os.sep + e

                if os.path.isfile(e_full_path) and e.endswith(".mp3"):

                    self.mp3_list.addItem(e)

    def get_selected_mp3(self):

        item = self.mp3_list.currentItem().text()
        return item




        