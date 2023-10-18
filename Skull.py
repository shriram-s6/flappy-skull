from tkinter import PhotoImage
class Skull:
    __instance = None
    __skull = None

    def __init__(self):
        raise RuntimeError("Call getInstance instead")
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            cls.__skull = PhotoImage(file="images/skull.png")
        return cls.__instance
    def getSkull(self):
        return self.__skull
