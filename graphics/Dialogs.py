from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import getpass

from code.Conector import getSesion
from code.Conector import setSesion
from code.Conector import setData
from code.Conector import getDataById
from code.Conector import updateData

from graphics.Extra import Center
from code.Objects import Sesion
from code.Objects import Secreto
from code.Crypto import getHash
from code.Crypto import cifrar
from code.Generator import generatorClave


class dialogSesion:
    def __init__(self, padre):
        self.sesion = Sesion

        self.ventana = Toplevel(padre)
        self.ventana.geometry('200x250')
        self.ventana.transient(padre)
        Center(self.ventana)

        self.ventana.title('Inicio de sesión')
        self.ventana.bind('<Return>', self.pressAceptar)  # Al darle a INTRO se pulsará el botón Aceptar
        self.ventana.bind('<Escape>', self.pressCancelar)  # Al darle a ESC se pulsará el botón Cancelar

        self.user = StringVar()
        self.user.set(getpass.getuser())
        self.password = StringVar()

        Label(self.ventana, text='Usuario').pack()
        self.userEntry = Entry(self.ventana, text=self.user)
        self.userEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Contraseña').pack()
        self.passEntry = Entry(self.ventana, text=self.password, show='·')
        self.passEntry.pack(padx=15, pady=5)
        self.passEntry.focus_set()

        botonAceptar = Button(self.ventana, text='Aceptar', command=self.pressAceptar).pack(pady=5)
        botonNuevo = Button(self.ventana, text='Nuevo usuario', command=self.pressNuevo).pack(pady=5)
        botonCancelar = Button(self.ventana, text='Cancelar', command=self.pressCancelar).pack(pady=5)

    def pressAceptar(self, event=None):
        self.sesion = getSesion(self.user.get(), self.password.get())

        if self.sesion:
            self.ventana.destroy()
        else:
            self.password.set('')
            self.userEntry.configure({'background': 'Red', 'foreground': 'White'})
            self.passEntry.configure({'background': 'Red', 'foreground': 'White'})
            self.passEntry.focus_set()

    def pressCancelar(self, event=None):
        self.ventana.destroy()

    def pressNuevo(self, event=None):
        dialogSetSesion(self.ventana)


class dialogSetSesion:
    def __init__(self, padre):

        self.ventana = Toplevel(padre)
        self.ventana.transient(padre)
        Center(self.ventana)

        self.ventana.title('Nuevo usuario')
        self.ventana.bind('<Return>', self.pressCreate)  # Al darle a INTRO se pulsará el botón Aceptar
        self.ventana.bind('<Escape>', self.pressCancelar)  # Al darle a ESC se pulsará el botón Cancelar

        self.name = StringVar()
        self.name.set(getpass.getuser())
        self.password = StringVar()

        Label(self.ventana, text='Nombre').pack()
        self.nameEntry = Entry(self.ventana, text=self.name)
        self.nameEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Contraseña').pack()
        self.passwordEntry = Entry(self.ventana, text=self.password, show='·')
        self.passwordEntry.pack(padx=15, pady=5)
        self.passwordEntry.focus_set()

        botonGenerate = Button(self.ventana, text='Generar contraseña', command=self.pressGenerate).pack(pady=5)
        botonAceptar = Button(self.ventana, text='Crear', command=self.pressCreate).pack(pady=5)
        botonCancelar = Button(self.ventana, text='Cancelar', command=self.pressCancelar).pack(pady=5)

    def pressGenerate(self, event=None):
        d = dialogGenerator(self.ventana)
        self.ventana.wait_window(d.ventana)
        self.password.set('')
        self.password.set(d.password.get())
        print(self.password.get())

    def pressCreate(self, event=None):
        setSesion(self.name.get(), self.password.get())
        self.ventana.destroy()

    def pressCancelar(self, event=None):
        self.ventana.destroy()


