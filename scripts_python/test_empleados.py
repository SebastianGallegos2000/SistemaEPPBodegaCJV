def insertar(host_v,port_v,database_v,user_v,password_v):
    import psycopg2         # permite conectarse a la base de datos y modificarla       
    from openpyxl import Workbook, load_workbook # permite leer archivos xlsx(excel)
    from datetime import datetime   # para trabajar con fechas
    from sin_tildes import sin_tilde

    # host_v = 'localhost' # credenciales para conectarse a la base
    # port_v = '5432'
    # database_v = 'bodega_db'
    # user_v = 'postgres'
    # password_v = 'SuperBodega'

    try:  # dentro de un try por si falla la conexión
        conn = psycopg2.connect(     # se conecta con la base de datos
            host = host_v, port = port_v, database = database_v, user = user_v, password = password_v
        )
        cur = conn.cursor()     # se crea cursor para ir modificando la base

    except psycopg2.OperationalError:   # si es que no se conecta a la base
        print('Ocurrió un error al conectarse con la base de datos.')

    book = load_workbook('empleado.xlsx')  # se carga el archivo xlsx con los empleados
    sheet = book.active # se activa el archivo

    i = 1   # empieza en 1 pues la primera fila solo es el nombre de las columnas
    vacio = False   # cuando esta variable cambie a True entonces se llegó a la primera fila en blanco

    while(i<1000 and not vacio):    # se leen a lo más 999 empleados
        i+=1    # avanza el índice/index goes up 
        fila = sheet[i] # se lee la fila i del archivo
        # ahora se guardan los valores de cada columna en la fila
        nombre = fila[0].value      # nombre
        rut = fila[1].value         # rut
        d_cargo = fila[2].value     # cargo
        fecha_ing = fila[3].value   # fecha de ingreso
        d_monti_ret = fila[4].value # vigencia
        gerencia_a = fila[5].value  # gerencia
        d_cencos = fila[6].value    # departamento
        d_seccion = fila[7].value   # sección

        # si fila_vacia es True entonces la fila i es vacía
        fila_vacia = (nombre == None) and (rut == None) and (d_cargo == None) and (fecha_ing == None) and (d_monti_ret == None) and (gerencia_a == None) and (d_cencos == None) and (d_seccion == None)
        
        if(fila_vacia): # si la fila i está vacía/if row i is empty
            vacio = True # vacio es True y se termina el while
        else:   # si no está vacía
            
            parametros = [None, None, None, None, None, None, None, None, None, None, None, None] # todos los parámetros empiezan en None

            rut = rut.strip()       # se borran posibles espacios en blanco al principio y final
            rut = rut.split('-')    # se sepera los numero del dígito verficador
            rut = rut[0]            # se guardan solo los primeros números
            rut = int(rut)          # se transforman de string a int
            parametros[0] = rut     

            nombre = sin_tilde(nombre)

            nombres_apellidos = nombre.split(',')   # se separa nombres de los apellidos

            nombres = nombres_apellidos[1].split()      # se separan los nombres
            apellidos = nombres_apellidos[0].split()    # se separan los apellidos

            nombre1 = nombres[0].strip()    	# se consigue el primer nombre y se borran posibles espacio en banco
            parametros[1] = nombre1             
        
            if(len(nombres) == 2):             # si solo hay dos palabras entonces solo hay dos palabras
                nombre2 = nombres[1].strip()    
                parametros[2] = nombre2
            elif(len(nombres) == 3):           # si hay tres palabras
                s_nombre = nombres[1].strip()   
                if(s_nombre != 'DEL' and s_nombre != 'DE'): # y la segunda palabra no es ni 'DEL' o 'DE' 
                    nombre2 = nombres[1].strip()
                    nombre3 = nombres[2].strip()    # entonces hay tres nombres (no hay nombres compuestos)
                    parametros[2] = nombre2
                    parametros[3] = nombre3
                else:   # si 'DE' o 'DEL' está en la segunda palabra entonces es nombre compuesto
                    n_compuesto_1 = nombres[1].strip()
                    n_compuesto_2 = nombres[2].strip()
                    nombre2 = n_compuesto_1+' '+n_compuesto_2
                    parametros[2] = nombre2
            elif(len(nombres) == 4):   # si hay cuatro palabras
                n_compuesto_1 = nombres[1].strip()
                n_compuesto_2 = nombres[2].strip()
                n_compuesto_3 = nombres[3].strip()
                articulos = ['LA','LOS','LAS']
                if(n_compuesto_1 == 'DE' and n_compuesto_2 in articulos):   # si las palabras siguen el formato 'DE LA', 'DE LOS', 'DE LAS'
                    nombre2 = n_compuesto_1+' '+n_compuesto_2+' '+n_compuesto_3
                    parametros[2] = nombre2     # es nombre compuesto

            apellidoP = apellidos[0].strip()    # se consigue el apellido
            parametros[4] = apellidoP           

            if(len(apellidos) == 2):            # si hay dos palabras entonces hay dos apellidos
                apellidoM = apellidos[1].strip()
                parametros[5] = apellidoM
            
            parametros[6] = d_monti_ret.strip()
            parametros[7] = gerencia_a.strip()
            parametros[8] = d_cencos.strip()
            parametros[9] = d_seccion.strip()
            parametros[10] = d_cargo.strip()

            parametros[6] = parametros[6].upper()
            parametros[7] = parametros[7].upper()
            parametros[8] = parametros[8].upper()
            parametros[9] = parametros[9].upper()
            parametros[10] = parametros[10].upper()

            parametros[6] = sin_tilde(parametros[6])
            parametros[7] = sin_tilde(parametros[7])
            parametros[8] = sin_tilde(parametros[8])
            parametros[9] = sin_tilde(parametros[9])
            parametros[10] = sin_tilde(parametros[10])

            parametros[11] = fecha_ing.strftime("%Y-%m-%d") # se guarda la fecha en el formato correcto

            # la consulta para insertar las palabras
            sql_insertar = '''      
                INSERT INTO empleado (id, nombre_1, nombre_2, nombre_3, apellido_p, apellido_m, vigencia, gerencia, departamento, seccion, cargo, fecha_de_ingreso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
            cur.execute(sql_insertar, [parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5], parametros[6], parametros[7], parametros[8], parametros[9], parametros[10], parametros[11]])
            conn.commit()   # se ejecuta la consulta y se hace commit 

    cur.close() # se cierra el curor y la conexión
    conn.close()



