import borrar_empleados
import borrar_epp
import borrar_stock
import borrar_jose
import borrar_entrega
import borrar_bodega

# SI YA SE ESTÁ USNADO NO USAR ESTÁ FUNCIONM

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


borrar_entrega.borrar(host_v,port_v,database_v,user_v,password_v)
borrar_jose.borrar(host_v,port_v,database_v,user_v,password_v)
borrar_stock.borrar(host_v,port_v,database_v,user_v,password_v)
borrar_bodega.borrar(host_v,port_v,database_v,user_v,password_v)
borrar_epp.borrar(host_v,port_v,database_v,user_v,password_v)
borrar_empleados.borrar(host_v,port_v,database_v,user_v,password_v)

# SI YA SE ESTÁ USNADO NO USAR ESTÁ FUNCIONM