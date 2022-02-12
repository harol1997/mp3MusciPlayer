from time import sleep
from audioplayer import AudioPlayer
import os
from threading import Thread
from datetime import timedelta
from eyed3.core import load
from time import time

class Timer:

    def __init__(self, delta_time=None) -> None:
        self.__running = False
        self.__delta_time = delta_time
        self.__pause = False
        self.__time = 0

    @property
    def time(self):
        return timedelta(seconds=round(self.__time))

    @property
    def running(self):
        return self.__running

    def start(self, callback=None, callback_executing=None,block=False):
        if self.__running == False:
            self.__running = True
            if not block:
                self.__thread = Thread(target=self.__running_until, args=(callback, callback_executing))
                self.__thread.setDaemon(True)
                self.__thread.start()
            else:
                self.__running_until(callback, callback_executing)
        else:
            print("Timer is running") 

    def __running_until(self, callback, callback_executing):
        actual_time = time()
        final_time = time()
        self.__time  = final_time-actual_time
        time_pause = 0
        delta_time_aux = self.__delta_time
        while  self.__running and  self.__time < delta_time_aux:
            if self.__pause:  # pause
                time_1_pause = time()
                while self.__running and self.__pause:sleep(0.2)
                time_2_pause = time()
                time_pause += time_2_pause-time_1_pause
                #delta_time_aux += time_pause
            else:
                final_time = time()
                self.__time = (final_time-actual_time) - time_pause
                
            sleep(0.2)
        self.__running = False

    def adjust(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        

    def pause(self):
        if not self.__pause: self.__pause = True

    def resume(self):
        if self.__pause: self.__pause = False
    
    def stop(self):
        self.__running = False
            
class Song:

    def __init__(self, path, filename, id_index) -> None:
        self.__path = path
        self.__filename = filename
        self.__id_index = id_index
        self.__player = None
        self.__clock = None
        self.__is_pause = False
        self.__is_playing = False
        self.__duration = load(os.path.join(path, filename)).info.time_secs
        self.__player = AudioPlayer(os.path.join(self.__path, self.__filename))

    
    @property
    def duration(self):
        return timedelta(seconds=round(self.__duration))

    @property
    def index(self):
        return self.__id_index

    @property
    def time(self):
        return self.__clock.time

    @property
    def is_pause(self):
        return self.__is_pause
    
    @property
    def is_playing(self):
        return self.__is_playing and self.__clock.running

    @property
    def filename(self):
        return self.__filename

    def __eq__(self, __o: "Song") -> bool:
        return self.__filename == __o.filename

    def play(self):
        self.__clock = Timer(self.__duration)
        self.__clock.start()
        
        self.__player.play()
        self.__is_playing = True
        self.__is_pause = False
    
    def pause(self):
        self.__player.pause()
        self.__clock.pause()
        self.__is_pause = True
        

    def resume(self):
        self.__player.resume()
        self.__is_pause = False
        self.__clock.resume()

    def stop(self):
        self.__is_playing = False
        self.__player.stop()
        self.__clock.stop()
        