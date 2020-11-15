import tkinter as tk
from criador import TheCreator

class TopWindow:

    def __init__(self):
        top = tk.Tk() #inicia a janela mãe
        top.title('Uma Interface Gráfica para o Keras')
        larg = int(top.winfo_screenwidth()/8)
        alt = int(top.winfo_screenheight()/8)
        top.geometry(str(2*larg)+'x'+str(2*alt)+'+'+str(3*larg)+'+'+str(2*alt))
            
        top_frame = tk.Frame()

        bt_CriarRede = tk.Button(top_frame,text="Criar nova rede", command=self.criarRede)
        bt_CriarRede.pack()

        bt_VerRedes = tk.Button(top_frame,text="Suas redes", command=self.verRedes)
        bt_VerRedes.pack()

        bt_Materiais = tk.Button(top_frame,text="Materiais disponíveis", command=self.materiaisDisp)
        bt_Materiais.pack()

        top_frame.pack(fill='both')
        #
        #
        #
        #
        #
        #
        #
        
        top.mainloop() #loop necessário pro app

    def criarRede(self):
        creator_Frame = TheCreator()
        print('creator frame\n')

        # fazer em outro arquivo
        #
        #
        #
        #
        #

    def verRedes(self):
        print('parabéns')
        # fazer em outro arquivo
        #
        #
        #
        #
        #
    
    def materiaisDisp(self):
        print('parabéns')
        # fazer em outro arquivo
        #
        #
        #
        #
        #

        
    
canvas = TopWindow()