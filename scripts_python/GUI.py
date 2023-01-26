from tkinter import *             # se importa tkninter para las ventanas
import psycopg2         # permite conectarse a la base de datos y modificarla       
from funciones import *

host_v = 'localhost' # credenciales para conectarse a la base
port_v = '5432'
database_v = 'bodega_db'
user_v = 'postgres'
password_v = 'SuperBodega'

try:  # dentro de un try por si falla la conexión
    conn = psycopg2.connect(     # se conecta con la base de datos
        host = host_v, port = port_v, database = database_v, user = user_v, password = password_v
    )
    cur = conn.cursor()     # se crea cursor para ir modificando la base

except psycopg2.OperationalError:   # si es que no se conecta a la base
    print('Ocurrió un error al conectarse con la base de datos.')






root = Tk()      # se crea la ventna
root.geometry("1200x1200")

def textoCaja():
    id = cajaTexto.get()
    try:
        nom1 = ver_empleado_id(id,cur,conn)[1]
        nom2 = ver_empleado_id(id,cur,conn)[2]
        nom3 = ver_empleado_id(id,cur,conn)[3]
        nom4 = ver_empleado_id(id,cur,conn)[4]
        nom5 = ver_empleado_id(id,cur,conn)[5]

    except:
        nom1 = 'Usuaro no encontrado'
        nom2 = 'Usuaro no encontrado'
        nom3 = 'Usuaro no encontrado'
        nom4 = 'Usuaro no encontrado'
        nom5 = 'Usuaro no encontrado'
    nombre1["text"] = nom1
    nombre2["text"] = nom2
    nombre3["text"] = nom3
    nombre4["text"] = nom4
    nombre5["text"] = nom5


boton1 = Button(root, text="Buscar", command = textoCaja)
boton1.pack()

cajaTexto = Entry(root, font= "Helvetica 20")
cajaTexto.pack()

nombre1 = Label(root)
nombre1.pack()
nombre2 = Label(root)
nombre2.pack()
nombre3 = Label(root)
nombre3.pack()
nombre4 = Label(root)
nombre4.pack()
nombre5 = Label(root)
nombre5.pack()



root.mainloop()            # se inicia el main loop de la ventana