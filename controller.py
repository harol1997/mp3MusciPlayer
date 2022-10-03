from os import listdir, pardir, path
from time import sleep

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QThread
from PySide6.QtGui import QMovie
from ffpyplayer.player import MediaPlayer

from view import App

class AppController:

    def __init__(self) -> None:
        self.__app = App()
        self.__player = None
        self.__song_state = "end"

    def run(self):
        self.__app.widget.btn_search.clicked.connect(self.search_directory)
        self.__app.widget.btn_reload.clicked.connect(self.reload)
        self.__app.widget.btn_play.clicked.connect(self.play)
        self.__app.widget.btn_pause.clicked.connect(self.pause)
        self.__app.widget.btn_next.clicked.connect(self.next)
        self.__app.widget.btn_back.clicked.connect(self.back)
        self.__app.widget.gif.frameChanged.connect(self.stop_gif)
        self.__app.widget.btn_pause.clicked.connect(self.pause)
        self.__app.show_window()
    
    def end_song(self, eof, val):
        if eof == "eof":
            self.__song_state = "end"


    def stop_gif(self):
        if self.__player:
            self.__app.widget.message.setText(f"{self.__app.widget.list_view_songs.currentItem().text()} {int(self.__player.get_pts())}/{int(self.__player.get_metadata()['duration'])}")
            if  self.__song_state == "end":
                self.__app.widget.gif.setPaused(True)
                self.__player.set_pause(True)
                self.__player.close_player()
                self.__app.widget.message.setText("No hay otra cancion en la cola")
                self.__player = None
                self.next()

            elif self.__song_state == "paused":
                self.__app.widget.gif.setPaused(True)
                self.__app.widget.message.setText(f"{self.__app.widget.list_view_songs.currentItem().text()} en pausa...")


    def check_status_song(self):
        song_name = self.__app.widget.list_view_songs.currentItem().text()
        path_song = path.join(self.__app.widget.txt_search.text(), song_name)
        self.__app.widget.message.setText(f"Reproduciendo {song_name}")
        self.__player = MediaPlayer(path_song, callback=self.end_song, ff_opts={"autoexit":True})


    def play(self):
        if self.__song_state == "end":
            total = self.__app.widget.list_view_songs.count()
            if total > 0 and not self.__player:
                current_row = self.__app.widget.list_view_songs.currentRow()
                if current_row < 0: current_row = 0
                self.__app.widget.list_view_songs.setCurrentRow(current_row)
                self.__song_state = "running"
                self.__app.widget.gif.setPaused(False)
                self.__check_song_worker = QThread()
                self.__check_song_worker.run = self.check_status_song
                self.__check_song_worker.start()
        elif self.__song_state == "paused":
            self.__app.widget.message.setText(f"Reproduciendo {self.__app.widget.list_view_songs.currentItem().text()}")
            self.__song_state = "running"
            self.__app.widget.gif.setPaused(False)
            self.__player.toggle_pause()


    def pause(self):
        if self.__player and self.__song_state == "running":
            self.__song_state = "paused"
            self.__player.toggle_pause()

    def stop(self):
        pass

    def next(self):
        total = self.__app.widget.list_view_songs.count()
        if total > 0:
            current_row = self.__app.widget.list_view_songs.currentRow()
            if current_row == total-1: current_row = -1
            self.__app.widget.list_view_songs.setCurrentRow(current_row+1)
            if self.__player:
                self.__player.close_player()
                self.__player = None
            self.__song_state = "end"
            self.play()


    def back(self):
        total = self.__app.widget.list_view_songs.count()
        if total > 0:
            current_row = self.__app.widget.list_view_songs.currentRow()
            if current_row == 0: current_row = total
            self.__app.widget.list_view_songs.setCurrentRow(current_row-1)
            if self.__player:
                self.__player.close_player()
                self.__player = None
            self.__song_state = "end"
            self.play()

    def search_directory(self):
        directory = QFileDialog.getExistingDirectory()
        self.__app.widget.txt_search.clear()
        self.__app.widget.txt_search.setText(directory)
        self.load_songs()

    def load_songs(self):
        self.__app.widget.list_view_songs.clear()
        if self.__app.widget.txt_search.text().strip():
            if self.__song_state == "running" or self.__song_state == "pause":
                self.__song_state = "end"
                self.__player.toggle_pause()
                self.__player.close_player()
                self.__player = None
                self.__app.widget.gif.setPaused(True)
            self.__app.widget.list_view_songs.addItems([
                song for song in listdir(self.__app.widget.txt_search.text()) if song.endswith(".mp3")
                ])

    def reload(self):
        self.load_songs()

