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

try:                                # dentro de un try por si falla la conexión
    conn = psycopg2.connect(        # se conecta con la base de datos
        host = host_v, port = port_v, database = database_v, user = user_v, password = password_v
    )
    cur = conn.cursor()             # se crea cursor para ir modificando la base

except psycopg2.OperationalError:   # si es que no se conecta a la base
    print('Ocurrió un error al conectarse con la base de datos.')

color_error = '#f00'
color_exito = '#61c80e'


root = Tk()             # se crea instancia de tkinter
root.title('Bodega')    # nombre de la ventana

# resolución de la pantalla
ancho_pantalla = 1280
alto_pantalla = 720

root.geometry(str(ancho_pantalla)+'x'+str(alto_pantalla))   # se ajusta la resolución de la ventana ("1280x720" originalmente)

tabs = ttk.Notebook(root)       # widget que tendrá las tabs
tabs.pack()                     # se ubica tabs en root

frame_empleados = Frame(tabs)   # frame para ver info de los empleados
frame_epp = Frame(tabs)         # frame para ver info de los epp
frame_stock = Frame(tabs)       # frame para ver info del stock
frame_bodegueros = Frame(tabs)  # frame para ver info de los bodegueros
frame_entregas = Frame(tabs)    # frame para ver info de las entregas

# se añaden los frames a sus tabs corresponidentes 
tabs.add(frame_empleados, text='Empleados')
tabs.add(frame_epp, text='EPP')
tabs.add(frame_stock, text='Stock')
tabs.add(frame_bodegueros, text='Bodegueros')
tabs.add(frame_entregas, text='Entregas')

# tabs empleado ////////////////////////////////////////

tabs_empleado = ttk.Notebook(frame_empleados)   # tabs de los empleados
tabs_empleado.pack()                            # se ubica en el frame de empleados

## frame para buscar empleado ////////////////////////////////////////

buscar_empleado = Frame(tabs_empleado)                           # se crea y se le da como padre las tabs de empleado 
tabs_empleado.add(buscar_empleado,text='Buscar')        # se ubica el frame en las tabs de empleado      

# _e_1 es por empleado tab 1


def selectID_e_1(id):       # muestra la info de un trabajador dando el id directamente 
    lista = ['']*12         # lista para los doce atributos
    res = ver_empleado_id(id,cur,conn)   # se ejecuta la consulta
    if(res == None):    # si no se encuetra
        id_sin_ultimo_digito = id[:len(id)-1]   # se revisa si se buscó con el digito verificador y sin guion
        res = ver_empleado_id(id_sin_ultimo_digito,cur,conn)   # se ejecuta la consulta    
    if(res == None):    # si no se encuentra
        id_sin_guion = id.split('-')        # se revisa si se buscó con guíon y digito verificador
        id_sin_guion = id_sin_guion[0]
        res = ver_empleado_id(id_sin_guion,cur,conn)   # se ejecuta la consulta    
    

    try:                    # con un try por si algo falla
        for i in range(0,12):           # se guardan los resultados en la lista
            lista[i] = res[i]
    except:                             # si es que falla
        for i in range(0,12):           # se llena con strings vacíos
            lista[i] = ''
    for i in range(0,12):               # escribe el resultado de la consulta en los labels 
        lista_output_e_1[i]['text'] = lista[i]
        if lista[i] == None:
            lista_output_e_1[i]['text'] = ''

def inputID_e_1():          # muestra la info de un trabajador dando su identificador (rut o pasaporte)
    id = entry_id_e_1.get() # se obtiene la id de la checkbox

    selectID_e_1(id)        # se llama a selectID_e_1

# para buscar por ID

label_texto_id_e_1 = Label(buscar_empleado, text='Buscar empleado por ID')
label_texto_id_e_1.grid(row=0, column=0)

label_id_input_e_1 = Label(buscar_empleado, text='ID:')               # label con texto en el frame 
label_id_input_e_1.grid(row=1, column=0)                                    # se pone en el frame

entry_id_e_1 = Entry(buscar_empleado)                                # caja para escribir el ID
entry_id_e_1.grid(row=1, column=1)                                          # se ubica la caja en el frame

boton_buscar_id_e_1 = Button(buscar_empleado, text='Buscar', command=inputID_e_1)         # botón para ejecutar la busqueda
boton_buscar_id_e_1.grid(row=1, column=2)                                   # se ubica el botón en el frame

# para filtar por otros parámetros

def filtrar_e_1():
    delete_e_1()                    # se borra la listbox para poner el contenido nuevo
    empleados =  ver_empleados(entry_nombre_e_1.get(),
                                entry_apellido_e_1.get(),options_vigencia_e_1.get(),
                                entry_gerencia_e_1.get(),entry_departamento_e_1.get(),
                                options_seccion_e_1.get(),entry_cargo_e_1.get(),
                                options_orden_e_1.get(),
                                cur,
                                conn)    # se guardan todos los empleados que cumplen los parámetros
    try:
        for empleado in empleados:             # se rellena la listbox con los empleados
            listbox_e_1.insert(END, empleado)  
    except:
        pass

label_filtrar_text_e_1 = Label(buscar_empleado, text='Filtrar empleados')       # label con texto en el frame
label_filtrar_text_e_1.grid(row=0,column=3)                                                     # se ubica en el frame

pos_y_e_1_filtar = 1

# Primer Nombre
label_nombre_input_e_1 = Label(buscar_empleado, text='Primer Nombre')       # label con texto en el frame
label_nombre_input_e_1.grid(row=pos_y_e_1_filtar, column=3)                                # se ubica en el frame

entry_nombre_e_1 = Entry(buscar_empleado)                            # caja para texto del nombre
entry_nombre_e_1.grid(row=pos_y_e_1_filtar, column=4)                                      # se ubica en el frame

# botón filtrar

boton_buscar_nombre_e_1 = Button(buscar_empleado, text='Filtrar', command=filtrar_e_1)     # botón para ejecutar la busqueda
boton_buscar_nombre_e_1.grid(row=pos_y_e_1_filtar, column=5)                               # se ubica el botón en el frame

# apellido paterno

label_apellido_input_e_1 = Label(buscar_empleado, text='Apellido Paterno')   # label con texto en el frame
label_apellido_input_e_1.grid(row=pos_y_e_1_filtar+1, column=3)                              # se ubica en el frame

entry_apellido_e_1 = Entry(buscar_empleado)                          # caja para texto del nombre
entry_apellido_e_1.grid(row=pos_y_e_1_filtar+1, column=4)                                    # se ubica en el frame

# vigencia

label_vigencia_input_e_1 = Label(buscar_empleado, text='Vigencia')
label_vigencia_input_e_1.grid(row=pos_y_e_1_filtar+2, column= 3)

options_vigencia_e_1 = StringVar()
options_vigencia_e_1.set('')
dropdown_vigencia_e_1 = OptionMenu(buscar_empleado, options_vigencia_e_1, '', 'CONTRATO VIGENTE', 'CONTRATO NO VIGENTE')
dropdown_vigencia_e_1.grid(row=pos_y_e_1_filtar+2, column=4)

# gerencia

label_gerencia_input_e_1 = Label(buscar_empleado, text='Gerencia')   # label con texto en el frame
label_gerencia_input_e_1.grid(row=pos_y_e_1_filtar+3, column=3)                              # se ubica en el frame

entry_gerencia_e_1 = Entry(buscar_empleado)                          # caja para texto del nombre
entry_gerencia_e_1.grid(row=pos_y_e_1_filtar+3, column=4)                                    # se ubica en el frame

# departamento

label_departamento_input_e_1 = Label(buscar_empleado, text='Departamento')   # label con texto en el frame
label_departamento_input_e_1.grid(row=pos_y_e_1_filtar+4, column=3)                              # se ubica en el frame

entry_departamento_e_1 = Entry(buscar_empleado)                          # caja para texto del nombre
entry_departamento_e_1.grid(row=pos_y_e_1_filtar+4, column=4)                                    # se ubica en el frame

