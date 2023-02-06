from tkinter import Tk, Frame, Label, Button, Entry                # se importa tkninter para la interfaz gráfica
from tkinter import ttk                                            # se importa para tener tabs
import psycopg2                                                    # permite conectarse a la base de datos y modificarla       
from funciones import *                                            # se importan las funciones de queries

def sin_tilde(texto):
    texto_sin_tildes = ''

    for char in texto:
        tildes = ['Á','É','Í','Ó','Ú','á','é','í','ó','ú']
        sin_tildes = ['A','E','I','O','U','a','e','i','o','u']
        char_annadido = char
        for i in range(0,10):
            if(char==tildes[i]):
                char_annadido=sin_tildes[i]
                break
        texto_sin_tildes+=char_annadido
    return texto_sin_tildes

def empleado_en_db_id(id,cur,conn):             # dice si el empleado está en la base de datos, si retorna 1 está, si retorna 0 no está y retorna -1 si está mal el formato 
    id = id.split('-')
    id = id[0]
    try:                                # dentro de un try por si algo falla 
        # se hace la consulta
        sql_check_empleado = '''        
                            SELECT id
                            FROM empleado
                            WHERE id = %s
                        '''
        cur.execute(sql_check_empleado,[id])
        if(cur.fetchone() == None):     # si es none entonces no está en la base de datos
            return 0
        else:                           # si es que retorna, entonces si está
            return 1 
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback()
        return -1       

def epp_en_db_id(id,cur,conn):             # dice si el empleado está en la base de datos, si retorna 1 está, si retorna 0 no está y retorna -1 si está mal el formato 
    try:                                # dentro de un try por si algo falla 
        # se hace la consulta
        sql_check_empleado = '''        
                            SELECT codigo_producto
                            FROM epp
                            WHERE codigo_producto = %s
                        '''
        cur.execute(sql_check_empleado,[id])
        if(cur.fetchone() == None):     # si es none entonces no está en la base de datos
            return 0
        else:                           # si es que retorna, entonces si está
            return 1 
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback()
        return -1      

def bodega_en_db_nombre(nombre,cur,conn):
    try:                                # dentro de un try por si algo falla 
        # se hace la consulta
        sql_check_bodega = '''        
                            SELECT nombre
                            FROM bodega
                            WHERE nombre = %s
                        '''
        cur.execute(sql_check_bodega,[nombre])
        if(cur.fetchone() == None):     # si es none entonces no está en la base de datos
            return 0
        else:                           # si es que retorna, entonces si está
            return 1 
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback()
        return -1    

def usuario_en_db_id(id,cur,conn):
    id = id.split('-')
    id = id[0]
    try:                                # dentro de un try por si algo falla 
        # se hace la consulta
        sql_check_usuario = '''        
                            SELECT id
                            FROM usuario
                            WHERE id = %s
                        '''
        cur.execute(sql_check_usuario,[id])
        if(cur.fetchone() == None):     # si es none entonces no está en la base de datos
            return 0
        else:                           # si es que retorna, entonces si está
            return 1 
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback()
        return -1   

def registro_stock_en_db(id,bodega,cur,conn):
    try:                                # dentro de un try por si algo falla 
        # se hace la consulta
        sql_check_registro = '''        
                            SELECT codigo_epp, bodega
                            FROM stock
                            WHERE codigo_epp = %s AND
                            bodega = %s
                        '''
        cur.execute(sql_check_registro,[id,bodega])
        if(cur.fetchone() == None):     # si es none entonces no está en la base de datos
            return 0
        else:                           # si es que retorna, entonces si está
            return 1 
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback()
        return -1   

def ver_empleado_id(id,cur,conn):   # muestra la info del empleado
    if(type(id) is str):
        id = id.split('-')
        id = id[0]

    # se hace la consulta
    sql_check_empleado = '''        
                        SELECT *
                        FROM empleado
                        WHERE id = %s
                    '''
    try:                                # dentro de un try por si algo falla 
        cur.execute(sql_check_empleado,[id])
        return cur.fetchone()
    except:   # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback() # se hace rollback para abortar la transacción
        return None
    
def ver_empleado_nombre(nombre,apellido,cur):   # muestra la info del empleado
    try:                                # dentro de un try por si algo falla 
        nombre = nombre.upper()
        apellido = apellido.upper()

        # se hace la consulta
        sql_check_empleado = '''        
                            SELECT *
                            FROM empleado
                            WHERE nombre_1 LIKE %s AND
                            apellido_p LIKE %s
                        '''
        cur.execute(sql_check_empleado,['%'+nombre+'%','%'+apellido+'%'])
        return cur.fetchone()
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        pass

