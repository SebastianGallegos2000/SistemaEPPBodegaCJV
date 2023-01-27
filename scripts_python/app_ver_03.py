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


def main(usuario_id):
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
    frame_bodega = Frame(tabs)      # frame para ver info de las bodegas
    frame_stock = Frame(tabs)       # frame para ver info del stock
    frame_usuarios = Frame(tabs)  # frame para ver info de los usuarios
    frame_entregas = Frame(tabs)    # frame para ver info de las entregas

    # se añaden los frames a sus tabs corresponidentes 
    tabs.add(frame_empleados, text='Empleados')
    tabs.add(frame_epp, text='EPP')
    tabs.add(frame_bodega, text='Bodega')
    tabs.add(frame_usuarios, text='Usuarios')
    tabs.add(frame_stock, text='Stock')
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
                                    entry_apellido_e_1.get(),
                                    options_vigencia_e_1.get(),
                                    entry_gerencia_e_1.get(),
                                    entry_departamento_e_1.get(),
                                    options_seccion_e_1.get(),
                                    entry_cargo_e_1.get(),
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

    # labels con los resultados de la busqueda 

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
            label_annadir_output_e_2['text'] = 'No se pudo añadir al empleado, por favor revisar que el formato esté correcto'
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

    label_actualizado_e_3 = Label(editar_empleado, text='')                               # label con texto en el frame 
    label_actualizado_e_3.grid(row=pos_y_e_3+12, column=3)                                # se pone en el frame

    def confirmar_eliminar_e_3(eleccion,id):
        popup_eliminar_empleado_e_3.destroy()           # se elimina la ventana
        if(eleccion):                                   # si se dijo que si 
            res = eliminar_empleado_func(id,cur,conn)         # se elimina el empleado
            if(res == 1):
                label_eliminado_e3['text'] = 'Se eliminó el empleado de id '+id+' de la base de datos'
                label_eliminado_e3['fg'] = color_exito
            elif(res == -1):
                label_eliminado_e3['text'] = 'No se pudo eliminar el empleado de id '+id+' de la base de datos'
                label_eliminado_e3['fg'] = color_error

        elif(not eleccion):                             # si se dijo que no, no se elimina
            label_eliminado_e3['text'] = 'El empleado de id '+id+' no se eliminó de la base de datos'
            label_eliminado_e3['fg'] = color_exito

    def eliminar_empleado_e_3():    # función al apretar el botón eliminar
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

    buscar_epp = Frame(tabs_epp)     # se crea y se le da como padre las tabs de epp
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
            label_eliminado_epp3['text'] = 'Se eliminó el EPP de id '+id+' de la base de datos'
            label_eliminado_epp3['fg'] = color_exito

        elif(not eleccion):                     # si se dijo que no, no se elimina
            label_eliminado_epp3['text'] = 'El EPP de id '+id+' no se eliminó de la base de datos'
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
            
    # tabs bodega

    tabs_bodega = ttk.Notebook(frame_bodega)   # tabs de los bodega
    tabs_bodega.pack()                            # se ubica en el frame de bodega

    ## frame para ver bodegas

    ver_bodega = Frame(tabs_bodega)                 # se crea y se le da como padre las tabs de bodega 
    tabs_bodega.add(ver_bodega,text='Ver')   # se ubica el frame en las tabs de bodega
    
    # _b_1 es por bodega tab 1

    def ver_bodegas_b_1():
        delete_b_1()            # se borra la listbox para poner el contenido nuevo
        bodegas = ver_todas_bodegas_func(cur,conn)  # se guardan todos los empleados que cumplen los parámetros

        try:
            for bodega in bodegas:             # se rellena la listbox con las bodegas
                listbox_b_1.insert(END, bodega[0])  # se insertan las bodegas
        except:
            pass


    listbox_b_1 = Listbox(ver_bodega, width=25, height=10)  # se crea una listbox que muestra los empleados
    listbox_b_1.grid(row=0, columnspan=4, sticky= W+E)      # se posiciona la listbox

    def delete_b_1():
        listbox_b_1.delete(0,END)   # se limpia la listbox

    ver_bodegas_b_1()       # se muestran las bodegas

    ## frame para añadir y eliminar bodegas

    annadir_bodega = Frame(tabs_bodega)                 # se crea y se le da como padre las tabs de bodega 
    tabs_bodega.add(annadir_bodega,text='Añadir')   # se ubica el frame en las tabs de bodega

    # _b_2 añadir bodegas o eliminar bodegas 

    def annadir_bodega_b_2():
        res = annadir_bodega_func(entry_nombre_b_2.get(),
                                cur,
                                conn)
        if(res == 1):
            label_annadir_output_b_2['text'] = 'Bodega '+str((entry_nombre_b_2.get()).upper())+' añadida'
            label_annadir_output_b_2['fg'] = color_exito
        elif(res == -1):
            label_annadir_output_b_2['text'] = 'No se pudo añadir la bodega, por favor revisar que el formato esté correcto o que no esté ya en la base'
            label_annadir_output_b_2['fg'] = color_error
        else:
            label_annadir_output_b_2['text'] = 'Error inseperado'
            label_annadir_output_b_2['fg'] = color_error
        
        ver_bodegas_b_1()

    label_info_b_2 = Label(annadir_bodega, text='Añadir bodegas')
    label_info_b_2.grid(row=0,column=0)

    label_nombre_b_2 = Label(annadir_bodega, text='Nombre:')   # label con texto en el frame
    label_nombre_b_2.grid(row=1,column=0)                               # se pone en el frame
    entry_nombre_b_2 = Entry(annadir_bodega)                   # caja para texto del nombre
    entry_nombre_b_2.grid(row=1,column=1)                               # se ubica en el frame  

    boton_annadir_b_2 = Button(annadir_bodega, text='Añadir bodega', command=annadir_bodega_b_2)    # boton para añadir
    boton_annadir_b_2.grid(row=2,column=1)

    label_annadir_output_b_2 = Label(annadir_bodega, text='')           # label con información de status 
    label_annadir_output_b_2.grid(row=3, column=2)                      

    ## frame para eliminar bodegas 

    eliminar_bodega = Frame(tabs_bodega)
    tabs_bodega.add(eliminar_bodega, text='Eliminar')

    # b_3 por bodega tab
        
    label_nombre_b_3 = Label(eliminar_bodega, text='Nombre de la bodega:')
    label_nombre_b_3.grid(row=0,column=0)


    def confirmar_eliminar_b_3(eleccion,nombre):
        popup_eliminar_bodega_b_3.destroy()      # se elimina la ventana
        if(eleccion):                           # si se dijo que si     
            eliminar_bodega_func(nombre,cur,conn)      # se elimina la bodega
            label_status_b_3['text'] = 'Se eliminó la bodega '+nombre+' de la base de datos'
            label_status_b_3['fg'] = color_exito
            ver_bodegas_b_1()        

        elif(not eleccion):                     # si se dijo que no, no se elimina
            label_status_b_3['text'] = 'La bodega '+nombre+' no se eliminó de la base de datos'
            label_status_b_3['fg'] = color_exito
        
        else:                                   # en caso de un error imprevisto
            label_status_b_3['text'] = 'Error insesperado'
            label_status_b_3['fg'] = color_error


    def eliminar_b_3():
        nombre = entry_nombre_b_3.get()
        nombre = nombre.strip()
        nombre = nombre.upper()
        
        res = bodega_en_db_nombre(nombre,cur,conn)   # se ejecuta la consulta

        if res == 1:                            # si es qu está
            global popup_eliminar_bodega_b_3  # global para poder ser llamada desde la funcíon de arriba
            popup_eliminar_bodega_b_3 = Toplevel(root)    # se crea la ventana
            popup_eliminar_bodega_b_3.title('Confimración de eliminar bodega')  #   titulo y dimensiones
            popup_eliminar_bodega_b_3.geometry('350x100')

            pop_label_b_3 = Label(popup_eliminar_bodega_b_3, text='¿Desea eliminar el bodega ' + nombre +' de las base de datos?')  # label para el texto
            pop_label_b_3.pack(pady=10)

            pop_frame_b_3 = Frame(popup_eliminar_bodega_b_3)  # frame para los botones
            pop_frame_b_3.pack(pady =5)

            boton_si_b_3 = Button(pop_frame_b_3, text='Sí', fg=color_error, command=lambda: confirmar_eliminar_b_3(True,nombre)) #   boton para confirmar la eliminación
            boton_si_b_3.grid(row=0,column=0,padx=10)

            boton_no_b_3 = Button(pop_frame_b_3, text='No', command=lambda: confirmar_eliminar_b_3(False,nombre))   # boton para desconfirmar la eliminación 
            boton_no_b_3.grid(row=0,column=1,padx=10)

            label_status_b_3['text'] = 'Confirme en la ventana que apareció'  # dice para que el usuario sepa que debe confirmar en la pantalla
            label_status_b_3['fg'] = color_exito
        elif res == 0:                                                  # si no lo encuentra
            label_status_b_3['text'] = 'No se econtró la bodega '+nombre+' en la base de datos'
            label_status_b_3['fg'] = color_error
        elif res == -1:                                                 # está mal el formato 
            label_status_b_3['text'] = 'Asegurese de que el nombre esté en el formato correcto'
            label_status_b_3['fg'] = color_error

    entry_nombre_b_3 = Entry(eliminar_bodega)       # caja para texto del nombre
    entry_nombre_b_3.grid(row=0, column=1)          # se posiciona en el frame


    boton_eliminar_nombre_b_3 = Button(eliminar_bodega, text='Eliminar', fg=color_error, command=eliminar_b_3)  # borón para eliminar   
    boton_eliminar_nombre_b_3.grid(row=0, column=2)         # se posiciona en el frame

    label_status_b_3 = Label(eliminar_bodega, text='')      # para tener info del status al borrar
    label_status_b_3.grid(row=1, column=0)

    # frame usuarios ////////////////////////////////////////

    tabs_usuarios = ttk.Notebook(frame_usuarios)   # tabs de los usuarios
    tabs_usuarios.pack()                            # se ubica en el frame de usuarios

    ## frame para buscar usuario ////////////////////////////////////////

    buscar_usuario = Frame(tabs_usuarios)                           # se crea y se le da como padre las tabs de usuario 
    tabs_usuarios.add(buscar_usuario,text='Buscar')        # se ubica el frame en las tabs de usuario  

    # _u_1 es por usuario tab 1

    # para buscar por ID

    def selectID_u_1(id):       # muestra la info de un trabajador dando el id directamente 
        lista = ['']*13         # lista para los doce atributos
        res = ver_usuario_id(id,cur,conn)   # se ejecuta la consulta

        try:                    # con un try por si algo falla
            for i in range(0,13):           # se guardan los resultados en la lista
                lista[i] = res[i]
        except:                             # si es que falla
            for i in range(0,13):           # se llena con strings vacíos
                lista[i] = ''
        for i in range(0,13):               # escribe el resultado de la consulta en los labels 
            lista_output_u_1[i]['text'] = lista[i]
            if lista[i] == None:
                lista_output_u_1[i]['text'] = ''


    def inputID_u_1():          # muestra la info de un trabajador dando su identificador (rut o pasaporte)
        id = entry_id_u_1.get() # se obtiene la id de la checkbox

        selectID_u_1(id)        # se llama a selectID_e_1

    label_texto_id_u_1 = Label(buscar_usuario, text='Buscar usuario por ID')
    label_texto_id_u_1.grid(row=0, column=0)

    label_id_input_u_1 = Label(buscar_usuario, text='ID:')               # label con texto en el frame 
    label_id_input_u_1.grid(row=1, column=0)                                    # se pone en el frame

    entry_id_u_1 = Entry(buscar_usuario)                                # caja para escribir el ID
    entry_id_u_1.grid(row=1, column=1)                                          # se ubica la caja en el frame

    boton_buscar_id_u_1 = Button(buscar_usuario, text='Buscar', command=inputID_u_1)         # botón para ejecutar la busqueda
    boton_buscar_id_u_1.grid(row=1, column=2)  

    # para filtrar por otros parámetros

    def filtrar_u_1():
        delete_u_1()                    # se borra la listbox para poner el contenido nuevo
        usuarios =  ver_usuarios(entry_nombre_u_1.get(),
                                    entry_apellido_u_1.get(),
                                    options_vigencia_u_1.get(),
                                    options_orden_u_1.get(),
                                    options_permisos_u_1.get(),
                                    cur,
                                    conn)    # se guardan todos los empleados que cumplen los parámetros
        try:
            for usuario in usuarios:             # se rellena la listbox con los empleados
                listbox_u_1.insert(END, usuario)  
        except:
            pass

    label_filtrar_text_u_1 = Label(buscar_usuario, text='Filtrar usuarios')       # label con texto en el frame
    label_filtrar_text_u_1.grid(row=0,column=3)   

    pos_y_u_1_filtar = 1

    # Primer Nombre
    label_nombre_input_u_1 = Label(buscar_usuario, text='Primer Nombre')       # label con texto en el frame
    label_nombre_input_u_1.grid(row=pos_y_u_1_filtar, column=3)                                # se ubica en el frame

    entry_nombre_u_1 = Entry(buscar_usuario)                            # caja para texto del nombre
    entry_nombre_u_1.grid(row=pos_y_u_1_filtar, column=4)                                      # se ubica en el frame

    # botón filtrar

    boton_buscar_nombre_u_1 = Button(buscar_usuario, text='Filtrar', command=filtrar_u_1)     # botón para ejecutar la busqueda
    boton_buscar_nombre_u_1.grid(row=pos_y_u_1_filtar, column=5)                               # se ubica el botón en el frame

    # apellido paterno

    label_apellido_input_u_1 = Label(buscar_usuario, text='Apellido Paterno')   # label con texto en el frame
    label_apellido_input_u_1.grid(row=pos_y_u_1_filtar+1, column=3)                              # se ubica en el frame

    entry_apellido_u_1 = Entry(buscar_usuario)                          # caja para texto del nombre
    entry_apellido_u_1.grid(row=pos_y_u_1_filtar+1, column=4)        

    # vigencia

    label_vigencia_input_u_1 = Label(buscar_usuario, text='Vigencia')
    label_vigencia_input_u_1.grid(row=pos_y_u_1_filtar+2, column= 3)

    options_vigencia_u_1 = StringVar()
    options_vigencia_u_1.set('')
    dropdown_vigencia_u_1 = OptionMenu(buscar_usuario, options_vigencia_u_1, '', 'CONTRATO VIGENTE', 'CONTRATO NO VIGENTE')
    dropdown_vigencia_u_1.grid(row=pos_y_u_1_filtar+2, column=4)

    # permisos

    label_permisos_input_u_1 = Label(buscar_usuario, text='Permisos')
    label_permisos_input_u_1.grid(row=pos_y_u_1_filtar+3, column= 3)

    options_permisos_u_1 = StringVar()
    options_permisos_u_1.set('')
    dropdown_permisos_u_1 = OptionMenu(buscar_usuario, options_permisos_u_1, '','SIN PERMISOS' , 'BODEGUERO', 'ADMIN BODEGUERO', 'ADMIN TI')
    dropdown_permisos_u_1.grid(row=pos_y_u_1_filtar+3, column=4)


    # orden de filtro

    label_orden_input_u_1 = Label(buscar_usuario, text='Orden de empleados')
    label_orden_input_u_1.grid(row=pos_y_u_1_filtar+4, column= 3)

    options_orden_u_1 = StringVar()
    options_orden_u_1.set('ID descendiente')
    dropdown_orden_u_1 = OptionMenu(buscar_usuario, options_orden_u_1, 'ID ascendiente', 'ID descendiente', 'Fecha de ingreso ascendiente', 'Fecha de ingreso descendiente')
    dropdown_orden_u_1.grid(row=pos_y_u_1_filtar+4, column=4)

    # labels con los resultados de la busqueda 

    pos_y_u_1=3

    label_id_u_1 = Label(buscar_usuario, text='ID:')                                     # label con texto en el frame 
    label_id_u_1.grid(row=pos_y_u_1, column=0)                                      # se pone en el frame
    label_id_output_u_1 = Label(buscar_usuario, text='')                                 # label con texto en el frame 
    label_id_output_u_1.grid(row=pos_y_u_1, column=1)                               # se pone en el frame

    label_nombre1_u_1 = Label(buscar_usuario, text='Primer Nombre:')                     # label con texto en el frame 
    label_nombre1_u_1.grid(row=pos_y_u_1+1, column=0)                               # se pone en el frame
    label_nombre1_output_u_1 = Label(buscar_usuario, text='')                            # label con texto en el frame 
    label_nombre1_output_u_1.grid(row=pos_y_u_1+1, column=1)                        # se pone en el frame

    label_nombre2_u_1 = Label(buscar_usuario, text='Segundo Nombre:')                    # label con texto en el frame 
    label_nombre2_u_1.grid(row=pos_y_u_1+2, column=0)                               # se pone en el frame
    label_nombre2_output_u_1 = Label(buscar_usuario, text='')                            # label con texto en el frame 
    label_nombre2_output_u_1.grid(row=pos_y_u_1+2, column=1)                        # se pone en el frame

    label_nombre3_u_1 = Label(buscar_usuario, text='Tercer Nombre:')                     # label con texto en el frame 
    label_nombre3_u_1.grid(row=pos_y_u_1+3, column=0)                               # se pone en el frame
    label_nombre3_output_u_1 = Label(buscar_usuario, text='')                            # label con texto en el frame 
    label_nombre3_output_u_1.grid(row=pos_y_u_1+3, column=1)                        # se pone en el frame

    label_apellidoP_u_1 = Label(buscar_usuario, text='Apellido Paterno:')                # label con texto en el frame 
    label_apellidoP_u_1.grid(row=pos_y_u_1+4, column=0)                             # se pone en el frame
    label_apellidoP_output_u_1 = Label(buscar_usuario, text='')                          # label con texto en el frame 
    label_apellidoP_output_u_1.grid(row=pos_y_u_1+4, column=1)                      # se pone en el frame

    label_apellidoM_u_1 = Label(buscar_usuario, text='Apellido Materno:')                # label con texto en el frame 
    label_apellidoM_u_1.grid(row=pos_y_u_1+5, column=0)                             # se pone en el frame
    label_apellidoM_output_u_1 = Label(buscar_usuario, text='')                          # label con texto en el frame 
    label_apellidoM_output_u_1.grid(row=pos_y_u_1+5, column=1)                      # se pone en el frame

    label_vigencia_u_1 = Label(buscar_usuario, text='Vigencia:')                         # label con texto en el frame 
    label_vigencia_u_1.grid(row=pos_y_u_1+6, column=0)                              # se pone en el frame
    label_vigencia_output_u_1 = Label(buscar_usuario, text='')                           # label con texto en el frame 
    label_vigencia_output_u_1.grid(row=pos_y_u_1+6, column=1)                       # se pone en el frame

    label_gerencia_u_1 = Label(buscar_usuario, text='Gerencia:')                         # label con texto en el frame 
    label_gerencia_u_1.grid(row=pos_y_u_1+7, column=0)                              # se pone en el frame
    label_gerencia_output_u_1 = Label(buscar_usuario, text='')                           # label con texto en el frame 
    label_gerencia_output_u_1.grid(row=pos_y_u_1+7, column=1)                       # se pone en el frame

    label_departamento_u_1 = Label(buscar_usuario, text='Departamento:')                 # label con texto en el frame 
    label_departamento_u_1.grid(row=pos_y_u_1+8, column=0)                          # se pone en el frame
    label_departamento_output_u_1 = Label(buscar_usuario, text='')                       # label con texto en el frame 
    label_departamento_output_u_1.grid(row=pos_y_u_1+8, column=1)                   # se pone en el frame

    label_seccion_u_1 = Label(buscar_usuario, text='Sección:')                           # label con texto en el frame 
    label_seccion_u_1.grid(row=pos_y_u_1+9, column=0)                               # se pone en el frame
    label_seccion_output_u_1 = Label(buscar_usuario, text='')                            # label con texto en el frame 
    label_seccion_output_u_1.grid(row=pos_y_u_1+9, column=1)                        # se pone en el frame

    label_fecha_u_1 = Label(buscar_usuario, text='Fecha de ingreso:')                    # label con texto en el frame 
    label_fecha_u_1.grid(row=pos_y_u_1+10, column=0)                                # se pone en el frame
    label_fecha_output_u_1 = Label(buscar_usuario, text='')                              # label con texto en el frame 
    label_fecha_output_u_1.grid(row=pos_y_u_1+10, column=1)                         # se pone en el frame

    label_cargo_u_1 = Label(buscar_usuario, text='Cargo:')                               # label con texto en el frame 
    label_cargo_u_1.grid(row=pos_y_u_1+11, column=0)                                # se pone en el frame
    label_cargo_output_u_1 = Label(buscar_usuario, text='')                              # label con texto en el frame 
    label_cargo_output_u_1.grid(row=pos_y_u_1+11, column=1)   

    label_permisos_u_1 = Label(buscar_usuario, text='Permisos:')                               # label con texto en el frame 
    label_permisos_u_1.grid(row=pos_y_u_1+12, column=0)                                # se pone en el frame
    label_permisos_output_u_1 = Label(buscar_usuario, text='')                              # label con texto en el frame 
    label_permisos_output_u_1.grid(row=pos_y_u_1+12, column=1)   

    # lista con las labels de output con la información
    lista_output_u_1 = [label_id_output_u_1,
                    label_nombre1_output_u_1,
                    label_nombre2_output_u_1,
                    label_nombre3_output_u_1,
                    label_apellidoP_output_u_1,
                    label_apellidoM_output_u_1,
                    label_vigencia_output_u_1,
                    label_gerencia_output_u_1,
                    label_departamento_output_u_1,
                    label_seccion_output_u_1,
                    label_fecha_output_u_1,
                    label_cargo_output_u_1,
                    label_permisos_output_u_1
                ]

    usuarios_u_1 = ver_todos_usuarios_func(cur,conn)    # se llama a la función para ver a todos los usuarios y se guardan las tuplas en la listbox 

    listbox_u_1 = Listbox(buscar_usuario, width=180, height=10) # se crea una listbox que muestra los usuarios
    listbox_u_1.grid(row=pos_y_u_1+13, columnspan=14, sticky= W+E)      # se posiciona la listbox

    for usuario_func in usuarios_u_1:             # se rellena la listbox con los usuarios
        listbox_u_1.insert(END, usuario_func)   
    
    def select_u_1():                           # función para seleccionar usuario directamente de las litbox 
        atributos = listbox_u_1.get(ANCHOR) # se obtiene el usuarrio subrayado en la listbox
        entry_id_u_1.delete(0,'end')        # se borra el texto en el campo
        id = atributos[0]
        entry_id_u_1.insert(0,id)           # y se inserta el texto
        selectID_u_1(id)          # se le da el rut (atributo 0) para que se muestre en pantalla

    boton_select_u_1 = Button(buscar_usuario, text='Seleccionar usuario', command=select_u_1)   # botón para seleccionar usuario subrayado    
    boton_select_u_1.grid(row=pos_y_u_1+14, column=0)           # se posiciona el botón 

    def delete_u_1():                   # borra todo el contenido de la listbox
        listbox_u_1.delete(0,END)

    ## frame para añadir usuario manalmente ////////////////////////////////////////

    annadir_usuario = Frame(tabs_usuarios)                     # se crea y se le da como padre las tabs de empleado 
    tabs_usuarios.add(annadir_usuario,text='Añadir')     # se ubica el frame en las tabs de empleado   

    label_info_u_2 = Label(annadir_usuario, text='Añadir usuario, los campos con * son obligatorios')
    label_info_u_2.grid(row=0, column=0)

    pos_y_u_2 = 1 

    label_id_u_2 = Label(annadir_usuario, text='ID*')                                     # label con texto en el frame 
    label_id_u_2.grid(row=pos_y_u_2, column=0)                                      # se pone en el frame
    entry_id_u_2 = Entry(annadir_usuario)                            # caja para texto del nombre
    entry_id_u_2.grid(row=pos_y_u_2, column=1)    

    label_permisos_u_2 = Label(annadir_usuario, text='Permisos*')                                     # label con texto en el frame 
    label_permisos_u_2.grid(row=pos_y_u_2+1, column=0)   
    options_permisos_u_2 = StringVar()
    dropdown_permisos_u_2 = OptionMenu(annadir_usuario, options_permisos_u_2, 'BODEGUERO', 'ADMIN BODEGUERO', 'ADMIN TI')
    dropdown_permisos_u_2.grid(row=pos_y_u_2+1, column=1)

    label_user_u_2 = Label(annadir_usuario, text='Nombre de Usuario*')                                     # label con texto en el frame 
    label_user_u_2.grid(row=pos_y_u_2+2, column=0)                                      # se pone en el frame
    entry_user_u_2 = Entry(annadir_usuario)                            # caja para texto del nombre
    entry_user_u_2.grid(row=pos_y_u_2+2, column=1)  

    label_password_u_2 = Label(annadir_usuario, text='Contraseña*')                                     # label con texto en el frame 
    label_password_u_2.grid(row=pos_y_u_2+3, column=0)                                      # se pone en el frame
    entry_password_u_2 = Entry(annadir_usuario)                            # caja para texto del nombre
    entry_password_u_2.grid(row=pos_y_u_2+3, column=1)  

    def annadir_usuario_u_2():
        res = annadir_usuario_func(entry_id_u_2.get(),
            options_permisos_u_2.get(),
            entry_user_u_2.get(),
            entry_password_u_2.get(),
            cur,
            conn
                )

        if(res == 1):
            label_annadir_output_u_2['text'] = 'Usuario añadido'
            label_annadir_output_u_2['fg'] = color_exito
        elif(res == 0):
            label_annadir_output_u_2['text'] = 'El empleado no está registrado en los empleados, agreguelo antes de volverlo un usuario'
            label_annadir_output_u_2['fg'] = color_error
        elif(res == -1):
            label_annadir_output_u_2['text'] = 'No se pudo añadir al usuario, por favor revisar que el formato esté correcto'
            label_annadir_output_u_2['fg'] = color_error
        else:
            label_annadir_output_u_2['text'] = 'Error inseperado'
            label_annadir_output_u_2['fg'] = color_error

    boton_annadir_u_2 = Button(annadir_usuario, text='Añadir Usuario', command=annadir_usuario_u_2)   # botón para añadir empleado 
    boton_annadir_u_2.grid(row=pos_y_u_2+4, column=1)           # se posiciona el botón 

    label_annadir_output_u_2 = Label(annadir_usuario, text='')
    label_annadir_output_u_2.grid(row=pos_y_u_2+4, column=2)    

    # frame para editar usuario

    editar_usuario = Frame(tabs_usuarios)
    tabs_usuarios.add(editar_usuario, text='Editar/Eliminar')

    # _u_3 por usuario tab 3

    def select_u_3(id):     # muestra la info de un empleado dando el id directamente 
        lista = ['']*4      # lista para 4 atributos
        res = ver_usuario_param_id(id,cur,conn)   # se ejecuta la consulta

        try:
            for i in range(0,4):        # se guardan los resultados en la lisra
                lista[i] =  res[i]
        except:                         # si es que falla
            for i in range(0,4):        # se llena con strings vacíos
                lista[i] = ''
        lista[3] = ''       # no se debe ver la contraseña
        for i in range(0,3):        # escribe el resultado en los labels
            lista_output_u_3[i]['text'] = lista[i+1]


    def inputID_u_3():  # muetra la info de un empleado
        id = entry_id_u_3.get() # se obtiene la id de la checkbox
        select_u_3(id)  # se llama a la función

    def actualizar_usuario_u_3():
        res = modificar_usuario_func(entry_id_u_3.get(),
                                    option_permisos_u_3.get(),
                                    entry_usuario_u_3.get(),
                                    entry_contrasenna_u_3.get(),
                                    cur,
                                    conn
                                    )
        id = entry_id_u_3.get()                        
        if(res == 1):
            label_actualizado_u_3["text"] = 'Usuario '+id+' actualizado correctamente'
            label_actualizado_u_3['fg'] = color_exito
        elif(res == -1):
            label_actualizado_u_3["text"] = 'No se pudo actualizar el usuario '+id+' , asegurese que esté todo en el formato correcto o que esté en la base de datos'
            label_actualizado_u_3['fg'] = color_error
        else:
            label_actualizado_u_3["text"] = 'Error inseperado'
            label_actualizado_u_3['fg'] = color_error
        
        inputID_u_3()   # para actualizar inmediatamente el usuario en la pantalla

    label_id_input_u_3 = Label(editar_usuario, text='ID')       # label con texto en el frame
    label_id_input_u_3.grid(row=0, column=0)                    # se pone en el frame

    boton_buscar_id_u_3 = Button(editar_usuario, text='Buscar', command=inputID_u_3)     # botón para ejecutar la busqueda
    boton_buscar_id_u_3.grid(row=0, column=2)                                   # se ubica el botón en el frame

    pos_y_u_3=0

    label_permisos_u_3 = Label(editar_usuario, text='Permisos')     # label con texto en el frame 
    label_permisos_u_3.grid(row=pos_y_u_3+1, column=0)                # se pone en el frame
    label_permisos_output_u_3 = Label(editar_usuario, text='')      # label con texto en el frame
    label_permisos_output_u_3.grid(row=pos_y_u_3+1,column=1)          # se pone en el frame

    label_usuario_u_3 = Label(editar_usuario, text='Usuario')      # label con texto en el frame 
    label_usuario_u_3.grid(row=pos_y_u_3+2, column=0)                # se pone en el frame
    label_usuario_output_u_3 = Label(editar_usuario, text='')      # label con texto en el frame
    label_usuario_output_u_3.grid(row=pos_y_u_3+2,column=1)          # se pone en el frame

    label_contrasenna_u_3 = Label(editar_usuario, text='Constraseña')  # label con texto en el frame 
    label_contrasenna_u_3.grid(row=pos_y_u_3+3, column=0)                # se pone en el frame
    label_contrasenna_output_u_3 = Label(editar_usuario, text='')      # label con texto en el frame
    label_contrasenna_output_u_3.grid(row=pos_y_u_3+3,column=1)          # se pone en el frame

    lista_output_u_3 = [
                    label_permisos_output_u_3,
                    label_usuario_output_u_3,
                    label_contrasenna_output_u_3
                ]

    # entries para modificar

    entry_id_u_3 = Entry(editar_usuario)        # caja de texto del id
    entry_id_u_3.grid(row=pos_y_u_3, column=1)    # se ubica en el frame

    option_permisos_u_3 = StringVar()
    option_permisos_u_3.set('')
    dropdown_permisos_u_3 = OptionMenu(editar_usuario, option_permisos_u_3, 'SIN PERMISOS' , 'BODEGUERO', 'ADMIN BODEGUERO', 'ADMIN TI')
    dropdown_permisos_u_3.grid(row=pos_y_u_3+1,column=2)

    entry_usuario_u_3 = Entry(editar_usuario)        # caja de texto del id
    entry_usuario_u_3.grid(row=pos_y_u_3+2, column=2)    # se ubica en el frame

    entry_contrasenna_u_3 = Entry(editar_usuario)        # caja de texto del id
    entry_contrasenna_u_3.grid(row=pos_y_u_3+3, column=2)    # se ubica en el frame

    boton_actualizar_u_3 = Button(editar_usuario, text='Actualizar',command=actualizar_usuario_u_3)
    boton_actualizar_u_3.grid(row=pos_y_u_3+4,column=2)

    label_actualizado_u_3 = Label(editar_usuario, text='')      # label con texto en el frame 
    label_actualizado_u_3.grid(row=pos_y_u_3+4,column=3)

    def confirmar_eliminar_u_3(eleccion,id):
        popup_eliminar_empleado_u_3.destroy()           # se elimina la ventana
        if(eleccion):                                   # si se dijo que si 
            res = eliminar_usuario_func(id,cur,conn)         # se elimina el empleado
            if(res == 1):
                label_eliminado_u3['text'] = 'Se eliminó el usuario de id '+id+' de la base de datos'
                label_eliminado_u3['fg'] = color_exito
            elif(res == -1):
                label_eliminado_u3['text'] = 'No se pudo eliminar el usuario de id '+id+' de la base de datos'
                label_eliminado_u3['fg'] = color_error

        elif(not eleccion):                             # si se dijo que no, no se elimina
            label_eliminado_u3['text'] = 'El usuario de id '+id+' no se eliminó de la base de datos'
            label_eliminado_u3['fg'] = color_exito

    def eliminar_usuario_u_3():    # función al apretar el botón eliminar
        id = entry_id_u_3.get()     # se obtiene el id del campo
        id = id.strip()

        res = usuario_en_db_id(id,cur,conn)    # se revisa si está en la base de datos
        if res == 1:                            # si es qu está
            global popup_eliminar_empleado_u_3  # global para poder ser llamada desde la funcíon de arriba
            popup_eliminar_empleado_u_3 = Toplevel(root)    # se crea la ventana
            popup_eliminar_empleado_u_3.title('Confimración de eliminar usuario')  #   titulo y dimensiones
            popup_eliminar_empleado_u_3.geometry('350x100')

            pop_label_u_3 = Label(popup_eliminar_empleado_u_3, text='¿Desea eliminar el usuario ' + id +' de las base de datos?')  # label para el texto
            pop_label_u_3.pack(pady=10)

            pop_frame_u_3 = Frame(popup_eliminar_empleado_u_3)  # frame para los botones
            pop_frame_u_3.pack(pady =5)

            boton_si_u_3 = Button(pop_frame_u_3, text='Sí', fg=color_error, command=lambda: confirmar_eliminar_u_3(True,id)) #   boton para confirmar la eliminación
            boton_si_u_3.grid(row=0,column=0,padx=10)

            boton_no_u_3 = Button(pop_frame_u_3, text='No', command=lambda: confirmar_eliminar_u_3(False,id))   # boton para desconfirmar la eliminación 
            boton_no_u_3.grid(row=0,column=1,padx=10)

            label_eliminado_u3['text'] = 'Confirme en la ventana que apareció'  # dice para que el usuario sepa que debe confirmar en la pantalla
            label_eliminado_u3['fg'] = color_exito
        elif res == 0:                                                  # si no lo encuentra
            label_eliminado_u3['text'] = 'No se econtró un empleado con la id '+id+' en la base de datos'
            label_eliminado_u3['fg'] = color_error
        elif res == -1:                                                 # está mal el formato 
            label_eliminado_u3['text'] = 'Asegurese de que el id esté en el formato correcto'
            label_eliminado_u3['fg'] = color_error

    boton_eliminar_u_3 = Button(editar_usuario, text='Eliminar', fg=color_error, command=eliminar_usuario_u_3)
    boton_eliminar_u_3.grid(row=pos_y_u_3+5, column=0)

    label_eliminado_u3 = Label(editar_usuario, text='')    # dice el status de la eliminación
    label_eliminado_u3.grid(row=pos_y_u_3+5, column=1)

    # tabs stock ////////////////////////////////////////

    tabs_stock = ttk.Notebook(frame_stock)   # tabs de los stock
    tabs_stock.pack()                            # se ubica en el frame de stock

    ## frame para ver stock ////////////////////////////////////////

    buscar_stock = Frame(tabs_stock)     # se crea y se le da como padre las tabs de stock
    tabs_stock.add(buscar_stock, text='Buscar')

    # _stock_1 de primer tab de stock

    def selectID_stock_1(id,bodega):     # muestra la info del stock dando el id y bodega directamente
        lista = ['']*10          # lista para los 10 atributos
        res = ver_stock_id(id,bodega,cur,conn)   # se ejecuta la consulta
        try:                    # en un try por si algo falla
            for i in range(0,10):    # se guardan los resultados en la lista
                lista[i] = res[i]
        except:                     # si es que falla
            for i in range(0,10):    # se llena con strings vacíos
                lista[i] = ''
        for i in range(0,10):        # escribe el resultado de la consulta en los labels
            lista_output_stock_1[i]['text'] = lista[i]
            if lista[i] == None:    # si es un none se llena con un string vacío (se debe llenar con algo o si no queda el texto que estaba antes)
                lista_output_stock_1[i]['text'] = ''
        try:
            if(lista[8]<=lista[9]):
                lista_output_stock_1[8]['fg'] = color_error
            else:
                lista_output_stock_1[8]['fg'] = color_exito    
        except:
            pass


    def inputID_stock_1():            # muestra la info de un trabajador dando su identificador (rut o pasaporte)
        id = entry_id_stock_1.get()   # se obtiene la id del entry
        bodega = options_bodega_input_stock_1.get() # bodega seleccionada
        selectID_stock_1(id,bodega)          # se llama a selectID_e_1

    # para buscar por código de producto

    label_texto_id_stock_1 = Label(buscar_stock, text='Buscar stock por código de producto y bodega')
    label_texto_id_stock_1.grid(row=0, column=0)

    label_id_input_stock_1 = Label(buscar_stock, text='Código de producto:')               # label con texto en el frame 
    label_id_input_stock_1.grid(row=1, column=0)                                    # se pone en el frame

    entry_id_stock_1 = Entry(buscar_stock)                                # caja para escribir el código 
    entry_id_stock_1.grid(row=1, column=1)                                          # se ubica la caja en el frame

    boton_buscar_id_stock_1 = Button(buscar_stock, text='Buscar', command=inputID_stock_1)         # botón para ejecutar la busqueda
    boton_buscar_id_stock_1.grid(row=1, column=2)                                   # se ubica el botón en el frame

    # label bodega

    label_bodega_info_stock_1 = Label(buscar_stock, text='Bodega:')               # label con texto en el frame 
    label_bodega_info_stock_1.grid(row=2, column=0)                                    # se pone en el frame

    # opciones de bodega

    options_bodega_input_stock_1 = StringVar()
    options_bodega_input_stock_1.set('')

    bodegas_tupla = ver_todas_bodegas_func(cur,conn)        # se consiguen todas las bodegas
    bodegas_lista = ['']    # lista con solo  ''
    for i in range(0,len(bodegas_tupla)):    # se llenan todas las bodegas en la lista 
        bodegas_lista.append(bodegas_tupla[i][0])

    dropdown_bodega_input_stock_1 = OptionMenu(buscar_stock, options_bodega_input_stock_1, *bodegas_lista)
    dropdown_bodega_input_stock_1.grid(row=2, column=1)

    # para filtrar por otros parámetros

    def filtrar_stock_1():
        delete_stock_1()          # se borra la listbox para poner el contenido nuevo
        stocks = ver_stocks(entry_c_construct_stock_1.get(),
                        entry_nombre_stock_1.get(),
                        entry_c_desig_stock_1.get(),
                        entry_talla_stock_1.get(),
                        entry_UM_stock_1.get(),
                        options_orden_stock_1.get(),
                        options_bodega_filtro_stock_1.get(),
                        var_critico.get(),
                        cur,
                        conn)
        try:
            for stock in stocks:
                listbox_stock_1.insert(END, stock)
        except:
            pass

    label_filtrar_text_stock_1 = Label(buscar_stock, text='Filtrar Stock')       # label con texto en el frame
    label_filtrar_text_stock_1.grid(row=0,column=3)                                                     # se ubica en el frame

    pos_y_stock_1_filtar = 1

    # Código trabajador
    label_c_construct_input_stock_1 = Label(buscar_stock, text='Codigo de constructor')       # label con texto en el frame
    label_c_construct_input_stock_1.grid(row=pos_y_stock_1_filtar, column=3)                                # se ubica en el frame

    entry_c_construct_stock_1 = Entry(buscar_stock)                            # caja para texto del nombre
    entry_c_construct_stock_1.grid(row=pos_y_stock_1_filtar, column=4)   

    # botón filtrar

    boton_filtrar_stock_1 = Button(buscar_stock, text='Filtrar', command=filtrar_stock_1)     # botón para ejecutar la busqueda
    boton_filtrar_stock_1.grid(row=pos_y_stock_1_filtar, column=5)                               # se ubica el botón en el frame

    # Nombre
    label_nombre_input_stock_1 = Label(buscar_stock, text='Nombre de producto')       # label con texto en el frame
    label_nombre_input_stock_1.grid(row=pos_y_stock_1_filtar+1, column=3)                                # se ubica en el frame

    entry_nombre_stock_1 = Entry(buscar_stock)                            # caja para texto del código constructor
    entry_nombre_stock_1.grid(row=pos_y_stock_1_filtar+1, column=4)    

    # Constructor designado
    label_c_desig_input_stock_1 = Label(buscar_stock, text='Constructor designado')       # label con texto en el frame
    label_c_desig_input_stock_1.grid(row=pos_y_stock_1_filtar+2, column=3)                                # se ubica en el frame

    entry_c_desig_stock_1 = Entry(buscar_stock)                            # caja para texto del constructor designado
    entry_c_desig_stock_1.grid(row=pos_y_stock_1_filtar+2, column=4)    

    # Talla 
    label_talla_stock_epp_1 = Label(buscar_stock, text='Talla')       # label con texto en el frame
    label_talla_stock_epp_1.grid(row=pos_y_stock_1_filtar+3, column=3)                                # se ubica en el frame

    entry_talla_stock_1 = Entry(buscar_stock)                            # caja para texto de la talla
    entry_talla_stock_1.grid(row=pos_y_stock_1_filtar+3, column=4)    

    # Unidad de medida 
    label_UM_input_stock_1 = Label(buscar_stock, text='Unidad de medida')       # label con texto en el frame
    label_UM_input_stock_1.grid(row=pos_y_stock_1_filtar+4, column=3)                                # se ubica en el frame

    entry_UM_stock_1 = Entry(buscar_stock)                            # caja para texto de la UM
    entry_UM_stock_1.grid(row=pos_y_stock_1_filtar+4, column=4)    

    # bodega 

    label_bodega_input_stock_1 = Label(buscar_stock, text='Bodega')             # label con texto en el frame
    label_bodega_input_stock_1.grid(row=pos_y_stock_1_filtar+5, column=3)       # se ubica en el frame

    options_bodega_filtro_stock_1 = StringVar()
    options_bodega_filtro_stock_1.set('')
    dropdown_bodega_filtro_stock_1 = OptionMenu(buscar_stock, options_bodega_filtro_stock_1, *bodegas_lista)
    dropdown_bodega_filtro_stock_1.grid(row=pos_y_stock_1_filtar+5, column=4)

    # su stock es crítico  

    label_stock_critico_input_stock_1 = Label(buscar_stock, text='Stock Critico')             # label con texto en el frame
    label_stock_critico_input_stock_1.grid(row=pos_y_stock_1_filtar+6, column=3)              # se ubica en el frame

    var_critico = IntVar()  # variable que dice si el check está presionado o no
    check_critico = Checkbutton(buscar_stock, variable=var_critico)
    check_critico.grid(row=pos_y_stock_1_filtar+6, column=4)

    # orden de filtro

    label_orden_input_stock_1 = Label(buscar_stock, text='Orden de stock')
    label_orden_input_stock_1.grid(row=pos_y_stock_1_filtar+7, column= 3)

    options_orden_stock_1 = StringVar()
    options_orden_stock_1.set('Código de producto descendiente')
    dropdown_orden_stock_1 = OptionMenu(buscar_stock, options_orden_stock_1, 'Código de producto ascendiente', 'Código de producto descendiente', 'Precio ascendiente', 'Precio descendiente', 'Stock ascendiente', 'Stock descendiente')
    dropdown_orden_stock_1.grid(row=pos_y_stock_1_filtar+7, column=4)

    # labels con los resultados de la busqueda
    
    pos_y_stock_1=3

    label_id_stock_1 = Label(buscar_stock, text='Código de producto:')                                     # label con texto en el frame 
    label_id_stock_1.grid(row=pos_y_stock_1, column=0)                                      # se pone en el frame
    label_id_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_id_output_stock_1.grid(row=pos_y_stock_1, column=1)                               # se pone en el frame

    label_c_c_stock_1 = Label(buscar_stock, text='Código de constructor:')                                     # label con texto en el frame 
    label_c_c_stock_1.grid(row=pos_y_stock_1+1, column=0)                                      # se pone en el frame
    label_c_c_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_c_c_output_stock_1.grid(row=pos_y_stock_1+1, column=1)                               # se pone en el frame

    label_nombre_stock_1 = Label(buscar_stock, text='Nombre:')                                     # label con texto en el frame 
    label_nombre_stock_1.grid(row=pos_y_stock_1+2, column=0)                                      # se pone en el frame
    label_nombre_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_nombre_output_stock_1.grid(row=pos_y_stock_1+2, column=1)    

    label_constructor_designado_stock_1 = Label(buscar_stock, text='Constructor designado:')                                     # label con texto en el frame 
    label_constructor_designado_stock_1.grid(row=pos_y_stock_1+3, column=0)                                      # se pone en el frame
    label_constructor_designado_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_constructor_designado_output_stock_1.grid(row=pos_y_stock_1+3, column=1) 

    label_talla_stock_1 = Label(buscar_stock, text='Talla:')                                     # label con texto en el frame 
    label_talla_stock_1.grid(row=pos_y_stock_1+4, column=0)                                      # se pone en el frame
    label_talla_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_talla_output_stock_1.grid(row=pos_y_stock_1+4, column=1) 

    label_UM_stock_1 = Label(buscar_stock, text='Unidad de medición:')                                     # label con texto en el frame 
    label_UM_stock_1.grid(row=pos_y_stock_1+5, column=0)                                      # se pone en el frame
    label_UM_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_UM_output_stock_1.grid(row=pos_y_stock_1+5, column=1) 

    label_precio_stock_1 = Label(buscar_stock, text='Precio:')                                     # label con texto en el frame 
    label_precio_stock_1.grid(row=pos_y_stock_1+6, column=0)                                      # se pone en el frame
    label_precio_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_precio_output_stock_1.grid(row=pos_y_stock_1+6, column=1) 

    label_bodega_stock_1 = Label(buscar_stock, text='Bodega:')                                     # label con texto en el frame 
    label_bodega_stock_1.grid(row=pos_y_stock_1+7, column=0)                                      # se pone en el frame
    label_bodega_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_bodega_output_stock_1.grid(row=pos_y_stock_1+7, column=1) 

    label_cantidad_stock_1 = Label(buscar_stock, text='Cantidad:')                                     # label con texto en el frame 
    label_cantidad_stock_1.grid(row=pos_y_stock_1+8, column=0)                                      # se pone en el frame
    label_cantidad_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_cantidad_output_stock_1.grid(row=pos_y_stock_1+8, column=1) 

    label_cantidad_critica_stock_1 = Label(buscar_stock, text='Cantidad crítica:')                                     # label con texto en el frame 
    label_cantidad_critica_stock_1.grid(row=pos_y_stock_1+9, column=0)                                      # se pone en el frame
    label_cantidad_critica_output_stock_1 = Label(buscar_stock, text='')                                 # label con texto en el frame 
    label_cantidad_critica_output_stock_1.grid(row=pos_y_stock_1+9, column=1) 


    # lista con las labels de output con la información
    lista_output_stock_1 = [
                    label_c_c_output_stock_1,
                    label_id_output_stock_1,
                    label_nombre_output_stock_1,
                    label_constructor_designado_output_stock_1,
                    label_talla_output_stock_1,
                    label_UM_output_stock_1,
                    label_precio_output_stock_1,
                    label_bodega_output_stock_1,
                    label_cantidad_output_stock_1,
                    label_cantidad_critica_output_stock_1
                ]

    stocks_stock_1 = ver_todos_los_stock_func(cur,conn)                    # se consiguen todos loe epp

    listbox_stock_1 = Listbox(buscar_stock, width=180, height=10) # se crea una listbox que muestra los epps
    listbox_stock_1.grid(row=pos_y_stock_1+10, columnspan=14, sticky= W+E)      # se posiciona la listbox

    for stock_func in stocks_stock_1:             # se rellena la listbox con los epps
        listbox_stock_1.insert(END, stock_func)      

    def select_stock_1():                                     # función para seleccionar empleado directamente de las litbox 
        atributos = listbox_stock_1.get(ANCHOR)               # se obtiene el empleado subrayado en la listbox
        entry_id_stock_1.delete(0,'end')                      # se borra lo que esté en la caja 
        id = atributos[1]   
        bodega = atributos[7]                
        entry_id_stock_1.insert(0,id)                         # se inserta el id clickeada
        options_bodega_input_stock_1.set(bodega)
        selectID_stock_1(id,bodega)                        # se le da el rut (atributo 0) para que se muestre en pantalla

    boton_select_stock_1 = Button(buscar_stock, text='Seleccionar stock', command=select_stock_1)   # botón para seleccionar empleado subrayado  
    boton_select_stock_1.grid(row=pos_y_stock_1+11, column=0)              # se posiciona el botón    

    def delete_stock_1():                         # borra todo el contenido de la listbox
        listbox_stock_1.delete(0,END)


    ## frame para agregar registro de stock ////////////////////////////////////////

    agregar_registro_stock = Frame(tabs_stock)     # se crea y se le da como padre las tabs de stock
    tabs_stock.add(agregar_registro_stock, text='Agregar registro')

    label_info_stock_2 = Label(agregar_registro_stock, text='Añadir registro de stock, los campos con * son obligatorios')
    label_info_stock_2.grid(row=0, column=0)    

    pos_y_stock_2 = 1

    label_id_stock_2 = Label(agregar_registro_stock, text='Código EPP*')                                     # label con texto en el frame 
    label_id_stock_2.grid(row=pos_y_stock_2, column=0)                                      # se pone en el frame
    entry_id_stock_2 = Entry(agregar_registro_stock)                            # caja para texto del nombre
    entry_id_stock_2.grid(row=pos_y_stock_2, column=1)       



    label_bodega_stock_2 = Label(agregar_registro_stock, text='Bodega*')                                     # label con texto en el frame 
    label_bodega_stock_2.grid(row=pos_y_stock_2+1, column=0)                                      # se pone en el frame

    options_bodega_stock_2 = StringVar()
    options_bodega_stock_2.set('')
    dropdown_bodega_stock_2 = OptionMenu(agregar_registro_stock, options_bodega_stock_2, *bodegas_lista)
    dropdown_bodega_stock_2.grid(row=pos_y_stock_2+1, column=1)

    label_cantidad_stock_2 = Label(agregar_registro_stock, text='Stock*')                                     # label con texto en el frame 
    label_cantidad_stock_2.grid(row=pos_y_stock_2+2, column=0)                                      # se pone en el frame
    entry_cantidad_stock_2 = Entry(agregar_registro_stock)                            # caja para texto del nombre
    entry_cantidad_stock_2.grid(row=pos_y_stock_2+2, column=1)   

    label_cantidad_critica_stock_2 = Label(agregar_registro_stock, text='Stock crítico*')                                     # label con texto en el frame 
    label_cantidad_critica_stock_2.grid(row=pos_y_stock_2+3, column=0)                                      # se pone en el frame
    entry_cantidad_critica_stock_2 = Entry(agregar_registro_stock)                            # caja para texto del nombre
    entry_cantidad_critica_stock_2.grid(row=pos_y_stock_2+3, column=1)    

    def annadir_registro_stock_2():
        res = annadir_registro_stock_func(entry_id_stock_2.get(),
            options_bodega_stock_2.get(),
            entry_cantidad_stock_2.get(),
            entry_cantidad_critica_stock_2.get(),
            cur,
            conn
                )

        if(res == 1):
            label_annadir_output_stock_2['text'] = 'Registro añadido'
            label_annadir_output_stock_2['fg'] = color_exito
        elif(res == 0):
            label_annadir_output_stock_2['text'] = 'La bodega o el EPP no están en la base de dates, agruegelos antes de crear un registro nuevo'
            label_annadir_output_stock_2['fg'] = color_error
        elif(res == -2):
            label_annadir_output_stock_2['text'] = 'El registro ya se encuentra en la base de datos'
            label_annadir_output_stock_2['fg'] = color_error
        elif(res == -1):
            label_annadir_output_stock_2['text'] = 'No se pudo añadir el registro, por favor revisar que el formato esté correcto'
            label_annadir_output_stock_2['fg'] = color_error
        else:
            label_annadir_output_stock_2['text'] = 'Error inseperado'
            label_annadir_output_stock_2['fg'] = color_error

    boton_annadir_stock_2 = Button(agregar_registro_stock, text='Añadir registro de stock', command=annadir_registro_stock_2)   # botón para añadir empleado 
    boton_annadir_stock_2.grid(row=pos_y_stock_2+4, column=1)           # se posiciona el botón 

    label_annadir_output_stock_2 = Label(agregar_registro_stock, text='')
    label_annadir_output_stock_2.grid(row=pos_y_stock_2+4, column=2)  


    # fame para modificar stock y stock crítico

    modificar_stock = Frame(tabs_stock)     # se crea el tab
    tabs_stock.add(modificar_stock, text ='Agregar/Modificar stock')

    # _stock_3 por stock tab 3

    def selectID_stock_3(id,bodega):  # muestra la info del stock dando el id y bodega directamente
        lista = ['']*3         # lista para los 2 atributos
        res = ver_stock_id(id,bodega,cur,conn)   # se ejecuta la consulta
        try:                    # en un try por si algo falla
            lista[0] = res[2]   # nombre
            lista[1] = res[8]   # stock
            lista[2] = res[9]   # stock crítico 
        except:                     # si es que falla
            for i in range(0,3):    # se llena con strings vacíos
                lista[i] = ''
        for i in range(0,3):        # escribe el resultado de la consulta en los labels
            lista_output_stock_3[i]['text'] = lista[i]
            if lista[i] == None:    # si es un none se llena con un string vacío (se debe llenar con algo o si no queda el texto que estaba antes)
                lista_output_stock_3[i]['text'] = ''        

    def inputID_stock_3():      # muestra la info de un epp dando su identificador (rut o pasaporte)
        id = entry_id_stock_3.get()     # se obtiene id del entry
        bodega =options_bodega_input_stock_3.get()  # bodega seleccionada
        selectID_stock_3(id,bodega)

    def agregar_stock_3():
        id = entry_id_stock_3.get()
        bodega = options_bodega_input_stock_3.get()
        cantidad = entry_agregar_stock_3.get()
        try:    # en un try por si falla
            if(int(cantidad)>=0):   # si la cantidad es mayor a 0
                res = sumar_restar_epp(id,int(cantidad),bodega, cur, conn)   # se ejecuta la consulta
            else:
                res = -2    # error al poner un número menor a 0 
        except:     # si falla
            res = -1    # código de error
        
        if(res == 1):
            label_agregar_output_stock_3["text"] = 'Stock de EPP '+id+' en bodega '+ bodega +' actualizado correctamente'
            label_agregar_output_stock_3['fg'] = color_exito
            hacer_entrega(usuario_id, usuario_id, id, int(cantidad), bodega, 'Stock agregado manualmente', cur,conn) 
        elif(res == -1):
            label_agregar_output_stock_3["text"] = 'No se pudo actualizar el stock de EPP '+id+' en bodega '+ bodega +', asegurese que esté todo en el formato correcto o que esté en la base de datos'
            label_agregar_output_stock_3['fg'] = color_error
        elif(res == 0):
            label_agregar_output_stock_3["text"] = 'No se puede tener stock negativo en la base de datos'
            label_agregar_output_stock_3['fg'] = color_error
        elif(res == -2):
            label_agregar_output_stock_3["text"] = 'El número ingresado debe ser positvo'
            label_agregar_output_stock_3['fg'] = color_error
        else:
            label_agregar_output_stock_3["text"] = 'Error inseperado'
            label_agregar_output_stock_3['fg'] = color_error    
        
        inputID_stock_3()


    def quitar_stock_3():
        id = entry_id_stock_3.get()
        bodega = options_bodega_input_stock_3.get()
        cantidad = entry_quitar_stock_3.get()
        try:    # en un try por si falla
            if(int(cantidad)>=0):   # si la cantidad es mayor a 0
                res = sumar_restar_epp(id,-int(cantidad),bodega, cur, conn)   # se ejecuta la consulta
            else:
                res = -2    # error al poner un número menor a 0 
        except:     # si falla
            res = -1    # código de error
        
        if(res == 1):
            label_quitar_output_stock_3["text"] = 'Stock de EPP '+id+' en bodega '+ bodega +' actualizado correctamente'
            label_quitar_output_stock_3['fg'] = color_exito
            hacer_entrega(usuario_id, usuario_id, id, -int(cantidad), bodega, 'Stock quitado manualmente', cur,conn)

        elif(res == -1):
            label_quitar_output_stock_3["text"] = 'No se pudo actualizar el stock de EPP '+id+' en bodega '+ bodega +', asegurese que esté todo en el formato correcto o que esté en la base de datos'
            label_quitar_output_stock_3['fg'] = color_error
        elif(res == 0):
            label_quitar_output_stock_3["text"] = 'No se puede tener stock negativo en la base de datos'
            label_quitar_output_stock_3['fg'] = color_error
        elif(res == -2):
            label_quitar_output_stock_3["text"] = 'El número ingresado debe ser positvo'
            label_quitar_output_stock_3['fg'] = color_error
        else:
            label_quitar_output_stock_3["text"] = 'Error inseperado'
            label_quitar_output_stock_3['fg'] = color_error  

        inputID_stock_3()

    def modificar_stock_3():
        id = entry_id_stock_3.get()
        bodega = options_bodega_input_stock_3.get()
        cantidad = entry_modificar_stock_3.get()
        try:    # en un try por si falla
            if(int(cantidad)>=0):   # si la cantidad es mayor a 0
                cantidad_antigua = get_stock_id(id,bodega,cur,conn)[0]
                res = modificar_stock_epp(id,cantidad,bodega,cur,conn)   # se ejecuta la consulta
            else:
                res = -2    # error al poner un número menor a 0 
        except:     # si falla
            res = -1    # código de error
        
        if(res == 1):
            label_modificar_output_stock_3["text"] = 'Stock de EPP '+id+' en bodega '+ bodega +' actualizado correctamente'
            label_modificar_output_stock_3['fg'] = color_exito
            hacer_entrega(usuario_id, usuario_id, id, int(cantidad)-cantidad_antigua, bodega, 'Stock modificado manualmente', cur,conn) 

        elif(res == -1):
            label_modificar_output_stock_3["text"] = 'No se pudo actualizar el stock de EPP '+id+' en bodega '+ bodega +', asegurese que esté todo en el formato correcto o que esté en la base de datos'
            label_modificar_output_stock_3['fg'] = color_error
        elif(res == 0):
            label_modificar_output_stock_3["text"] = 'No se puede tener stock negativo en la base de datos'
            label_modificar_output_stock_3['fg'] = color_error
        elif(res == -2):
            label_modificar_output_stock_3["text"] = 'El número ingresado debe ser positvo'
            label_modificar_output_stock_3['fg'] = color_error
        else:
            label_modificar_output_stock_3["text"] = 'Error inseperado'
            label_modificar_output_stock_3['fg'] = color_error  
        
        inputID_stock_3()

    def modificar_stock_ctitico_3():
        id = entry_id_stock_3.get()
        bodega = options_bodega_input_stock_3.get()
        cantidad = entry_modificar_critica_stock_3.get()
        try:    # en un try por si falla
            if(int(cantidad)>=0):   # si la cantidad es mayor a 0
                res = modificar_stock_critico(id,cantidad,bodega,cur,conn)   # se ejecuta la consulta
            else:
                res = -2    # error al poner un número menor a 0 
        except:     # si falla
            res = -1    # código de error
        
        if(res == 1):
            label_modificar_critica_output_stock_3["text"] = 'Stock de EPP '+id+' en bodega '+ bodega +' actualizado correctamente'
            label_modificar_critica_output_stock_3['fg'] = color_exito
        elif(res == -1):
            label_modificar_critica_output_stock_3["text"] = 'No se pudo actualizar el stock de EPP '+id+' en bodega '+ bodega +', asegurese que esté todo en el formato correcto o que esté en la base de datos'
            label_modificar_critica_output_stock_3['fg'] = color_error
        elif(res == 0):
            label_modificar_critica_output_stock_3["text"] = 'No se puede tener stock negativo en la base de datos'
            label_modificar_critica_output_stock_3['fg'] = color_error
        elif(res == -2):
            label_modificar_critica_output_stock_3["text"] = 'El número ingresado debe ser positvo'
            label_modificar_critica_output_stock_3['fg'] = color_error
        else:
            label_modificar_critica_output_stock_3["text"] = 'Error inseperado'
            label_modificar_critica_output_stock_3['fg'] = color_error  
        
        inputID_stock_3()

    pos_y_stock_3 = 1

    
    # label info stock

    label_info_stock_3 = Label(modificar_stock, text = 'Ingrese código de producto y bodega:')
    label_info_stock_3.grid(row=0, column=0)

    # label id producto

    label_id_input_stock_3 = Label(modificar_stock, text = 'Código producto:')       # label con texto en el frame
    label_id_input_stock_3.grid(row=pos_y_stock_3, column=0)    # se posiciona
    entry_id_stock_3 =  Entry(modificar_stock)      # caja para escribir ID
    entry_id_stock_3.grid(row=pos_y_stock_3, column=1)          # se posiciona

    # label bodega

    label_bodega_input_stock_3 = Label(modificar_stock, text = 'Bodega:')       # label con texto en el frame
    label_bodega_input_stock_3.grid(row=pos_y_stock_3+1, column=0)    # se posiciona

    options_bodega_input_stock_3 = StringVar()
    options_bodega_input_stock_3.set('')
    dropdown_bodega_input_stock_3 = OptionMenu(modificar_stock, options_bodega_input_stock_3, *bodegas_lista)
    dropdown_bodega_input_stock_3.grid(row=pos_y_stock_3+1, column=1)

    # botón para ejecutar las busqueda

    boton_buscar_id_stock_3 = Button(modificar_stock, text='Buscar', command=inputID_stock_3)   # botón para ejecutar la busqueda
    boton_buscar_id_stock_3.grid(row=pos_y_stock_3,column=2)    # se ubica el botón en el frame

    # label nombre

    label_nombre_input_stock_3 = Label(modificar_stock, text='Nombre') # label con texto en el frame
    label_nombre_input_stock_3.grid(row=pos_y_stock_3+2, column=0)       # se posiciona

    label_nombre_output_stock_3 = Label(modificar_stock, text='')       # label con texto en el frame
    label_nombre_output_stock_3.grid(row=pos_y_stock_3+2, column=1)       # se posiciona

    # label cantidad

    label_cantidad_input_stock_3 = Label(modificar_stock, text='Cantidad') # label con texto en el frame
    label_cantidad_input_stock_3.grid(row=pos_y_stock_3+3, column=0)       # se posiciona

    label_cantidad_output_stock_3 = Label(modificar_stock, text='')       # label con texto en el frame
    label_cantidad_output_stock_3.grid(row=pos_y_stock_3+3, column=1)       # se posiciona
    
    # label cantidad crítica 

    label_cantidad_critica_input_stock_3 = Label(modificar_stock, text='Cantidad crítica') # label con texto en el frame
    label_cantidad_critica_input_stock_3.grid(row=pos_y_stock_3+4, column=0)       # se posiciona

    label_cantidad_critica_output_stock_3 = Label(modificar_stock, text='')       # label con texto en el frame
    label_cantidad_critica_output_stock_3.grid(row=pos_y_stock_3+4, column=1)       # se posiciona

    lista_output_stock_3 = [label_nombre_output_stock_3,
                            label_cantidad_output_stock_3,
                            label_cantidad_critica_output_stock_3]

    # espaceado

    label_space_stock_3 = Label(modificar_stock, text = '')
    label_space_stock_3.grid(row=pos_y_stock_3+5, column=0)


    # label info stock

    label_info_mod_stock_3 = Label(modificar_stock, text = 'Modifique stock:')
    label_info_mod_stock_3.grid(row=pos_y_stock_3+6, column=0)

    # agregar stock 
    
    label_agregar_stock_3 = Label(modificar_stock, text= 'Agregar stock:')
    label_agregar_stock_3.grid(row=pos_y_stock_3+7, column=0)

    entry_agregar_stock_3 = Entry(modificar_stock)
    entry_agregar_stock_3.grid(row=pos_y_stock_3+7, column=1)

    boton_agregar_stock_3 = Button(modificar_stock, text='Agregar', command=agregar_stock_3)
    boton_agregar_stock_3.grid(row=pos_y_stock_3+7, column=2)

    label_agregar_output_stock_3 = Label(modificar_stock, text='')
    label_agregar_output_stock_3.grid(row=pos_y_stock_3+7, column=3)

    # entry para quitar stock

    label_quitar_stock_3 = Label(modificar_stock, text= 'Quitar stock:')
    label_quitar_stock_3.grid(row=pos_y_stock_3+8, column=0)

    entry_quitar_stock_3 = Entry(modificar_stock)
    entry_quitar_stock_3.grid(row=pos_y_stock_3+8, column=1)

    boton_quitar_stock_3 = Button(modificar_stock, text='Quitar', command=quitar_stock_3)
    boton_quitar_stock_3.grid(row=pos_y_stock_3+8, column=2)

    label_quitar_output_stock_3 = Label(modificar_stock, text='')
    label_quitar_output_stock_3.grid(row=pos_y_stock_3+8, column=3)

    # entry para modificar stock 

    label_modificar_stock_3 = Label(modificar_stock, text= 'Modificar stock:')
    label_modificar_stock_3.grid(row=pos_y_stock_3+9, column=0)

    entry_modificar_stock_3 = Entry(modificar_stock)
    entry_modificar_stock_3.grid(row=pos_y_stock_3+9, column=1)

    boton_modificar_stock_3 = Button(modificar_stock, text='Modificar', command=modificar_stock_3)
    boton_modificar_stock_3.grid(row=pos_y_stock_3+9, column=2)

    label_modificar_output_stock_3 = Label(modificar_stock, text='')
    label_modificar_output_stock_3.grid(row=pos_y_stock_3+9, column=3)

    # espaceado

    label_space_1_stock_3 = Label(modificar_stock, text = '')
    label_space_1_stock_3.grid(row=pos_y_stock_3+10, column=0)

    # label info stock

    label_info_mod_stock_critico_3 = Label(modificar_stock, text = 'Modifique stock crítico:')
    label_info_mod_stock_critico_3.grid(row=pos_y_stock_3+11, column=0)

    # entry para moficiar stock crítica 

    label_modificar_critica_stock_3 = Label(modificar_stock, text= 'Modificar stock crítico:')
    label_modificar_critica_stock_3.grid(row=pos_y_stock_3+12, column=0)

    entry_modificar_critica_stock_3 = Entry(modificar_stock)
    entry_modificar_critica_stock_3.grid(row=pos_y_stock_3+12, column=1)

    boton_modificar_critica_stock_3 = Button(modificar_stock, text='Modificar', command=modificar_stock_ctitico_3)
    boton_modificar_critica_stock_3.grid(row=pos_y_stock_3+12, column=2)

    label_modificar_critica_output_stock_3 = Label(modificar_stock, text='')
    label_modificar_critica_output_stock_3.grid(row=pos_y_stock_3+12, column=3)  

    def confirmar_eliminar_stock_3(eleccion,id,bodega):
        popup_eliminar_stock_3.destroy()           # se elimina la ventana
        if(eleccion):                                   # si se dijo que si 
            res = eliminar_registro_stock(id,bodega,cur,conn)         # se elimina el empleado
            if(res == 1):
                label_eliminado_stock_3['text'] = 'Se eliminó el registro EPP '+id+' y bodega '+ bodega+' de la base de datos'
                label_eliminado_stock_3['fg'] = color_exito
            elif(res == -1):
                label_eliminado_stock_3['text'] = 'No se pudo eliminar el registro EPP '+id+' y bodega '+ bodega+' de la base de datos'
                label_eliminado_stock_3['fg'] = color_error

        elif(not eleccion):                             # si se dijo que no, no se elimina
            label_eliminado_stock_3['text'] = 'No se ha eliminado el registro EPP '+id+' y bodega '+ bodega+' de la base de datos'
            label_eliminado_stock_3['fg'] = color_exito

    def eliminar_registro_stock_3():    # función al apretar el botón eliminar
        id = entry_id_stock_3.get()     # se obtiene el id del campo
        id = id.strip()

        bodega = options_bodega_input_stock_3.get() # bodega

        res = registro_stock_en_db(id,bodega,cur,conn)    # se revisa si está en la base de datos
        if res == 1:                            # si es qu está
            global popup_eliminar_stock_3  # global para poder ser llamada desde la funcíon de arriba
            popup_eliminar_stock_3 = Toplevel(root)    # se crea la ventana
            popup_eliminar_stock_3.title('Confimración de eliminar empleado')  #   titulo y dimensiones
            popup_eliminar_stock_3.geometry('350x100')

            pop_label_stock_3 = Label(popup_eliminar_stock_3, text='¿Desea eliminar el registro EPP ' + id +' con bodega '+bodega+' de las base de datos?')  # label para el texto
            pop_label_stock_3.pack(pady=10)

            pop_frame_stock_3 = Frame(popup_eliminar_stock_3)  # frame para los botones
            pop_frame_stock_3.pack(pady =5)

            boton_si_stock_3 = Button(pop_frame_stock_3, text='Sí', fg=color_error, command=lambda: confirmar_eliminar_stock_3(True,id,bodega)) #   boton para confirmar la eliminación
            boton_si_stock_3.grid(row=0,column=0,padx=10)

            boton_no_stock_3 = Button(pop_frame_stock_3, text='No', command=lambda: confirmar_eliminar_stock_3(False,id,bodega))   # boton para desconfirmar la eliminación 
            boton_no_stock_3.grid(row=0,column=1,padx=10)

            label_eliminado_stock_3['text'] = 'Confirme en la ventana que apareció'  # dice para que el usuario sepa que debe confirmar en la pantalla
            label_eliminado_stock_3['fg'] = color_exito
        elif res == 0:                                                  # si no lo encuentra
            label_eliminado_stock_3['text'] = 'No se econtró un registro con el EPP '+id+' y bodega '+bodega+' en la base de datos'
            label_eliminado_stock_3['fg'] = color_error
        elif res == -1:                                                 # está mal el formato 
            label_eliminado_stock_3['text'] = 'Asegurese de que el registro esté en el formato correcto'
            label_eliminado_stock_3['fg'] = color_error


    boton_eliminar_stock_3 = Button(modificar_stock, text='Eliminar', fg=color_error, command=eliminar_registro_stock_3)
    boton_eliminar_stock_3.grid(row=pos_y_stock_3+13, column=0)

    label_eliminado_stock_3 = Label(modificar_stock, text='')    # dice el status de la eliminación
    label_eliminado_stock_3.grid(row=pos_y_stock_3+14, column=1)

    # tabs entrega  ////////////////////////////////////////

    tabs_entrega = ttk.Notebook(frame_entregas)     # tabs de los empleados
    tabs_entrega.pack()                             # se ubica en el frame de epp

    ## frame para hacer entregas ////////////////////////////////////////    

    realizar_entrega = Frame(tabs_entrega)     # se crea y se le da como padre las tabs de entregas
    tabs_entrega.add(realizar_entrega, text='Realizar entrega')

    info_usuario = ver_empleado_id(usuario_id,cur,conn)    # se obtiene la info del usuario

    pos_y_entrega_1 = 1

    def select_empleado_entrega_1():
        empleado = ver_empleado_id(entry_empleado_id_entrega_1.get(),cur,conn)
        if(empleado == None):
            label_empleado_nombre_entrega_output_1['text'] = ''
            label_empleado_apellido_entrega_output_1['text'] = ''
            label_empleado_vigencia_entrega_output_1['text'] = ''
            label_empleado_gerencia_entrega_output_1['text'] = ''
            label_empleado_departamento_entrega_output_1['text'] = ''
            label_empleado_seccion_entrega_output_1['text'] = ''
            label_empleado_fecha_entrega_output_1['text'] = ''
            label_empleado_cargo_entrega_output_1['text'] = ''
        else:
            label_empleado_nombre_entrega_output_1['text'] = empleado[1]
            label_empleado_apellido_entrega_output_1['text'] = empleado[4]
            label_empleado_vigencia_entrega_output_1['text'] = empleado[6]
            label_empleado_gerencia_entrega_output_1['text'] = empleado[7]
            label_empleado_departamento_entrega_output_1['text'] = empleado[8]
            label_empleado_seccion_entrega_output_1['text'] = empleado[9]
            label_empleado_fecha_entrega_output_1['text'] = empleado[10]
            label_empleado_cargo_entrega_output_1['text'] = empleado[11]

    def select_stock_entrega_1():
        stock = ver_stock_id(entry_epp_id_entrega_1.get(),options_bodega_input_entrega_1.get(),cur,conn)
        if(stock == None):
            for i in range(0,10):
                lista_output_stock_entrega_1[i]['text'] = ''  # se llena
        else:
            for i in range(0,10):
                lista_output_stock_entrega_1[i]['text'] = stock[i]  # se llena


            if(stock[8]<=stock[9]):
                lista_output_stock_entrega_1[8]['fg'] = color_error
            else:
                lista_output_stock_entrega_1[8]['fg'] = color_exito  


            


        

    # info

    label_info_user_entrega_1 = Label(realizar_entrega,text='Información del usuario:')
    label_info_user_entrega_1.grid(row=0,column=0)

    label_info_empleado_entrega_1 = Label(realizar_entrega,text='Información del empleado:')
    label_info_empleado_entrega_1.grid(row=0,column=2)

    boton_empleado_entrega_1 = Button(realizar_entrega, text='Seleccionar', command=select_empleado_entrega_1)
    boton_empleado_entrega_1.grid(row=1,column=4)
    # user

    # id
    label_user_id_entrega_1 = Label(realizar_entrega, text='ID:')
    label_user_id_entrega_1.grid(row=pos_y_entrega_1,column=0)

    label_user_id_entrega_output_1 = Label(realizar_entrega, text=info_usuario[0])
    label_user_id_entrega_output_1.grid(row=pos_y_entrega_1,column=1)

    # nombre
    label_user_nombre_entrega_1 = Label(realizar_entrega, text='Nombre:')
    label_user_nombre_entrega_1.grid(row=pos_y_entrega_1+1,column=0)

    label_user_nombre_entrega_output_1 = Label(realizar_entrega, text=info_usuario[1])
    label_user_nombre_entrega_output_1.grid(row=pos_y_entrega_1+1,column=1)

    # apellido
    label_user_apellido_entrega_1 = Label(realizar_entrega, text='Apellido:')
    label_user_apellido_entrega_1.grid(row=pos_y_entrega_1+2,column=0)

    label_user_apellido_entrega_output_1 = Label(realizar_entrega, text=info_usuario[4])
    label_user_apellido_entrega_output_1.grid(row=pos_y_entrega_1+2,column=1)

    # vigencia
    label_user_vigencia_entrega_1 = Label(realizar_entrega, text='Vigencia:')
    label_user_vigencia_entrega_1.grid(row=pos_y_entrega_1+3,column=0)

    label_user_vigencia_entrega_output_1 = Label(realizar_entrega, text=info_usuario[6])
    label_user_vigencia_entrega_output_1.grid(row=pos_y_entrega_1+3,column=1)

    # gerencia
    label_user_gerencia_entrega_1 = Label(realizar_entrega, text='Gerencia:')
    label_user_gerencia_entrega_1.grid(row=pos_y_entrega_1+4,column=0)

    label_user_gerencia_entrega_output_1 = Label(realizar_entrega, text=info_usuario[7])
    label_user_gerencia_entrega_output_1.grid(row=pos_y_entrega_1+4,column=1)

    # deartamento
    label_user_departamento_entrega_1 = Label(realizar_entrega, text='Departamento:')
    label_user_departamento_entrega_1.grid(row=pos_y_entrega_1+5,column=0)

    label_user_departamento_entrega_output_1 = Label(realizar_entrega, text=info_usuario[8])
    label_user_departamento_entrega_output_1.grid(row=pos_y_entrega_1+5,column=1)

    # sección
    label_user_seccion_entrega_1 = Label(realizar_entrega, text='Sección:')
    label_user_seccion_entrega_1.grid(row=pos_y_entrega_1+6,column=0)

    label_user_seccion_entrega_output_1 = Label(realizar_entrega, text=info_usuario[9])
    label_user_seccion_entrega_output_1.grid(row=pos_y_entrega_1+6,column=1)

    # fecha
    label_user_fecha_entrega_1 = Label(realizar_entrega, text='Fecha:')
    label_user_fecha_entrega_1.grid(row=pos_y_entrega_1+7,column=0)

    label_user_fecha_entrega_output_1 = Label(realizar_entrega, text=info_usuario[10])
    label_user_fecha_entrega_output_1.grid(row=pos_y_entrega_1+7,column=1)

    # cargo
    label_user_cargo_entrega_1 = Label(realizar_entrega, text='Cargo:')
    label_user_cargo_entrega_1.grid(row=pos_y_entrega_1+8,column=0)

    label_user_cargo_entrega_output_1 = Label(realizar_entrega, text=info_usuario[11])
    label_user_cargo_entrega_output_1.grid(row=pos_y_entrega_1+8,column=1)

    # empleado

    # id
    label_empleado_id_entrega_1 = Label(realizar_entrega, text='ID:')
    label_empleado_id_entrega_1.grid(row=pos_y_entrega_1,column=2)

    entry_empleado_id_entrega_1 = Entry(realizar_entrega)
    entry_empleado_id_entrega_1.grid(row=pos_y_entrega_1,column=3)

    # nombre
    label_empleado_nombre_entrega_1 = Label(realizar_entrega, text='Nombre:')
    label_empleado_nombre_entrega_1.grid(row=pos_y_entrega_1+1,column=2)

    label_empleado_nombre_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_nombre_entrega_output_1.grid(row=pos_y_entrega_1+1,column=3)

    # apellido
    label_empleado_apellido_entrega_1 = Label(realizar_entrega, text='Apellido:')
    label_empleado_apellido_entrega_1.grid(row=pos_y_entrega_1+2,column=2)

    label_empleado_apellido_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_apellido_entrega_output_1.grid(row=pos_y_entrega_1+2,column=3)

    # vigencia
    label_empleado_vigencia_entrega_1 = Label(realizar_entrega, text='Vigencia:')
    label_empleado_vigencia_entrega_1.grid(row=pos_y_entrega_1+3,column=2)

    label_empleado_vigencia_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_vigencia_entrega_output_1.grid(row=pos_y_entrega_1+3,column=3)

    # gerencia
    label_empleado_gerencia_entrega_1 = Label(realizar_entrega, text='Gerencia:')
    label_empleado_gerencia_entrega_1.grid(row=pos_y_entrega_1+4,column=2)

    label_empleado_gerencia_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_gerencia_entrega_output_1.grid(row=pos_y_entrega_1+4,column=3)

    # deartamento
    label_empleado_departamento_entrega_1 = Label(realizar_entrega, text='Departamento:')
    label_empleado_departamento_entrega_1.grid(row=pos_y_entrega_1+5,column=2)

    label_empleado_departamento_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_departamento_entrega_output_1.grid(row=pos_y_entrega_1+5,column=3)

    # sección
    label_empleado_seccion_entrega_1 = Label(realizar_entrega, text='Sección:')
    label_empleado_seccion_entrega_1.grid(row=pos_y_entrega_1+6,column=2)

    label_empleado_seccion_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_seccion_entrega_output_1.grid(row=pos_y_entrega_1+6,column=3)

    # fecha
    label_empleado_fecha_entrega_1 = Label(realizar_entrega, text='Fecha:')
    label_empleado_fecha_entrega_1.grid(row=pos_y_entrega_1+7,column=2)

    label_empleado_fecha_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_fecha_entrega_output_1.grid(row=pos_y_entrega_1+7,column=3)

    # cargo
    label_empleado_cargo_entrega_1 = Label(realizar_entrega, text='Cargo:')
    label_empleado_cargo_entrega_1.grid(row=pos_y_entrega_1+8,column=2)

    label_empleado_cargo_entrega_output_1 = Label(realizar_entrega, text='')
    label_empleado_cargo_entrega_output_1.grid(row=pos_y_entrega_1+8,column=3)

    # stock 
    
    label_info_stock_entrega_1 = Label(realizar_entrega,text='Información del stock:')
    label_info_stock_entrega_1.grid(row=pos_y_entrega_1+9,column=0)

    # id
    label_epp_id_entrega_1 = Label(realizar_entrega, text='ID:')
    label_epp_id_entrega_1.grid(row=pos_y_entrega_1+10,column=0)

    entry_epp_id_entrega_1 = Entry(realizar_entrega)
    entry_epp_id_entrega_1.grid(row=pos_y_entrega_1+10,column=1)

    boton_buscar_stock_entrega_1 = Button(realizar_entrega, text='Seleccionar', command=select_stock_entrega_1)         # botón para ejecutar la busqueda
    boton_buscar_stock_entrega_1.grid(row=pos_y_entrega_1+10, column=2)                                   # se ubica el botón en el frame

    # opciones bodega

    label_bodega_input_entrega_1 = Label(realizar_entrega, text='Bodega:') # label con texto en el frame 
    label_bodega_input_entrega_1.grid(row=pos_y_entrega_1+11,column=0)

    # opciones bodega

    options_bodega_input_entrega_1 = StringVar()
    options_bodega_input_entrega_1.set('')

    dropdown_bodega_input_entrega_1 = OptionMenu(realizar_entrega,options_bodega_input_entrega_1, *bodegas_lista)
    dropdown_bodega_input_entrega_1.grid(row=pos_y_entrega_1+11,column=1)


    # labels con los resultados de la busqueda
    
    label_id_entrega_1 = Label(realizar_entrega, text='Código de producto:')                                     # label con texto en el frame 
    label_id_entrega_1.grid(row=pos_y_entrega_1+12, column=0)                                      # se pone en el frame
    label_id_output_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_id_output_entrega_1.grid(row=pos_y_entrega_1+12, column=1)                               # se pone en el frame

    label_c_c_entrega_1 = Label(realizar_entrega, text='Código de constructor:')                                     # label con texto en el frame 
    label_c_c_entrega_1.grid(row=pos_y_entrega_1+13, column=0)                                      # se pone en el frame
    label_c_c_output_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_c_c_output_entrega_1.grid(row=pos_y_entrega_1+13, column=1)                               # se pone en el frame

    label_nombre_entrega_1 = Label(realizar_entrega, text='Nombre:')                                     # label con texto en el frame 
    label_nombre_entrega_1.grid(row=pos_y_entrega_1+14, column=0)                                      # se pone en el frame
    label_nombre_output_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_nombre_output_entrega_1.grid(row=pos_y_entrega_1+14, column=1)    

    label_constructor_designado_entrega_1 = Label(realizar_entrega, text='Constructor designado:')                                     # label con texto en el frame 
    label_constructor_designado_entrega_1.grid(row=pos_y_entrega_1+15, column=0)                                      # se pone en el frame
    label_constructor_designado_output_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_constructor_designado_output_entrega_1.grid(row=pos_y_entrega_1+15, column=1) 

    label_talla_stock_entrega_1 = Label(realizar_entrega, text='Talla:')                                     # label con texto en el frame 
    label_talla_stock_entrega_1.grid(row=pos_y_entrega_1+16, column=0)                                      # se pone en el frame
    label_talla_output_stock_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_talla_output_stock_entrega_1.grid(row=pos_y_entrega_1+16, column=1) 

    label_UM_stock_entrega_1 = Label(realizar_entrega, text='Unidad de medición:')                                     # label con texto en el frame 
    label_UM_stock_entrega_1.grid(row=pos_y_entrega_1+17, column=0)                                      # se pone en el frame
    label_UM_output_stock_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_UM_output_stock_entrega_1.grid(row=pos_y_entrega_1+17, column=1) 

    label_precio_stock_entrega_1 = Label(realizar_entrega, text='Precio:')                                     # label con texto en el frame 
    label_precio_stock_entrega_1.grid(row=pos_y_entrega_1+18, column=0)                                      # se pone en el frame
    label_precio_output_stock_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_precio_output_stock_entrega_1.grid(row=pos_y_entrega_1+18, column=1) 

    label_bodega_stock_entrega_1 = Label(realizar_entrega, text='Bodega:')                                     # label con texto en el frame 
    label_bodega_stock_entrega_1.grid(row=pos_y_entrega_1+19, column=0)                                      # se pone en el frame
    label_bodega_output_stock_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_bodega_output_stock_entrega_1.grid(row=pos_y_entrega_1+19, column=1) 

    label_cantidad_stock_entrega_1 = Label(realizar_entrega, text='Cantidad:')                                     # label con texto en el frame 
    label_cantidad_stock_entrega_1.grid(row=pos_y_entrega_1+20, column=0)                                      # se pone en el frame
    label_cantidad_output_stock_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_cantidad_output_stock_entrega_1.grid(row=pos_y_entrega_1+20, column=1) 

    label_cantidad_critica_stock_entrega_1 = Label(realizar_entrega, text='Cantidad crítica:')                                     # label con texto en el frame 
    label_cantidad_critica_stock_entrega_1.grid(row=pos_y_entrega_1+21, column=0)                                      # se pone en el frame
    label_cantidad_critica_output_stock_entrega_1 = Label(realizar_entrega, text='')                                 # label con texto en el frame 
    label_cantidad_critica_output_stock_entrega_1.grid(row=pos_y_entrega_1+21, column=1) 


    # lista con las labels de output con la información
    lista_output_stock_entrega_1 = [
                    label_c_c_output_entrega_1,
                    label_id_output_entrega_1,
                    label_nombre_output_entrega_1,
                    label_constructor_designado_output_entrega_1,
                    label_talla_output_stock_entrega_1,
                    label_UM_output_stock_entrega_1,
                    label_precio_output_stock_entrega_1,
                    label_bodega_output_stock_entrega_1,
                    label_cantidad_output_stock_entrega_1,
                    label_cantidad_critica_output_stock_entrega_1
                ]

    

    label_info_cantidad_entrega_1 = Label(realizar_entrega, text = 'Decida cantidad que sale o entra de la bodega:')
    label_info_cantidad_entrega_1.grid(row=pos_y_entrega_1+9,column=3)

    # si entra o sale 

    label_entra_sale_entrega_1 = Label(realizar_entrega, text = 'EPP entra o sale:')
    label_entra_sale_entrega_1.grid(row=pos_y_entrega_1+10,column=3)

    options_entra_sale_entrega_1 = StringVar()
    options_entra_sale_entrega_1.set('')
    dropdown_entra_sale_stock_3 = OptionMenu(realizar_entrega, options_entra_sale_entrega_1, 'ENTRA A BODEGA', 'SALE DE BODEGA')
    dropdown_entra_sale_stock_3.grid(row=pos_y_entrega_1+10,column=4)    

    # cantidad 

    label_cantidad_entrega_1 = Label(realizar_entrega, text = 'Cantidad de EPP:')
    label_cantidad_entrega_1.grid(row=pos_y_entrega_1+11,column=3)    
    entry_cantidad_entrega_1 = Entry(realizar_entrega)
    entry_cantidad_entrega_1.grid(row=pos_y_entrega_1+11,column=4) 

    # razón 

    label_razon_entrega_1 = Label(realizar_entrega, text = 'Razón:')
    label_razon_entrega_1.grid(row=pos_y_entrega_1+12,column=3)    
    entry_razon_entrega_1 = Entry(realizar_entrega)
    entry_razon_entrega_1.grid(row=pos_y_entrega_1+12,column=4) 

    # función para transacción

    def realizar_transaccion_entrega_1():
        res = None
        res1 = None
        try:
            numero = int(entry_cantidad_entrega_1.get())
            if(numero<0):
                res = -2
            else:
                if(options_entra_sale_entrega_1.get() == 'ENTRA A BODEGA'):
                    res = sumar_restar_epp(entry_epp_id_entrega_1.get(),int(entry_cantidad_entrega_1.get()),options_bodega_input_entrega_1.get(),cur,conn)
                    if(res == 1):
                        res1 = hacer_entrega(usuario_id,entry_empleado_id_entrega_1.get(),entry_epp_id_entrega_1.get(),numero,options_bodega_input_entrega_1.get(),entry_razon_entrega_1.get(),cur,conn)

                elif(options_entra_sale_entrega_1.get() == 'SALE DE BODEGA'):
                    res = sumar_restar_epp(entry_epp_id_entrega_1.get(),-int(entry_cantidad_entrega_1.get()),options_bodega_input_entrega_1.get(),cur,conn)
                    if(res == 1):
                        res1 = hacer_entrega(usuario_id,entry_empleado_id_entrega_1.get(),entry_epp_id_entrega_1.get(),-numero,options_bodega_input_entrega_1.get(),entry_razon_entrega_1.get(),cur,conn)
                else:
                    return -3
        except:
            res = -1

        
        if(res == 1 and res1 == 1):
            label_status_transaccion_entrega_1['text'] = 'Transacción realizada'
            label_status_transaccion_entrega_1['fg'] = color_exito
        elif(res == 0):
            label_status_transaccion_entrega_1['text'] = 'No hay stock suficiente para realizar la transacción'
            label_status_transaccion_entrega_1['fg'] = color_error
        elif(res == -2):
            label_status_transaccion_entrega_1['text'] = 'La cantidad debe ser un entero positivo'
            label_status_transaccion_entrega_1['fg'] = color_error  
        elif(res == -3):
            label_status_transaccion_entrega_1['text'] = 'Porfavor elegir una bodega'
            label_status_transaccion_entrega_1['fg'] = color_error  
        elif(res == -1):
            label_status_transaccion_entrega_1['text'] = 'No se pudo hacer la transacción, por favor revisar que el formato esté correcto'
            label_status_transaccion_entrega_1['fg'] = color_error  
        else:
            label_status_transaccion_entrega_1['text'] = 'Error inserperado'
            label_status_transaccion_entrega_1['fg'] = color_error  

        select_stock_entrega_1()  # se actualiza el stock en tiempo real

            

    # botón para trnasacción

    boton_realizar_transaccion = Button(realizar_entrega, text='Realizar transacción', command=realizar_transaccion_entrega_1)
    boton_realizar_transaccion.grid(row=pos_y_entrega_1+13,column=3) 

    label_status_transaccion_entrega_1 = Label(realizar_entrega, text='')
    label_status_transaccion_entrega_1.grid(row=pos_y_entrega_1+14,column=3) 

    ## frame para ver entregas ////////////////////////////////////////    

    buscar_entregas = Frame(tabs_entrega)     # se crea y se le da como padre las tabs de entregas
    tabs_entrega.add(buscar_entregas, text='Buscar')

    entregas = ver_todas_las_entregas_func(cur,conn)


    def filtrar_entrega_2():
        delete_listbox_entregra_2() # se borra la listbox para poner le contenido nuevo 
        entregas =  ver_entregas(entry_usuario_id_filtro_entrega_output_2.get(), entry_empleado_id_filtro_entrega_output_2.get(), entry_epp_id_filtro_entrega_output_2.get(), options_bodega_filtro_entrega_2.get(), label_antes_filtro_entrega_output_2.get(), label_despues_filtro_entrega_output_2.get(), options_orden_entrega_2.get(), cur, conn) 

        try:
            for entrega in entregas:
                listbox_entregas_2.insert(END,entrega)
        except:
            pass


    # info usuarios

    label_info_usuario = Label(buscar_entregas, text='Info del usuario:')    
    label_info_usuario.grid(row=0,column=0) 

    # id
    label_usuario_id_entrega_2 = Label(buscar_entregas, text='ID:')
    label_usuario_id_entrega_2.grid(row=1,column=0)

    label_usuario_id_entrega_output_2 = Label(buscar_entregas, text='')
    label_usuario_id_entrega_output_2.grid(row=1,column=1)

    # nombre
    label_usuario_nombre_entrega_2 = Label(buscar_entregas, text='Nombre:')
    label_usuario_nombre_entrega_2.grid(row=2,column=0)

    label_usuario_nombre_entrega_output_2 = Label(buscar_entregas, text='')
    label_usuario_nombre_entrega_output_2.grid(row=2,column=1)

    # apellido
    label_usuario_apellido_entrega_2 = Label(buscar_entregas, text='Apellido:')
    label_usuario_apellido_entrega_2.grid(row=3,column=0)

    label_usuario_apellido_entrega_output_2 = Label(buscar_entregas, text='')
    label_usuario_apellido_entrega_output_2.grid(row=3,column=1)

    # vigencia
    label_usuario_vigencia_entrega_2 = Label(buscar_entregas, text='Vigencia:')
    label_usuario_vigencia_entrega_2.grid(row=4,column=0)

    label_usuario_vigencia_entrega_output_2 = Label(buscar_entregas, text='')
    label_usuario_vigencia_entrega_output_2.grid(row=4,column=1) 

    # info empleado

    label_info_empleado = Label(buscar_entregas, text='Info del empleado:')    
    label_info_empleado.grid(row=5,column=0) 

    # id
    label_empleado_id_entrega_2 = Label(buscar_entregas, text='ID:')
    label_empleado_id_entrega_2.grid(row=6,column=0)

    label_empleado_id_entrega_output_2 = Label(buscar_entregas, text='')
    label_empleado_id_entrega_output_2.grid(row=6,column=1)

    # nombre
    label_empleado_nombre_entrega_2 = Label(buscar_entregas, text='Nombre:')
    label_empleado_nombre_entrega_2.grid(row=7,column=0)

    label_empleado_nombre_entrega_output_2 = Label(buscar_entregas, text='')
    label_empleado_nombre_entrega_output_2.grid(row=7,column=1)

    # apellido
    label_empleado_apellido_entrega_2 = Label(buscar_entregas, text='Apellido:')
    label_empleado_apellido_entrega_2.grid(row=8,column=0)

    label_empleado_apellido_entrega_output_2 = Label(buscar_entregas, text='')
    label_empleado_apellido_entrega_output_2.grid(row=8,column=1)

    # vigencia
    label_empleado_vigencia_entrega_2 = Label(buscar_entregas, text='Vigencia:')
    label_empleado_vigencia_entrega_2.grid(row=9,column=0)

    label_empleado_vigencia_entrega_output_2 = Label(buscar_entregas, text='')
    label_empleado_vigencia_entrega_output_2.grid(row=9,column=1)    

    # info epp

    label_info_epp_entrega_2 = Label(buscar_entregas, text='Info del EPP:')    
    label_info_epp_entrega_2.grid(row=10,column=0) 

    # id
    label_epp_id_entrega_2 = Label(buscar_entregas, text='ID:')
    label_epp_id_entrega_2.grid(row=11,column=0)

    label_epp_id_entrega_output_2 = Label(buscar_entregas, text='')
    label_epp_id_entrega_output_2.grid(row=11,column=1)

    # nombre
    label_epp_nombre_entrega_2 = Label(buscar_entregas, text='Nombre:')
    label_epp_nombre_entrega_2.grid(row=12,column=0)

    label_epp_nombre_entrega_output_2 = Label(buscar_entregas, text='')
    label_epp_nombre_entrega_output_2.grid(row=12,column=1)

    # bodega 
    label_bodega_entrega_2 = Label(buscar_entregas, text='Bodega')
    label_bodega_entrega_2.grid(row=13,column=0)

    label_bodega_entrega_output_2 = Label(buscar_entregas, text='')
    label_bodega_entrega_output_2.grid(row=13,column=1)

    # precio unitario
    label_precio_unitario_entrega_2 = Label(buscar_entregas, text='Precio Unitario')
    label_precio_unitario_entrega_2.grid(row=14,column=0)

    label_precio_unitario_entrega_output_2 = Label(buscar_entregas, text='')
    label_precio_unitario_entrega_output_2.grid(row=14,column=1)

    # cantidad
    label_cantidad_entrega_2 = Label(buscar_entregas, text='Cantidad')
    label_cantidad_entrega_2.grid(row=15,column=0)

    label_cantidad_entrega_output_2 = Label(buscar_entregas, text='')
    label_cantidad_entrega_output_2.grid(row=15,column=1)

    # precio total
    label_precio_total_entrega_2 = Label(buscar_entregas, text='Precio Total')
    label_precio_total_entrega_2.grid(row=16,column=0)

    label_precio_total_entrega_output_2 = Label(buscar_entregas, text='')
    label_precio_total_entrega_output_2.grid(row=16,column=1)

    # fecha
    label_fecha_entrega_2 = Label(buscar_entregas, text='Fecha')
    label_fecha_entrega_2.grid(row=17,column=0)

    label_fecha_entrega_output_2 = Label(buscar_entregas, text='')
    label_fecha_entrega_output_2.grid(row=17,column=1)

    # razón
    label_razon_entrega_2 = Label(buscar_entregas, text='Razón')
    label_razon_entrega_2.grid(row=18,column=0)

    label_razon_entrega_output_2 = Label(buscar_entregas, text='')
    label_razon_entrega_output_2.grid(row=18,column=1)

    # filtros

    lista_output_entrega_2 = [
                        label_usuario_id_entrega_output_2,
                        label_usuario_nombre_entrega_output_2,
                        label_usuario_apellido_entrega_output_2,
                        label_usuario_vigencia_entrega_output_2,
                        label_empleado_id_entrega_output_2,
                        label_empleado_nombre_entrega_output_2,
                        label_empleado_apellido_entrega_output_2,
                        label_empleado_vigencia_entrega_output_2,
                        label_epp_id_entrega_output_2,
                        label_epp_nombre_entrega_output_2,
                        label_bodega_entrega_output_2,
                        label_precio_unitario_entrega_output_2,
                        label_cantidad_entrega_output_2,
                        label_precio_total_entrega_output_2,
                        label_fecha_entrega_output_2,
                        label_razon_entrega_output_2
    ]

    ## filtros

    label_flitro_info_entrega_2 = Label(buscar_entregas, text='Filtros')
    label_flitro_info_entrega_2.grid(row=0,column=3)

    # id usuario

    label_usuario_id_filtro_entrega_2 = Label(buscar_entregas, text='ID Usuario:')
    label_usuario_id_filtro_entrega_2.grid(row=1,column=3)

    entry_usuario_id_filtro_entrega_output_2 = Entry(buscar_entregas)
    entry_usuario_id_filtro_entrega_output_2.grid(row=1,column=4)

    # botón filtrar
    
    boton_filtrar_entrega_2 = Button(buscar_entregas, text='Filtrar', command=filtrar_entrega_2)    # botón para relizar la busqueda
    boton_filtrar_entrega_2.grid(row =1, column=5)

    # id empleado

    label_empleado_id_filtro_entrega_2 = Label(buscar_entregas, text='ID Empleado:')
    label_empleado_id_filtro_entrega_2.grid(row=2,column=3)

    entry_empleado_id_filtro_entrega_output_2 = Entry(buscar_entregas)
    entry_empleado_id_filtro_entrega_output_2.grid(row=2,column=4)

    # id epp

    label_epp_id_filtro_entrega_2 = Label(buscar_entregas, text='ID EPP:')
    label_epp_id_filtro_entrega_2.grid(row=3,column=3)

    entry_epp_id_filtro_entrega_output_2 = Entry(buscar_entregas)
    entry_epp_id_filtro_entrega_output_2.grid(row=3,column=4)

    # bodega

    label_bodega_id_filtro_entrega_2 = Label(buscar_entregas, text='Bodega:')
    label_bodega_id_filtro_entrega_2.grid(row=4,column=3)

    options_bodega_filtro_entrega_2 = StringVar()
    options_bodega_filtro_entrega_2.set('')
    dropdown_bodega_filtro_entrega_2 = OptionMenu(buscar_entregas, options_bodega_filtro_entrega_2, *bodegas_lista)
    dropdown_bodega_filtro_entrega_2.grid(row=4,column=4)

    # antes de 

    label_antes_filtro_entrega_2 = Label(buscar_entregas, text = 'Antes de:')
    label_antes_filtro_entrega_2.grid(row=5,column=3)

    label_antes_filtro_entrega_output_2 = Entry(buscar_entregas)
    label_antes_filtro_entrega_output_2.grid(row=5,column=4)

    # después de 

    label_despues_filtro_entrega_2 = Label(buscar_entregas, text = 'Después de:')
    label_despues_filtro_entrega_2.grid(row=6,column=3)

    label_despues_filtro_entrega_output_2 = Entry(buscar_entregas)
    label_despues_filtro_entrega_output_2.grid(row=6,column=4)


    # orden de filtro

    label_orden_filtro_entrega_2 = Label(buscar_entregas, text='Orden de entregas')
    label_orden_filtro_entrega_2.grid(row=7,column=3)

    options_orden_entrega_2 = StringVar()
    options_orden_entrega_2.set('Fecha descendiente')
    dropdown_orden_entrega_2 = OptionMenu(buscar_entregas, options_orden_entrega_2, 'Fecha ascendiente', 'Fecha descendiente', 'Precio ascendiente', 'Precio descendiente', 'Precio total ascendiente', 'Precio total descendiente')
    dropdown_orden_entrega_2.grid(row=7,column=4)


    listbox_entregas_2 = Listbox(buscar_entregas, width=180, height=10) # se crea una listbox que muestra los epps
    listbox_entregas_2.grid(row=19, columnspan=14, sticky= W+E)      # se posiciona la listbox

    for entrega in entregas:             # se rellena la listbox con los epps
        listbox_entregas_2.insert(END, entrega)     


    def select_entrega_2():                                     # función para seleccionar entrega directamente de las listbox 
        atributos = listbox_entregas_2.get(ANCHOR)               # se obtiene el empleado subrayado en la listbox
        id_usuario = atributos[0]
        id_empleado = atributos[1]
        id_epp = atributos[2]

        print(id_usuario)
        print(id_empleado)
        print(id_epp)

        empleado = ver_empleado_id(id_empleado,cur,conn)
        usuario = ver_empleado_id(id_usuario,cur,conn)
        epp = ver_epp_id(id_epp, cur, conn)

        lista_parametros = [usuario[0],usuario[1],usuario[4],usuario[6],empleado[0],empleado[1],empleado[4],empleado[6],epp[1],epp[2],atributos[7],atributos[3],atributos[4],atributos[5],atributos[6],atributos[8]]

        lista_output_entrega_2

        try:
            for i in range(0,16):
                lista_output_entrega_2[i]['text'] = lista_parametros[i]
        except:
            for i in range(0,16):
                lista_output_entrega_2[i]['text'] = ''


    boton_select_entrega_2 = Button(buscar_entregas, text='Seleccionar entrega', command=select_entrega_2) # para seleccionar entrega subrayada
    boton_select_entrega_2.grid(row=20, column=0)   # se posiciona el botón

    def delete_listbox_entregra_2():        # borra todo el contenido en la listbox
        listbox_entregas_2.delete(0,END)





    root.mainloop()

    cur.close()
    conn.close()

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
                main(id[0])
                

            cur_login.close()
            conn_login.close()    

        except psycopg2.OperationalError:
            label_login_status['text'] = 'No se pudo conectar a la base de datos'

    boton_login = Button(frame_login, text='Ingresar', command=login_func)         # botón para ejecutar la busqueda
    boton_login.grid(row=1, column=2)   

    root_login.mainloop()


#login()

main(21007272)