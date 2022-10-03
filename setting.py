from os import path
from platform import system
from pathlib import Path


PATH_IMG = Path(__file__).parent / "img"

class Setting:
    PATH_ICON_APP = path.join(PATH_IMG, "musicplayer.ico") if system() == "Windows" else path.join("@"+PATH_IMG, "musicplayer.xbm")
    PATH_IMG_PLAY = path.join(PATH_IMG, "play.png")
    PATH_IMG_PAUSE = path.join(PATH_IMG, "pause.png")
    PATH_IMG_NEXT = path.join(PATH_IMG, "next.png")
    PATH_IMG_BACK = path.join(PATH_IMG, "back.png")
    PATH_IMG_PLAYING = path.join(PATH_IMG, "playingmusic.gif")