def ver_epp_id(id,cur,conn):   # muestra la info del epp
    # se hace la consulta
    sql_check_epp = '''        
                        SELECT *
                        FROM epp
                        WHERE codigo_producto = %s
                    '''
    try:                                # dentro de un try por si algo falla 
        cur.execute(sql_check_epp,[id])
        return cur.fetchone()
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def ver_stock_id(id,bodega,cur,conn):
    # se hace la consulta
    sql_check_stock = '''        
                        SELECT epp.codigo_constructor, epp.codigo_producto, epp.nombre, epp.constructor_designado, epp.talla, epp.unidad_medicion, epp.precio, stock.bodega, stock.cantidad, stock.cantidad_critica
                        FROM epp, stock
                        WHERE codigo_epp = %s AND
                        bodega = %s AND
                        stock.codigo_epp = epp.codigo_producto
                    '''
    try:                                # dentro de un try por si algo falla 
        cur.execute(sql_check_stock,[id,bodega])
        return cur.fetchone()
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def ver_todos_empleados_func(cur,conn):       # retorna info de todos los empleados
    try:                            # en un try por si falla 
        sql_ver_empleados = '''
                            SELECT *
                            FROM empleado
                            ORDER BY id DESC;
                        '''  
        cur.execute(sql_ver_empleados)  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados
    except:                 # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def ver_empleados(nombre,apellido,vigencia,gerencia,departamento,seccion,cargo, orden, cur,conn):            # muestra los empleados con las restricciones dadas
    # se ponen en mayúsculas los parámetros    sql
    nombre = nombre.upper()             
    apellido = apellido.upper()         
    gerencia = gerencia.upper()
    departamento = departamento.upper()
    cargo = cargo.upper()

    # consulta sql
    sql_ver_empleados = ''' 
                        SELECT *
                        FROM empleado 
                        WHERE nombre_1 LIKE %s AND
                        apellido_p LIKE %s AND
                        vigencia LIKE %s AND
                        gerencia LIKE %s AND
                        departamento LIKE %s AND 
                        seccion LIKE %s AND
                        cargo LIKE %s
                        '''
    # dice en que orden estarán los resultados
    if(orden == 'ID ascendiente'):
        sql_ver_empleados += 'ORDER BY id ASC'
    elif(orden == 'ID descendiente'):
        sql_ver_empleados += 'ORDER BY id DESC'
    elif(orden == 'Fecha de ingreso ascendiente'):
        sql_ver_empleados += 'ORDER BY fecha_de_ingreso ASC'
    elif(orden == 'Fecha de ingreso descendiente'):
        sql_ver_empleados += 'ORDER BY fecha_de_ingreso DESC'

    # se devuelven todos los empleados que cumplen las condiciones
    try:                # en un try por si falla
        cur.execute(sql_ver_empleados,['%'+nombre+'%','%'+apellido+'%','%'+vigencia+'%','%'+gerencia+'%','%'+departamento+'%','%'+seccion+'%','%'+cargo+'%'])  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados        
    except:     # quizá poner un conn.rollback()
        conn.rollback()
        return None

