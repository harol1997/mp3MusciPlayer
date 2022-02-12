from threading import Thread
from time import sleep
from model import Song
from setting import Setting
from view import MainWindow
from img import Img

from tkinter import filedialog, END
from os import listdir, path
from typing import List


class MainController:

    def __init__(self) -> None:
        self.__window = None
        self.__songs:List[Song] = []  # contain all mp3 files after search directory
        self.__song:Song = None  # if a song is playing
        self.__last_song:Song = None  # to back o next song

    def run(self):
        # cargamos los gif y png aqui para que no ocurra una pausa al iniciar la ventana
        data_gif = Img.get_gif(Setting.PATH_IMG_PLAYING)
        img_play = Img.get_img(Setting.PATH_IMG_PLAY)
        img_pause = Img.get_img(Setting.PATH_IMG_PAUSE)
        img_next = Img.get_img(Setting.PATH_IMG_NEXT, size=(20, 20))
        img_back = Img.get_img(Setting.PATH_IMG_BACK, size=(20, 20))

        self.__window = MainWindow(data_gif, img_play, img_pause, img_next, img_back)
        self.__window.btn_back.config(command=self.back)  # back song
        self.__window.btn_play.config(command=self.play)  # play song
        self.__window.btn_next.config(command=self.next)  # next song
        self.__window.btn_open_folder.config(command=self.each_directory)  # search directory
        self.__img_play = Img.img2Photo(img_play)
        self.__img_pause = Img.img2Photo(img_pause)
        self.__window.protocol("WM_DELETE_WINDOW", self.close_all)
        self.__window.mainloop()

    def set_timer(self):
        
        if self.__song:
            self.__window.txt_timer = f"{str(self.__song.time)} / {str(self.__song.duration)}"
        else:
            self.__window.txt_timer = "00:00:00 / 00:00:00"

    def back(self):
        if not self.__last_song:
            self.play()
        else:
            self.stop()
            index = len(self.__songs)-1 if self.__last_song.index-1 == -1 else self.__last_song.index-1
            self.__window.box_songs.select_clear(self.__last_song.index)
            self.__window.box_songs.select_set(index)
            self.play()

    def play(self):
        """Play song"""
        if not self.__song:  # if any song is playing
            item_tuple = self.__window.box_songs.curselection()
            
            if item_tuple:
                self.__song = self.__songs[item_tuple[0]]  # get song from songs list
                self.__song.play()  # play song and a callback will be execute at song end
                self.__window.btn_play.config(image=self.__img_pause)  # change image from play to pause
                self.__window.btn_play.image = self.__img_pause
                self.__last_song = self.__song
                self.__window.play_gif()
                self.__ask_thread = True
                Thread(target=self.ask_is_stopped, daemon=True).start()
                
                
        else:  # if a song is playing there are two options
            if self.__song.is_pause:
                self.__window.btn_play.config(image=self.__img_pause)
                self.__window.btn_play.image = self.__img_pause
                self.__song.resume()
                self.__window.play_gif()
            else:
                self.__window.btn_play.config(image=self.__img_play)
                self.__window.btn_play.image = self.__img_play
                self.__song.pause()
                self.__window.stop_gif()

    def ask_is_stopped(self):
        while self.__ask_thread:
            if self.__song:    
                if not self.__song.is_playing:
                    self.stop()
                    break
                elif not self.__song.is_pause:
                    self.set_timer()
                sleep(0.2)
        self.__window.txt_timer = "00:00:00 / 00:00:00"

    def stop(self):
        """Se ejecuta cuando se termina de reproducir una cancion o al cambiar de cancion.
        Establece los elementosd en sus configuraciones iniciales"""
        self.__ask_thread = False
        self.__window.btn_play.config(image=self.__img_play)
        self.__window.btn_play.image = self.__img_play
        self.__window.stop_gif()
        if self.__song:
            self.__song.stop()
            self.__song = None  # end song
        self.__window.txt_timer = "00:00:00 / 00:00:00"

    def next(self):
        if not self.__last_song:
            self.play()
        else:
            self.stop()
            index = 0 if self.__last_song.index+1 == len(self.__songs) else self.__last_song.index+1
            self.__window.box_songs.select_clear(self.__last_song.index)
            self.__window.box_songs.select_set(index)
            self.play()

    def each_directory(self):
        directory = filedialog.askdirectory().strip()
        if directory:
            self.stop()
            self.__window.txt_directory.delete(0, END)
            self.__window.txt_directory.insert(0, directory)
            
            # add songs in listbox
            self.__window.box_songs.delete(0, END)
            self.__songs.clear()
            for i in listdir(directory):
                if path.isfile(i) and (i.endswith(".mp3") or i.endswith(".wav")):
                    self.__window.box_songs.insert(END, i)
                    self.__songs.append(Song(directory, i, len(self.__songs)))
            if self.__songs: self.__window.box_songs.select_set(0)
            
        
    def close_all(self):
        """Se ejecuta cuando cerramos la ventana
        """
        self.__window.destroy()