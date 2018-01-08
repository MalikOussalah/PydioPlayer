import sys
from PyQt5.QtCore import pyqtSlot, QTimer, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import datetime
import time
from functools import partial
import webbrowser
import os
from pygame import mixer
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import threading

class PydioPlayer(QMainWindow):
    def __init__(self):
        super(PydioPlayer, self).__init__()
        self.loaded_mp3 = ''
        self.paused = False
        loadUi('pydioplayerwindow.ui', self)
        self.duration_progress = 0
        self.setWindowTitle('PydioPlayer v1.0')
        # exit action
        self.actionQuitter.triggered.connect(self.quitting)

        # charger Mp3
        self.actionCharger_Mp3.triggered.connect(self.loadmp3)

        #Play button
        self.pushButton.clicked.connect(self._playsong)

        #Pause button
        self.pushButton_2.clicked.connect(self._pausesong)

        #Stop button
        self.pushButton_3.clicked.connect(self._stopsong)

    @pyqtSlot()
    def _pausesong(self):
        try:
            if self.paused != True:
                mixer.music.pause()
                self.paused = True
            else:
                mixer.music.unpause()
                self.paused = False
        except:
            return None

    @pyqtSlot()
    def _stopsong(self):
        try:
            mixer.music.stop()
        except:
            return None

    @pyqtSlot()
    def _playsong(self):
        try:
            mixer.init()
            mixer.music.load(self.loaded_mp3)
            mixer.music.play()
            self.played = True
            self.completed = 0
            infos = EasyID3(self.loaded_mp3)
            title_song = infos['title'][0]
            artist_song = infos['artist'][0]
            album_song = infos['album'][0]
            duration = MP3(self.loaded_mp3).info.length
            self.duration_progress = duration/100.0
            m, s = divmod(duration, 60)
            h, m = divmod(m, 60)
            self.lineEdit.setText(title_song)
            self.lineEdit_2.setText(artist_song)
            self.lineEdit_3.setText(album_song)
            self.lineEdit_4.setText("%d:%02d" % (m, s))
            t = threading.Timer(self.duration_progress, self._progress)
            t.start()

        except:
            return False

    @pyqtSlot()
    def _progress(self):
        if self.completed == 100:
            return None
        else:
            self.completed += 1
            print(self.completed)
            self.progressBar.setValue(self.completed)

    @pyqtSlot()
    def quitting(self):
        self.close()

    @pyqtSlot()
    def loadmp3(self):
        self.loaded_mp3, _ = QFileDialog.getOpenFileName()



app = QApplication(sys.argv)
widget = PydioPlayer()
widget.show()

#def progress():
#    widget.initial += 1
#    widget.progressBar.setValue(widget.initial)


#timer = QTimer()
#timer.timeout.connect(progress)
#timer.start(widget.duration_progress)

sys.exit(app.exec_())