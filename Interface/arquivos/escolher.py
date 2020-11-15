import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np
import csv
import os
from about import about


class Dataset:
    count=1
    def __init__(self, nome, itens, rotulos):
        self.nome = nome
        self.itens = itens
        self.labels = rotulos
        
        
    def show(self):
        print(self.nome, len(self.itens),len(self.labels))


class TheEscolher:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Datasets para Redes Neurais")
        wtela = self.root.winfo_screenwidth()
        htela = self.root.winfo_screenheight()

        self.largura=wtela*(6/10)
        self.altura=htela*(6/10)
        self.DATAMASTER = dict()
        self.choosen = 0
        self.dados = None
        menubar = tk.Menu(self.root)
        menubar.add_command(label='Sobre...', command = about)
        self.root.config(menu=menubar)
        
        self.root.geometry('%dx%d+%d+%d' % (self.largura, self.altura, wtela*0.2, htela*0.2))
        self.thecanvas = tk.Canvas(self.root, width=self.largura, height=self.altura, bg='burlywood1')
        

        self.bt_validar = tk.Button(self.root, text='Validar',command=self.validar)
        self.bt_validar.pack()

        self.thecanvas.pack()
                
        pos = [0,0]

        self.dts = list()

        pt = Path('./arquivos/datasets')
        pt.resolve()

        for pasta in pt.iterdir():
            nome_temp = pasta.name
            aux = list(pasta.glob('**/*.*'))
            img_temp = None
            parent_temp = None

            for arqv in aux:
                try: img_temp = Image.open(arqv)
                except IOError: continue
                parent_temp = str(arqv.parent)
                parent_temp = parent_temp.split('\\')
                parent_temp = parent_temp[len(parent_temp)-1]
                img_temp = img_temp.resize((96,96), Image.ANTIALIAS)
                img_temp = ImageTk.PhotoImage(img_temp)
                break

            pos_img = (pos[0],pos[1])
            temp = self.thecanvas.create_image(pos_img, image=img_temp, anchor='nw')
            
            pr2 = (pos[0]+96*3/4, pos[1]+96*3/4, pos[0]+96, pos[1]+96)
            pr2 = self.thecanvas.create_rectangle(pr2, fill='khaki')

            pr3 = (pos[0]+96*0.6, pos[1]+96*0.85, pos[0]+96*3/4, pos[1]+96)
            pr3 = self.thecanvas.create_rectangle(pr3, fill='MediumPurple2')

            self.thecanvas.tag_bind(pr2, '<Button-1>', self.clicado)
            self.thecanvas.tag_bind(pr3, '<Button-1>', self.informe)

            self.DATAMASTER[str(temp)] = dict()
            self.DATAMASTER[str(temp)]['nome'] = nome_temp
            self.DATAMASTER[str(temp)]['imagem'] = img_temp
            self.DATAMASTER[str(temp)]['parent'] = parent_temp
            self.DATAMASTER[str(temp)]['position'] = pos_img
            self.DATAMASTER[str(temp)]['selec_pos'] = pr2
            pos[0] += 106
        self.root.wait_window()
        
            


        #
        #
        #
        #
        #
        #
        #

    def mainloop(self):
        self.root.wait_window()
        self.root.mainloop()


           
    def clicado(self, event):
        tagged = self.thecanvas.find_closest(event.x, event.y)
        tagged = tagged[0]
        if(self.choosen != 0):
            self.thecanvas.itemconfig(self.choosen, fill = 'khaki')
        self.thecanvas.itemconfig(tagged, fill = 'springgreen2')
        self.choosen=tagged

    def compile(self):
        entity = self.DATAMASTER[self.tag]
        divs = dict()
        codigo = str()
        path = Path('./arquivos/datasets/'+entity['nome'])
        if((path/'train').exists()): divs['train'] = True
        else: divs['train'] = False
        if((path/'test').exists()): divs['test'] = True
        else: divs['test'] = False
        if((path/'val').exists()): divs['val'] = True
        else: divs['val'] = False
        if((path/'validation').exists()): divs['validation'] = True
        else: divs['validation'] = False

        if(divs['train']): path = path/'train'
        fs_item = list(path.iterdir())
        fs_item = fs_item[0]
        if(fs_item.is_dir()):
            self.labels = 'inferred'
        else:
            self.labels = 'csvbased'
        

        if(Path('proibido.py').exists()): os.remove('proibido.py')
        
        
        path = path.absolute()
        path = path.resolve()
        mystr = str(path)
        mystr = mystr.replace("\\", "/")


        self.tamanho_imagem = None
        self.img_shape = None
        for item in path.rglob('*.*'):
            if(item.suffix != '.csv'):
                a = Image.open(item)
                a = np.asarray(a)
                a = a.shape
                self.img_shape = a
                self.tamanho_imagem = str(a[0])+'x'+str(a[1])
                break
        if(len(self.img_shape)==2):
            self.img_shape = (self.img_shape[0],self.img_shape[1],1)
        

        
        
        codigo+='import tensorflow as tf\n'
        codigo+='import numpy as np\n'
        codigo+='from keras import layers\n'
        codigo+='from keras import models\n'
        codigo+='from keras.preprocessing import image\n'
        codigo+='from pathlib import Path\nimport csv\n'
        codigo+='from PIL import Image\n'
        codigo+='from keras.utils import to_categorical\n'
        codigo+='path=\''+str(mystr)+'\'\n'
        codigo+='path = Path(path)\n'
        if(self.labels=='inferred'):
            codigo+='labels = \'inferred\'\n'
            codigo+='itenes = list(path.rglob(\'*.*\'))\n'
        else:
            codigo+='csvlist = list(path.glob(\'*.csv\'))\n'
            codigo+='itenes = list(path.glob(\'*.*\'))\n'
            codigo+='labels = list()\n'
            codigo+='for a in range(0,len(itenes)):\n'
            codigo+='   if(itenes[a].suffix == \'.csv\'):\n'
            codigo+='       itenes.pop(a)\n'
            codigo+='       break\n\n'
            codigo+='with open(csvlist[0], \'rt\') as f:\n'
            codigo+='   csv_reader = csv.reader(f)\n'
            codigo+='   next(csv_reader)\n'
            codigo+='   for line in csv_reader:\n'
            codigo+='       if(len(line)>1): labels.append(line[1])\n'
            codigo+='labels = to_categorical(labels)\n'
        codigo+='features = len(itenes)\n'
        codigo+='input_shape = '+str(self.img_shape)

        with open('proibido.py', 'wt') as f:
            f.write(codigo)
        



    
    
    def validar(self):
        #pegando o dataset selecionado.
        if(self.choosen!=0):
            itens = self.DATAMASTER
            for tag in itens.keys():
                if(itens[tag]['selec_pos'] == self.choosen):
                    self.tag = tag
        
        self.compile()
        self.root.destroy()


        
    
    def informe(self, event):
        temp = self.thecanvas.find_closest(event.x, event.y)
        temp = temp[0]

#start = TheEscolher()
#start.mainloop()