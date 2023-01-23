from tkinter import *
from tkinter import messagebox

#--------------CREACION DE VENTANA-----------------------#

ventana = Tk()
ventana.title("Log In") #Funcion para colocar nombre a la ventana.
ventana.geometry("1280x720+100+50") #Funcion para dale tamanno a la ventana.
ventana.resizable(False,False) #Funcion para que la ventana quede estática.

#--------------FIN CREACION DE VENTANA--------------------#
#----------CONFIGURACION IMAGEN DE FONDO------------------#
fondo = PhotoImage(file="fondoTI.png")
labelFondo = Label(ventana, image=fondo)
labelFondo.place(x=0,y=0,relheight=1,relwidth=1)
#----------FIN DE CONFIGURACION DE FONDO------------------#
#COLORES
# #7d7d7d Plomo Iniciar Sesion
# #000000 Negro Usuario
# #c3c3c3 Plomo claro TextoUsuario
#---------------------------------------------------------INICIO FRAME PRINCIPAL----------------------------------------------------#
frameRegistro = Frame(ventana,bg='white')
frameRegistro.place(x=380,y=40,height=600,width=521)

logo = PhotoImage(file="logoInterfaz.png")
labelLogo = Label(frameRegistro, image=logo,border=0)
labelLogo.place(x=170,y=45)

tituloRegisto = Label(frameRegistro,text="Iniciar sesión", font=("Calibri", 30, "bold"),fg="#7d7d7d",bg='white').place(x=140,y=150)
usuarioRegistro = Label(frameRegistro,text="Usuario", font=("Calibri", 18),fg="#000000",bg='white').place(x=60,y=250)
passwordRegistro = Label(frameRegistro,text="Password", font=("Calibri", 18),fg="#000000",bg='white').place(x=60,y=360)

#-----------INICIO CAPTURA DE DATOS----------------------#

textoUsuario = Entry(frameRegistro,font=("Calibri", 15),bg="#c3c3c3")
textoUsuario.place(x=60,y=295,width=390,height=30)

textoPassword = Entry(frameRegistro,font=("Calibri", 15),bg="#c3c3c3")
textoPassword.place(x=60,y=400,width=390,height=30)

#-----------FIN CAPTURA DE DATOS-------------------------#
#-----------BOTONES------------#

iniciarSesionBtn = Button(frameRegistro,command=loginFunction, text="Iniciar Sesión", font=("Calibri", 15),bg="#7d7d7d",fg="white",height=1,width=15).place(x=290,y=500)
salirBtn = Button(frameRegistro, text="Salir", font=("Calibri", 15),bg="#7d7d7d",fg="white",height=1,width=15).place(x=60,y=500)


#-----------BOTONES------------#
#---------------------------------------------------------FIN FRAME PRINCIPAL----------------------------------------------------------#
#======================= FUNCIONES LOG IN ==========================#

def loginFunction():
    if textoUsuario.get() == "" and textoPassword.get() == "":
        messagebox.showerror("Error","Todos los campos deben tener datos")
    elif textoUsuario.get() != "Sebastian" and textoPassword.get() != "123":
        messagebox.showerror("Error","Usuario inválido")
    else:
        messagebox.showinfo("Bienvenido",f"Bienvenido {textoUsuario.get()}")

    
ventana.mainloop() #Funcion para ejecutar ventana.