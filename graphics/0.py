import tkinter
from tkinter import Tk
from tkinter import ttk
from tkinter import Frame
from tkinter import Button
from tkinter import filedialog
from tkinter import messagebox

from graphics.Tree import Init

from code.Objects import Sesion
from code.Objects import Secreto
from graphics.Extra import Center
from graphics.Dialogs import dialogSesion
from graphics.Dialogs import dialogSetData
from graphics.Dialogs import dialogCryptData
#from graphics.Dialogs import dialogDecryptData

from code.Conector import setData
from code.Conector import getCryptedFile
from code.Conector import getCryptedInfo
from code.Conector import getCryptedPassword
from code.Conector import getHashData
from code.Conector import deleteData
from code.Conector import cryptBool

from code.Crypto import cifrar
from code.Crypto import descifrar


root = Tk()
root.geometry('1000x400')
root.title('securebox')
Center(root)

d = dialogSesion(root)
root.wait_window(d.ventana)
ss = d.sesion

if ss is not False:

    def treeRefresh():
        Init.treeRefresh(tree, ss.id)

    def pressCrypt():
        d = dialogSetData(ss, root, '', None)
        root.wait_window(d.ventana)
        treeRefresh()

    def pressDecrypt():
        try:
            selectedItem = tree.tree.focus()  # Obtenemos el foco
            id = tree.tree.item(selectedItem)['text']  # Obtenemos la id
            name = tree.tree.item(selectedItem)['values'][0]  # Obtenemos el nombre de archivo

            # Construcción del objeto de secretos
            secreto = Secreto(descifrar(
                ss.hash, getCryptedPassword(id, name)),
                descifrar(ss.hash, getCryptedInfo(id, name)),
                getCryptedFile(id, name))
            dialogCryptData(root, secreto)

            '''
            if cryptBool(id):
                datahashed = getHashData(id, name)

                def ok():
                    carpeta = filedialog.askdirectory()  # Y la carpeta donde queremos descomprimir
                    o = getCryptData(id, name)
                    with open(carpeta + '/' + name, 'wb') as f:
                        f.write(o)
                        messagebox.showinfo('Info', 'Archivo descifrado')
                        treeRefresh()

                if datahashed == ss.hash:
                    ok()
                else:
                    messagebox.showerror('Error', 'Contraseña incorrecta')
            else:
                decrypted = descifrar(ss.hash, getCryptInfo(id, name))
                messagebox.showinfo('Descifrado', 'Mensaje secreto:' + decrypted)
            '''
        except IndexError:
            messagebox.showerror('Error', 'No ha seleccionado ningún elemento')
        except TypeError:
            messagebox.showwarning('No decrypt', 'No decrypt')
        treeRefresh()

    def pressUpdate():
        selectedItem = tree.tree.focus()
        id = tree.tree.item(selectedItem)['text']
        name = tree.tree.item(selectedItem)['values'][0]
        d = dialogSetData(ss, root, '', None, id)
        root.wait_window(d.ventana)
        treeRefresh()

    def pressDelete():
        selectedItem = tree.tree.focus()
        id = tree.tree.item(selectedItem)['text']
        name = tree.tree.item(selectedItem)['values'][0]
        deleteData(id, name)
        treeRefresh()

    n = ttk.Notebook()
    f = Frame()
    tree = Init(f, ss)
    n.add(f, text='Información secreta de ' + ss.name.upper())
    n.pack(padx=10, pady=10)

    botones = Frame(root)
    botonCrypt = Button(botones, text="Cifrar info", fg='green', command=pressCrypt).pack(side='left', padx=10, pady=30)
    btonDecrypt = Button(botones, text="Descifrar", fg='red', command=pressDecrypt).pack(side='left', padx=10, pady=30)
    botonUpdate = Button(botones, text="Actualizar", fg='blue', command=pressUpdate).pack(side='left', padx=10, pady=30)
    botonDelete = Button(botones, text="Eliminar", fg='red', command=pressDelete).pack(side='left', padx=10, pady=30)
    # b6 = Button(botones, text="Updatemysql ").pack(side='left', padx=10, pady=30)
    botones.pack(side='top')

root.mainloop()
