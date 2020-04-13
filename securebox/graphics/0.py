from tkinter import Tk
from tkinter import ttk
from tkinter import Frame
from tkinter import Button
from tkinter import messagebox

from Tree import Init

from Dialogs import dialogSesion
from Dialogs import dialogSetData
from Dialogs import dialogCryptData

from Conector import getCryptedFile
from Conector import getCryptedInfo
from Conector import getCryptedPassword
from Conector import deleteData

from Cryptos import descifrar
from Objects import Secreto


root = Tk()
root.geometry('1000x400')
root.title('securebox')

d = dialogSesion(root)
root.wait_window(d.ventana)
ss = d.sesion

if ss is not False:

    def treeRefresh():
        Init.treeRefresh(tree, ss.id)

    def pressCrypt(event=None):
        d = dialogSetData(ss, root, None)
        root.wait_window(d.ventana)
        treeRefresh()

    def pressDecrypt(event=None):
        try:
            selectedItem = tree.tree.focus()
            id = tree.tree.item(selectedItem)['text']
            name = tree.tree.item(selectedItem)['values'][0]

            secreto = Secreto(
                descifrar(ss.hash, getCryptedPassword(id, name)),
                descifrar(ss.hash, getCryptedInfo(id, name)),
                getCryptedFile(id, name))
            dialogCryptData(root, secreto)

        except IndexError:
            messagebox.showerror('Error', 'No ha seleccionado ningún elemento')
        except TypeError:
            messagebox.showwarning('No decrypt', 'No decrypt')
        treeRefresh()

    def pressUpdate(event=None):
        try:
            selectedItem = tree.tree.focus()
            id = tree.tree.item(selectedItem)['text']
            d = dialogSetData(ss, root, id)
            root.wait_window(d.ventana)
        except IndexError:
            messagebox.showerror('Error', 'No ha seleccionado ningún elemento')
        except TypeError:
            messagebox.showerror('Error', 'No ha seleccionado ningún elemento')
        treeRefresh()

    def pressDelete(event=None):
        try:
            selectedItem = tree.tree.focus()
            id = tree.tree.item(selectedItem)['text']
            name = tree.tree.item(selectedItem)['values'][0]
            deleteData(id, name)
            treeRefresh()
        except IndexError:
            messagebox.showerror('Error', 'No ha seleccionado ningún elemento')

    def pressExit(event=None):
        root.destroy()

    root.bind('<c>', pressCrypt)
    root.bind('<d>', pressDecrypt)
    root.bind('<Double-Button-1>', pressDecrypt)
    root.bind('<Delete>', pressDelete)
    root.bind('<u>', pressUpdate)
    root.bind('<Escape>', pressExit)

    n = ttk.Notebook()
    f = Frame()
    tree = Init(f, ss)
    n.add(f, text='Información secreta de ' + ss.name.upper())
    n.pack(padx=10, pady=10)

    botones = Frame(root)
    botonCrypt = Button(botones, text="Cifrar", fg='green', command=pressCrypt).pack(side='left', padx=10, pady=30)
    btonDecrypt = Button(botones, text="Descifrar", fg='red', command=pressDecrypt).pack(side='left', padx=10, pady=30)
    botonUpdate = Button(botones, text="Actualizar", fg='blue', command=pressUpdate).pack(side='left', padx=10, pady=30)
    botonDelete = Button(botones, text="Eliminar", fg='red', command=pressDelete).pack(side='left', padx=10, pady=30)
    botones.pack(side='top')

root.mainloop()
