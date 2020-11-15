import tkinter as tk
from PIL import Image
from about import about
#from criador import myNumbEntry
def get_ints_from_geo(s):
    aux = str()
    ls = list()
    for letter in s:
        if(letter.isdigit()):
            aux+=letter
        else:
            if(len(aux)>0):
                ls.append(int(aux))
                aux = str()
    
    if(len(aux)>0): ls.append(int(aux))
    
    return ls

class myNumbEntry(tk.Frame):
    def __init__(self, master, numb, tipo, width=4, state = 'normal'):
        tk.Frame.__init__(self,master=master)
        self.numb = numb
        self.tipo = tipo
        self.imgup = tk.PhotoImage(file='arquivos/upp.png')
        self.imgdw = tk.PhotoImage(file='arquivos/dwp.png')
        self.var = tk.StringVar()
        self.var.set(str(self.numb))
        self.entry = tk.Entry(self, textvariable=self.var, width=width, state = state)
        self.upbt = tk.Button(self, image=self.imgup, command= self.up)
        self.dwbt = tk.Button(self, image=self.imgdw, command= self.down)
        self.entry.pack(side=tk.LEFT)
        self.upbt.pack(side=tk.RIGHT)
        self.dwbt.pack(side=tk.RIGHT)
        self.entry.bind('<FocusOut>', self.validate)    
    
    def config(self, state='normal'):
        self.entry.config(state = state)
        self.entry.update()
    
    def up(self):
        try: 
            n = self.tipo(self.var.get())
            if(self.tipo==int): n+=1
            else: n+=0.1
            self.var.set(str(n))
        except(ValueError):
            return
        
    def down(self):
        try: 
            n = self.tipo(self.var.get())
            if(self.tipo==int): n-=1
            else: n-=0.1
            self.var.set(str(n))
        except(ValueError):
            return
    
    def validate(self, event):
        try:
            aux = self.tipo(self.var.get())
        except(ValueError):
            self.var.set('115')
        
    def get(self):
        return self.var.get()



