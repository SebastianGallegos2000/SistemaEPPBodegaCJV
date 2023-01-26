import ver_stock

def hacer_entrega(id_bodeguero,id_empleado,id_epp,cantidad,lugar):                  # función para hacer una retiro de ep
    try:
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

        cantidad_real = ver_stock.get_stock(id_epp, lugar)

        if(cantidad_real == None):      # si es que no se pudo encontrar en la base de datos entonces los parámetros no eran válidos
            print('Porfavor ingrese un código y bodega válidos')
        elif(cantidad_real < cantidad): # si la cantidad real es menor que la pedida entonces no se puede hacer el pedido  
            print('No hay suficiente stock en la bodega para realizar la transaccion')
        else:                           # si hay stock suficiente 

            cantidad_nueva = cantidad_real-cantidad     # se calcula la cantidad nueva
            
            # se actualiza el stock
            sql_actualiza_stock = '''
                                UPDATE stock
                                SET stock = %s
                                WHERE codigo_epp = %s AND
                                lugar = %s
                        '''
            cur.execute(sql_actualiza_stock,[cantidad_nueva,id_epp,lugar])

            # se consigue el tiempo actual
            sql_timestamp = '''     
                                SELECT now()::timestamp(0);
                            '''
            cur.execute(sql_timestamp)          # se ejecuta la consulta
            fecha_hora = (cur.fetchone())[0]    # se guarda la fecha y hora   

            # se consigue el precio actual del producto
            sql_precio = '''
                                SELECT precio
                                FROM epp
                                WHERE codigo_producto = %s
                            '''
            cur.execute(sql_precio,[id_epp])    # se ejecuta la consulta
            precio = (cur.fetchone())[0]        # se guarda el precio actual

            # se inserta en la tabla entrega
            sql_insertar = '''
                                INSERT INTO entrega (id_bodeguero, id_empleado, id_epp, precio_en_transaccion, cantidad, fecha_y_hora, lugar)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            '''
            cur.execute(sql_insertar, [id_bodeguero, id_empleado, id_epp, precio, -cantidad, fecha_hora, lugar])


        conn.commit()   # se le hacen commit a los cambios
        cur.close()     # se cierra el curor y la conexión
        conn.close()
        return 1
    except:
        print('Ocurrió un error')
        return 0


