import sys

from PySide6.QtWidgets import (QSizePolicy, QWidget,
        QApplication,
        QLineEdit,
        QPushButton,
        QListWidget,
        QLabel,
        QGridLayout,
        QHBoxLayout)
from PySide6.QtGui import QMovie, QIcon
from PySide6.QtCore import Qt

from setting import Setting



class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reproductor mp3")
        self.__txt_search = QLineEdit()
        self.__btn_search = QPushButton(text="Buscar Directorio")
        self.__btn_reload = QPushButton(text="Recargar")
        self.__list_view_songs = QListWidget()
        self.__lbl_message = QLabel("No ha seleccionado niguna cancion")
        self.__lbl_gif = QLabel()
        self.__btn_play = QPushButton()
        self.__btn_back = QPushButton()
        self.__btn_next = QPushButton()
        self.__btn_pause = QPushButton()
        self.__btn_stop = QPushButton()
        self.__icon_back = QIcon(Setting.PATH_IMG_BACK)
        self.__icon_next = QIcon(Setting.PATH_IMG_NEXT)
        self.__icon = QIcon(Setting.PATH_IMG_PLAY)
        self.__icon_pause = QIcon(Setting.PATH_IMG_PAUSE)
        self.__box_layout = QGridLayout()

        self.__txt_search.setEnabled(False)
        self.__btn_play.setIcon(self.__icon)
        self.__btn_back.setIcon(self.__icon_back)
        self.__btn_next.setIcon(self.__icon_next)
        self.__btn_pause.setIcon(self.__icon_pause)
        self.__container_buttons_song = QWidget()
        self.__lbl_message.setAlignment(Qt.AlignCenter)
        self.__container_buttons_song.setLayout(self.__box_layout)
        self.__gif = QMovie(Setting.PATH_IMG_PLAYING)
        self.__lbl_gif.setMovie(self.__gif)
        self.__gif.start()
        self.__gif.setPaused(True)
        self.__txt_search.setPlaceholderText("Ingresa la ruta del directorio de archivos de musica")

        self.__layout = QGridLayout()
        self.setLayout(self.__layout)
        self.__btn_play.setContentsMargins(200, 10, 100, 100)
        self.__box_layout.addWidget(self.__btn_back, 0, 0, 1, 1, Qt.AlignRight)
        self.__box_layout.addWidget(self.__btn_play, 0, 1, 1, 1, Qt.AlignCenter)
        self.__box_layout.addWidget(self.__btn_pause, 0, 2, 1, 1, Qt.AlignCenter)
        self.__box_layout.addWidget(self.__btn_next, 0, 3, Qt.AlignLeft)
        self.__box_layout.setColumnStretch(0, 1)
        self.__box_layout.setColumnStretch(3, 1)

        self.__layout.addWidget(self.__txt_search, 0, 0, 1, 2)
        self.__layout.addWidget(self.__lbl_gif, 0, 2, 3, 1)
        self.__layout.addWidget(self.__btn_search, 1, 0)
        self.__layout.addWidget(self.__btn_reload, 1, 1)
        self.__layout.addWidget(self.__list_view_songs, 2, 0, 1, 2)
        self.__layout.addWidget(self.__lbl_message, 3, 0, 1, 3)
        self.__layout.addWidget(self.__container_buttons_song, 4, 0, 1, 3)

    @property
    def message(self):
        return self.__lbl_message

    @property
    def btn_pause(self):
        return self.__btn_pause

    @property
    def btn_play(self):
        return self.__btn_play

    @property
    def btn_back(self):
        return self.__btn_back

    @property
    def btn_next(self):
        return self.__btn_next

    @property
    def btn_pause(self):
        return self.__btn_pause

    @property
    def btn_search(self):
        return self.__btn_search
    
    @property
    def btn_reload(self):
        return self.__btn_reload
    @property
    def txt_search(self):
        return self.__txt_search

    @property
    def list_view_songs(self):
        return self.__list_view_songs

    @property
    def gif(self):
        return self.__gif

class App(QApplication):
    def __init__(self, arg=[]):
        super().__init__(arg)

        self.__widget = Window()
        self.__widget.resize(800, 600)
    
    @property
    def widget(self):
        return self.__widget

    def show_window(self):
        self.__widget.show()
        sys.exit(self.exec())    

if __name__ == "__main__":
    app = App()
    app.show_window()
