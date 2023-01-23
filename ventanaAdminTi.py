from tkinter import *
from tkinter import ttk


#--------------CREACION DE VENTANA-----------------------#

ventanaBodeguero = Tk()
ventanaBodeguero.title("Bodeguero") #Funcion para colocar nombre a la ventana.
ventanaBodeguero.geometry("1280x720+100+50") #Funcion para dale tamanno a la ventana.
ventanaBodeguero.resizable(False,False) #Funcion para que la ventana quede estática.


#--------------FIN CREACION DE VENTANA--------------------#
#----------CONFIGURACION IMAGEN DE FONDO------------------#
fondo = PhotoImage(file="fondoTI.png")
labelFondo = Label(ventanaBodeguero, image=fondo)
labelFondo.place(x=0,y=0,relheight=1,relwidth=1)
#----------FIN DE CONFIGURACION DE FONDO------------------#

#---------------NOTEBOOK MENU----------------#

notebookMenu = ttk.Notebook(ventanaBodeguero)
notebookMenu.pack(pady=15)
frameMenu1 = Frame(notebookMenu, width=1250,height=1000)
frameMenu2 = Frame(notebookMenu, width=500,height=500)
frameMenu3 = Frame(notebookMenu, width=1250,height=1000)
frameMenu4 = Frame(notebookMenu, width=1250,height=1000)
frameMenu5 = Frame(notebookMenu, width=1250,height=1000)
frameMenu6 = Frame(notebookMenu, width=1250,height=1000)
frameMenu7 = Frame(notebookMenu, width=1250,height=1000)

frameMenu1.pack(fill="both",expand=1)
frameMenu2.pack(fill="both",expand=1)
frameMenu3.pack(fill="both",expand=1)
frameMenu4.pack(fill="both",expand=1)
frameMenu5.pack(fill="both",expand=1)
frameMenu6.pack(fill="both",expand=1)
frameMenu7.pack(fill="both",expand=1)


notebookMenu.add(frameMenu1, text="Escanear Credencial")
notebookMenu.add(frameMenu2, text="Trabajadores")
notebookMenu.add(frameMenu3, text="EPP's")
notebookMenu.add(frameMenu4, text="Exportar documentos")
notebookMenu.add(frameMenu5, text="Insertar trabajadores")
notebookMenu.add(frameMenu6, text="Bodegueros")
notebookMenu.add(frameMenu7, text="Usuarios del sistema")

#------------------ NOTEBOOK MENU 1 ---------------------------#
textoEscaneoCredencial = Entry(frameMenu1, font=("Calibri", 15),bg="#c3c3c3")
textoEscaneoCredencial.place(x=450,y=380,width=350,height=30)

buscarBtn = Button(frameMenu1, text="Buscar", font=("Calibri", 15),bg="#7d7d7d",fg="white",height=1,width=15).place(x=545,y=450)
borrarBtn = Button(frameMenu1, text="Borrar", font=("Calibri", 15),bg="#7d7d7d",fg="white",height=1,width=15).place(x=545,y=500)

credencial = PhotoImage(file="imgCredencial.png")
labelCredencial = Label(frameMenu1, image=credencial)
labelCredencial.place(x=465,y=20)
#------------------ FIN NOTEBOOK MENU 1 ------------------------#

#-----------------NOTEBOOK MENU 2-----------------------------#

notebookTrabajadores = ttk.Notebook(frameMenu2)
notebookTrabajadores.pack(pady=2)
frameTrabajadores1 = Frame(notebookTrabajadores, width=1230, height=930)
frameTrabajadores2 = Frame(notebookTrabajadores, width=1230, height=930)
frameTrabajadores3 = Frame(notebookTrabajadores, width=1230, height=930)

frameTrabajadores1.pack(fill="both",expand=1)
frameTrabajadores2.pack(fill="both",expand=1)
frameTrabajadores3.pack(fill="both",expand=1)

notebookTrabajadores.add(frameTrabajadores1, text="Trabajadores")
notebookTrabajadores.add(frameTrabajadores2, text="Insertar trabajadores")
notebookTrabajadores.add(frameTrabajadores3, text="Editar trabajadores")
#----------------FIN NOTEBOOK MENU 2--------------------------#

#---------------- NOTEBOOK MENU 3------------------------------#

notebookEpp = ttk.Notebook(frameMenu3)
notebookEpp.pack(pady=2)
frameEpp1 = Frame(notebookEpp, width=1230, height=930)
frameEpp2 = Frame(notebookEpp, width=1230, height=930)
frameEpp3 = Frame(notebookEpp, width=1230, height=930)

frameEpp1.pack(fill="both",expand=1)
frameEpp2.pack(fill="both",expand=1)
frameEpp3.pack(fill="both",expand=1)

notebookEpp.add(frameEpp1, text="EPP's")
notebookEpp.add(frameEpp2, text="Insertar EPP")
notebookEpp.add(frameEpp3, text="Modificar EPP")
#--------------- FIN NOTEBOOK MENU 3-------------------------#
#--------------- NOTEBOOK MENU 4 ----------------------------#

#--------------- FIN NOTEBOOK MENU 4-------------------------#
#--------------- NOTEBOOK MENU 5 ----------------------------#

#--------------- FIN NOTEBOOK MENU 5-------------------------#
#--------------- NOTEBOOK MENU 6 ----------------------------#

notebookBodegueros = ttk.Notebook(frameMenu6)
notebookBodegueros.pack(pady=2)
frameBodeguero1 = Frame(notebookBodegueros, width=1230, height=930)
frameBodeguero2 = Frame(notebookBodegueros, width=1230, height=930)
frameBodeguero3 = Frame(notebookBodegueros, width=1230, height=930)

frameBodeguero1.pack(fill="both",expand=1)
frameBodeguero2.pack(fill="both",expand=1)
frameBodeguero3.pack(fill="both",expand=1)

notebookBodegueros.add(frameBodeguero1,text="Bodegueros")
notebookBodegueros.add(frameBodeguero2,text="Insertar Bodeguero")
notebookBodegueros.add(frameBodeguero3,text="Modificar Bodeguero")
#--------------- FIN NOTEBOOK MENU 6-------------------------#
#------------------ NOTEBOOK MENU 7 --------------------------#
notebookUsuarios = ttk.Notebook(frameMenu7)
notebookUsuarios.pack(pady=2)
frameUsuario1 = Frame(notebookUsuarios, width=1230, height=930)
frameUsuario2 = Frame(notebookUsuarios, width=1230, height=930)
frameUsuario3 = Frame(notebookUsuarios, width=1230, height=930)

frameUsuario1.pack(fill="both",expand=1)
frameUsuario2.pack(fill="both",expand=1)
frameUsuario3.pack(fill="both",expand=1)

notebookUsuarios.add(frameUsuario1,text="Usuarios")
notebookUsuarios.add(frameUsuario2,text="Insertar Usuarios")
notebookUsuarios.add(frameUsuario3,text="Modificar Usuarios")
#--------------- FIN NOTEBOOK MENU 7-------------------------#
ventanaBodeguero.mainloop() #Funcion para ejecutar ventana.