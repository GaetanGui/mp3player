import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5 import Qt

from ui import MainWindow

""" Fichier a executer pour lancer le player mp3
"""

def main():

    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec_()
    
main()