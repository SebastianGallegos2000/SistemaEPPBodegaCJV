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

    tallas = ['XXXS', 'XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']      # lista con todas las tallas de XXXS a XXXL
    tallas_T = []       # lista para guardar tallas con formato T- (ej: T=XL)
    tallasSlashT = []   # lista para guardar tallas con formato T/ (ej: T/XL)

    for j in range(0, len(tallas)):         # se llena la lista de tallas -
        tallas_T.append('T-'+tallas[j])

    for j in range(0, len(tallas)):
        tallasSlashT.append('T/'+tallas[j]) # se llena la lista de tallas /

    nTallas = []        # lista para tallas con formtato NUMERO (ej: 47)
    ntTallas = []       # lista para tallas con formtato T+NUMERO (ej: T47)
    ncTallas = []       # lista para tallas con formtato N°+NUMERO (ej: N°47)
    nc_Tallas = []      # lista para tallas con formtato Nº+NUMERO (ej: Nº47)

    # tallas con unidad de medidda distinta
    sTallas = [None, None, '37(5,5)', '38(6)', '39(7)', '40(7,5)', '41(8)', '42(8,5)', '43(9)', '44(10,5)', '45(11,5)', '46(12)', None, None, None, None, None, None, None, None]

    talla_min = 35      # rango de tallas númericas válidas
    talla_max = 54

    for j in range(talla_min, talla_max+1):     # se llenan todas las tablas
        char = str(j)
        nTallas.append(char)

    for j in range(talla_min, talla_max+1):
        char = str(j)
        ntTallas.append('T'+char)  

    for j in range(talla_min, talla_max+1):
        char = str(j)
        ncTallas.append('N°'+char)  

    for j in range(talla_min, talla_max+1):
        char = str(j)
        nc_Tallas.append('Nº'+char)  

    while(i<1000 and not vacio):    # se leen a lo más 999 productos
        i+=1    # avanza el índice/index goes up 
        fila = sheet[i] # se lee la fila i del archivo
        # ahora se guardan los valores de cada columna en la fila
        c_constructor = fila[0].value                     # código constructor
        constructor_designacion = fila[1].value           # constructor designación
        c_producto = fila[2].value                        # código producto
        pieza_designacion = fila[3].value                 # pieza designación (nombre)
        um = fila[4].value                                # unidad medida
        precio = fila[6].value                            # precio del producto

        fila_vacia = (c_constructor == None) and (constructor_designacion == None) and (c_producto == None) and (pieza_designacion == None) and (um == None) and (precio == None)

        if(fila_vacia): # si la fila i está vacía/if row i is empty
            vacio = True # vacio es True y se termina el while
        else:   # si no está vacía
            parametros = [None, None, None, None, None, None, None, None] # todos los parámetros empiezan en None
            
            parametros[0] = c_constructor
            parametros[1] = c_producto
            parametros[2] = pieza_designacion.strip()
            parametros[2] = parametros[2].upper()
            parametros[3] = constructor_designacion.strip()
            parametros[3] = parametros[3].upper()

            lista_nombre = pieza_designacion.split()   # se separa el nombre por espacios para buscar la talla

            for talla in tallas:                        # se revisa si la talla se encunetra en formato LETRAS (ej: XL)
                if(talla in lista_nombre):
                    parametros[4] = talla

            if(parametros[4] == None):                  # se revisa si la talla se encunetra en formato T-LETRAS (ej: T-XL)
                for j in range(0,len(tallas)):
                    if(tallas_T[j] in lista_nombre):
                        parametros[4] = tallas[j] 

            if(parametros[4] == None):                  # se revisa si la talla se encunetra en formato T/LETRAS (ej: T/XL)
                for j in range(0,len(tallas)):
                    if(tallasSlashT[j] in lista_nombre):
                        parametros[4] = tallas[j] 

            if(parametros[4] == None):                  # se revisa si la talla se encunetra en formato NUMERO (ej: 47)
                for talla in nTallas:
                    if(talla in lista_nombre):
                        parametros[4] = talla
                    
            if(parametros[4] == None):                  # se revisa si la talla se encunetra en formato T+NUMERO (ej: T47)
                for j in range(0,len(nTallas)):
                    if(ntTallas[j] in lista_nombre):
                        parametros[4] = nTallas[j]

            if(parametros[4] == None):                  # se revisa si la talla se encunetra en formato N°+NUMERO (ej: N°47)
                for j in range(0,len(nTallas)):
                    if(ncTallas[j] in lista_nombre):
                        parametros[4] = nTallas[j]

            if(parametros[4] == None):                  # se revisa si la talla se encunetra en formato Nº+NUMERO (ej: Nº47)
                for j in range(0,len(nTallas)):
                    if(nc_Tallas[j] in lista_nombre):
                        parametros[4] = nTallas[j]

            if(parametros[4] == None):                  # se revisa si la talla se encunetra en formato NUMERO(NUMERO) (ej: 46(12))
                for j in range(0,len(nTallas)):
                    if(sTallas[j] in lista_nombre):
                        parametros[4] = nTallas[j]
                
            parametros[5] = um.strip()
            parametros[5] = parametros[5].upper()
            parametros[6] = precio

            # la consulta para insertar las palabras
            sql_insertar = '''      
                INSERT INTO epp (codigo_constructor, codigo_producto, nombre, constructor_designado, talla, unidad_medicion, precio)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
            cur.execute(sql_insertar, [parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5], parametros[6]]) 
            conn.commit()   # se ejecuta la consulta y se hace commit 
            
    cur.close() # se cierra el curor y la conexión
    conn.close()
