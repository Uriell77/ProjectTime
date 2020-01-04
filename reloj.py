#!/usr/bin/env python37
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:41:14 2019
@author: Ing. Luis Hermoso
Empresa: GP System, Media & Games
proyecto: reloj de rendimiento.
es un reloj que lleva estadisticas de tiempo invertido en determinada actividad
"""

import tkinter
import datetime
import time
from tkinter import messagebox
from winsound import PlaySound as ply
import winsound

#variable global que define el estado de las funciones
#si run es True las funciones corren, si es false se detienen
global run
run = False
global proyecto
global minute
global minut
global spin
global nproyect
global rendises
global hijo
global puls
global pul
pul = 1
global butproyect3
# =============================================================================
# funciones
# =============================================================================
def leer(arch):
    #lee el archivo que guarda las estadisticas
    proye = spin.get()
    with open(arch, "r") as f:
        linea = f.readlines()
        for i in linea:
            if i[:i.index(" ")] == proye:
                return i[i.index(" ")+1:i.index("\n")]


def escribir(nota, arch):
    #escribe en el archivo 
    with open(arch, "a") as f:
        f.write(nota)

def reescribir(nota):
    proye = spin.get()
    f = open("conteo.txt", "r+")
    linea = f.readlines()
    f.close()
    f = open("conteo.txt", "w")
    for i in linea:
        if i[:i.index(" ")] == proye:
            linea[linea.index(i)]="{} {}\n".format(proye, nota)
            f.writelines(linea)
    f.close()

            

def reset():
    #reinicia los valores a cero
    global anterior
    global horac
    global h_inicio
    global h_fin
    reescribir("00:00:00")
    h_inicio = datetime.datetime.now()
    h_fin = datetime.datetime.now()
    horac = datetime.datetime.now()
    fijo()
    
def fijo():
    #funcion que muestra valores constantes
    if run == True:
        global h_inicio
        global anterior
        h_inicio = datetime.datetime.now()
        labder.configure(text=h_inicio.strftime("%I:%M:%S %p"))
        anterior = leer("conteo.txt")
    
def reloj():
    #funcion para que el reloj sea independiente de las estadisticas
     hora = (datetime.datetime.now().time()).strftime("%I:%M:%S %p")
     labiz.configure(text="\n{}".format(hora))
     root.after(1000, reloj)
    
def conteo():
    global rendises
    #funcion que actualiza valores de las estadisticas dinamicas
    if run == True:
        horac = datetime.datetime.now()
        h_fin = horac
        rendises = h_fin.__sub__(h_inicio)
        RTotal = (datetime.datetime.strptime(anterior, "%H:%M:%S") + rendises).time().strftime("%H:%M:%S")
        reescribir(RTotal)
        resultado = '''
Inicio: {0}
Fin: {1}
Actual: {2}
      
  
RAnterior: {3}
RTotal: {4}'''.format(h_inicio.strftime("%I:%M:%S %p"), 
        h_fin.strftime("%I:%M:%S %p"), 
        str(rendises)[:7],
        anterior,
        RTotal)
        labder.configure(text=resultado)
        #print(str(rendises)[:7])
        alarm(rendises)
        root.after(1000, conteo)


def toma():
    global al
    alarma = datetime.datetime.now()
    hou = hour.get()
    minut= minute.get() 
    sec = second.get()
    al = alarma.replace(hour=int(hou), minute=int(minut), second=int(sec))
    hijo3.withdraw()
    return al

def alarm(ren):
    global al
    global butproyect3
    #print(al)
    delt = datetime.timedelta(seconds=1)
    al = al - delt
    #print(str(al)[10:19])
    if str(al)[11:19] == '00:00:00':
        messagebox.showinfo('Alarma', 'Lapso Completo')
        labbut4['text']='Alarma'
    if int(str(al)[10:13])>3:
        labbut4['text']='Alarma'
    elif int(str(al)[10:13])<=3:
        labbut4['text']='{}'.format(str(al)[10:19])
        
def pause():
    #coloca run en false para pausar los calculos
    global run
    run = False
    
def start():
    #inicia los calculos y funciones detenidos por pause
    start = True
    if start:
        global run
        run = True
        fijo()
        conteo()
    

def pulsador(*args):
    #funcion para crear un pulsador
    #puls es el boton que sera el pulsador
    global pul
    #print(pul)
    if pul == 1:
        labbut1['text']='Start'
        labbut1['bg']='green'
        labbut1['command']= start()
        pul = 0
    elif pul == 0:
        labbut1['text']='Pausa'
        labbut1['bg']='red'
        labbut1['command']= pause()
        pul = 1

    
def lista_proyect():
    global res
    res =[]
    with open("conteo.txt", "r") as f:
        lista = f.readlines()
        for i in lista:
            res.append(i[:i.index(" ")])
    return res

def lista_proyect2():
    global res
    res = ''
    with open("conteo.txt", "r") as f:
        lista = f.readlines()
        for i in lista:
            res = str(res)+str(i)
    return res

def reescribir2():
    proye = spin.get()
    pregunta = messagebox.askokcancel('Eliminar','Desea eliminar el proyecto?')
    #print(pregunta)
    if pregunta == True:
        f = open("conteo.txt", "r+")
        linea = f.readlines()
        f.close()
        f = open("conteo.txt", "w")
        for i in linea:
            if i[:i.index(" ")] == proye:
                linea[linea.index(i)]=""
                f.writelines(linea)
        f.close()
        spin['values']=lista_proyect()
    else:
        pass
    
    

def agregar_proyecto():
    proy = proyecto.get()
    hijo.withdraw()
    escribir("{} {}\n".format(proy, "00:00:00"), "conteo.txt")
    lista_proyect()
    spin.configure(values=lista_proyect())
    nproyect.delete(0,len(proy))
    

class gpinfo(object):
    
    def __init__(self, padre):
        fp = tkinter.Toplevel(padre,
                      bg='',
                      padx=10,
                      pady=10)
        fp.geometry('300x200+1000+500')
        info = '{0}\n\n{2}\n{1}\n{3}\n{4}\n{5}'.format('GP System, Media & Games ®', 'CEO: Ing. Luis Hermoso @Uriell77',
                'Empresa de desarrollo en Python','hermoso77@gmail.com\nTlf: +58 04161450146', '@Uriell77 GPSM&G',
                'San Fernando, Apure, Venezuela')
        frank1 = tkinter.Label(fp,
                       height=190,
                       width=190,
                       bg='#333986',
                       justify='center',
                       text=info,
                       foreground="white")
        frank1.pack(fill='both', expand='True')

# =============================================================================
# programa principal
    #se crea la interfaz grafica y ejecuta las funciones
# =============================================================================
#ventana principal
#=================================================
root = tkinter.Tk()
root.geometry("350x200+1000+500")
root.resizable(width="False", height="False")
root.iconbitmap(default="rend.ico")
root.iconname(newName="rendimiento")
root.title("StudyTime")
proyecto = tkinter.StringVar()

hour = tkinter.StringVar(value='0')
minute = tkinter.StringVar(value='00')
second = tkinter.StringVar(value='00')

#base maestra
#todo esta empacado en ella
#=================================================
basetotal = tkinter.Frame(root,
                          bg = "black",
                          pady=5,
                          padx=5)
basetotal.pack(fill = "both",
               expand=1)

#bases de elementos
#=================================================

#base de botones
basebut = tkinter.Frame(basetotal,
                        bg = "#333986",
                        borderwidth=2,
                        relief="groove",
                        padx=3)
basebut.pack(side = "bottom",
             fill = "both",
             expand = 1)

#base derecha
baseder = tkinter.Frame(basetotal,
                        bg = "#333986",
                        pady=10,
                        padx=3,
                        borderwidth=2,
                        relief="groove")
baseder.pack(side = "right",
             fill = "both",
             expand = 1)

#base izquierda
baseiz = tkinter.Frame(basetotal,
                        bg = "#333986",
                        pady=1,
                        padx=1,
                        borderwidth=2,
                        relief="groove")
baseiz.pack(side = "left",
             fill = "both",
             expand = 1)


#botones
#=====================================================

#boton start
labbut1 = tkinter.Button(basebut,
                       text = "Pausa",
                       width=13,
                       bg = 'red',
                       command=pulsador)
labbut1.pack(side="left",
             fill="x")
#boton reset
labbut2 = tkinter.Button(basebut,
                       text = "Reset",
                       width=13,
                       command=reset)
labbut2.pack(side="right",
             fill="x")
#boton estad
labbut3 = tkinter.Button(basebut,
                       text = "Estado",
                       width=8,
                       command=lambda:hijo2.deiconify())
labbut3.pack(side="left",
             fill="x")
#boton alarm
labbut4 = tkinter.Button(basebut,
                       text = "Alarma",
                       width=8,
                       command=lambda:hijo3.deiconify())
labbut4.pack(side="right",
             fill="x")

#etiquetas de contenido
#===================================================
labder = tkinter.Label(baseder,
                       text = "\n"*8,
                       font=("bold 10"),
                       justify="left",
                       bg="#333986",
                       padx=1,
                       foreground="white")
labder.pack(fill="both")

labizent = tkinter.Label(baseiz,
                         text='''GP System, Media 
& Games''',
                         font=("Arial",7),
                         justify="left",
                         height=2,
                         bg="#000000",
                         relief="flat",
                         foreground="white")
labizent.pack(side="top",
              fill="x")


log = tkinter.PhotoImage(file='gepe.png')
#logo = tkinter.Label(labizent, image=log, width=40, height=30)
#logo.pack(side='left')

logogp = tkinter.Button(labizent,
                        image=log,
                        borderwidth=-1,
                        height=34,
                        command=lambda *args:gpinfo(root))
logogp.pack(side='left')

labiz = tkinter.Label(baseiz,
                       text = "",
                       font=("bold 12"),
                       bg="#333986",
                       padx=3,
                       foreground="white")
labiz.pack(fill="both",
           side="top")

#boton para agregar proyecto
mas = tkinter.Button(baseiz,
                     text="+",
                     height=0,
                     width=-1,
                     command=lambda:hijo.deiconify())
mas.pack(side="left",
         fill="x",
         anchor="s")

#boton para borrar proyecto
mas2 = tkinter.Button(baseiz,
                     text="-",
                     height=0,
                     width=-1,
                     command=reescribir2)
mas2.pack(side="left",
         fill="x",
         anchor="s")
#spin para seleccionar proyecto
spin = tkinter.Spinbox(baseiz,
                       width=180,
                       values=lista_proyect(),
                       font=('', 10))
spin.pack(side="right",
          fill="x",
          anchor="s")
spin.focus()

#ventana hija para agregar proyecto

hijo = tkinter.Toplevel(root)
hijo.geometry("200x150+1050+500")
hijo.configure(bg="#333986",
               pady=30,
               borderwidth=2,
               relief="groove")
hijo.withdraw()

textoproy = tkinter.Label(hijo,
                          text="Ingrese un Nuevo Proyecto\n",
                          bg="#333986",
                          foreground="white")
textoproy.pack()

nproyect = tkinter.Entry(hijo,
                         textvariable=proyecto, 
                         width=20,
                         )
nproyect.pack()
nproyect.focus()

butproyect = tkinter.Button(hijo,
                            text="Agregar",
                            command=agregar_proyecto)
butproyect.pack(side="bottom")


#ventana hija para visualizar las estadisticas

hijo2 = tkinter.Toplevel(root,
                         padx=5)
hijo2.geometry("200x170+1050+450")
hijo2.configure(bg="#333986",
               relief="groove")
hijo2.withdraw()

fre2 = tkinter.Frame(hijo2,
                     height=100)
fre2.pack(side='top', fill='x')

loop = tkinter.Scrollbar(fre2)
loop.pack(side="right", fill="y")

textoproys = tkinter.Canvas(fre2,
                            height=140,
                          bg="#333986",
                          yscrollcommand=loop.set)
textoproys.pack(side='top',
                fill='both',
                expand='True')

loop.config(command=textoproys.yview)

texto = lista_proyect2()

textoproys.create_text(300, 0, text=texto, fill='white')
textoproys.configure(scrollregion=textoproys.bbox('all'))
butmat = tkinter.Button(hijo2,
                        text="Salir",
                        command=lambda:hijo2.withdraw())
butmat.pack(side='top',
            fill='both',
            expand='True')


#ventana hija para crear una alarma

hijo3 = tkinter.Toplevel(root)
hijo3.geometry("200x150+1050+500")
hijo3.configure(bg="#333986",
               pady=30,
               borderwidth=2,
               relief="groove")
hijo3.withdraw()

textoproy3 = tkinter.Label(hijo3,
                          text="Ingrese Tiempo de Alarma",
                          bg="#333986",
                          foreground="white")
textoproy3.pack(fill='x')

nproyect3 = tkinter.Entry(hijo3,
                         textvariable=hour, 
                         width=2,
                         )
nproyect3.place(x=50,y=32)
nproyect3.focus()
nproyect3.select_adjust(1)
nproyect31 = tkinter.Entry(hijo3,
                         textvariable=minute, 
                         width=2,
                         )
nproyect31.place(x=90,y=32)
nproyect32 = tkinter.Entry(hijo3,
                         textvariable=second, 
                         width=2,
                         )
nproyect32.place(x=130,y=32)

butproyect3 = tkinter.Button(hijo3,
                            text="Agregar",
                            command=lambda:toma())
butproyect3.pack(side="bottom")

reloj()
fijo()
conteo()
toma()

root.mainloop()

if __name__ == '__main__':
  main()