# sección

label_seccion_input_e_1 = Label(buscar_empleado, text='Sección')
label_seccion_input_e_1.grid(row=pos_y_e_1_filtar+5, column= 3)

options_seccion_e_1 = StringVar()
options_seccion_e_1.set('')
dropdown_seccion_e_1 = OptionMenu(buscar_empleado, options_seccion_e_1 , '', 'PERSONAL DIRECTO', 'PERSONAL INDIRECTO', 'PERSONAL EXPATRIADOS')
dropdown_seccion_e_1.grid(row=pos_y_e_1_filtar+5, column=4)
# cargo

label_cargo_input_e_1 = Label(buscar_empleado, text='Cargo')   # label con texto en el frame
label_cargo_input_e_1.grid(row=pos_y_e_1_filtar+6, column=3)                              # se ubica en el frame

entry_cargo_e_1 = Entry(buscar_empleado)                          # caja para texto del nombre
entry_cargo_e_1.grid(row=pos_y_e_1_filtar+6, column=4)                                    # se ubica en el frame

# orden de filtro

label_orden_input_e_1 = Label(buscar_empleado, text='Orden de empleados')
label_orden_input_e_1.grid(row=pos_y_e_1_filtar+7, column= 3)

options_orden_e_1 = StringVar()
options_orden_e_1.set('ID descendiente')
dropdown_orden_e_1 = OptionMenu(buscar_empleado, options_orden_e_1, 'ID ascendiente', 'ID descendiente', 'Fecha de ingreso ascendiente', 'Fecha de ingreso descendiente')
dropdown_orden_e_1.grid(row=pos_y_e_1_filtar+7, column=4)

# lables con los resultados de la busqueda 

pos_y_e_1=3

label_id_e_1 = Label(buscar_empleado, text='ID:')                                     # label con texto en el frame 
label_id_e_1.grid(row=pos_y_e_1, column=0)                                      # se pone en el frame
label_id_output_e_1 = Label(buscar_empleado, text='')                                 # label con texto en el frame 
label_id_output_e_1.grid(row=pos_y_e_1, column=1)                               # se pone en el frame

label_nombre1_e_1 = Label(buscar_empleado, text='Primer Nombre:')                     # label con texto en el frame 
label_nombre1_e_1.grid(row=pos_y_e_1+1, column=0)                               # se pone en el frame
label_nombre1_output_e_1 = Label(buscar_empleado, text='')                            # label con texto en el frame 
label_nombre1_output_e_1.grid(row=pos_y_e_1+1, column=1)                        # se pone en el frame

label_nombre2_e_1 = Label(buscar_empleado, text='Segundo Nombre:')                    # label con texto en el frame 
label_nombre2_e_1.grid(row=pos_y_e_1+2, column=0)                               # se pone en el frame
label_nombre2_output_e_1 = Label(buscar_empleado, text='')                            # label con texto en el frame 
label_nombre2_output_e_1.grid(row=pos_y_e_1+2, column=1)                        # se pone en el frame

label_nombre3_e_1 = Label(buscar_empleado, text='Tercer Nombre:')                     # label con texto en el frame 
label_nombre3_e_1.grid(row=pos_y_e_1+3, column=0)                               # se pone en el frame
label_nombre3_output_e_1 = Label(buscar_empleado, text='')                            # label con texto en el frame 
label_nombre3_output_e_1.grid(row=pos_y_e_1+3, column=1)                        # se pone en el frame

label_apellidoP_e_1 = Label(buscar_empleado, text='Apellido Paterno:')                # label con texto en el frame 
label_apellidoP_e_1.grid(row=pos_y_e_1+4, column=0)                             # se pone en el frame
label_apellidoP_output_e_1 = Label(buscar_empleado, text='')                          # label con texto en el frame 
label_apellidoP_output_e_1.grid(row=pos_y_e_1+4, column=1)                      # se pone en el frame

label_apellidoM_e_1 = Label(buscar_empleado, text='Apellido Materno:')                # label con texto en el frame 
label_apellidoM_e_1.grid(row=pos_y_e_1+5, column=0)                             # se pone en el frame
label_apellidoM_output_e_1 = Label(buscar_empleado, text='')                          # label con texto en el frame 
label_apellidoM_output_e_1.grid(row=pos_y_e_1+5, column=1)                      # se pone en el frame

label_vigencia_e_1 = Label(buscar_empleado, text='Vigencia:')                         # label con texto en el frame 
label_vigencia_e_1.grid(row=pos_y_e_1+6, column=0)                              # se pone en el frame
label_vigencia_output_e_1 = Label(buscar_empleado, text='')                           # label con texto en el frame 
label_vigencia_output_e_1.grid(row=pos_y_e_1+6, column=1)                       # se pone en el frame

label_gerencia_e_1 = Label(buscar_empleado, text='Gerencia:')                         # label con texto en el frame 
label_gerencia_e_1.grid(row=pos_y_e_1+7, column=0)                              # se pone en el frame
label_gerencia_output_e_1 = Label(buscar_empleado, text='')                           # label con texto en el frame 
label_gerencia_output_e_1.grid(row=pos_y_e_1+7, column=1)                       # se pone en el frame

label_departamento_e_1 = Label(buscar_empleado, text='Departamento:')                 # label con texto en el frame 
label_departamento_e_1.grid(row=pos_y_e_1+8, column=0)                          # se pone en el frame
label_departamento_output_e_1 = Label(buscar_empleado, text='')                       # label con texto en el frame 
label_departamento_output_e_1.grid(row=pos_y_e_1+8, column=1)                   # se pone en el frame

label_seccion_e_1 = Label(buscar_empleado, text='Sección:')                           # label con texto en el frame 
label_seccion_e_1.grid(row=pos_y_e_1+9, column=0)                               # se pone en el frame
label_seccion_output_e_1 = Label(buscar_empleado, text='')                            # label con texto en el frame 
label_seccion_output_e_1.grid(row=pos_y_e_1+9, column=1)                        # se pone en el frame

label_fecha_e_1 = Label(buscar_empleado, text='Fecha de ingreso:')                    # label con texto en el frame 
label_fecha_e_1.grid(row=pos_y_e_1+10, column=0)                                # se pone en el frame
label_fecha_output_e_1 = Label(buscar_empleado, text='')                              # label con texto en el frame 
label_fecha_output_e_1.grid(row=pos_y_e_1+10, column=1)                         # se pone en el frame

label_cargo_e_1 = Label(buscar_empleado, text='Cargo:')                               # label con texto en el frame 
label_cargo_e_1.grid(row=pos_y_e_1+11, column=0)                                # se pone en el frame
label_cargo_output_e_1 = Label(buscar_empleado, text='')                              # label con texto en el frame 
label_cargo_output_e_1.grid(row=pos_y_e_1+11, column=1)                         # se pone en el frame

# lista con las labels de output con la información
lista_output_e_1 = [label_id_output_e_1,
                label_nombre1_output_e_1,
                label_nombre2_output_e_1,
                label_nombre3_output_e_1,
                label_apellidoP_output_e_1,
                label_apellidoM_output_e_1,
                label_vigencia_output_e_1,
                label_gerencia_output_e_1,
                label_departamento_output_e_1,
                label_seccion_output_e_1,
                label_fecha_output_e_1,
                label_cargo_output_e_1
            ]

empleados_e_1 = ver_todos_empleados_func(cur,conn)    # se llama a la función para ver a todos los empleados y se guardan las tuplas en la listbox 

listbox_e_1 = Listbox(buscar_empleado, width=180, height=10) # se crea una listbox que muestra los empleados
listbox_e_1.grid(row=pos_y_e_1+12, columnspan=14, sticky= W+E)      # se posiciona la listbox

for empleado_func in empleados_e_1:             # se rellena la listbox con los empleados
    listbox_e_1.insert(END, empleado_func)      


