import tkinter as tk
def about():
    wind = tk.Toplevel()
    txt = 'Interface para criação de Redes Neurais com Keras.'
    txt+='\nSoftware desenvolvido por Fabio Augusto Ramalho,'
    txt+='\ngraduando em Engenharia de Computação pela UNIFEI.'
    txt+='\n\nAplicação sob condições da licença GPL (GNU General Public License).\n'
    tk.Label(wind, text = txt).pack()

def plot(x,y,x_label,y_label,title,grid,modo):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if(grid): plt.grid()
    plt.plot(x, y, modo)
    plt.show()