def annadir_empleado_func(id,nombre1,nombre2,nombre3,apellidoP,apellidoM,vigencia,gerencia,departamento,seccion,fecha,cargo, cur, conn):
    # se dejan todos los parámetros en mayúscula
    nombre1 = nombre1.upper()   
    nombre2 = nombre2.upper()
    nombre3 = nombre3.upper()
    apellidoP = apellidoP.upper()
    apellidoM = apellidoM.upper()   
    gerencia = gerencia.upper()
    departamento  = departamento.upper()
    cargo = cargo.upper()

    nombre1 = sin_tilde(nombre1)
    nombre2 = sin_tilde(nombre2)
    nombre3 = sin_tilde(nombre3)
    apellidoP = sin_tilde(apellidoP)
    apellidoM = sin_tilde(apellidoM)
    gerencia = sin_tilde(gerencia)
    departamento = sin_tilde(departamento)
    cargo = sin_tilde(cargo)

    id = id.split('-')
    id = id[0]

    # si se deja vacío nombre2,nombre3 y apellido materno entonces se vuelve un None en vez de '' 
    nombres = [nombre2,nombre3,apellidoM]
    for nombre in nombres:
        if nombre == '':
            nombre = None
    try:    # en un try por si falla
        # se hace la inserción
        sql_insertar = '''
                        INSERT INTO empleado(id, nombre_1, nombre_2, nombre_3, apellido_p, apellido_m, vigencia, gerencia, departamento, seccion, fecha_de_ingreso, cargo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
        # se ejecuta la inserción
        cur.execute(sql_insertar, [id, nombre1, nombre2, nombre3, apellidoP, apellidoM, vigencia, gerencia, departamento, seccion, fecha, cargo])
        conn.commit()
        return 1    # si se hace exitosamente retorna 1
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1

def modificar_empleado_func(id,nombre1,nombre2,nombre3,apellidoP,apellidoM,vigencia,gerencia,departamento,seccion,fecha,cargo, cur, conn):
    id = id.split('-')
    id = id[0]

    # se dejan todos los parámetros en mayúscula
    nombre1 = nombre1.upper()   
    nombre2 = nombre2.upper()
    nombre3 = nombre3.upper()
    apellidoP = apellidoP.upper()
    apellidoM = apellidoM.upper()   
    gerencia = gerencia.upper()
    departamento  = departamento.upper()
    cargo = cargo.upper()

    nombre1 = sin_tilde(nombre1)
    nombre2 = sin_tilde(nombre2)
    nombre3 = sin_tilde(nombre3)
    apellidoP = sin_tilde(apellidoP)
    apellidoM = sin_tilde(apellidoM)
    gerencia = sin_tilde(gerencia)
    departamento = sin_tilde(departamento)
    cargo = sin_tilde(cargo)

    # lista para todos los parámetros
    lista = [id,nombre1,nombre2,nombre3,apellidoP,apellidoM,vigencia,gerencia,departamento,seccion,fecha,cargo]

    try: # en un try por si falla 
        # consulta para obtener los parámetros actuales
        sql_empleado = '''
                        SELECT *
                        FROM empleado
                        WHERE id = %s
                    '''
        cur.execute(sql_empleado,[id])
        empleado = cur.fetchone()       # se consiguen los parámetos actuales del empleado

        lista_empleado = [None]*12      # lista con none para los doce atributos
        for i in range(0,12):           # se llena la lista con los atributos de la tupla empleado
            lista_empleado[i] = empleado[i]

        lista_empleado[10] = lista_empleado[10].strftime("%Y-%m-%d") # se guarda la fecha en el formato correcto
        lista_empleado[10].strip()

        for i in range(0, 12):      # si algún campo en la interfaz se deja en blanco entonces se deja el parametro previo 
            if(lista[i] == '' ):
                lista[i] = lista_empleado[i]

        indices_opcionales = [2,3,5]            # indices para los opcionales
        for indice in indices_opcionales:        # si se deja un guíon en los campos opcionales se deja como un none 
            if lista[indice] == '-':
                lista[indice] = None    
        # se hace la actualización  
        sql_actualizar = '''
                        UPDATE empleado
                        SET nombre_1=%s,nombre_2=%s,nombre_3=%s,apellido_p=%s,apellido_m=%s,vigencia=%s,gerencia=%s,departamento=%s,seccion=%s,fecha_de_ingreso=%s,cargo=%s
                        WHERE id = %s       
                    '''   
        cur.execute(sql_actualizar, [lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9],lista[10],lista[11],lista[0]])
        conn.commit()
        return 1    # si se hace exitosamente retorna 1
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1

def eliminar_empleado_func(id,cur,conn):
    id = id.split('-')
    id = id[0]
    
    try:
        # se eliminan las entregas relacionadas
        sql_eliminar_entregas = '''
                            DELETE FROM entrega
                            WHERE id_empleado = %s
                            OR id_usuario = %s
                        '''

        cur.execute(sql_eliminar_entregas,[id,id])

        # se eliminan los usuarios relacionados
        sql_eliminar_usuario = '''
                            DELETE FROM usuario
                            WHERE id = %s
                        '''
        
        cur.execute(sql_eliminar_usuario,[id])

        # se elimina el empleado 
        sql_eliminar = '''
                        DELETE FROM empleado
                        WHERE id = %s
                    '''
        cur.execute(sql_eliminar,[id])
        conn.commit()
        return 1
    except:
        conn.rollback()
        return -1

def ver_todos_los_epp_func(cur,conn):
        try:                            # en un try por si falla 
            sql_ver_empleados = '''
                                SELECT *
                                FROM epp
                                ORDER BY codigo_producto ASC;
                            '''  
            cur.execute(sql_ver_empleados)  # se ejecuta la consulta
            return cur.fetchall()           # y se retornan todos los resultados
        except:                 # si falla
            conn.rollback()
            return None

def ver_epps(c_construct,nombre,contruct_desig,talla,UM,orden,cur,conn):
    nombre = nombre.upper()
    contruct_desig = contruct_desig.upper()
    UM = UM.upper()  
    talla = talla.upper()  

    # consulta sql
    sql_ver_epps = '''
                    SELECT *
                    FROM epp
                    WHERE nombre LIKE %s AND
                    constructor_designado LIKE %s AND
                    unidad_medicion LIKE %s
                '''
    parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%']

    if(c_construct != '' and talla != ''):
        sql_ver_epps+= 'AND codigo_constructor = %s AND talla = %s '
        parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%',c_construct,talla]
    elif(c_construct != ''):
        sql_ver_epps+= 'AND codigo_constructor = %s'
        parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%',c_construct]
    elif(talla != ''):
        sql_ver_epps+= 'AND talla = %s'
        parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%', talla]


    # dice en que orden estarán los resultados
    if(orden == 'Código de producto ascendiente'):
        sql_ver_epps += 'ORDER BY codigo_producto ASC'
    elif(orden == 'Código de producto descendiente'):
        sql_ver_epps += 'ORDER BY codigo_producto DESC'
    elif(orden == 'Precio ascendiente'):
        sql_ver_epps += 'ORDER BY precio ASC'
    elif(orden == 'Precio descendiente'):
        sql_ver_epps += 'ORDER BY precio DESC'

    # se devuelven todos los empleados que cumplen las condiciones
    try:                # en un try por si falla
        cur.execute(sql_ver_epps,parametros)  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados        
    except:     # quizá poner un conn.rollback()
        conn.rollback()
        return None

def annadir_epp_func(id,c_construct,nombre,contruct_desig,talla,UM,precio,cur,conn):
    # se dejan todos los parámetros en mayúsculas
    nombre = nombre.upper()
    contruct_desig = contruct_desig.upper()
    talla = talla.upper()
    UM = UM.upper()

    nombre = sin_tilde(nombre)
    contruct_desig = sin_tilde(contruct_desig)
    talla = sin_tilde(talla)
    UM = sin_tilde(UM)

    try:
        precio_double = float(precio)
        if(precio_double<0):
            return -1
    except:
        pass

    # si talla se deja vacía entonces se transforma en un None en vez de ''
    if  talla == '':
        talla = None
    try:    # en un try por si falla
        # se hace la inserción
        sql_insertar = '''
                        INSERT INTO epp(codigo_producto,codigo_constructor,nombre,constructor_designado,talla,unidad_medicion,precio)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    '''
        # se ejecuta la inserción 
        cur.execute(sql_insertar, [id, c_construct, nombre, contruct_desig, talla, UM, precio])
        conn.commit()
        return 1    # si se hace exitosamente retorna 1 
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1

def modificar_epp_func(id,c_constructor,nombre,constructor_designado,talla,unidad_medicion,precio,cur,conn):
    # se dejan los parámetros en mayúscula
    nombre = nombre.upper()
    constructor_designado = constructor_designado.upper()
    talla = talla.upper()
    unidad_medicion = unidad_medicion.upper()

    nombre = sin_tilde(nombre)
    constructor_designado = sin_tilde(constructor_designado)
    talla = sin_tilde(talla)
    unidad_medicion = sin_tilde(unidad_medicion)
    
    lista = [id, c_constructor, nombre, constructor_designado, talla, unidad_medicion, precio]

    try:
        precio_double = float(precio)
        if(precio_double<0):
            return -1
    except:
        pass

    try: # en un try por si falla 
        # consulta para obtener los parámetros actuales
        sql_epp = '''
                        SELECT *
                        FROM epp
                        WHERE codigo_producto = %s
                    '''

        cur.execute(sql_epp,[id])
        epp = cur.fetchone()       # se consiguen los parámetos actuales del epp

        lista_epp = [None]*7      # lista con none para los siete atributos
        for i in range(0,7):           # se llena la lista con los atributos de la tupla empleado
            lista_epp[i] = epp[i]

        for i in range(0, 7):      # si algún campo en la interfaz se deja en blanco entonces se deja el parametro previo 
            if(lista[i] == '' ):
                lista[i] = lista_epp[i]
        
        if lista[4] == '-':     # si el campo opcional talla se escribe '-' se deja como un none 
            lista[4] = None
        # se hace la actualización  
        sql_actualizar = '''
                        UPDATE epp
                        SET codigo_constructor=%s,nombre=%s,constructor_designado=%s,talla=%s,unidad_medicion=%s,precio=%s
                        WHERE codigo_producto = %s       
                    '''          
        cur.execute(sql_actualizar,[lista[1],lista[2],lista[3],lista[4],lista[5],lista[6],lista[0]]) 
        conn.commit()
        return 1    # si se hace exitosamente retorna 1
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1
   
def eliminar_epp_func(id,cur,conn):
    try:
        # se eliminan las entregas relacionadas
        sql_eliminar_entregas = '''
                        DELETE FROM entrega
                        WHERE id_epp = %s
                    '''
        
        cur.execute(sql_eliminar_entregas,[id])

        # se eliminan los registros de stock relacionados
        sql_eliminar_registros = '''
                        DELETE FROM stock 
                        WHERE codigo_epp = %s
                    ''' 

        cur.execute(sql_eliminar_registros,[id])

        # se elimina el epp
        sql_eliminar = '''
                        DELETE FROM epp
                        WHERE codigo_producto = %s
                    '''
        cur.execute(sql_eliminar,[id])
        conn.commit()
        return 1
    except:
        conn.rollback()
        return -1

def ver_todas_bodegas_func(cur,conn):       # retorna info de todas las bodegas
    try:                            # en un try por si falla 
        sql_ver_bodegas = '''
                            SELECT *
                            FROM bodega
                            ORDER BY nombre ASC;
                        '''  
        cur.execute(sql_ver_bodegas)  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados
    except:                 # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def annadir_bodega_func(nombre,cur,conn):
    nombre = nombre.upper()  # se deja en mayúscula 
    try:    # en un try por si falla
        # se hace la inserción
        sql_insertar = '''
                        INSERT INTO bodega(nombre)
                        VALUES (%s)
                    '''
        # se ejecuta la inserción 
        cur.execute(sql_insertar, [nombre])
        conn.commit()
        return 1    # si se hace exitosamente retorna 1 
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1    

def eliminar_bodega_func(nombre,cur,conn):
    try:
        # se eliminan las entregas relacionadas
        sql_eliminar_entregas = '''
                        DELETE FROM entrega
                        WHERE bodega = %s
                    '''

        cur.execute(sql_eliminar_entregas,[nombre])

        # se eliminan los registros de stock relacionados
        sql_eliminar_registros = '''
                        DELETE FROM stock 
                        WHERE bodega = %s
                    '''

        cur.execute(sql_eliminar_registros,[nombre])

        # se elimina la bodega 
        sql_eliminar = '''
                        DELETE FROM bodega
                        WHERE nombre = %s
                    '''
        cur.execute(sql_eliminar,[nombre])
        conn.commit()
        return 1
    except:
        conn.rollback()
        return -1

def ver_todos_usuarios_func(cur,conn):
    try:                            # en un try por si falla 
        sql_ver_usuarios = '''
                            SELECT *
                            FROM empleado
                            WHERE id IN 
                                (SELECT id
                                FROM usuario)
                            ORDER BY id DESC;
                        '''  
        cur.execute(sql_ver_usuarios)  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados
    except:                 # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def ver_usuario_id(id,cur,conn):
    if(type(id) is str):
        id = id.split('-')
        id = id[0]

    # se hace la consulta
    sql_check_usuario = '''        
                        SELECT empleado.id, empleado.nombre_1, empleado.nombre_2, empleado.nombre_3, empleado.apellido_p, empleado.apellido_m, empleado.vigencia, empleado.gerencia, empleado.departamento, empleado.seccion, empleado.fecha_de_ingreso, empleado.cargo, usuario.permisos 
                        FROM empleado, usuario
                        WHERE empleado.id = %s
                        AND empleado.id = usuario.id
                    '''
    try:                                # dentro de un try por si algo falla 
        cur.execute(sql_check_usuario,[id])
        return cur.fetchone()
    except:   # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def ver_usuario_param_id(id,cur,conn):
    if(type(id) is str):
        id = id.split('-')
        id = id[0]

    # se hace la consulta
    sql_check_usuario = '''        
                        SELECT id, permisos, usuario, contrasenna
                        FROM usuario
                        WHERE id = %s
                    '''
    try:                                # dentro de un try por si algo falla 
        cur.execute(sql_check_usuario,[id])
        return cur.fetchone()
    except:   # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def ver_usuarios(nombre,apellido,vigencia,orden,permisos,cur,conn):            # muestra los empleados con las restricciones dadas
    # se ponen en mayúsculas los parámetros    
    nombre = nombre.upper()             
    apellido = apellido.upper()         

    # consulta sql
    sql_ver_usuarios = ''' 
                        SELECT empleado.id, empleado.nombre_1, empleado.nombre_2, empleado.nombre_3, empleado.apellido_p, empleado.apellido_m, empleado.vigencia, empleado.gerencia, empleado.departamento, empleado.seccion, empleado.fecha_de_ingreso, empleado.cargo, usuario.permisos 
                        FROM empleado, usuario 
                        WHERE empleado.nombre_1 LIKE %s AND
                        empleado.apellido_p LIKE %s AND
                        empleado.vigencia LIKE %s AND
                        usuario.permisos LIKE %s AND
                        empleado.id = usuario.id
                        '''
    # dice en que orden estarán los resultados
    if(orden == 'ID ascendiente'):
        sql_ver_usuarios += 'ORDER BY id ASC'
    elif(orden == 'ID descendiente'):
        sql_ver_usuarios += 'ORDER BY id DESC'
    elif(orden == 'Fecha de ingreso ascendiente'):
        sql_ver_usuarios += 'ORDER BY fecha_de_ingreso ASC'
    elif(orden == 'Fecha de ingreso descendiente'):
        sql_ver_usuarios += 'ORDER BY fecha_de_ingreso DESC'

    # se devuelven todos los empleados que cumplen las condiciones
    try:                # en un try por si falla
        cur.execute(sql_ver_usuarios,['%'+nombre+'%','%'+apellido+'%','%'+vigencia+'%','%'+permisos+'%'])  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados        
    except:     # quizá poner un conn.rollback()
        conn.rollback()
        return None

def annadir_usuario_func(id,permisos,user,contrasenna,cur,conn):
    id = id.split('-')
    id = id[0]    


    try:    # en un try por si falla
        # se hace la inserción
        sql_insertar = '''
                        INSERT INTO usuario(id, permisos, usuario, contrasenna)
                        VALUES (%s, %s, %s, %s)
                    '''
        # se ejecuta la inserción
        cur.execute(sql_insertar, [id, permisos, user, contrasenna])
        conn.commit()
        return 1    # si se hace exitosamente retorna 1
    except psycopg2.errors.ForeignKeyViolation: # no está en la tabla empleado
        conn.rollback() # se hace rollback para abortar la transacción
        return 0   # y se retorna -1        
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1

def modificar_usuario_func(id,permisos,usuario,contrasenna,cur,conn):
    id = id.split('-')
    id = id[0]

    lista = [id,usuario,contrasenna,permisos]

    try: # en un try por si falla 
        # consulta para obtener los parámetros actuales
        sql_usuario = '''
                        SELECT *
                        FROM usuario
                        WHERE id = %s
                    '''
        cur.execute(sql_usuario,[id])
        usuario_param = cur.fetchone()       # se consiguen los parámetos actuales del usuario

        lista_usuario = [None]*4      # lista con none para los doce atributos

        for i in range(0,4):           # se llena la lista con los atributos de la tupla usuario
            lista_usuario[i] = usuario_param[i]

        for i in range(0,4):      # si algún campo en la interfaz se deja en blanco entonces se deja el parametro previo 
            if(lista[i] == '' ):
                lista[i] = lista_usuario[i]

        # se hace la actualización  
        sql_actualizar = '''
                        UPDATE usuario
                        SET usuario=%s,contrasenna=%s,permisos=%s
                        WHERE id = %s       
                    '''   
        cur.execute(sql_actualizar, [lista[1], lista[2], lista[3],lista[0]])
        conn.commit()
        return 1    # si se hace exitosamente retorna 1
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1

def eliminar_usuario_func(id,cur,conn):
    id = id.split('-')
    id = id[0]
    
    try:
        # se eliminan las entregas que tengan al usuario
        sql_eliminar_entregas = '''
                        DELETE FROM entrega
                        WHERE id_usuario = %s
                    '''
        
        cur.execute(sql_eliminar_entregas,[id])

        # se elimina al usuario
        sql_eliminar = '''
                        DELETE FROM usuario
                        WHERE id = %s
                    '''
        cur.execute(sql_eliminar,[id])
        conn.commit()
        return 1
    except:
        conn.rollback()
        return -1

def ver_todos_los_stock_func(cur,conn):       # retorna info de todos los empleados
    try:                            # en un try por si falla 
        sql_ver_stocks = '''
                            SELECT epp.codigo_constructor, epp.codigo_producto, epp.nombre, epp.constructor_designado, epp.talla, epp.unidad_medicion, epp.precio, stock.bodega, stock.cantidad, stock.cantidad_critica
                            FROM epp,stock
                            WHERE epp.codigo_producto = stock.codigo_epp
                            ORDER BY codigo_epp,bodega DESC;
                        '''  
        cur.execute(sql_ver_stocks)  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados
    except:                 # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def ver_stocks(c_construct,nombre,contruct_desig,talla,UM,orden,bodega,critico,cur,conn):
    nombre = nombre.upper()
    contruct_desig = contruct_desig.upper()
    UM = UM.upper()  
    talla = talla.upper()  

    # consulta sql
    sql_ver_stock = '''
                    SELECT epp.codigo_constructor, epp.codigo_producto, epp.nombre, epp.constructor_designado, epp.talla, epp.unidad_medicion, epp.precio, stock.bodega, stock.cantidad, stock.cantidad_critica
                    FROM epp,stock
                    WHERE epp.codigo_producto = stock.codigo_epp AND
                    epp.nombre LIKE %s AND
                    epp.constructor_designado LIKE %s AND
                    epp.unidad_medicion LIKE %s AND
                    stock.bodega LIKE %s
                    
                '''
    parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%','%'+bodega+'%']

    if(c_construct != '' and talla != ''):
        sql_ver_stock+= 'AND codigo_constructor = %s AND talla = %s '
        parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%', '%'+bodega+'%', c_construct, talla]
    elif(c_construct != ''):
        sql_ver_stock+= 'AND codigo_constructor = %s'
        parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%', '%'+bodega+'%', c_construct]
    elif(talla != ''):
        sql_ver_stock+= 'AND talla = %s'
        parametros = ['%'+nombre+'%','%'+contruct_desig+'%','%'+UM+'%', '%'+bodega+'%', talla]

    if(critico ==1):
        sql_ver_stock+= 'AND stock.cantidad <= stock.cantidad_critica ' 

    # dice en que orden estarán los resultados
    if(orden == 'Código de producto ascendiente'):
        sql_ver_stock += 'ORDER BY codigo_producto ASC'
    elif(orden == 'Código de producto descendiente'):
        sql_ver_stock += 'ORDER BY codigo_producto DESC'
    elif(orden == 'Precio ascendiente'):
        sql_ver_stock += 'ORDER BY precio ASC'
    elif(orden == 'Precio descendiente'):
        sql_ver_stock += 'ORDER BY precio DESC'
    elif(orden == 'Stock ascendiente'):
        sql_ver_stock += 'ORDER BY cantidad ASC'
    elif(orden == 'Stock descendiente'):
        sql_ver_stock += 'ORDER BY cantidad DESC'
    

    # se devuelven todos los empleados que cumplen las condiciones
    try:                # en un try por si falla
        cur.execute(sql_ver_stock,parametros)  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados     
    except:
        conn.rollback()
        return None   

def annadir_registro_stock_func(id,bodega,cantidad,cantidad_critica,cur,conn):
    try:
        if((int(cantidad)<0) or (int(cantidad_critica)<0)):
            return -1
    except:
        pass

    try:    # en un try por si falla
        # se hace la inserción
        sql_insertar = '''
                        INSERT INTO stock(codigo_epp, bodega, cantidad, cantidad_critica)
                        VALUES (%s, %s, %s, %s)
                    '''
        # se ejecuta la inserción
        cur.execute(sql_insertar, [id, bodega, cantidad, cantidad_critica])
        conn.commit()
        return 1    # si se hace exitosamente retorna 1
    except psycopg2.errors.ForeignKeyViolation: # no está en la tabla bodegas o epp
        conn.rollback() # se hace rollback para abortar la transacción
        return 0   # y se retorna -1      
    except psycopg2.errors.UniqueViolation:
        conn.rollback() # se hace rollback para abortar la transacción
        return -2   # y se retorna -1            
    except: # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return -1   # y se retorna -1    

def modificar_stock_epp(id,cantidad,bodega,cur,conn,commit):
        try:                                # dentro de un try por si algo falla 
            # se hace la inserción
            sql_cambiar_cantidad_epp = '''    
                                UPDATE stock
                                SET cantidad = %s
                                WHERE codigo_epp = %s AND
                                bodega = %s    
                            '''
            if(type(cantidad) == str):
                cantidad = int(cantidad)
            if(cantidad>=0):            # la cantidad de stock no puede ser menor a 0 
                cur.execute(sql_cambiar_cantidad_epp,[cantidad,id,bodega])
                if(commit):
                    conn.commit()
                return 1
            else:
                return 0    # no se puede tener menos de 0 en stock 
        except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
            conn.rollback()
            return -1

def sumar_restar_epp(id,cantidad,bodega,cur,conn,commit):       # cantidad postiva o negativa
    cantidad_nueva = get_stock_id(id,bodega,cur,conn)[0]+cantidad
    return modificar_stock_epp(id,cantidad_nueva,bodega,cur,conn,commit)

def modificar_stock_critico(id, cantidad, bodega, cur, conn):   # modifica cantidad crítica
        try:                                # dentro de un try por si algo falla 
            # se hace la inserción
            sql_cambiar_stock_critico_epp = '''    
                                UPDATE stock
                                SET cantidad_critica = %s
                                WHERE codigo_epp = %s AND
                                bodega = %s    
                            '''
            if(type(cantidad) == str):
                cantidad = int(cantidad)
            if(cantidad>=0):            # la cantidad de stock no puede ser menor a 0 
                cur.execute(sql_cambiar_stock_critico_epp,[cantidad,id,bodega])
                conn.commit()
                return 1
            else:
                return 0    # no se puede tener menos de 0 en stock 
        except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
            conn.rollback()
            return -1    

def get_stock_id(id_epp,bodega,cur,conn): 
    try:
        # se checkea la cantidad de stock en la bodega 
        sql_check_cantidad = '''                    
                            SELECT cantidad
                            FROM stock
                            WHERE codigo_epp = %s AND
                            bodega = %s
                        '''
        cur.execute(sql_check_cantidad,[id_epp,bodega])  # se ejecuta la consulta 
        conn.commit()
        return cur.fetchone()
    except:
        conn.rollback()
        return None

def eliminar_registro_stock(id,bodega,cur,conn):
    try:
        sql_eliminar = '''
                        DELETE FROM stock
                        WHERE codigo_epp = %s AND
                        bodega = %s
                    '''
        cur.execute(sql_eliminar,[id,bodega])
        conn.commit()
        return 1
    except:
        conn.rollback()
        return -1

def ver_todas_las_entregas_func(cur,conn):
    try:                            # en un try por si falla 
        sql_ver_entregas = '''
                            SELECT *
                            FROM entrega
                            ORDER BY fecha_y_hora DESC
                            LIMIT 100;
                        '''  
        cur.execute(sql_ver_entregas)  # se ejecuta la consulta
        return cur.fetchall()           # y se retornan todos los resultados
    except:                 # si falla
        conn.rollback() # se hace rollback para abortar la transacción
        return None

def tiempo_actual(cur,conn):
    try:
        # se consigue el tiempo actual
        sql_timestamp = '''     
                            SELECT now()::timestamp(0);
                        '''
        cur.execute(sql_timestamp)          # se ejecuta la consulta
        return (cur.fetchone())[0]    # se guarda la fecha y hora  
    except:
        conn.rollback() # rollback si falla
        return None

def hacer_entrega(id_usuario,id_empleado,id_epp,cantidad,bodega,razon,cur,conn, commit):                  # función para hacer una retiro de epp
    try:
        if(type(id_usuario) == str):
            id_usuario = id_usuario.split('-')
            id_usuario = id_usuario[0]

        if(type(id_empleado) == str):
            id_empleado = id_empleado.split('-')
            id_empleado = id_empleado[0]



        if(type(cantidad) is str):
            cantidad = int(cantidad) 

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
        precio_total = precio*cantidad      # precio total
        precio_total - abs(precio_total) 

        # se inserta en la tabla entrega
        sql_insertar = '''
                            INSERT INTO entrega (id_usuario, id_empleado, id_epp, precio_en_transaccion, cantidad, precio_total, fecha_y_hora, bodega)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        '''
        if razon != '':
            sql_insertar = '''
                                INSERT INTO entrega (id_usuario, id_empleado, id_epp, precio_en_transaccion, cantidad, precio_total, fecha_y_hora, bodega, razon)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            '''     
            cur.execute(sql_insertar, [id_usuario, id_empleado, id_epp, precio, cantidad, precio_total, fecha_hora, bodega, razon])
        else:
            cur.execute(sql_insertar, [id_usuario, id_empleado, id_epp, precio, cantidad, precio_total, fecha_hora, bodega])

        if(commit):
            conn.commit()   # se le hacen commit a los cambios
        return 1
    except:
        conn.rollback()
        return -1

def ver_entregas(id_usuario,id_empleado,id_epp,bodega,antes_de,depues_de,orden, cur, conn):
    try:
        id_usuario = id_usuario.split('-')
        id_usuario = id_usuario[0]
    except:
        pass

    try:
        id_empleado = id_empleado.split('-')
        id_empleado = id_empleado[0]
    except:
        pass



    parametros = [id_usuario,id_empleado,id_epp,bodega,antes_de,depues_de,orden]
    filtros = False   # se asume que no se dan filtro al principio

    for parametro in parametros:
        if parametro != '':
            filtros = True


    # consulta sql
    if(not filtros):
        sql_ver_entregas = '''
                        SELECT *
                        FROM entrega
                    '''
    else:
        sql_ver_entregas = '''
                        SELECT *
                        FROM entrega
                        WHERE (1=1)
                    '''

        if(id_usuario == ''):
            sql_ver_entregas += ' AND ((1=1) OR bodega = %s)'
        else:
            sql_ver_entregas += ' AND id_usuario = %s'

        if(id_empleado == ''):
            sql_ver_entregas += ' AND ((1=1)  OR bodega = %s)'
        else:
            sql_ver_entregas += ' AND id_empleado = %s'

        if(id_epp == ''):
            sql_ver_entregas += ' AND ((1=1)  OR bodega = %s )'
        else:
            sql_ver_entregas += ' AND id_epp = %s'

        if(bodega == ''):
            sql_ver_entregas += ' AND ((1=1)  OR bodega = %s)'
        else:
            sql_ver_entregas += ' AND bodega = %s'

        if(antes_de == ''):
            sql_ver_entregas += ' AND ((1=1) OR bodega = %s)'
        else:
            sql_ver_entregas += ' AND fecha_y_hora < %s'

        if(depues_de == ''):
            sql_ver_entregas += ' AND ((1=1) OR bodega = %s)'
        else:
            sql_ver_entregas += ' AND fecha_y_hora > %s'

    if(orden == 'Fecha ascendiente'):
        sql_ver_entregas += 'ORDER BY fecha_y_hora ASC'
    elif(orden == 'Fecha descendiente'):
        sql_ver_entregas += 'ORDER BY fecha_y_hora DESC'
    elif(orden == 'Precio ascendiente'):
        sql_ver_entregas += 'ORDER BY precio_en_transaccion DESc'
    elif(orden == 'Precio descendiente'):
        sql_ver_entregas += 'ORDER BY precio_en_transaccion ASC'
    elif(orden == 'Precio total ascendiente'):
        sql_ver_entregas += 'ORDER BY precio_total DESC'
    elif(orden == 'Precio total descendiente'):
        sql_ver_entregas += 'ORDER BY precio_total ASC'

    sql_ver_entregas+= ' LIMIT 500'

 
    # se devuelven todos los empleados que cumplen las condiciones
    try:                # en un try por si falla
        cur.execute(sql_ver_entregas,[parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5]])  # se ejecuta la consulta
        conn.commit()
        return cur.fetchall()           # y se retornan todos los resultados        
    except:     # quizá poner un conn.rollback()
        conn.rollback()
        return None    

def vale_de_salida(cur,conn):
    try:
        # se consigue el "serial" de vale de salida
        sql_vale_de_salida = '''     
                            SELECT numero
                            FROM pdf 
                            WHERE name = 'vale de salida'
                            '''
        cur.execute(sql_vale_de_salida)          # se ejecuta la consulta
        numero_vale = cur.fetchone()[0]

        sql_aumentar_vale_de_salida = '''
                            UPDATE pdf
                            SET numero = %s
                            WHERE name = 'vale de salida'
                        '''
        cur.execute(sql_aumentar_vale_de_salida,[numero_vale+1])
        conn.commit()
        return numero_vale    # se guarda la fecha y hora  
    except:
        conn.rollback() # rollback si falla
        return None