def select_e_1():                           # función para seleccionar empleado directamente de las litbox 
    atributos = listbox_e_1.get(ANCHOR) # se obtiene el empleado subrayado en la listbox
    entry_id_e_1.delete(0,'end')        # se borra el texto en el campo
    id = atributos[0]
    entry_id_e_1.insert(0,id)           # y se inserta el texto
    selectID_e_1(id)          # se le da el rut (atributo 0) para que se muestre en pantalla

boton_select_e_1 = Button(buscar_empleado, text='Seleccionar empleado', command=select_e_1)   # botón para seleccionar empleado subrayado    
boton_select_e_1.grid(row=pos_y_e_1+13, column=0)           # se posiciona el botón 

def delete_e_1():                   # borra todo el contenido de la listbox
    listbox_e_1.delete(0,END)

## frame para añadir empleado manualmente ////////////////////////////////////////

annadir_empleado = Frame(tabs_empleado)                     # se crea y se le da como padre las tabs de empleado 
tabs_empleado.add(annadir_empleado,text='Añadir')     # se ubica el frame en las tabs de empleado   

label_info_e_2 = Label(annadir_empleado, text='Añadir empleado, los campos con * son obligatorios')
label_info_e_2.grid(row=0, column=0)

pos_y_e_2 = 1 

label_id_e_2 = Label(annadir_empleado, text='ID*')                                     # label con texto en el frame 
label_id_e_2.grid(row=pos_y_e_2, column=0)                                      # se pone en el frame
entry_id_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_id_e_2.grid(row=pos_y_e_2, column=1)                                      # se ubica en el frame

label_nombre1_e_2 = Label(annadir_empleado, text='Primer Nombre*')                                     # label con texto en el frame 
label_nombre1_e_2.grid(row=pos_y_e_2+1, column=0)                                      # se pone en el frame
entry_nombre1_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_nombre1_e_2.grid(row=pos_y_e_2+1, column=1)                                      # se ubica en el frame

label_nombre2_e_2 = Label(annadir_empleado, text='Segundo Nombre')                                     # label con texto en el frame 
label_nombre2_e_2.grid(row=pos_y_e_2+2, column=0)                                      # se pone en el frame
entry_nombre2_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_nombre2_e_2.grid(row=pos_y_e_2+2, column=1)                                      # se ubica en el frame

label_nombre3_e_2 = Label(annadir_empleado, text='Tercer Nombre')                                     # label con texto en el frame 
label_nombre3_e_2.grid(row=pos_y_e_2+3, column=0)                                      # se pone en el frame
entry_nombre3_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_nombre3_e_2.grid(row=pos_y_e_2+3, column=1)                                      # se ubica en el frame

label_apellidoP_e_2 = Label(annadir_empleado, text='Apellido Paterno*')                                     # label con texto en el frame 
label_apellidoP_e_2.grid(row=pos_y_e_2+4, column=0)                                      # se pone en el frame
entry_apellidoP_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_apellidoP_e_2.grid(row=pos_y_e_2+4, column=1)                                      # se ubica en el frame

label_apellidoM_e_2 = Label(annadir_empleado, text='Apellido Materno')                                     # label con texto en el frame 
label_apellidoM_e_2.grid(row=pos_y_e_2+5, column=0)                                      # se pone en el frame
entry_apellidoM_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_apellidoM_e_2.grid(row=pos_y_e_2+5, column=1)                                      # se ubica en el frame

label_vigencia_e_2 = Label(annadir_empleado, text='Vigencia*')                                     # label con texto en el frame 
label_vigencia_e_2.grid(row=pos_y_e_2+6, column=0)                                      # se pone en el frame

options_vigencia_e_2 = StringVar()
dropdown_vigencia_e_2 = OptionMenu(annadir_empleado, options_vigencia_e_2, 'CONTRATO VIGENTE', 'CONTRATO NO VIGENTE')
dropdown_vigencia_e_2.grid(row=pos_y_e_2+6, column=1)

label_gerencia_e_2 = Label(annadir_empleado, text='Gerencia*')                                     # label con texto en el frame 
label_gerencia_e_2.grid(row=pos_y_e_2+7, column=0)                                      # se pone en el frame
entry_gerencia_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_gerencia_e_2.grid(row=pos_y_e_2+7, column=1)                                      # se ubica en el frame

label_departamento_e_2 = Label(annadir_empleado, text='Departamento*')                                     # label con texto en el frame 
label_departamento_e_2.grid(row=pos_y_e_2+8, column=0)                                      # se pone en el frame
entry_departamento_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_departamento_e_2.grid(row=pos_y_e_2+8, column=1)                                      # se ubica en el frame

label_seccion_e_2 = Label(annadir_empleado, text='Sección*')                                     # label con texto en el frame 
label_seccion_e_2.grid(row=pos_y_e_2+9, column=0)                                      # se pone en el frame

options_seccion_e_2 = StringVar()
dropdown_seccion_e_2 = OptionMenu(annadir_empleado, options_seccion_e_2, 'PERSONAL DIRECTO', 'PERSONAL INDIRECTO', 'PERSONAL EXPATRIADOS')
dropdown_seccion_e_2.grid(row=pos_y_e_2+9, column=1)

label_fecha_e_2 = Label(annadir_empleado, text='Fecha de ingreso*')                                     # label con texto en el frame 
label_fecha_e_2.grid(row=pos_y_e_2+10, column=0)                                      # se pone en el frame
entry_fecha_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_fecha_e_2.grid(row=pos_y_e_2+10, column=1)                                      # se ubica en el frame

label_cargo_e_2 = Label(annadir_empleado, text='Cargo*')                                     # label con texto en el frame 
label_cargo_e_2.grid(row=pos_y_e_2+11, column=0)                                      # se pone en el frame
entry_cargo_e_2 = Entry(annadir_empleado)                            # caja para texto del nombre
entry_cargo_e_2.grid(row=pos_y_e_2+11, column=1)                                      # se ubica en el frame


def annadir_empleado_e_2():
    res = annadir_empleado_func(entry_id_e_2.get(),
                            entry_nombre1_e_2.get(),
                            entry_nombre2_e_2.get(),
                            entry_nombre3_e_2.get(),
                            entry_apellidoP_e_2.get(),
                            entry_apellidoM_e_2.get(),
                            options_vigencia_e_2.get(),
                            entry_gerencia_e_2.get(),
                            entry_departamento_e_2.get(),
                            options_seccion_e_2.get(),
                            entry_fecha_e_2.get(),
                            entry_cargo_e_2.get(),
                            cur,
                            conn)
    if(res == 1):
        label_annadir_output_e_2['text'] = 'Empleado añadido'
        label_annadir_output_e_2['fg'] = color_exito
    elif(res == -1):
        label_annadir_output_e_2['text'] = 'No se puedo añadir al empleado, por favor revisar que el formato esté correcto'
        label_annadir_output_e_2['fg'] = color_error

    else:
        label_annadir_output_e_2['text'] = 'Error inseperado'
        label_annadir_output_e_2['fg'] = color_error

 
 


boton_annadir_e_2 = Button(annadir_empleado, text='Añadir empleado', command=annadir_empleado_e_2)   # botón para añadir empleado 
boton_annadir_e_2.grid(row=pos_y_e_2+12, column=1)           # se posiciona el botón 

label_annadir_output_e_2 = Label(annadir_empleado, text='')
label_annadir_output_e_2.grid(row=pos_y_e_2+12, column=2)

## frame para editar empleados ////////////////////////////////////////

editar_empleado = Frame(tabs_empleado)
tabs_empleado.add(editar_empleado, text='Editar/Eliminar')

# _e_3 por empleado tab 3

def selectID_e_3(id):       # muestra la info de un trabajador dando el id directamente 
    lista = ['']*12         # lista para los doce atributos
    res = ver_empleado_id(id,cur,conn)   # se ejecuta la consulta
    try:
        for i in range(0,12):           # se guardan los resultados en la lista
            lista[i] = res[i]
    except:                             # si es que falla
        for i in range(0,12):           # se llena con strings vacíos
            lista[i] = ''
    for i in range(0,11):               # escribe el resultado de la consulta en los labels 
        lista_output_e_3[i]['text'] = lista[i+1]
        if lista[i+1] == None:
            lista_output_e_3[i]['text'] = ''

