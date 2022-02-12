from PIL import Image, ImageTk
from itertools import cycle
class Img:

    @staticmethod
    def get_img(path, size=(40, 40)):
        # obetenemos el objeto Image una imagen
        img = Image.open(path)
        img = img.resize(size)
        return img

    @staticmethod
    def img2Photo(img:Image)->ImageTk.PhotoImage:
        """Convertirmos un objeto Image a un objeto ImageTk.PhotoImage

        :param img: objeto Image
        :type img: Image
        :return: objeto ImageTk.PhotoImage
        :rtype: ImageTk.PhotoImage
        """
        return ImageTk.PhotoImage(img)


    @staticmethod
    def get_gif(path:str, size:tuple=(40, 40))->cycle:
        """obtenemos una lista de cada frame del gif como Image

        :param path: ruta del gif
        :type path: str
        :param size: para redimensionar la imagen (ancho, alto), defaults to (40, 40)
        :type size: tuple, optional
        :return: generador de Image
        :rtype: cycle
        """
        img = Image.open(path)
        imgss = list()
        while True:
            try:
                imgss.append(img.copy())
                img.seek(img.tell()+1)
            except EOFError:
                break
        return cycle(imgss)
