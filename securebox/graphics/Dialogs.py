from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import getpass

from Conector import getSesion
from Conector import setSesion
from Conector import setData
from Conector import getDataById
from Conector import updateData
from Conector import existUser

from Objects import Sesion
from Objects import Secreto
from Cryptos import getHash
from Cryptos import cifrar
from Cryptos import descifrar
from Generator import generatorClave


'''
Diálogo de inicio de sesión.
'''
class dialogSesion:
    def __init__(self, padre):
        self.sesion = Sesion

        self.ventana = Toplevel(padre)
        self.ventana.geometry('200x250')
        self.ventana.transient(padre)

        self.ventana.title('Inicio de sesión')
        self.ventana.bind('<Return>', self.pressAceptar)
        self.ventana.bind('<Escape>', self.pressCancelar)

        self.user = StringVar()
        self.user.set(getpass.getuser())
        self.password = StringVar()
        self.p = IntVar()

        Label(self.ventana, text='Usuario').pack()
        self.userEntry = Entry(self.ventana, text=self.user)
        self.userEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Contraseña').pack()
        self.passEntry = Entry(self.ventana, text=self.password, show='·')
        self.passEntry.pack(padx=15, pady=5)
        self.passEntry.focus_set()
        self.checkShowPassword = Checkbutton(self.ventana, text='Mostrar clave', variable=self.p, command=self.showPassword).pack()

        botonAceptar = Button(self.ventana, text='Aceptar', command=self.pressAceptar).pack(pady=5)
        botonNuevo = Button(self.ventana, text='Nuevo usuario', command=self.pressNuevo).pack(pady=5)
        botonCancelar = Button(self.ventana, text='Cancelar', command=self.pressCancelar).pack(pady=5)

    def showPassword(self):
        if self.p.get() == 0:
            self.passEntry.config(show='·')
        else:
            self.passEntry.config(show='')

    def pressAceptar(self, event=None):
        self.sesion = getSesion(self.user.get(), getHash(self.password.get()))

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
        dialogNewSesion(self.ventana)


'''
Diálogo de creación de nuevo usuario.
'''
class dialogNewSesion:
    def __init__(self, padre):

        self.ventana = Toplevel(padre)
        self.ventana.transient(padre)

        self.ventana.title('Nuevo usuario')
        self.ventana.bind('<Return>', self.pressCreate)
        self.ventana.bind('<Escape>', self.pressCancelar)

        self.name = StringVar()
        self.name.set(getpass.getuser())
        self.password = StringVar()
        self.p = IntVar()

        Label(self.ventana, text='Nombre').pack()
        self.nameEntry = Entry(self.ventana, text=self.name)
        self.nameEntry.pack(padx=15, pady=5)

        Label(self.ventana, text='Contraseña').pack()
        self.passEntry = Entry(self.ventana, text=self.password, show='·')
        self.passEntry.pack(padx=15, pady=5)
        self.passEntry.focus_set()
        self.checkShowPassword = Checkbutton(self.ventana, text='Mostrar clave', variable=self.p, command=self.showPassword).pack()

        botonGenerate = Button(self.ventana, text='Generar contraseña', command=self.pressGenerate).pack(pady=5)
        botonAceptar = Button(self.ventana, text='Crear', command=self.pressCreate).pack(pady=5)
        botonCancelar = Button(self.ventana, text='Cancelar', command=self.pressCancelar).pack(pady=5)

    def showPassword(self):
        if self.p.get() == 0:
            self.passEntry.config(show='·')
        else:
            self.passEntry.config(show='')

    def pressGenerate(self, event=None):
        d = dialogGenerator(self.ventana)
        self.ventana.wait_window(d.ventana)
        self.password.set('')
        self.password.set(d.password.get())
        print(self.password.get())

    def pressCreate(self, event=None):
        if self.name.get() == '' or self.password.get() == '' or existUser(self.name.get()):
            messagebox.showerror('Usuario no creado', 'No es posible crear el usuario')
        else:
            setSesion(self.name.get(), getHash(self.password.get()))
            messagebox.showinfo('Usuario creado', 'Usuario creado correctamente')
        self.ventana.destroy()

    def pressCancelar(self, event=None):
        self.ventana.destroy()


'''
Diálogo de creación de nueva información secreta.
Este diálogo hace las veces de crear y actualizar.
'''
class dialogSetData:
    def __init__(self, sesion, padre, id, filename=''):
        self.padre = padre
        self.filename = filename
        self.sesion = sesion
        self.id = id

        self.ventana = Toplevel(padre)
        self.ventana.geometry('200x470')
        self.ventana.transient(padre)

        self.ventana.title('Cifrar')
        self.ventana.bind('<Return>', self.pressAceptar)
        self.ventana.bind('<Escape>', self.pressCancelar)

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
            self.site.set(self.data[7])
            self.user = StringVar()
            self.user.set(self.data[8])
            self.mail = StringVar()
            self.mail.set(self.data[9])

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
            self.notes.insert(INSERT, self.data[10])

        botonAceptar = Button(self.ventana, text='Aceptar', command=self.pressAceptar).pack(pady=5)
        botonCancelar = Button(self.ventana, text='Cancelar', command=self.pressCancelar).pack(pady=5)

    def pressAceptar(self, event=None):
        if self.name.get() == '':
            messagebox.showerror('No creado', 'El nombre no puede estar en blanco')
        else:
            if self.id is None:
                d = dialogCryptData(self.ventana, None)
                self.ventana.wait_window(d.ventana)
                secreto = d.secreto

                setData(self.name.get(), self.algorithm.get(), self.sesion.id, self.password.get(),
                    secreto.file, cifrar(self.sesion.hash, secreto.password), cifrar(self.sesion.hash, secreto.info),
                    self.site.get(), self.user.get(), self.mail.get(), self.notes.get(1.0, END))
            else:
                secreto = Secreto(
                    descifrar(self.sesion.hash, self.data[4]),
                    descifrar(self.sesion.hash, self.data[5]),
                    self.data[6])
                d = dialogCryptData(self.ventana, secreto)
                self.ventana.wait_window(d.ventana)
                updateData(self.name.get(), self.data[2] + 1, self.algorithm.get(), self.password.get(),
                           cifrar(self.sesion.hash, d.secreto.password), cifrar(self.sesion.hash, d.secreto.info), d.secreto.file,
                           self.site.get(), self.user.get(), self.mail.get(), self.notes.get(1.0, END), self.sesion.id, self.id)

            self.ventana.destroy()

    def pressCancelar(self, event=None):
        self.ventana.destroy()


''' 
 Diálogo de gestión de información secreta para cifrar.
 Este diálogo hace las veces de crear y de visualizar información secreta.
 Además es llamado por dialogSetData tanto al crear como al actualizar información.
'''
class dialogCryptData:
    def __init__(self, padre, secreto):
        self.secreto = secreto

        self.ventana = Toplevel(padre)
        self.ventana.transient(padre)
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
        self.secreto = Secreto(self.password.get(), self.info.get(1.0, END), None)

        if self.f.get() == 1:
            archivo = filedialog.askopenfile()
            with open(archivo.name, 'rb') as f:
                self.secreto.file = f.read()

        self.ventana.destroy()

'''
Diálogo de generador de contraseña.
'''
class dialogGenerator:
    def __init__(self, padre):

        self.ventana = Toplevel(padre)
        self.ventana.transient(padre)

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

    def pressGenerate(self, event=None):
        self.password.set('')
        self.password.set(generatorClave(self.n.get(), self.l.get(), self.s.get(), self.long.get()))

    def pressOk(self, event=None):
        self.ventana.destroy()