def inputID_e_3():          # muestra la info de un trabajador dando su identificador (rut o pasaporte)
    id = entry_id_e_3.get() # se obtiene la id de la checkbox
    selectID_e_3(id)        # se llama a selectID_e_1

def actualizar_empleado_e_3():
    res = modificar_empleado_func(entry_id_e_3.get(),
                            entry_nombre1_e_3.get(),
                            entry_nombre2_e_3.get(),
                            entry_nombre3_e_3.get(),
                            entry_apellidoP_e_3.get(),
                            entry_apellidoM_e_3.get(),
                            options_vigencia_e_3.get(),
                            entry_gerencia_e_3.get(),
                            entry_departamento_e_3.get(),
                            options_seccion_e_3.get(),
                            entry_fecha_e_3.get(),
                            entry_cargo_e_3.get(),
                            cur,
                            conn)
    id = entry_id_e_3.get()                        
    if(res == 1):
        label_actualizado_e_3["text"] = 'Empleado '+id+' actualizado correctamente'
        label_actualizado_e_3['fg'] = color_exito
    elif(res == -1):
        label_actualizado_e_3["text"] = 'No se pudo actualizar el empleado '+id+' , asegurese que esté todo en el formato correcto o que esté en la base de datos'
        label_actualizado_e_3['fg'] = color_error
    else:
        label_actualizado_e_3["text"] = 'Error inseperado'
        label_actualizado_e_3['fg'] = color_error

    inputID_e_3()   # para actualizar inmeditamente el empleado en la pantalla

label_id_input_e_3 = Label(editar_empleado, text='ID:')               # label con texto en el frame 
label_id_input_e_3.grid(row=0, column=0)                                    # se pone en el frame

boton_buscar_id_e_3 = Button(editar_empleado, text='Buscar', command=inputID_e_3)         # botón para ejecutar la busqueda
boton_buscar_id_e_3.grid(row=0, column=2)                                   # se ubica el botón en el frame

pos_y_e_3=0

label_nombre1_e_3 = Label(editar_empleado, text='Primer Nombre:')                     # label con texto en el frame 
label_nombre1_e_3.grid(row=pos_y_e_3+1, column=0)                               # se pone en el frame
label_nombre1_output_e_3 = Label(editar_empleado, text='')                            # label con texto en el frame 
label_nombre1_output_e_3.grid(row=pos_y_e_3+1, column=1)                        # se pone en el frame

label_nombre2_e_3 = Label(editar_empleado, text='Segundo Nombre:')                    # label con texto en el frame 
label_nombre2_e_3.grid(row=pos_y_e_3+2, column=0)                               # se pone en el frame
label_nombre2_output_e_3 = Label(editar_empleado, text='')                            # label con texto en el frame 
label_nombre2_output_e_3.grid(row=pos_y_e_3+2, column=1)                        # se pone en el frame

label_nombre3_e_3 = Label(editar_empleado, text='Tercer Nombre:')                     # label con texto en el frame 
label_nombre3_e_3.grid(row=pos_y_e_3+3, column=0)                               # se pone en el frame
label_nombre3_output_e_3 = Label(editar_empleado, text='')                            # label con texto en el frame 
label_nombre3_output_e_3.grid(row=pos_y_e_3+3, column=1)                        # se pone en el frame

label_apellidoP_e_3 = Label(editar_empleado, text='Apellido Paterno:')                # label con texto en el frame 
label_apellidoP_e_3.grid(row=pos_y_e_3+4, column=0)                             # se pone en el frame
label_apellidoP_output_e_3 = Label(editar_empleado, text='')                          # label con texto en el frame 
label_apellidoP_output_e_3.grid(row=pos_y_e_3+4, column=1)                      # se pone en el frame

label_apellidoM_e_3 = Label(editar_empleado, text='Apellido Materno:')                # label con texto en el frame 
label_apellidoM_e_3.grid(row=pos_y_e_3+5, column=0)                             # se pone en el frame
label_apellidoM_output_e_3 = Label(editar_empleado, text='')                          # label con texto en el frame 
label_apellidoM_output_e_3.grid(row=pos_y_e_3+5, column=1)                      # se pone en el frame

label_vigencia_e_3 = Label(editar_empleado, text='Vigencia:')                         # label con texto en el frame 
label_vigencia_e_3.grid(row=pos_y_e_3+6, column=0)                              # se pone en el frame
label_vigencia_output_e_3 = Label(editar_empleado, text='')                           # label con texto en el frame 
label_vigencia_output_e_3.grid(row=pos_y_e_3+6, column=1)                       # se pone en el frame

label_gerencia_e_3 = Label(editar_empleado, text='Gerencia:')                         # label con texto en el frame 
label_gerencia_e_3.grid(row=pos_y_e_3+7, column=0)                              # se pone en el frame
label_gerencia_output_e_3 = Label(editar_empleado, text='')                           # label con texto en el frame 
label_gerencia_output_e_3.grid(row=pos_y_e_3+7, column=1)                       # se pone en el frame

label_departamento_e_3 = Label(editar_empleado, text='Departamento:')                 # label con texto en el frame 
label_departamento_e_3.grid(row=pos_y_e_3+8, column=0)                          # se pone en el frame
label_departamento_output_e_3 = Label(editar_empleado, text='')                       # label con texto en el frame 
label_departamento_output_e_3.grid(row=pos_y_e_3+8, column=1)                   # se pone en el frame

label_seccion_e_3 = Label(editar_empleado, text='Sección:')                           # label con texto en el frame 
label_seccion_e_3.grid(row=pos_y_e_3+9, column=0)                               # se pone en el frame
label_seccion_output_e_3 = Label(editar_empleado, text='')                            # label con texto en el frame 
label_seccion_output_e_3.grid(row=pos_y_e_3+9, column=1)                        # se pone en el frame

label_fecha_e_3 = Label(editar_empleado, text='Fecha de ingreso:')                    # label con texto en el frame 
label_fecha_e_3.grid(row=pos_y_e_3+10, column=0)                                # se pone en el frame
label_fecha_output_e_3 = Label(editar_empleado, text='')                              # label con texto en el frame 
label_fecha_output_e_3.grid(row=pos_y_e_3+10, column=1)                         # se pone en el frame

label_cargo_e_3 = Label(editar_empleado, text='Cargo:')                               # label con texto en el frame 
label_cargo_e_3.grid(row=pos_y_e_3+11, column=0)                                # se pone en el frame
label_cargo_output_e_3 = Label(editar_empleado, text='')                              # label con texto en el frame 
label_cargo_output_e_3.grid(row=pos_y_e_3+11, column=1)                         # se pone en el frame

# lista con los outputs
lista_output_e_3 = [
                label_nombre1_output_e_3,
                label_nombre2_output_e_3,
                label_nombre3_output_e_3,
                label_apellidoP_output_e_3,
                label_apellidoM_output_e_3,
                label_vigencia_output_e_3,
                label_gerencia_output_e_3,
                label_departamento_output_e_3,
                label_seccion_output_e_3,
                label_fecha_output_e_3,
                label_cargo_output_e_3
            ]

# entries para modificar

entry_id_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_id_e_3.grid(row=pos_y_e_3, column=1)                                      # se ubica en el frame

entry_nombre1_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_nombre1_e_3.grid(row=pos_y_e_3+1, column=2)                                      # se ubica en el frame

entry_nombre2_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_nombre2_e_3.grid(row=pos_y_e_3+2, column=2)                                      # se ubica en el frame

entry_nombre3_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_nombre3_e_3.grid(row=pos_y_e_3+3, column=2)                                      # se ubica en el frame

entry_apellidoP_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_apellidoP_e_3.grid(row=pos_y_e_3+4, column=2)                                      # se ubica en el frame