class dialogSetData:
    def __init__(self, sesion, padre, filename, id):
        self.padre = padre
        self.filename = filename
        self.sesion = sesion
        self.id = id

        self.ventana = Toplevel(padre)
        self.ventana.geometry('200x470')
        self.ventana.transient(padre)
        Center(self.ventana)

        self.ventana.title('Cifrar')
        self.ventana.bind('<Return>', self.pressAceptar)  # Al darle a INTRO se pulsará el botón Aceptar
        self.ventana.bind('<Escape>', self.pressCancelar)  # Al darle a ESC se pulsará el botón Cancelar

        if id is None:
            self.name = StringVar()
            self.name.set(filename.split("/")[len(filename.split("/")) - 1])
            self.password = StringVar()
            self.password.set(sesion.hash)
            self.algorithm = StringVar()
            self.algorithm.set('AES')
            self.site = StringVar()
            self.user = StringVar()
            self.mail = StringVar()
        else:
            self.data = getDataById(sesion.id, id)
            self.name = StringVar()
            self.name.set(self.data[1])
            self.password = StringVar()
            self.password.set(sesion.hash)
            self.algorithm = StringVar()
            self.algorithm.set(self.data[3])
            self.site = StringVar()
            self.site.set(self.data[4])
            self.user = StringVar()
            self.user.set(self.data[5])
            self.mail = StringVar()
            self.mail.set(self.data[6])

        Label(self.ventana, text='Nombre').pack()
        self.nameEntry = Entry(self.ventana, text=self.name)
        self.nameEntry.pack(padx=15, pady=5)
        self.nameEntry.focus_set()

        Label(self.ventana, text='Contraseña').pack()
        self.passwordEntry = Entry(self.ventana, text=self.password, show='·', state='disabled')
        self.passwordEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Algoritmo').pack()
        self.algorithmEntry = Entry(self.ventana, text=self.algorithm, state='disabled')
        self.algorithmEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Sitio').pack()
        self.siteEntry = Entry(self.ventana, text=self.site)
        self.siteEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Usuario de sitio').pack()
        self.userEntry = Entry(self.ventana, text=self.user)
        self.userEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Mail').pack()
        self.mailEntry = Entry(self.ventana, text=self.mail)
        self.mailEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Notas').pack()
        self.notes = Text(self.ventana, height=3)
        self.notes.pack(padx=15, pady=5)

        if id is not None:
            self.notes.insert(INSERT, self.data[7])

        botonAceptar = Button(self.ventana, text='Aceptar', command=self.pressAceptar).pack(pady=5)
        botonCancelar = Button(self.ventana, text='Cancelar', command=self.pressCancelar).pack(pady=5)

    def pressAceptar(self, event=None):
        d = dialogCryptData(self.ventana, None)
        self.ventana.wait_window(d.ventana)

        if self.id is None:
            secreto = d.secreto
            setData(self.name.get(), self.algorithm.get(), self.sesion.id, self.password.get(),
                    secreto.file, cifrar(self.sesion.hash, secreto.password), cifrar(self.sesion.hash, secreto.info),
                    self.site.get(), self.user.get(), self.mail.get(), self.notes.get(1.0, END))
        else:
            print('Actualizar archivo')


        '''
        if self.file is None:
            if self.id is None:
                d = dialogCryptData(self.ventana, 'Contraseña o texto a cifrar', '')
                self.ventana.wait_window(d.ventana)
                setData(self.name.get(), self.algorithm.get(), self.sesion.id, self.password.get(),
                        self.notes.get(1.0, END), self.site.get(), self.user.get(), self.mail.get(), None,
                        cryptInfo(self.sesion.hash, d.password.get()))
            else:
                d = dialogCryptData(self.ventana, 'Contraseña o texto a cifrar', 'default')
                self.ventana.wait_window(d.ventana)
                version = self.data[2] + 1

                updateData(self.name.get(), version, self.algorithm.get(), self.password.get(), self.site.get(),
                           self.user.get(), self.mail.get(), None, cryptInfo(self.sesion.hash, d.password.get()),
                           self.notes.get(1.0, END), self.sesion.id, self.id)
        else:
            setData(self.name.get(), self.algorithm.get(), self.sesion.id, self.password.get(),
                    self.notes.get(1.0, END), self.site.get(), self.user.get(), self.mail.get(), self.file, None)
        '''
        self.ventana.destroy()

    def pressCancelar(self, event=None):
        self.ventana.destroy()


