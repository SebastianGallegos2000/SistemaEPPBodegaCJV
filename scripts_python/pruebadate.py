import psycopg2         # permite conectarse a la base de datos y modificarla/allows connection to the database and to modify it        
from openpyxl import Workbook, load_workbook # permite leer archivos xlsx(excel)/allows us to read xlsx (excel) files
import re               # permite trabajar con expresiones regulare/allows us to work with regular expressions 

host_v = 'localhost' # credenciales para conectarse a la base/credentials to connect to the database
port_v = '5432'
database_v = 'bodega_db'
user_v = 'postgres'
password_v = 'SuperBodega'

try:  # dentro de un try por si falla la conexión/inside a try if the conection fails
    conn = psycopg2.connect(     # se conecta con la base de datos/conection to the database is established
        host = host_v, port = port_v, database = database_v, user = user_v, password = password_v
    )
    cur = conn.cursor()     # se crea cursor para ir modificando la base/a cursor is created to modify the database

except psycopg2.OperationalError:   # si es que no se conecta a la basa/if conection to the database is not established
    print('Ocurrió un error al conectarse con la base de datos.')

sql_insertar = '''
    INSERT INTO empleado (id, nombre_1, nombre_2, nombre_3, apellido_p, apellido_m, vigencia, gerencia, departamento, seccion, fecha_de_ingreso)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
parametros = [21007272, 'BENJAMIN','GABRIEL', None, 'CONTRERAS', 'SANCHEZ', 'CONTRATO VIGENTE', 'ADMINISTRACION Y FINANZA', 'INFORMATICA', 'PERSONAL DIRECTO', '2023-01-03']
cur.execute(sql_insertar, [parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5], parametros[6], parametros[7], parametros[8], parametros[9], parametros[10]])
conn.commit()

cur.close() # se cierra el curor y la conexión/cursor and connection are closed 
conn.close()