entry_apellidoM_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_apellidoM_e_3.grid(row=pos_y_e_3+5, column=2)                                      # se ubica en el frame

options_vigencia_e_3 = StringVar()
options_vigencia_e_3.set('')
dropdown_vigencia_e_3 = OptionMenu(editar_empleado, options_vigencia_e_3, '' ,'CONTRATO VIGENTE', 'CONTRATO NO VIGENTE')
dropdown_vigencia_e_3.grid(row=pos_y_e_3+6, column=2)

entry_gerencia_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_gerencia_e_3.grid(row=pos_y_e_3+7, column=2)                                      # se ubica en el frame

entry_departamento_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_departamento_e_3.grid(row=pos_y_e_3+8, column=2)                                      # se ubica en el frame

options_seccion_e_3 = StringVar()
options_seccion_e_3.set('')
dropdown_seccion_e_3 = OptionMenu(editar_empleado, options_seccion_e_3, '' ,'PERSONAL DIRECTO', 'PERSONAL INDIRECTO', 'PERSONAL EXPATRIADOS')
dropdown_seccion_e_3.grid(row=pos_y_e_3+9, column=2)

entry_fecha_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_fecha_e_3.grid(row=pos_y_e_3+10, column=2)                                      # se ubica en el frame

entry_cargo_e_3 = Entry(editar_empleado)                            # caja para texto del nombre
entry_cargo_e_3.grid(row=pos_y_e_3+11, column=2)                                      # se ubica en el frame

boton_actualizar = Button(editar_empleado, text='Actualizar',command=actualizar_empleado_e_3)
boton_actualizar.grid(row=pos_y_e_3+12, column=2)

label_actualizado_e_3 = Label(editar_empleado, text=' ')                               # label con texto en el frame 
label_actualizado_e_3.grid(row=pos_y_e_3+12, column=3)                                # se pone en el frame


def confirmar_eliminar_e_3(eleccion,id):
    popup_eliminar_empleado_e_3.destroy()           # se elimina la ventana
    if(eleccion):                                   # si se dijo que si 
        eliminar_empleado_func(id,cur,conn)         # se elimina el empleado
        label_eliminado_e3['text'] = 'Se eliminó el empleado de id '+id+' de la base de datos'
        label_eliminado_e3['fg'] = color_exito

    elif(not eleccion):                             # si se dijo que no, no se elimina
        label_eliminado_e3['text'] = 'El empleado de id '+id+' no se eliminó de la base de datos'
        label_eliminado_e3['fg'] = color_exito

    else:                                           # en caso de un error imprevisto 
        label_eliminado_e3['text'] = 'Error insesperado'
        label_eliminado_e3['fg'] = color_error


def eliminar_empleado_e_3():    # función al apretar el valor eliminar
    id = entry_id_e_3.get()     # se obtiene el id del campo
    id = id.strip()

    res = empleado_en_db_id(id,cur,conn)    # se revisa si está en la base de datos
    if res == 1:                            # si es qu está
        global popup_eliminar_empleado_e_3  # global para poder ser llamada desde la funcíon de arriba
        popup_eliminar_empleado_e_3 = Toplevel(root)    # se crea la ventana
        popup_eliminar_empleado_e_3.title('Confimración de eliminar empleado')  #   titulo y dimensiones
        popup_eliminar_empleado_e_3.geometry('350x100')

        pop_label_e_3 = Label(popup_eliminar_empleado_e_3, text='¿Desea eliminar el empleado ' + id +' de las base de datos?')  # label para el texto
        pop_label_e_3.pack(pady=10)

        pop_frame_e_3 = Frame(popup_eliminar_empleado_e_3)  # frame para los botones
        pop_frame_e_3.pack(pady =5)

        boton_si_e_3 = Button(pop_frame_e_3, text='Sí', fg=color_error, command=lambda: confirmar_eliminar_e_3(True,id)) #   boton para confirmar la eliminación
        boton_si_e_3.grid(row=0,column=0,padx=10)

        boton_no_e_3 = Button(pop_frame_e_3, text='No', command=lambda: confirmar_eliminar_e_3(False,id))   # boton para desconfirmar la eliminación 
        boton_no_e_3.grid(row=0,column=1,padx=10)

        label_eliminado_e3['text'] = 'Confirme en la ventana que apareció'  # dice para que el usuario sepa que debe confirmar en la pantalla
        label_eliminado_e3['fg'] = color_exito
    elif res == 0:                                                  # si no lo encuentra
        label_eliminado_e3['text'] = 'No se econtró un empleado con la id '+id+' en la base de datos'
        label_eliminado_e3['fg'] = color_error
    elif res == -1:                                                 # está mal el formato 
        label_eliminado_e3['text'] = 'Asegurese de que el id esté en el formato correcto'
        label_eliminado_e3['fg'] = color_error
        
boton_eliminar_e_3 = Button(editar_empleado, text='Eliminar', fg=color_error, command=eliminar_empleado_e_3)        # botón para eliminar (en rojo para que de mas susto)
boton_eliminar_e_3.grid(row=pos_y_e_3+13, column=0)

label_eliminado_e3 = Label(editar_empleado, text='')    # dice el status de la eliminación
label_eliminado_e3.grid(row=pos_y_e_3+13, column=1)

# tabs epp ////////////////////////////////////////

tabs_epp = ttk.Notebook(frame_epp)          # tabs de los empleados
tabs_epp.pack()                             # se ubica en el frame de epp

## frame para buscar epp ////////////////////////////////////////

buscar_epp= Frame(tabs_epp)     # se crea y se le da como padre las tabs de epp
tabs_epp.add(buscar_epp, text='Buscar')

# _epp_1 de primer tab de EPP

def selectID_epp_1(id):     # muestra la info de un trabajador dando el id directamente 
    lista = ['']*7          # lista para los 7 atributos
    res = ver_epp_id(id,cur,conn)   # se ejecuta la consulta
    try:                    # en un try por si algo falla
        for i in range(0,7):    # se guardan los resultados en la lista
            lista[i] = res[i]
    except:                     # si es que falla
        for i in range(0,7):    # se llena con strings vacíos
            lista[i] = ''
    for i in range(0,7):        # escribe el resultado de la consulta en los labels
        lista_output_epp_1[i]['text'] = lista[i]
        if lista[i] == None:    # si es un none se llena con un string vacío (se debe llenar con algo o si no queda el texto que estaba antes)
            lista_output_epp_1[i]['text'] = ''


def inputID_epp_1():            # muestra la info de un trabajador dando su identificador (rut o pasaporte)
    id = entry_id_epp_1.get()   # se obtiene la id de la checkbox
    selectID_epp_1(id)          # se llama a selectID_e_1

# para buscar por código de producto

label_texto_id_epp_1 = Label(buscar_epp, text='Buscar EPP por código de producto')
label_texto_id_epp_1.grid(row=0, column=0)

label_id_input_epp_1 = Label(buscar_epp, text='Código de producto:')               # label con texto en el frame 
label_id_input_epp_1.grid(row=1, column=0)                                    # se pone en el frame

entry_id_epp_1 = Entry(buscar_epp)                                # caja para escribir el código 
entry_id_epp_1.grid(row=1, column=1)                                          # se ubica la caja en el frame

boton_buscar_id_epp_1 = Button(buscar_epp, text='Buscar', command=inputID_epp_1)         # botón para ejecutar la busqueda
boton_buscar_id_epp_1.grid(row=1, column=2)                                   # se ubica el botón en el frame

# para filtrar por otros parámetros

def filtrar_epp_1():
    delete_epp_1()          # se borra la listbox para poner el contenido nuevo
    epps = ver_epps(entry_c_construct_epp_1.get(),
                    entry_nombre_epp_1.get(),
                    entry_c_desig_epp_1.get(),
                    entry_talla_epp_1.get(),
                    entry_UM_epp_1.get(),
                    options_orden_epp_1.get(),
                    cur,
                    conn)
    try:
        for epp in epps:
            listbox_epp_1.insert(END, epp)
    except:
        pass

