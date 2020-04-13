import tkinter as tk
from tkinter import ttk
from tkinter import font
from Conector import getData
from Conector import cryptBool

cabecera = ['Nombre', 'Versión', 'Cifrado', 'Sitio', 'Usuario', 'Mail', 'Notas']

class Init:

    cabecera = cabecera

    def __init__(self, master, sesion):
        self.sesion = sesion

        def ordenar(tree, columna, descendiente):
            data = [(tree.set(child, columna), child) \
                    for child in tree.get_children('')]
            data.sort(reverse=descendiente)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)

            tree.heading(columna, command=lambda col=columna: ordenar(tree, col, int(not descendiente)))

        self.tree = ttk.Treeview(master, columns=self.cabecera, show='headings')
        self.tree.column(cabecera[0], width=130)
        self.tree.column(cabecera[1], width=60)
        self.tree.column(cabecera[2], width=60)
        self.tree.column(cabecera[3], width=140)
        self.tree.column(cabecera[4], width=120)
        self.tree.column(cabecera[5], width=200)
        self.tree.pack()

        scrolly = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        scrollx = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=master)
        scrolly.grid(column=1, row=0, sticky='ns', in_=master)
        scrollx.grid(column=0, row=1, sticky='ew', in_=master)

        for col in self.cabecera:
            self.tree.heading(col, text=col.title(),
                         command=lambda c=col: ordenar(self.tree, c, 0))

        self.treeRefresh(sesion.id)

    def treeRefresh(self, property):
        valores = getData(property)
        items = self.tree.get_children()

        # Reseteo de tabla
        for item in items:
            self.tree.delete(item)

        for elemento in valores:

            e = elemento[1:]

            if cryptBool(elemento[0]) == 1:
                self.tree.insert('', 'end', text=elemento[0], values=e, tags=('file',))
            else:
                self.tree.insert('', 'end', text=elemento[0], values=e, tags=('text',))
                #hola = self.tree.insert('', 'end', text="Dir 3", values='↘')
                #self.tree.insert(hola, 'end', text=" sub dir 3", values=("3A AGHJSG ASHJAG SJAHSG JAHSG AJHSG AJHSG AJHSAG SHJAG SHJAG JHA SHJAG SJA", " 3B"))
            self.tree.tag_configure('file', background='#73F63B')
            self.tree.tag_configure('text', background='#B0FA92')


            '''
            [DEPRECATED]
            # Ajusta el ancho de la columna si fuera necesarioen función de la longitud del elemento
            for ix, val in enumerate(e):
                col_w = font.Font().measure(val)
                if self.tree.column(self.cabecera[ix], width=None) < col_w:
                    self.tree.column(self.cabecera[ix], width=col_w)
            '''