''' 
 Diálogo de gestión de información secreta para cifrar
'''
class dialogCryptData:
    def __init__(self, padre, secreto):
        self.secreto = secreto

        self.ventana = Toplevel(padre)
        self.ventana.transient(padre)
        Center(self.ventana)
        self.ventana.bind('<Return>', self.pressOk)
        self.ventana.bind('<Escape>', self.pressOk)

        self.password = StringVar()
        self.f = IntVar()
        self.p = IntVar()
        self.file = None

        Label(self.ventana, text='Contraseña').pack()
        self.passwordEntry = Entry(self.ventana, text=self.password, show='·')
        self.passwordEntry.pack(padx=15, pady=5)
        self.passwordEntry.focus_set()

        self.checkShowPassword = Checkbutton(self.ventana, text='Mostrar clave', variable=self.p, command=self.showPassword).pack()

        Label(self.ventana, text='Información secreta').pack()
        self.info = Text(self.ventana, height=3)
        self.info.pack(padx=15, pady=5)

        if secreto is not None:
            self.password.set(secreto.password)
            self.info.insert(END, secreto.info)
            botonFile = Button(self.ventana, text='Descargar archivo', command=self.pressFile).pack(pady=5)
        else:
            self.checkFile = Checkbutton(self.ventana, text='Archivo adjunto', variable=self.f).pack()

        botonOk = Button(self.ventana, text='Ok', command=self.pressOk).pack(pady=5)

    def showPassword(self):
        if self.p.get() == 0:
            self.passwordEntry.config(show='·')
        else:
            self.passwordEntry.config(show='')
    def pressFile(self):
        carpeta = filedialog.askdirectory()
        with open(carpeta + '/' + 'DESCIFRADO', 'wb') as f:
            f.write(self.secreto.file)
            messagebox.showinfo('Info', 'Archivo descifrado')

    def pressOk(self, event=None):
        if self.secreto is None:
            self.secreto = Secreto(self.password.get(), self.info.get(1.0, END), None)

            if self.f.get() == 1:
                archivo = filedialog.askopenfile()
                with open(archivo.name, 'rb') as f:
                    #self.file = f.read()
                    self.secreto.file = f.read()

        self.ventana.destroy()


class dialogGenerator:
    def __init__(self, padre):

        self.ventana = Toplevel(padre)
        self.ventana.transient(padre)
        Center(self.ventana)

        self.ventana.bind('<Return>', self.pressOk)
        self.ventana.bind('<Escape>', self.pressOk)

        self.password = StringVar()
        self.n = IntVar()
        self.l = IntVar()
        self.s = IntVar()

        Label(self.ventana, text='Contraseña').pack()
        self.passwordEntry = Entry(self.ventana, text=self.password)
        self.passwordEntry.pack(padx=15, pady=5)
        self.passwordEntry.focus_set()

        self.numeros = Checkbutton(self.ventana, text='Números', variable=self.n).pack()
        self.letras = Checkbutton(self.ventana, text='Letras', variable=self.l).pack()
        self.special = Checkbutton(self.ventana, text='Caracteres especiales', variable=self.s).pack()
        self.long = Spinbox(self.ventana, from_=4, to=64)
        self.long.pack()

        botonGenerate = Button(self.ventana, text='Generar', command=self.pressGenerate).pack(pady=5)
        botonOk = Button(self.ventana, text='Ok', command=self.pressOk).pack(pady=5)

    def pressGenerate(self):
        self.password.set('')
        self.password.set(generatorClave(self.n.get(), self.l.get(), self.s.get(), self.long.get()))

    def pressOk(self):
        self.ventana.destroy()