label_filtrar_text_epp_1 = Label(buscar_epp, text='Filtrar EPP')       # label con texto en el frame
label_filtrar_text_epp_1.grid(row=0,column=3)                                                     # se ubica en el frame

pos_y_epp_1_filtar = 1

# Código trabajador
label_c_construct_input_epp_1 = Label(buscar_epp, text='Codigo de constructor')       # label con texto en el frame
label_c_construct_input_epp_1.grid(row=pos_y_epp_1_filtar, column=3)                                # se ubica en el frame

entry_c_construct_epp_1 = Entry(buscar_epp)                            # caja para texto del nombre
entry_c_construct_epp_1.grid(row=pos_y_epp_1_filtar, column=4)   

# botón filtrar

boton_filtrar_epp_1 = Button(buscar_epp, text='Filtrar', command=filtrar_epp_1)     # botón para ejecutar la busqueda
boton_filtrar_epp_1.grid(row=pos_y_epp_1_filtar, column=5)                               # se ubica el botón en el frame

# Nombre
label_nombre_input_epp_1 = Label(buscar_epp, text='Nombre de producto')       # label con texto en el frame
label_nombre_input_epp_1.grid(row=pos_y_epp_1_filtar+1, column=3)                                # se ubica en el frame

entry_nombre_epp_1 = Entry(buscar_epp)                            # caja para texto del código constructor
entry_nombre_epp_1.grid(row=pos_y_epp_1_filtar+1, column=4)    

# Constructor designado
label_c_desig_input_epp_1 = Label(buscar_epp, text='Constructor designado')       # label con texto en el frame
label_c_desig_input_epp_1.grid(row=pos_y_epp_1_filtar+2, column=3)                                # se ubica en el frame

entry_c_desig_epp_1 = Entry(buscar_epp)                            # caja para texto del constructor designado
entry_c_desig_epp_1.grid(row=pos_y_epp_1_filtar+2, column=4)    

# Talla 
label_talla_input_epp_1 = Label(buscar_epp, text='Talla')       # label con texto en el frame
label_talla_input_epp_1.grid(row=pos_y_epp_1_filtar+3, column=3)                                # se ubica en el frame

entry_talla_epp_1 = Entry(buscar_epp)                            # caja para texto de la talla
entry_talla_epp_1.grid(row=pos_y_epp_1_filtar+3, column=4)    

# Unidad de medida 
label_UM_input_epp_1 = Label(buscar_epp, text='Unidad de medida')       # label con texto en el frame
label_UM_input_epp_1.grid(row=pos_y_epp_1_filtar+4, column=3)                                # se ubica en el frame

entry_UM_epp_1 = Entry(buscar_epp)                            # caja para texto de la UM
entry_UM_epp_1.grid(row=pos_y_epp_1_filtar+4, column=4)    

# orden de filtro

label_orden_input_epp_1 = Label(buscar_epp, text='Orden de EPP')
label_orden_input_epp_1.grid(row=pos_y_epp_1_filtar+5, column= 3)

options_orden_epp_1 = StringVar()
options_orden_epp_1.set('Código de producto descendiente')
dropdown_orden_epp_1 = OptionMenu(buscar_epp, options_orden_epp_1, 'Código de producto ascendiente', 'Código de producto descendiente', 'Precio ascendiente', 'Precio descendiente')
dropdown_orden_epp_1.grid(row=pos_y_epp_1_filtar+5, column=4)

# labels con los resultados de la busqueda
 
pos_y_e_1=3

label_id_epp_1 = Label(buscar_epp, text='Código de producto:')                                     # label con texto en el frame 
label_id_epp_1.grid(row=pos_y_e_1, column=0)                                      # se pone en el frame
label_id_output_epp_1 = Label(buscar_epp, text='')                                 # label con texto en el frame 
label_id_output_epp_1.grid(row=pos_y_e_1, column=1)                               # se pone en el frame

label_c_c_epp_1 = Label(buscar_epp, text='Código de constructor:')                                     # label con texto en el frame 
label_c_c_epp_1.grid(row=pos_y_e_1+1, column=0)                                      # se pone en el frame
label_c_c_output_epp_1 = Label(buscar_epp, text='')                                 # label con texto en el frame 
label_c_c_output_epp_1.grid(row=pos_y_e_1+1, column=1)                               # se pone en el frame

label_nombre_epp_1 = Label(buscar_epp, text='Nombre:')                                     # label con texto en el frame 
label_nombre_epp_1.grid(row=pos_y_e_1+2, column=0)                                      # se pone en el frame
label_nombre_output_epp_1 = Label(buscar_epp, text='')                                 # label con texto en el frame 
label_nombre_output_epp_1.grid(row=pos_y_e_1+2, column=1)    

label_constructor_designado_epp_1 = Label(buscar_epp, text='Constructor designado:')                                     # label con texto en el frame 
label_constructor_designado_epp_1.grid(row=pos_y_e_1+3, column=0)                                      # se pone en el frame
label_constructor_designado_output_epp_1 = Label(buscar_epp, text='')                                 # label con texto en el frame 
label_constructor_designado_output_epp_1.grid(row=pos_y_e_1+3, column=1) 

label_talla_epp_1 = Label(buscar_epp, text='Talla:')                                     # label con texto en el frame 
label_talla_epp_1.grid(row=pos_y_e_1+4, column=0)                                      # se pone en el frame
label_talla_output_epp_1 = Label(buscar_epp, text='')                                 # label con texto en el frame 
label_talla_output_epp_1.grid(row=pos_y_e_1+4, column=1) 

label_UM_epp_1 = Label(buscar_epp, text='Unidad de medición:')                                     # label con texto en el frame 
label_UM_epp_1.grid(row=pos_y_e_1+5, column=0)                                      # se pone en el frame
label_UM_output_epp_1 = Label(buscar_epp, text='')                                 # label con texto en el frame 
label_UM_output_epp_1.grid(row=pos_y_e_1+5, column=1) 

label_precio_epp_1 = Label(buscar_epp, text='Precio:')                                     # label con texto en el frame 
label_precio_epp_1.grid(row=pos_y_e_1+6, column=0)                                      # se pone en el frame
label_precio_output_epp_1 = Label(buscar_epp, text='')                                 # label con texto en el frame 
label_precio_output_epp_1.grid(row=pos_y_e_1+6, column=1) 

# lista con las labels de output con la información
lista_output_epp_1 = [
                label_c_c_output_epp_1,
                label_id_output_epp_1,
                label_nombre_output_epp_1,
                label_constructor_designado_output_epp_1,
                label_talla_output_epp_1,
                label_UM_output_epp_1,
                label_precio_output_epp_1
            ]

epps_epp_1 = ver_todos_los_epp_func(cur,conn)                    # se consiguen todos loe epp

listbox_epp_1 = Listbox(buscar_epp, width=180, height=10) # se crea una listbox que muestra los epps
listbox_epp_1.grid(row=pos_y_e_1+7, columnspan=14, sticky= W+E)      # se posiciona la listbox

for epp_func in epps_epp_1:             # se rellena la listbox con los epps
    listbox_epp_1.insert(END, epp_func)      

def select_epp_1():                                     # función para seleccionar empleado directamente de las litbox 
    atributos = listbox_epp_1.get(ANCHOR)               # se obtiene el empleado subrayado en la listbox
    entry_id_epp_1.delete(0,'end')                      # se borra lo que esté en la caja 
    id = atributos[1]                   
    entry_id_epp_1.insert(0,id)                         # se inserta el id clickeada
    selectID_epp_1(id)                        # se le da el rut (atributo 0) para que se muestre en pantalla

boton_select_epp_1 = Button(buscar_epp, text='Seleccionar EPP', command=select_epp_1)   # botón para seleccionar empleado subrayado  
boton_select_epp_1.grid(row=pos_y_e_1+8, column=0)              # se posiciona el botón    

