import tkinter
from tkinter import Tk
from tkinter import ttk
from tkinter import Frame
from tkinter import Button
from tkinter import filedialog
from tkinter import messagebox

from graphics.Tree import Init

from code.Objects import Sesion
from graphics.Extra import Center
from graphics.Dialogs import dialogSesion
from graphics.Dialogs import dialogSetData
from graphics.Dialogs import dialogCryptPass
#from graphics.Dialogs import dialogDecryptData

from code.Conector import setData
from code.Conector import getCryptData
from code.Conector import getCryptInfo
from code.Conector import getHashData
from code.Conector import deleteData
from code.Conector import cryptBool

from code.Crypto import cifrar
from code.Crypto import descifrar
from code.Crypto import decryptInfo


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

    def pressCryptFile():
        archivo = filedialog.askopenfile()
        with open(archivo.name, 'rb') as f: file = f.read()

        #cifrar(b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18', archivo.name)

        # Envío el propiertario, el padre, el nombre de archivo y el archivo
        d = dialogSetData(ss, root, archivo.name, file)
        root.wait_window(d.ventana)
        treeRefresh()

    def pressCryptInfo():
        d = dialogSetData(ss, root, '', None)
        root.wait_window(d.ventana)
        treeRefresh()

    def pressDecrypt():
        try:
            selectedItem = tree.tree.focus()  # Obtenemos el foco
            id = tree.tree.item(selectedItem)['text']  # Obtenemos la id
            name = tree.tree.item(selectedItem)['values'][0]  # Obtenemos el nombre de archivo

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
                decrypted = decryptInfo(ss.hash, getCryptInfo(id, name))
                messagebox.showinfo('Descifrado', 'Mensaje secreto:' + decrypted)

        except IndexError:
            messagebox.showerror('Error', 'No ha seleccionado ningún elemento')
        except TypeError:
            messagebox.showwarning('No decrypt', 'No decrypt')
        treeRefresh()

    def pressDelete():
        selectedItem = tree.tree.focus()
        id = tree.tree.item(selectedItem)['text']
        name = tree.tree.item(selectedItem)['values'][0]
        deleteData(id, name)
        treeRefresh()

    n = ttk.Notebook()
    f_0 = Frame()
    f = Frame()
    tree = Init(f, ss)
    n.add(f, text='Información secreta de ' + ss.name.upper())
    n.pack(padx=10, pady=10)

    botones = Frame(root)
    botonCryptFile = Button(botones, text="Cifrar archivo", fg='green', command=pressCryptFile).pack(side='left',
                                                                                                     padx=10, pady=30)
    botonCryptInfo = Button(botones, text="Cifrar info", fg='green', command=pressCryptInfo).pack(side='left', padx=10,
                                                                                                  pady=30)
    btonDecrypt = Button(botones, text="Descifrar", fg='red', command=pressDecrypt).pack(side='left', padx=10,
                                                                                                 pady=30)
    botonDelete = Button(botones, text="Eliminar", fg='red', command=pressDelete).pack(side='left', padx=10, pady=30)
    # b6 = Button(botones, text="Updatemysql ").pack(side='left', padx=10, pady=30)
    botones.pack(side='top')

root.mainloop()
