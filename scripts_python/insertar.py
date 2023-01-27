import test_empleados
import test_epp
import test_stock
import insertar_usuarios
import insertar_bodegas

host_v = None
port_v = None
database_v = None
user_v = None
password_v = None

server = 'mio'

if(server == 'mio'):
    host_v = 'localhost' # credenciales para conectarse a la base
    port_v = '5432'
    database_v = 'bodega_db'
    user_v = 'postgres'
    password_v = 'SuperBodega' 
elif(server == 'remoto'):    
    host_v = '10.56.102.135' # credenciales para conectarse a la base
    port_v = '5432'
    database_v = 'postgres'
    user_v = 'postgres'
    password_v = 'B2023Psb'

test_empleados.insertar(host_v,port_v,database_v,user_v,password_v)
test_epp.insertar(host_v,port_v,database_v,user_v,password_v)
insertar_bodegas.insertar(host_v,port_v,database_v,user_v,password_v)
test_stock.insertar(host_v,port_v,database_v,user_v,password_v)
insertar_usuarios.insertar(host_v,port_v,database_v,user_v,password_v)

