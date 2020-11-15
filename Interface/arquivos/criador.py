import tkinter as tk
from PIL import Image
from modelcreator import ModelCreator
from escolher import TheEscolher
from ete import ETE
from pathlib import Path
from matplotlib import pyplot as plt
    
class TheCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Criador de Redes Neurais")
        self.root.config(bg='steelblue1')
        larg = int(self.root.winfo_screenwidth()/8)
        alt = int(self.root.winfo_screenheight()/8)
        self.root.geometry(str(3*larg)+'x'+str(3*alt)+'+'+str(int(2.5*larg))+'+'+str(2*alt))
        
        for i in range(0,4):
            tk.Label(self.root, bg='steelblue1').pack()
        
        self.bt_EscolherDados = tk.Button(self.root, text='escolher dados',command=self.EscolherDados)
        self.bt_EscolherDados.pack()


        self.bt_TratarDados = tk.Button(self.root, text='tratar dados', 
                                    state='disabled')
        self.bt_TratarDados.pack()


        self.bt_Modelo = tk.Button(self.root, text='modelo',
                                    state='disabled')
        self.bt_Modelo.pack()

        self.spacelist = list()
        for i in range(0,6):
            self.spacelist.append(tk.Label(self.root, bg='steelblue1'))
            self.spacelist[i].pack()
        self.spacelist.append(tk.Label(self.root, text='UNIFEI 2020', bg='steelblue1'))
        self.spacelist[6].pack()
        self.root.mainloop()


    def EscolherDados(self):
        x = TheEscolher()
        self.tam_imagem = x.tamanho_imagem
        self.labels = x.labels
        
        for leibe in self.spacelist:
            leibe.pack_forget()
        self.bt_Modelo.pack_forget()
        self.bt_TratarDados.destroy()

        self.bt_TratarDados = tk.Button(self.root, text='tratar dados',
                                    command=self.TratarDados)
        self.bt_TratarDados.pack()
        self.bt_Modelo.pack()
        for leibe in self.spacelist:
            leibe.pack()
        

        
        

    def TratarDados(self):
        x = ETE(self.tam_imagem, self.labels)
        
        for leibe in self.spacelist:
            leibe.pack_forget()
        self.bt_Modelo.destroy()
        self.bt_Modelo = tk.Button(self.root, text='modelo',
                                    command=self.Modelo)
        self.bt_Modelo.pack()
        for leibe in self.spacelist:
            leibe.pack()
        


    def Modelo(self):
        self.modelo = ModelCreator()
        self.root.destroy()



start = TheCreator()

