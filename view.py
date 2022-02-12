from itertools import cycle
from tkinter import Frame, Label, ttk, Tk, Listbox, StringVar, END, Button
from PIL import ImageTk, Image

from setting import Setting
from img import Img


class Window(Frame):

    def __init__(self, root):
        super().__init__(root)
        self.__row = 0
        self.__column = 0

    def add_widget(self, widget, end=False, **kargs):
        widget.grid(row=self.__row, column=self.__column, **kargs)

        if not end:
            delta_column = kargs.get("columnspan", 1)
            self.__column += delta_column
        else:
            self.__row += kargs.get("rowspan", 1)
            self.__column = 0

class MainWindow(Tk):

    def __init__(self, data_gif, img_play, img_pause, img_next, img_back):

        super().__init__()

        
        self.title("Mp3 Music Player")
        self.iconbitmap(Setting.PATH_ICON_APP)
        self.geometry("1000x500")
        # self.state("zoomed")
        
        # main frame
        main_panel = Window(self)

        # panel left
        panel_left = Window(main_panel)
        self.__txt_directory = ttk.Entry(panel_left, width=40)
        self.__btn_open_folder = ttk.Button(panel_left, text="Search")
        self.__box_songs = Listbox(panel_left, selectmode="single")

        panel_left.add_widget(self.__txt_directory, padx=5, pady=5)
        panel_left.add_widget(self.__btn_open_folder, end=True, padx=5)
        panel_left.add_widget(self.__box_songs, columnspan=2, sticky = "nswe", padx=5, pady=5)

        panel_left.rowconfigure(1, weight=1)
        # panel left

        # panel rigth
        self.__panel_right = Window(main_panel)
        self.__lbl_img_playing = LabelGif(self.__panel_right, data_gif)
        self.__lbl_img_playing.pack(expand=1, fill="both")
        self.__panel_right.config(bg="yellow")
        # panel rigth

        # panel bottom
        self.__panel_bottom = Window(main_panel)
        self.__panel_bottom_aux = Window(self.__panel_bottom)  # to center items
        
        self.__txt_timer = StringVar()
        self.__lbl_timer = Label(self.__panel_bottom_aux, textvariable = self.__txt_timer, font=("Arial", 13))
        self.__txt_timer.set("00:00:00 / 00:00:00")

        img_back = Img.img2Photo(img_back)
        self.__btn_back = Button(self.__panel_bottom_aux, image=img_back, border=0)
        self.__btn_back.image = img_back

        img_play = Img.img2Photo(img_play)
        self.__btn_play = Button(self.__panel_bottom_aux, text="Play", image=img_play, border=0)
        self.__btn_play.image = img_play

        
        img_next = Img.img2Photo(img_next)
        self.__btn_next = Button(self.__panel_bottom_aux, image=img_next, border=0)
        self.__btn_next.image = img_next

        self.__panel_bottom_aux.add_widget(self.__lbl_timer, columnspan=3, end=True)
        self.__panel_bottom_aux.add_widget(self.__btn_back)
        self.__panel_bottom_aux.add_widget(self.__btn_play, padx=(10,10))
        self.__panel_bottom_aux.add_widget(self.__btn_next)

        self.__panel_bottom.add_widget(self.__panel_bottom_aux)
        self.__panel_bottom.columnconfigure(0, weight=1)
        # panel bottom

        main_panel.add_widget(panel_left, padx=5, pady=5, sticky="ns")
        main_panel.add_widget(self.__panel_right, sticky="nswe", end=True)
        main_panel.add_widget(self.__panel_bottom, sticky="we", columnspan=2)

        
        main_panel.rowconfigure(0, weight=1)
        main_panel.columnconfigure(1, weight=1)
        main_panel.pack(expand=True, fill="both")
        
        self.update_idletasks()
        self.__width_last_window = self.__lbl_img_playing.winfo_width()
        self.__height_last_window = self.__lbl_img_playing.winfo_height()
        self.__lbl_img_playing.size = (self.__width_last_window-10, self.__height_last_window-10)
        
        self.__txt_directory.bind("<FocusIn>", self.event_enter_txtsearch)
        self.__txt_directory.bind("<FocusOut>", self.event_leave_txtsearch)
        self.bind("<Configure>", self.event_window_resize)

        # falta ajustar que la imagen en LabelGIf se redimensione bien
        # al cambiar el tamaño de la ventana
        # problemas de redimension de la imagen al maximizar 
        #self.minsize(width=1000, height=500)
        self.resizable(False, False)

    def play_gif(self):
        self.__lbl_img_playing.play()
    
    def stop_gif(self):
        self.__lbl_img_playing.stop()

    def new_size_gif(self, size):
        self.__lbl_img_playing.size = size

    @property
    def txt_timer(self):
        return self.__txt_timer.get()
    
    @txt_timer.setter
    def txt_timer(self, time):
         self.__txt_timer.set(time)

    @property
    def btn_back(self):
        return self.__btn_back

    @property
    def btn_play(self):
        return self.__btn_play

    @property
    def btn_next(self):
        return self.__btn_next


    @property
    def btn_open_folder(self):
        return self.__btn_open_folder

    @property
    def txt_directory(self):
        return self.__txt_directory

    @property
    def box_songs(self):
        return self.__box_songs

    def event_enter_txtsearch(self, event):
        self.__last_txt = self.txt_directory.get()

    def event_leave_txtsearch(self, event):
        self.txt_directory.delete(0, END)
        self.txt_directory.insert(0, self.__last_txt)

    def event_window_resize(self, event):
        
        if isinstance(event.widget, Tk) :
            size = [self.__width_last_window, self.__height_last_window]
            
            new_width = self.__panel_right.winfo_width()-10
            new_heigth = self.__panel_right.winfo_height()-10
            if new_width > 0:
                size[0] = new_width
                self.__width_last_window = new_width
            if new_heigth > 0:
                size[1] = new_heigth
                self.__height_last_window = new_heigth
            self.__lbl_img_playing.size = tuple(size)

class LabelGif(Label):
    
    def __init__(self, root, data_gif, **kwargs):

        super().__init__(root, **kwargs)
        self.imgs = data_gif
        self.__time = 20
        self.__size = (50, 50)
        self.__execute = None
        

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size:tuple):
        self.__size = size
        img = next(self.imgs)
        img = img.resize(self.__size)
        img = ImageTk.PhotoImage(img, Image.ANTIALIAS)
        self.config(image = img)
        self.image = img
        
        

    def play(self):
        self.__playing = True
        self.__execute = self.after(self.__time, self.change_image)

    def change_image(self):
        img = next(self.imgs)
        img = img.resize(self.__size)
        img = ImageTk.PhotoImage(img)
        self.config(image = img)
        self.image = img
        self.__execute = self.after(self.__time, self.change_image)
    
    def stop(self):
        self.__playing = False
        if self.__execute:
            self.after_cancel(self.__execute)
            self.__execute = None