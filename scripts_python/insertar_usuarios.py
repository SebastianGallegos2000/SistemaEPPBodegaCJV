def insertar(host_v,port_v,database_v,user_v,password_v):
    import psycopg2         # permite conectarse a la base de datos y modificarla       

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

    sql_insertar_luciano = '''
                        INSERT INTO usuario (id, usuario, contrasenna, permisos)
                        VALUES (%s, %s, %s, %s)
                    '''
    cur.execute(sql_insertar_luciano,[15070720, 'user_luciano', 'password_luciano', 'ADMIN TI']) 
    conn.commit() # se ejecuta la consulta y se hace commit 

    cur.close() # se cierra el curor y la conexión
    conn.close()


