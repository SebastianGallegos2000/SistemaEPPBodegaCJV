import app_ver_02
#from tkinter import Tk, Frame, Label, Button, Entry, Listbox, W, E, END, ANCHOR                # se importa tkninter para la interfaz gráfica
from tkinter import *
from tkinter import ttk                                            # se importa para tener tabs
import psycopg2                                                    # permite conectarse a la base de datos y modificarla       
from funciones import *                                            # se importan las funciones de queries


# credenciales para conectarse a la base
host_v = 'localhost' 
port_v = '5432'
database_v = 'bodega_db'
user_v = 'postgres'
password_v = 'SuperBodega'

def login():


    root_login = Tk()             # se crea instancia de tkinter
    root_login.title('Login')    # nombre de la ventana
    root_login.geometry('1280x720')   # se ajusta la resolución de la ventana ("1280x720" originalmente)


    frame_login = Frame(root_login)
    frame_login.pack()

    label_login_usuario = Label(frame_login, text='Usuario')
    label_login_usuario.grid(row=0, column=0)

    entry_login_usuario = Entry(frame_login)                                # caja para escribir el ID
    entry_login_usuario.grid(row=0, column=1)  

    label_login_password = Label(frame_login, text='Contraseña')
    label_login_password.grid(row=1, column=0)

    entry_login_password = Entry(frame_login)                                # caja para escribir el ID
    entry_login_password.grid(row=1, column=1)  

    label_login_status = Label(frame_login, text='')
    label_login_status.grid(row=2,column=0)

    def login_func():
        usuario = entry_login_usuario.get()
        contrasenna = entry_login_password.get()

        try:
            conn_login = psycopg2.connect(        # se conecta con la base de datos
                host = host_v, port = port_v, database = database_v, user = user_v, password = password_v
            )
            cur_login = conn_login.cursor() 

            sql_login = '''
                    SELECT id
                    FROM usuario 
                    WHERE usuario = %s 
                    AND contrasenna = %s
                '''
            
            cur_login.execute(sql_login,[usuario,contrasenna])
            id = cur_login.fetchone()

            if(id == None):
                    label_login_status['text'] = 'Usario y contraseña incorrectos'
            else:
                root_login.destroy()
                app_ver_02.main(id[0])
                

            cur_login.close()
            conn_login.close()    

        except psycopg2.OperationalError:
            label_login_status['text'] = 'No se pudo conectar a la base de datos'

    boton_login = Button(frame_login, text='Ingresar', command=login_func)         # botón para ejecutar la busqueda
    boton_login.grid(row=1, column=2)   

    root_login.mainloop()

login()