class ETE:
    def __init__(self, tam_imagem, labels):
        self.root = tk.Toplevel()
        self.root.title("Central de Tratamento de Dados")
        self.show_up_infos = dict()
        self.data_gen_args = dict()
        self.data_gen_args2 = dict()
        self.tam_imagem = tam_imagem
        self.labels = labels
        menubar = tk.Menu(self.root)
        menubar.add_command(label='Sobre...', command = about)
        self.root.config(menu=menubar)
        larg = int(self.root.winfo_screenwidth()/8)
        alt = int(self.root.winfo_screenheight()/8)
        self.root.geometry(str(3*larg)+'x'+str(int(3.5*alt))+'+'+str(int(2.5*larg))+'+'+str(2*alt))
        
        optframe = tk.Frame(self.root, bg ='lavender')
        self.generalframe = tk.Frame(self.root)
        

        self.optframe_dict = dict()
        tk.Label(optframe, bg='lavender').pack(fill='x')
        self.optframe_dict['popup_info'] = tk.Button(optframe, text = 'Info', bg='IndianRed2')
        self.optframe_dict['popup_info'].pack()
        self.optframe_dict['popup_info'].bind("<Button-1>", self.togou)
        tk.Label(optframe, bg='lavender').pack(fill='x')
        optframe.pack(fill='x')

        self.foptions = list()
        x = tk.Button(self.generalframe, text = 'ImageDataGenerator', command = self.imdtfunc1)
        x.grid(row=1, column=0, columnspan=2)
        self.foptions.append(x)
        tk.Label(self.root).pack()
        self.generalframe.pack()
        

        

        
    def togou(self, event):
        temp = event.widget
        if(temp.cget('bg')=='IndianRed2'):
            temp.config(bg='OliveDrab2')
        else:
            temp.config(bg='IndianRed2')

    
    
    def mainloop(self):
        self.root.wait_window()
        self.root.mainloop()


    def callentra(self, event):
        print('click ', event.widget)
        try:
            self.tl.destroy()
            self.tl = None
        except:
            thevar = self.optframe_dict['popup_info'].cget('bg')
            if(thevar=='OliveDrab2'):
                wid = event.widget
                newtxt = wid.cget('text')
                newtxt = self.show_up_infos[newtxt]
                self.tl = tk.Toplevel(self.root)
                tk.Label(self.tl,text = newtxt).pack()
                g = self.root.geometry()
                g = get_ints_from_geo(g)
                self.tl.geometry('+'+str(g[2]+event.x)+'+'+str(g[3]+event.y))
                self.tl.transient(self.root)
        
        
    def fillmodeconstantfunc(self, event):
        f = self.data_gen_args2['fill_mode'].get('active')
        if(f=='constant'):
            self.data_gen_args2['cval'][1].set(True)
            self.data_gen_args2['cval'][0].config(state='normal')
        else:
            self.data_gen_args2['cval'][1].set(False)
            self.data_gen_args2['cval'][0].config(state='disabled')
        for wid in self.generalframe.grid_slaves():
            if(type(wid) == tk.Checkbutton):
                wid.update()

    def zcawhiteningfunc(self, event):
        f = self.data_gen_args['zca_whitening'].get()
        if(not f):
            self.data_gen_args['zca_epsilon'][1].set(True)
            self.data_gen_args['zca_epsilon'][0].config(state='normal')
        else:
            self.data_gen_args['zca_epsilon'][1].set(False)
            self.data_gen_args['zca_epsilon'][0].config(state='disabled')
        for wid in self.generalframe.grid_slaves():
            if(type(wid) == tk.Checkbutton):
                wid.update()
        


    def imdtcompile(self):
        
        for arg in self.data_gen_args2.keys():
            self.data_gen_args[arg] = self.data_gen_args2[arg]
        self.data_gen_args2 = None
        
        codigo = str()
        codigo += '\ngenerator = image.ImageDataGenerator('

        for arg in self.data_gen_args.keys():
            temp = self.data_gen_args[arg]
            if(type(temp) == tk.Listbox):
                temp = temp.get('active')
                codigo+=str(arg)+'=\''+str(temp)+'\','
                continue
            if(type(temp) == list and type(temp[1]) == tk.BooleanVar):
                if(temp[1].get()):
                    temp = temp[0].get()
                    codigo+=str(arg)+'='+str(temp)+','
                continue
            if(type(temp) == tk.BooleanVar and temp.get()):
                codigo+=str(arg)+'='+'True,'
                
                
        tam = len(codigo)
        codigo = codigo[:tam-1] + ')\n'
        
        codigo+='batch_size = '+str(self.batch_size)+'\n'
        
        self.tam_imagem = str.split(self.tam_imagem, 'x')
        codigo+='input_size = ('+str(self.tam_imagem[0])+','+str(self.tam_imagem[1])+')\n'
        codigo+='timesteps = int(features/batch_size)\n'

        codigo+='for x in range(0,len(itenes)):\n'
        codigo+='   itenes[x] = Image.open(itenes[x])\n'
        codigo+='   itenes[x] = itenes[x].resize(size=input_size)\n'
        codigo+='   itenes[x] = np.asarray(itenes[x])\n'
        codigo+='itenes = np.asarray(itenes)\n'
        codigo+='y = itenes.shape\n'
        codigo+='if(len(y)==3):\n'
        codigo+='   itenes = np.reshape(itenes, (y[0],y[1],y[2],1))\n'
        codigo+='generator.fit(itenes)\n'
        
            
        if(self.labels=='inferred'):
            codigo+='traingen = generator.flow_from_directory(path, target_size=input_size,batch_size=batch_size)\n'
        else:
            codigo+='traingen = generator.flow(itenes, labels, batch_size=batch_size)\n'
        
        
        with open('proibido.py', 'a') as f:
            f.write(codigo)
        self.root.destroy()
        
    
    def imdtfunc2(self):
        for i in range(0,len(self.templist)):
            if(i!=5): self.templist[i].grid_forget()
        self.tam_imagem = self.templist[5].get()
        self.batch_size = self.templist[3].get()


        self.data_gen_args2['rotation_range'] = [myNumbEntry(self.generalframe,90, int), tk.BooleanVar(False)]
        self.data_gen_args2['width_shift_range']=[myNumbEntry(self.generalframe, 0.1, float), tk.BooleanVar(False)]
        self.data_gen_args2['height_shift_range']=[myNumbEntry(self.generalframe, 0.1, float), tk.BooleanVar(False)]
        self.data_gen_args2['brigthness_range']=[myNumbEntry(self.generalframe, 1, float), tk.BooleanVar(False)]
        self.data_gen_args2['shear_range']=[myNumbEntry(self.generalframe, 1, float), tk.BooleanVar(False)]
        self.data_gen_args2['zoom_range']=[myNumbEntry(self.generalframe,1, float), tk.BooleanVar(False)]
        self.data_gen_args2['channel_shift_range']=[myNumbEntry(self.generalframe, 1, float), tk.BooleanVar(False)]
        self.data_gen_args2['fill_mode']=['constant', 'nearest', 'reflect', 'wrap']
        self.data_gen_args2['cval']=[tk.Entry(self.generalframe, state='disabled'),tk.BooleanVar(False)]
        self.data_gen_args2['horizontal_flip']=[myNumbEntry(self.generalframe, 1, float), tk.BooleanVar(False)]
        self.data_gen_args2['vertical_flip']=[myNumbEntry(self.generalframe, 1, float), tk.BooleanVar(False)]
        self.data_gen_args2['rescale']=[myNumbEntry(self.generalframe, 1, float), tk.BooleanVar(False)]
        self.data_gen_args2['validation_split']=[myNumbEntry(self.generalframe ,1, float), tk.BooleanVar(False)]

        
        temp = tk.Listbox(self.generalframe, selectmode='SINGLE', height=3)
        temp.bind('<FocusOut>', self.fillmodeconstantfunc)
        for itens in self.data_gen_args2['fill_mode']:
            temp.insert(tk.END, itens)
        self.data_gen_args2['fill_mode'] = temp
        self.data_gen_args2['fill_mode'].select_set(1)
        self.data_gen_args2['fill_mode'].event_generate("<<ListboxSelect>>")
        
        
        self.show_up_infos['rotation_range'] = "de 0 a 180.\nIntervalo para rotações aleatórias na imagem."
        self.show_up_infos['width_shift_range'] = "Fração da imagem que pode ser 'esticada' verticalmente (se <1) ou número de pixels (se >1)"
        self.show_up_infos['height_shift_range'] = "[height_shift_range]\nFração da imagem que pode ser 'esticada' honrizontalmente (se <1) ou número de pixels (se >1)"
        self.show_up_infos['brigthness_range'] = "Intervalo para mudança de brilho.\n0 escurece totalmente, 1.0 não muda nada e 1.5 a deixa bem clara."
        self.show_up_infos['shear_range'] = "A operação de de shear consiste em fixar um eixo e rotacionar o outro, \'esticando\' a imagem. O parâmetro é o limite dessa rotação."
        self.show_up_infos['zoom_range'] = "Operação de zoom. Um valor <1 se afasta da imagem, enquanto >1 se aproxima."
        self.show_up_infos['channel_shift_range'] = "Aleatoriamente troca os valores de um canal dentro desse limite. \Deve ser levada em consideração a normalização da imagem."
        self.show_up_infos['fill_mode'] = "Como serão preenchidos os pixels fora do limite da imagem.\nconstant: kkkkkkkk|abcd|kkkkkkkk (cval=k)\nnearest: aaaaaaaa|abcd|dddddddd\nreflect: abcddcba|abcd|dcdaabcd\nwrap: abcdabcd|abcd|abcdabcd"
        self.show_up_infos['cval'] = "O valor, caso fill_mode=constant"
        self.show_up_infos['horizontal_flip'] = 'Aleatoriamente inverte a imagem horizontalmente. Valor de 0 a 1'
        self.show_up_infos['vertical_flip'] = 'Aleatoriamente inverte a imagem verticalmente. Valor de 0 a 1'
        self.show_up_infos['rescale'] = "Rearranja os pixels da imagem por este fator.\nPor exemplo:\nUma imagem contendo pixels no intervalo de 0 a 255 pode ser rearranjada para conter pixels com valores de 0 a 1 se rearranjadas por um fator de 0.0039216."
        self.show_up_infos['preprocessing_function'] = "Função customizada para preprocessamento de uma imagem. Construída pelo usuário.(link)"
        self.show_up_infos['validation_split'] = 'Fração das imagens que serão reservadas para validação. Valor de 0.0 a 1.0'
        
        row = 1
        for key in self.data_gen_args2.keys():
            wid = tk.Label(self.generalframe, text=key)
            wid.bind("<Button-1>", self.callentra)
            
            wid.grid(row=row,column=0)
            if(type(self.data_gen_args2[key])==tk.BooleanVar):
                tk.Checkbutton(self.generalframe, variable = self.data_gen_args2[key]).grid(row=row, column=1)
            if(type(self.data_gen_args2[key]) == list and type(self.data_gen_args2[key][1]) == tk.BooleanVar):
                self.data_gen_args2[key][0].grid(row=row, column=1)
                tk.Checkbutton(self.generalframe, variable = self.data_gen_args2[key][1]).grid(row=row, column=2)
            if(type(self.data_gen_args2[key]) == tk.Listbox):
                self.data_gen_args2[key].grid(row=row, column=1)
            row+=1

        btsframe = tk.Frame(self.generalframe)

        btok = tk.Button(btsframe, text = 'Validar', bg='OliveDrab2', command = self.imdtcompile)
        btcancel = tk.Button(btsframe, text = 'Cancelar', bg='IndianRed2', command = self.generalframe.destroy)
        btreturn = tk.Button(btsframe, text = '<-', bg = 'PeachPuff3', command = self.imdtfunc1)

        btsframe.grid(row=row, column= 0, columnspan=3)
        btok.pack(side=tk.RIGHT)
        btreturn.pack(side = tk.LEFT)
        btcancel.pack(side=tk.LEFT)
        


    def imdtfunc1(self):
        larg = int(self.root.winfo_screenwidth()/8)
        alt = int(self.root.winfo_screenheight()/8)
        self.root.geometry(str(3*larg)+'x'+str(6*alt)+'+'+str(int(2.5*larg))+'+'+str(1*alt))

        for slave in self.foptions:
            slave.grid_forget()
        
        for slave in self.generalframe.grid_slaves():
            slave.grid_forget()

        self.data_gen_args['featurewise_center']=tk.BooleanVar(False)
        self.data_gen_args['featurewise_std_normalization']=tk.BooleanVar(False)
        self.data_gen_args['samplewise_center']=tk.BooleanVar(False)
        self.data_gen_args['samplewise_std_normalization']=tk.BooleanVar(False)
        self.data_gen_args['zca_whitening']=tk.BooleanVar(False)
        self.data_gen_args['zca_epsilon']=[myNumbEntry(self.generalframe, 0.000001, float, state = 'disabled', width=6), tk.BooleanVar(False)]


        tam_var = tk.StringVar()
        self.templist = list()

        self.templist.append(tk.Label(self.generalframe, text='tamanho'))
        self.templist.append(tk.Entry(self.generalframe, textvariable=tam_var))
        tam_var.set(self.tam_imagem)

        self.templist.append(tk.Label(self.generalframe, text = 'batch_size'))
        self.templist.append(myNumbEntry(self.generalframe, 20, int))


        self.templist[0].grid(row=1, column=0)
        self.templist[1].grid(row=1, column=1)
        self.templist[2].grid(row=2, column=0)
        self.templist[3].grid(row=2, column=1)

        self.show_up_infos['tamanho'] = '[tamanho]\nVocê deseja alterar o tamanho da imagem?\nSe sim, reescreva-o.'
        self.templist[0].bind("<Button-1>", self.callentra)
        

        self.show_up_infos['batch_size'] = 'Tamanho do lote de imagens a serem treinadas por etapa(timesteps) na rede.'
        self.templist[2].bind("<Button-1>", self.callentra)
        
        self.templist.append(tk.Button(self.generalframe, text='->', bg='OliveDrab2', command=self.imdtfunc2))        
        self.templist[4].grid(row=9, column=0, columnspan=2)
        self.templist.append(tam_var)

        #até aqui foram ajustes, agora são os argumentos

        self.templist.append(tk.Label(self.generalframe, text='featurewise_center'))#6
        self.templist.append(tk.Checkbutton(self.generalframe, variable=self.data_gen_args['featurewise_center']))#7
        self.templist.append(tk.Label(self.generalframe, text='featurewise_std_normalization'))#8
        self.templist.append(tk.Checkbutton(self.generalframe, variable=self.data_gen_args['featurewise_std_normalization']))#9
        self.templist.append(tk.Label(self.generalframe, text='samplewise_center'))#10
        self.templist.append(tk.Checkbutton(self.generalframe, variable=self.data_gen_args['samplewise_center']))#11
        self.templist.append(tk.Label(self.generalframe, text='samplewise_std_normalization'))#12
        self.templist.append(tk.Checkbutton(self.generalframe, variable=self.data_gen_args['samplewise_std_normalization']))#13
        self.templist.append(tk.Label(self.generalframe, text='zca_whitening'))#14
        self.templist.append(tk.Checkbutton(self.generalframe, variable=self.data_gen_args['zca_whitening']))#15
        self.templist.append(tk.Label(self.generalframe, text = 'zca_epsilon'))#16
        self.templist.append(self.data_gen_args['zca_epsilon'][0])#17
        self.templist.append(tk.Checkbutton(self.generalframe, variable=self.data_gen_args['zca_epsilon'][1]))#7
        
        
            
        self.show_up_infos['featurewise_center'] = "Subtrai de cada pixel o valor médio dos pixels de todo o conjunto de dados, deixando a média próxima de 0."
        self.templist[6].bind("<Button-1>", self.callentra)
        
        self.templist[6].grid(row=3,column=0)
        self.templist[7].grid(row=3,column=1)

        self.show_up_infos['featurewise_std_normalization'] = "[featurewise_std_normalization]\nDivide cada pixel pelo desvio padrão de todo o conjunto de dados, deixando o desvio padrão próximo de 1"
        self.templist[8].bind("<Button-1>", self.callentra)
        
        self.templist[8].grid(row=4,column=0)
        self.templist[9].grid(row=4,column=1)
        
        self.show_up_infos['samplewise_center'] = "Subtrai de cada pixel o valor médio dos pixels do dado em questão, deixando a média próxima de 0."
        self.templist[10].bind("<Button-1>", self.callentra)
        
        self.templist[10].grid(row=5,column=0)
        self.templist[11].grid(row=5,column=1)
        
        self.show_up_infos['samplewise_std_normalization'] = "Divide cada pixel pelo desvio padrão do dado em questão, deixando o desvio padrão próximo de 1"
        self.templist[12].bind("<Button-1>", self.callentra)
        
        self.templist[12].grid(row=6,column=0)
        self.templist[13].grid(row=6,column=1)

        self.show_up_infos['zca_whitening'] = "[zca_whitening]\nUma operação que busca remover ruído dos dados, maximizando as informações presentes.\nCovariância = Matriz Identidade\nDica: Treine a Rede com e sem esta opção e avalie."
        self.templist[14].bind("<Button-1>", self.callentra)
        
        self.templist[15].bind('<Button-1>', self.zcawhiteningfunc)
        self.templist[14].grid(row=7,column=0)
        self.templist[15].grid(row=7,column=1)
        

        self.show_up_infos['zca_epsilon'] = "Epsilon usado na operação ZCA.\nO padrão é 1e-6"
        self.templist[16].bind("<Button-1>", self.callentra)
        
        self.templist[16].grid(row=8,column=0)
        self.templist[17].grid(row=8,column=1)
        self.templist[18].grid(row=8,column=2)
        
        

        

        
        


        
        

        
#x = ETE(2,2)
#x.mainloop()

