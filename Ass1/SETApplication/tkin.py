
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")


class File:
    def __init__(self):
        self.fileText = None
        self.fileName = ""
        self.listbit = None
        self.fileExtendsion = ""

    def c_open_file(self):
        rep = filedialog.askopenfilenames(
            parent=root,
            initialdir='C:/Users/BuiLong/source/Python/Tkinter/Picture',
            initialfile='tmp',
            filetypes=[
    		("All files", "*")])
        print(rep[0])
        dataSplit = rep[0].split("/")[-1].split(".")
        print("____", dataSplit)
        for x in dataSplit[:-1]:
            self.fileName+= x
        print("----", self.fileName)
        self.fileExtendsion = "."+dataSplit[-1]
        with open(rep[0], 'rb') as f:
            self.fileText = f.read()

        self.listbit = [bin(x)[2:] for x in self.fileText]
        
        

    def c_open_folder(self):
        rep = filedialog.askdirectory()+"/"
        with open(rep+'cypher.txt','w') as f:
            f.write(self.fileText.decode('utf8'))
        print(rep)
        lstBytes = b''.join([int(s,2).to_bytes(1,"big") for s in self.listbit])
        with open(rep+self.fileName+self.fileExtendsion, 'wb') as f:
            f.write(lstBytes)

file = File()

ttk.Button(root, text="Open files", command=file.c_open_file).grid(
    row=0, column=0, padx=4, pady=4, sticky='ew')

ttk.Button(root, text="Open folder", command=file.c_open_folder).grid(
    row=1, column=0, padx=4, pady=4, sticky='ew')

root.mainloop()
