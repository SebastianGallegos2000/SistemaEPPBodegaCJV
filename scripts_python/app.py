from tkinter import Tk, Frame, Label, Button, Entry                # se importa tkninter para la interfaz gráfica
from tkinter import ttk                                            # se importa para tener tabs
import psycopg2                                                    # permite conectarse a la base de datos y modificarla       
from funciones import *                                            # se importan las funciones de queries

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


root = Tk()             # se crea instancia de tkinter
root.title("Bodega")    # nombre de la ventana
root.geometry("500x500")

# resolución de la pantalla
ancho_pantalla = root.winfo_screenmmwidth() 
alto_pantalla = root.winfo_screenmmheight() 


tabs = ttk.Notebook(root)
tabs.pack(pady=15)

frame = Frame(tabs,width=500,height=500) 
frame.pack(fill="both", expand=1)

tabs.add(frame, text='Buscar o editar empleado')
# canvas
# canvas = Canvas(root, height=alto_pantalla*3, width=ancho_pantalla*3)    # widget para tener todo en la app
# canvas.pack()                                   # se ubica correctamente en la ventana


def inputID():
    id = entry_id.get()
    lista = ['']*12         # lista para los doce atributos
    try:
        res = ver_empleado_id(id,cur)
        for i in range(0,12):
            lista[i] = res[i]
    except:
        for i in range(0,12):
            lista[i] = ''
    for i in range(0,12):
        lista_output[i]['text'] = lista[i]

def inputNombre():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    lista = ['']*12         # lista para los doce atributos
    try:
        res = ver_empleado_nombre(nombre,apellido,cur)
        for i in range(0,12):
            lista[i] = res[i]
    except:
        for i in range(0,12):
            lista[i] = ''
    for i in range(0,12):
        lista_output[i]['text'] = lista[i]

label_id_input = Label(frame, text='ID:')  # label con texto en el frame 
label_id_input.grid(row=0, column=0)                  # se pone en el frame

entry_id = Entry(frame)                               # caja para escribir el ID
entry_id.grid(row=0, column=1)                        # se ubica la caja en el frame

boton_buscar_id = Button(frame, text='Buscar', command=inputID)     # botón para ejecutar la busqueda
boton_buscar_id.grid(row=0, column=2)                               # se ubica el botón en el frame

label_nombre_input = Label(frame, text='Nombre:')        # label con texto en el frame
label_nombre_input.grid(row=1, column=0)                            # se ubica en el frame

entry_nombre = Entry(frame)         # caja para texto del nombre
entry_nombre.grid(row=1, column=1)      # se ubica en el frame

label_apellido_input = Label(frame, text='Apellido:')        # label con texto en el frame
label_apellido_input.grid(row=2, column=0)                            # se ubica en el frame

entry_apellido = Entry(frame)         # caja para texto del nombre
entry_apellido.grid(row=2, column=1)      # se ubica en el frame

boton_buscar_nombre = Button(frame, text='Buscar', command=inputNombre)     # botón para ejecutar la busqueda
boton_buscar_nombre.grid(row=1, column=2)                               # se ubica el botón en el frame



pos_y=3

label_id = Label(frame, text='ID:')  # label con texto en el frame 
label_id.grid(row=pos_y, column=0)       # se pone en el frame
label_id_output = Label(frame, text='')  # label con texto en el frame 
label_id_output.grid(row=pos_y, column=1)       # se pone en el frame

label_nombre1 = Label(frame, text='Primer Nombre:')  # label con texto en el frame 
label_nombre1.grid(row=pos_y+1, column=0)       # se pone en el frame
label_nombre1_output = Label(frame, text='')  # label con texto en el frame 
label_nombre1_output.grid(row=pos_y+1, column=1)       # se pone en el frame

label_nombre2 = Label(frame, text='Segundo Nombre:')  # label con texto en el frame 
label_nombre2.grid(row=pos_y+2, column=0)       # se pone en el frame
label_nombre2_output = Label(frame, text='')  # label con texto en el frame 
label_nombre2_output.grid(row=pos_y+2, column=1)       # se pone en el frame

label_nombre3 = Label(frame, text='Tercer Nombre:')  # label con texto en el frame 
label_nombre3.grid(row=pos_y+3, column=0)       # se pone en el frame
label_nombre3_output = Label(frame, text='')  # label con texto en el frame 
label_nombre3_output.grid(row=pos_y+3, column=1)       # se pone en el frame

label_apellidoP = Label(frame, text='Apellido Paterno:')  # label con texto en el frame 
label_apellidoP.grid(row=pos_y+4, column=0)       # se pone en el frame
label_apellidoP_output = Label(frame, text='')  # label con texto en el frame 
label_apellidoP_output.grid(row=pos_y+4, column=1)       # se pone en el frame

label_apellidoM = Label(frame, text='Apellido Materno:')  # label con texto en el frame 
label_apellidoM.grid(row=pos_y+5, column=0)       # se pone en el frame
label_apellidoM_output = Label(frame, text='')  # label con texto en el frame 
label_apellidoM_output.grid(row=pos_y+5, column=1)       # se pone en el frame

label_vigencia = Label(frame, text='Vigencia:')  # label con texto en el frame 
label_vigencia.grid(row=pos_y+6, column=0)       # se pone en el frame
label_vigencia_output = Label(frame, text='')  # label con texto en el frame 
label_vigencia_output.grid(row=pos_y+6, column=1)       # se pone en el frame

label_gerencia = Label(frame, text='Gerencia:')  # label con texto en el frame 
label_gerencia.grid(row=pos_y+7, column=0)       # se pone en el frame
label_gerencia_output = Label(frame, text='')  # label con texto en el frame 
label_gerencia_output.grid(row=pos_y+7, column=1)       # se pone en el frame

label_departamento = Label(frame, text='Departamento:')  # label con texto en el frame 
label_departamento.grid(row=pos_y+8, column=0)       # se pone en el frame
label_departamento_output = Label(frame, text='')  # label con texto en el frame 
label_departamento_output.grid(row=pos_y+8, column=1)       # se pone en el frame

label_seccion = Label(frame, text='Sección:')  # label con texto en el frame 
label_seccion.grid(row=pos_y+9, column=0)       # se pone en el frame
label_seccion_output = Label(frame, text='')  # label con texto en el frame 
label_seccion_output.grid(row=pos_y+9, column=1)       # se pone en el frame

label_fecha = Label(frame, text='Fecha de ingreso:')  # label con texto en el frame 
label_fecha.grid(row=pos_y+10, column=0)       # se pone en el frame
label_fecha_output = Label(frame, text='')  # label con texto en el frame 
label_fecha_output.grid(row=pos_y+10, column=1)       # se pone en el frame

label_cargo = Label(frame, text='Cargo:')  # label con texto en el frame 
label_cargo.grid(row=pos_y+11, column=0)       # se pone en el frame
label_cargo_output = Label(frame, text='')  # label con texto en el frame 
label_cargo_output.grid(row=pos_y+11, column=1)       # se pone en el frame

lista_output = [label_id_output,
                label_nombre1_output,
                label_nombre2_output,
                label_nombre3_output,
                label_apellidoP_output,
                label_apellidoM_output,
                label_vigencia_output,
                label_gerencia_output,
                label_departamento_output,
                label_seccion_output,
                label_fecha_output,
                label_cargo_output
            ]

root.mainloop()         # loop