def delete_epp_1():                         # borra todo el contenido de la listbox
    listbox_epp_1.delete(0,END)

## frame para annadir epp manualmente ////////////////////////////////////////

annadir_epp = Frame(tabs_epp)     # se crea y se le da como padre las tabs de epp
tabs_epp.add(annadir_epp, text='Añadir')

label_info_epp_2 = Label(annadir_epp, text='Añadir EPP, los campos con * son obligatorios')
label_info_epp_2.grid(row=0, column=0)

pos_y_epp_2 = 1 

label_id_epp_2 = Label(annadir_epp, text='Código de producto*')                                     # label con texto en el frame 
label_id_epp_2.grid(row=pos_y_epp_2, column=0)                                      # se pone en el frame
entry_id_epp_2 = Entry(annadir_epp)                            # caja para texto del nombre
entry_id_epp_2.grid(row=pos_y_epp_2, column=1)                                      # se ubica en el frame

label_c_c_epp_2 = Label(annadir_epp, text='Código de constructor*')                                     # label con texto en el frame 
label_c_c_epp_2.grid(row=pos_y_epp_2+1, column=0)                                      # se pone en el frame
entry_c_c_epp_2 = Entry(annadir_epp)                            # caja para texto del nombre
entry_c_c_epp_2.grid(row=pos_y_epp_2+1, column=1)                                      # se ubica en el frame

label_nombre_epp_2 = Label(annadir_epp, text='Nombre del prodcuto*')                                     # label con texto en el frame 
label_nombre_epp_2.grid(row=pos_y_epp_2+2, column=0)                                      # se pone en el frame
entry_nombre_epp_2 = Entry(annadir_epp)                            # caja para texto del nombre
entry_nombre_epp_2.grid(row=pos_y_epp_2+2, column=1)                                      # se ubica en el frame

label_constructor_designado_epp_2 = Label(annadir_epp, text='Constructor designado*')                                     # label con texto en el frame 
label_constructor_designado_epp_2.grid(row=pos_y_epp_2+3, column=0)                                      # se pone en el frame
entry_constructor_designado_epp_2 = Entry(annadir_epp)                            # caja para texto del nombre
entry_constructor_designado_epp_2.grid(row=pos_y_epp_2+3, column=1)                                      # se ubica en el frame

label_talla_epp_2 = Label(annadir_epp, text='Talla')                                     # label con texto en el frame 
label_talla_epp_2.grid(row=pos_y_epp_2+4, column=0)                                      # se pone en el frame
entry_talla_epp_2 = Entry(annadir_epp)                            # caja para texto del nombre
entry_talla_epp_2.grid(row=pos_y_epp_2+4, column=1)                                      # se ubica en el frame

label_UM_epp_2 = Label(annadir_epp, text='Unidad de medición*')                                     # label con texto en el frame 
label_UM_epp_2.grid(row=pos_y_epp_2+5, column=0)                                      # se pone en el frame
entry_UM_epp_2 = Entry(annadir_epp)                            # caja para texto del nombre
entry_UM_epp_2.grid(row=pos_y_epp_2+5, column=1)                                      # se ubica en el frame

label_precio_epp_2 = Label(annadir_epp, text='Precio*')                                     # label con texto en el frame 
label_precio_epp_2.grid(row=pos_y_epp_2+6, column=0)                                      # se pone en el frame
entry_precio_epp_2 = Entry(annadir_epp)                            # caja para texto del nombre
entry_precio_epp_2.grid(row=pos_y_epp_2+6, column=1)                                      # se ubica en el frame

def annadir_epp_epp_2():
    res = annadir_epp_func(entry_id_epp_2.get(),
                            entry_c_c_epp_2.get(),
                            entry_nombre_epp_2.get(),
                            entry_constructor_designado_epp_2.get(),
                            entry_talla_epp_2.get(),
                            entry_UM_epp_2.get(),
                            entry_precio_epp_2.get(),
                            cur,
                            conn
                            )
    if(res == 1):
        label_annadir_output_epp_2['text'] = 'EPP añadido'
        label_annadir_output_epp_2['fg'] = color_exito
    elif(res == -1):
        label_annadir_output_epp_2['text'] = 'No se pudo añadir el EPP, por favor revise que el formate esté correcto'
        label_annadir_output_epp_2['fg'] = color_error
    else:
        label_annadir_output_epp_2['text'] = 'Error inseperado'
        label_annadir_output_epp_2['fg'] = color_error
    
boton_annadir_epp_2 = Button(annadir_epp, text='Añadir EPP', command=annadir_epp_epp_2) # botón para añadir EPP
boton_annadir_epp_2.grid(row=pos_y_epp_2+7, column=1)   # se posiciona el botón

label_annadir_output_epp_2 = Label(annadir_epp, text='')
label_annadir_output_epp_2.grid(row=pos_y_epp_2+7, column=2)

## frame para editar y eliminar epp de la base de datos ////////////////////////////////////////

editar_epp = Frame(tabs_epp)
tabs_epp.add(editar_epp, text='Editar/Eliminar')

# _epp_3 por empleado tab 3

def selectID_epp_3(id):     # muestra la info de un trabajador dando el id directamente 
    lista = ['']*7          # lista para los 7 atributos
    res = ver_epp_id(id,cur,conn)   # se ejecuta la consulta
    try:                    # en un try por si algo falla
        for i in range(0,7):    # se guardan los resultados en la lista
            lista[i] = res[i]
    
    except:                     # si es que falla
        for i in range(0,7):    # se llena con strings vacíos
            lista[i] = ''
    lista_output_epp_3[0]['text'] = lista[0]    # se pone el código constructor
    for i in range(1,6):        # escribe el resultado de la consulta en los labels
        lista_output_epp_3[i]['text'] = lista[i+1]
    if(lista[4]==None):             # si la talla es nula se deja como ''
        lista_output_epp_3[3]['text'] = ''


def inputID_epp_3():          # muestra la info de un epp dando su identificador (rut o pasaporte)
    id = entry_id_epp_3.get() # se obtiene la id de la checkbox
    selectID_epp_3(id)        # se llama a selectID_e_1  

def actualizar_epp_epp_3():
    res = modificar_epp_func(entry_id_epp_3.get(),
                                entry_c_c_epp_3.get(),
                                entry_nombre_epp_3.get(),
                                entry_constructor_designado_epp_3.get(),
                                entry_talla_epp_3.get(),
                                entry_UM_epp_3.get(),
                                entry_precio_epp_3.get(),
                                cur,
                                conn)    
    id = entry_id_epp_3.get()                        
    if(res == 1):
        label_actualizado_epp_3["text"] = 'EPP '+id+' actualizado correctamente'
        label_actualizado_epp_3['fg'] = color_exito
    elif(res == -1):
        label_actualizado_epp_3["text"] = 'No se pudo actualizar el EPP '+id+' , asegurese que esté todo en el formato correcto o que esté en la base de datos'
        label_actualizado_epp_3['fg'] = color_error
    else:
        label_actualizado_epp_3["text"] = 'Error inseperado'
        label_actualizado_epp_3['fg'] = color_error 

    inputID_epp_3()     # para actualizar inmeditamente el epp en la pantalla

label_id_input_epp_3 = Label(editar_epp, text='Código producto:')               # label con texto en el frame 
label_id_input_epp_3.grid(row=0, column=0)                                    # se pone en el frame

boton_buscar_id_epp_3 = Button(editar_epp, text='Buscar', command=inputID_epp_3)         # botón para ejecutar la busqueda
boton_buscar_id_epp_3.grid(row=0, column=2)                                   # se ubica el botón en el frame

pos_y_epp_3=0

label_c_c_epp_3 = Label(editar_epp, text='Código constructor:')                     # label con texto en el frame 
label_c_c_epp_3.grid(row=pos_y_epp_3+1, column=0)                               # se pone en el frame
label_c_c_output_epp_3 = Label(editar_epp, text='')                            # label con texto en el frame 
label_c_c_output_epp_3.grid(row=pos_y_epp_3+1, column=1)                        # se pone en el frame

