import psycopg2                                                    # permite conectarse a la base de datos y modificarla       

# credenciales para conectarse a la base
host_v = '10.56.102.135' 
port_v = '5432'
database_v = 'postgres'
user_v = 'postgres'
password_v = 'B2023Psb'

try:                                # dentro de un try por si falla la conexión
    conn = psycopg2.connect(        # se conecta con la base de datos
        host = host_v, port = port_v, database = database_v, user = user_v, password = password_v
    )
    cur = conn.cursor()             # se crea cursor para ir modificando la base

except psycopg2.OperationalError:   # si es que no se conecta a la base
    print('Ocurrió un error al conectarse con la base de datos.')


sql_insertar = '''
                INSERT INTO tabla_prueba(nombre)
                VALUES (%s)
            '''
# se ejecuta la inserción
cur.execute(sql_insertar, ['isaias'])
conn.commit()

cur.close()
conn.close()