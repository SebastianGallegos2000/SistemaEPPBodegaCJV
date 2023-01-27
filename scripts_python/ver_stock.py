def get_stock(id_epp,lugar): 
    import psycopg2         # permite conectarse a la base de datos y modificarla       

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

    # se checkea la cantidad de stock en la bodega 
    sql_check_cantidad = '''                    
                        SELECT stock
                        FROM stock
                        WHERE codigo_epp = %s AND
                        lugar = %s
                    '''
    cur.execute(sql_check_cantidad,[id_epp,lugar])  # se ejecuta la consulta 
    cantidad_real = cur.fetchone()

    cur.close() # se cierra el curor y la conexión
    conn.close()

    if(cantidad_real == None):
        print('No se encontró EPP con el código dado, asegurese de que el código esté bien escrito.')
    else:
        return cantidad_real[0]


