def insertar(host_v,port_v,database_v,user_v,password_v):
    import psycopg2         # permite conectarse a la base de datos y modificarla       
    from openpyxl import Workbook, load_workbook # permite leer archivos xlsx(excel)

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

    book = load_workbook('epp.xlsx')  # se carga el archivo xlsx con los empleados
    sheet = book.active # se activa el archivo

    i = 1   # empieza en 1 pues la primera fila solo es el nombre de las columnas
    vacio = False   # cuando esta variable cambie a True entonces se llegó a la primera fila en blanco

    while(i<1000 and not vacio):    # se leen a lo más 999 productos
        i+=1    # avanza el índice
        fila = sheet[i] # se lee la fila i del archivo

        c_producto = fila[2].value                        # código producto
        stock = fila[5].value                             # stock del producto

        fila_vacia = (c_producto == None) and (stock == None)

        if(fila_vacia): # si la fila i está vacía
            vacio = True # vacio es True y se termina el while
        else:   # si no está vacía
            # consulta para inseertar a tabla stock 
            lugar = 'BODEGA CENTRAL'
            
            sql_insertar_stock = '''
                                INSERT INTO stock (codigo_epp, bodega, cantidad,cantidad_critica)
                                VALUES (%s, %s, %s, %s)
                            '''
            cur.execute(sql_insertar_stock, [c_producto, lugar, stock, 0]) 

            lugar = 'BODEGA CS'

            sql_insertar_stock = '''
                                INSERT INTO stock (codigo_epp, bodega, cantidad,cantidad_critica)
                                VALUES (%s, %s, %s, %s)
                            '''
            cur.execute(sql_insertar_stock, [c_producto, lugar, stock, 0]) 

            lugar = 'BODEGA T1A'

            sql_insertar_stock = '''
                                INSERT INTO stock (codigo_epp, bodega, cantidad,cantidad_critica)
                                VALUES (%s, %s, %s, %s)
                            '''
            cur.execute(sql_insertar_stock, [c_producto, lugar, stock, 0]) 


            conn.commit()   # se ejecuta la consulta y se hace commit 

    cur.close() # se cierra el curor y la conexión 
    conn.close()