def borrar(host_v,port_v,database_v,user_v,password_v):
    import psycopg2         # permite conectarse a la base de datos y modificarla/allows connection to the database and to modify it 

    # host_v = 'localhost' # credenciales para conectarse a la base/credentials to connect to the database
    # port_v = '5432'
    # database_v = 'bodega_db'
    # user_v = 'postgres'
    # password_v = 'SuperBodega'

    try:  # dentro de un try por si falla la conexión/inside a try if the conection fails
        conn = psycopg2.connect(     # se conecta con la base de datos/conection to the database is established
            host = host_v, port = port_v, database = database_v, user = user_v, password = password_v
        )
        cur = conn.cursor()     # se crea cursor para ir modificando la base/a cursor is created to modify the database

    except psycopg2.OperationalError:   # si es que no se conecta a la basa/if conection to the database is not established
        print('Ocurrió un error al conectarse con la base de datos.')

    sql_borrar = ''' 
                DELETE FROM empleado
                WHERE id != 0 
                ''' 
    cur.execute(sql_borrar)

    conn.commit()


    cur.close() # se cierra el curor y la conexión/cursor and connection are closed 
    conn.close()