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

def bodeguero_en_db_id(id,cur):             # dice si el empleado está en la base de datos, si retorna 1 está, si retorna -1 no está 
    try:                                # dentro de un try por si algo falla 
        # se hace la consulta
        sql_check_bodeguero = '''        
                            SELECT id_bodeguero
                            FROM bodeguero
                            WHERE id_bodeguero = %s
                        '''
        cur.execute(sql_check_bodeguero,[id])
        if(cur.fetchone() == None):     # si es none entonces no está en la base de datos
            return 0
        else:                           # si es que retorna, entonces si está
            return 1 
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
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

def ver_bodega_nombre(nombre,cur,conn):
    # se hace la consulta
    sql_check_bodega = '''        
                        SELECT *
                        FROM bodega
                        WHERE nombre = %s
                    '''
    try:                                # dentro de un try por si algo falla 
        cur.execute(sql_check_bodega,[nombre])
        return cur.fetchone()
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        conn.rollback() # se hace rollback para abortar la transacción
        return None    

def ver_epp_nombre(nombre,cur):   # muestra la info del epp
    try:                                # dentro de un try por si algo falla 
        nombre = nombre.upper()
        # se hace la consulta
        sql_check_epp = '''        
                            SELECT *
                            FROM epp
                            WHERE nombre LIKE %s 
                        '''
        cur.execute(sql_check_epp,['%'+nombre+'%'])
        return cur.fetchone()
    except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
        pass

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
    # se ponen en mayúsculas los parámetros    
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
                                ORDER BY codigo_producto DESC;
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





def modificar_cantidad_epp(id,cantidad,lugar,cur,conn):
        try:                                # dentro de un try por si algo falla 
            # se hace la inserción
            sql_cambiar_cantidad_epp = '''    
                                UPDATE stock
                                SET cantidad = %s
                                WHERE codigo_epp = %s AND
                                lugar = %s    
                            '''
            if(cantidad>=0):            # la cantidad de stock no puede ser menor a 0 
                cur.execute(sql_cambiar_cantidad_epp,[cantidad,id,lugar])
                conn.commit()
                return 1
            else:
                return 0
        except:                             # si algo sale mal (error de formato por ejemplo, se retorna -1)
            return -1

def sumar_restar_epp(id,cantidad,lugar,cur,conn):       # cantidad postiva o negativa
    try:
        cantidad_nueva = get_stock_id(id,lugar,cur)+cantidad
        modificar_cantidad_epp(id,cantidad_nueva,lugar,cur,conn)
    except:
        pass

def get_stock_id(id_epp,lugar,cur): 
    try:
        # se checkea la cantidad de stock en la bodega 
        sql_check_cantidad = '''                    
                            SELECT *
                            FROM stock
                            WHERE codigo_epp = %s AND
                            lugar = %s
                        '''
        cur.execute(sql_check_cantidad,[id_epp,lugar])  # se ejecuta la consulta 
        return cur.fetchone()[0]
    except:
        pass



#CORREGIR, HACER CONSULTA GRANDE

# def get_stock_nombre(nombre,lugar,cur):
#     # se checkea la cantidad de stock en la bodega 
#     sql_check_cantidad = '''                    
#                         SELECT *
#                         FROM stock
#                         WHERE nombre LIKE %s AND
#                         lugar = %s
#                     '''
#     cur.execute(sql_check_cantidad,['%'+nombre+'%',lugar])  # se ejecuta la consulta 
#     return cur.fetchall()
 

def hacer_entrega(id_bodeguero,id_empleado,id_epp,cantidad,lugar,razon,cur,conn):                  # función para hacer una retiro de ep

    cantidad_real = get_stock_id(id_epp, lugar,cur)    # se calcula la cantidad real 

    if(cantidad_real == None):      # si es que no se pudo encontrar en la base de datos entonces los parámetros no eran válidos
        print('Porfavor ingrese un código y bodega válidos')
    elif(cantidad_real[2] < cantidad): # si la cantidad real es menor que la pedida entonces no se puede hacer el pedido  
        print('No hay suficiente stock en la bodega para realizar la transaccion')
    else:                           # si hay stock suficiente 
        cantidad_nueva = cantidad_real[2]-cantidad     # se calcula la cantidad nueva
        
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