label_nombre_epp_3 = Label(editar_epp, text='Nombre:')                     # label con texto en el frame 
label_nombre_epp_3.grid(row=pos_y_epp_3+2, column=0)                               # se pone en el frame
label_nombre_output_epp_3 = Label(editar_epp, text='')                            # label con texto en el frame 
label_nombre_output_epp_3.grid(row=pos_y_epp_3+2, column=1)                        # se pone en el frame

label_constructor_designado_epp_3 = Label(editar_epp, text='Constructor designado:')                     # label con texto en el frame 
label_constructor_designado_epp_3.grid(row=pos_y_epp_3+3, column=0)                               # se pone en el frame
label_constructor_designado_output_epp_3 = Label(editar_epp, text='')                            # label con texto en el frame 
label_constructor_designado_output_epp_3.grid(row=pos_y_epp_3+3, column=1)                        # se pone en el frame

label_talla_epp_3 = Label(editar_epp, text='Talla:')                     # label con texto en el frame 
label_talla_epp_3.grid(row=pos_y_epp_3+4, column=0)                               # se pone en el frame
label_talla_output_epp_3 = Label(editar_epp, text='')                            # label con texto en el frame 
label_talla_output_epp_3.grid(row=pos_y_epp_3+4, column=1)                        # se pone en el frame

label_UM_epp_3 = Label(editar_epp, text='Unidad de medición:')                     # label con texto en el frame 
label_UM_epp_3.grid(row=pos_y_epp_3+5, column=0)                               # se pone en el frame
label_UM_output_epp_3 = Label(editar_epp, text='')                            # label con texto en el frame 
label_UM_output_epp_3.grid(row=pos_y_epp_3+5, column=1)                        # se pone en el frame

label_precio_epp_3 = Label(editar_epp, text='Precio:')                     # label con texto en el frame 
label_precio_epp_3.grid(row=pos_y_epp_3+6, column=0)                               # se pone en el frame
label_precio_output_epp_3 = Label(editar_epp, text='')                            # label con texto en el frame 
label_precio_output_epp_3.grid(row=pos_y_epp_3+6, column=1)                        # se pone en el frame

# lista con los output

lista_output_epp_3 = [
                    label_c_c_output_epp_3,
                    label_nombre_output_epp_3,
                    label_constructor_designado_output_epp_3,
                    label_talla_output_epp_3,
                    label_UM_output_epp_3,
                    label_precio_output_epp_3   
                ]

# entries para modificar

entry_id_epp_3 = Entry(editar_epp)                            # caja para texto del nombre
entry_id_epp_3.grid(row=pos_y_epp_3, column=1)                                      # se ubica en el frame

entry_c_c_epp_3 = Entry(editar_epp)                            # caja para texto del nombre
entry_c_c_epp_3.grid(row=pos_y_epp_3+1, column=2)                                      # se ubica en el frame

entry_nombre_epp_3 = Entry(editar_epp)                            # caja para texto del nombre
entry_nombre_epp_3.grid(row=pos_y_epp_3+2, column=2)                                      # se ubica en el frame

entry_constructor_designado_epp_3 = Entry(editar_epp)                            # caja para texto del nombre
entry_constructor_designado_epp_3.grid(row=pos_y_epp_3+3, column=2)                                      # se ubica en el frame

entry_talla_epp_3 = Entry(editar_epp)                            # caja para texto del nombre
entry_talla_epp_3.grid(row=pos_y_epp_3+4, column=2)                                      # se ubica en el frame

entry_UM_epp_3 = Entry(editar_epp)                            # caja para texto del nombre
entry_UM_epp_3.grid(row=pos_y_epp_3+5, column=2)                                      # se ubica en el frame

entry_precio_epp_3 = Entry(editar_epp)                            # caja para texto del nombre
entry_precio_epp_3.grid(row=pos_y_epp_3+6, column=2)                                      # se ubica en el frame

boton_actualizar_epp_3 = Button(editar_epp, text='Actualizar',command=actualizar_epp_epp_3)
boton_actualizar_epp_3.grid(row=pos_y_epp_3+7, column=2)

label_actualizado_epp_3 = Label(editar_epp, text=' ')                               # label con texto en el frame 
label_actualizado_epp_3.grid(row=pos_y_epp_3+7, column=3)                                # se pone en el frame

def confirmar_eliminar_epp_3(eleccion,id):
    popup_eliminar_epp_epp_3.destroy()      # se elimina la ventana
    if(eleccion):                           # si se dijo que si     
        eliminar_epp_func(id,cur,conn)      # se elimina el empleado
        label_eliminado_epp3['text'] = 'Se eliminó el empleado de id '+id+' de la base de datos'
        label_eliminado_epp3['fg'] = color_exito

    elif(not eleccion):                     # si se dijo que no, no se elimina
        label_eliminado_epp3['text'] = 'El empleado de id '+id+' no se eliminó de la base de datos'
        label_eliminado_epp3['fg'] = color_exito
    
    else:                                   # en caso de un error imprevisto
        label_eliminado_epp3['text'] = 'Error insesperado'
        label_eliminado_epp3['fg'] = color_error


def eliminar_epp_epp_3():    # función al apretar el valor eliminar
    id = entry_id_epp_3.get()     # se obtiene el id del campo
    id = id.strip()

    res = epp_en_db_id(id,cur,conn)    # se revisa si está en la base de datos
    if res == 1:                            # si es qu está
        global popup_eliminar_epp_epp_3  # global para poder ser llamada desde la funcíon de arriba
        popup_eliminar_epp_epp_3 = Toplevel(root)    # se crea la ventana
        popup_eliminar_epp_epp_3.title('Confimración de eliminar empleado')  #   titulo y dimensiones
        popup_eliminar_epp_epp_3.geometry('350x100')

        pop_label_epp_3 = Label(popup_eliminar_epp_epp_3, text='¿Desea eliminar el EPP ' + id +' de las base de datos?')  # label para el texto
        pop_label_epp_3.pack(pady=10)

        pop_frame_epp_3 = Frame(popup_eliminar_epp_epp_3)  # frame para los botones
        pop_frame_epp_3.pack(pady =5)

        boton_si_epp_3 = Button(pop_frame_epp_3, text='Sí', fg=color_error, command=lambda: confirmar_eliminar_epp_3(True,id)) #   boton para confirmar la eliminación
        boton_si_epp_3.grid(row=0,column=0,padx=10)

        boton_no_epp_3 = Button(pop_frame_epp_3, text='No', command=lambda: confirmar_eliminar_epp_3(False,id))   # boton para desconfirmar la eliminación 
        boton_no_epp_3.grid(row=0,column=1,padx=10)

        label_eliminado_epp3['text'] = 'Confirme en la ventana que apareció'  # dice para que el usuario sepa que debe confirmar en la pantalla
        label_eliminado_epp3['fg'] = color_exito
    elif res == 0:                                                  # si no lo encuentra
        label_eliminado_epp3['text'] = 'No se econtró un EPP con la id '+id+' en la base de datos'
        label_eliminado_epp3['fg'] = color_error
    elif res == -1:                                                 # está mal el formato 
        label_eliminado_epp3['text'] = 'Asegurese de que el id esté en el formato correcto'
        label_eliminado_epp3['fg'] = color_error

boton_eliminar_epp_3 = Button(editar_epp, text='Eliminar', fg=color_error, command=eliminar_epp_epp_3)        # botón para eliminar (en rojo para que de mas susto)
boton_eliminar_epp_3.grid(row=pos_y_epp_3+8, column=0)

label_eliminado_epp3 = Label(editar_epp, text='')    # dice el status de la eliminación
label_eliminado_epp3.grid(row=pos_y_epp_3+8, column=1)    
        
# tabs stock ////////////////////////////////////////


root.mainloop()

cur.close()
conn.close()
