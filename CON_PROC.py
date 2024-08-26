from typing import Counter
import mysql.connector
from mysql.connector import Error

#Buscar producto (si se pasa una tupla se cae xd)
def buscarprod (datos)  :
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT id_prod,nom,cant,cod_bar,prec,marca FROM producto WHERE nom like '%{}%' and activo=True"
            cursor.execute(sentencia.format(datos))
            resultados = cursor.fetchall()
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados

def buscarprodVenta (datos)  :
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT p.nom,sl.cant,p.cod_bar,p.prec,p.marca,p.id_prod FROM producto as p, stock_local as sl WHERE p.id_prod=sl.id_prod and p.nom like '%{}%' and p.activo=True and sl.cant>0"
            cursor.execute(sentencia.format(datos))
            resultados = cursor.fetchall()
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados
                        
def buscarprodUnico (nom,codigo)  :
    resultados=[]
    resultadosTotales=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT id_prod,nom,cant,cod_bar,prec,marca FROM producto WHERE nom='{}' and cod_bar={} and activo=True"
            cursor.execute(sentencia.format(nom,codigo))
            resultados = cursor.fetchall()
            id_prod=resultados[0][0]
            resultadosTotales=resultados[0]
            sentencia = "SELECT cant FROM stock_bodega WHERE id_prod={} and id_bod={}"
            cursor.execute(sentencia.format(id_prod,1))
            resultados = cursor.fetchall()
            resultadosTotales+=resultados[0]
            sentencia = "SELECT cant FROM stock_local WHERE id_prod={} and id_loc={}"
            cursor.execute(sentencia.format(id_prod,1))
            resultados = cursor.fetchall()
            resultadosTotales+=resultados[0]
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultadosTotales
        return resultadosTotales

#Agregar producto
def agregarprod (datos)  :
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "INSERT INTO producto (nom, cant, cod_bar, prec, marca,activo) VALUES ('{0}',{1},{2},{3},'{4}',True)".format(datos[0], datos[1], datos [2],datos [3],datos[4])
            cursor.execute(sentencia)
            sentencia = "SELECT id_prod FROM producto WHERE nom='{}' and cod_bar={}"
            cursor.execute(sentencia.format(datos[0],datos [2]))
            resultados = cursor.fetchall()
            sentencia = "INSERT INTO stock_bodega (id_prod, id_bod, cant) VALUES ({0},{1},{2})".format(resultados[0][0], 1,datos[6])
            cursor.execute(sentencia)
            sentencia = "INSERT INTO stock_local (id_prod, id_loc, cant) VALUES ({0},{1},{2})".format(resultados[0][0], 1,datos[5])
            cursor.execute(sentencia)
            conexion.commit()
            print("Registro insertado con exito") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")

#Eliminar producto
def eliminarProd (datos)  :
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("conexion exitosa.")
            cursor=conexion.cursor()

            sentencia = "SELECT id_prod FROM producto WHERE nom='{}' and cod_bar={}"
            cursor.execute(sentencia.format(datos[0],datos[1]))
            resultados = cursor.fetchall()

            sentencia = "UPDATE stock_bodega SET cant=0 where id_prod={}".format(resultados[0][0])
            cursor.execute(sentencia)
            
            sentencia = "UPDATE stock_local SET cant=0 WHERE id_prod={}".format(resultados[0][0])
            cursor.execute(sentencia)

            sentencia = "UPDATE producto SET activo=False WHERE nom='{}' AND cod_bar ={}".format(datos[0],datos[1])
            cursor.execute(sentencia)
            conexion.commit()
            print("Registro eliminado con exito") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
                
#Actualizar producto
def actualizarProd (datos,_sentencia)  :
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = _sentencia
            cursor.execute(sentencia.format(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5]))
            conexion.commit()
            print("Registro actualizado con exito") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")

def existe (nom,cod)  :
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT id_prod,nom,cant,cod_bar,prec,marca FROM producto WHERE nom='{}' and cod_bar={} and activo=True"
            cursor.execute(sentencia.format(nom,cod))
            resultados = cursor.fetchall()
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
    if resultados==[]:
        return False
    return True
 
            
#MOSTRAR STOCK DE UN PRODUCTO (SE PUEDE ARREGLAR)
def buscarstockUnico (nom)  :
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT DISTINCT producto.nom as nombre, stock_local.cant as stock_Local, stock_bodega.cant as stock_Bodega FROM producto, stock_local, stock_bodega WHERE producto.nom = '{}'"
            cursor.execute(sentencia.format(nom))
            resultados = cursor.fetchall()
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados

#MOSTRAR STOCK EN TIENDA DE LOS PRODUCTOS CON STOCK IGUAL Y MAYOR A 0
def stockLocal ( )  :
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT DISTINCT producto.cant, nom AS nombre, cod_bar AS codigo_de_barra, stock_local.cant AS stockLocal FROM producto, stock_local WHERE stock_local.cant>=0"
            cursor.execute(sentencia)
            resultados = cursor.fetchall()
            for fila in resultados  :
                print("{:<8} {:<34} {:<13} {:<10}".format(fila[0], fila[1],fila[2],fila[3]))
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados 
    

#MOSTRAR STOCK EN BODEGA DE LOS PRODUCTOS CON STOCK IGUAL Y MAYOR A 0
def stockBodega ( )  :
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT DISTINCT producto.cant, nom AS nombre, cod_bar AS codigo_de_barra, stock_bodega.cant AS stockBodega FROM producto, stock_bodega WHERE stock_bodega.cant>=0"
            cursor.execute(sentencia)
            resultados = cursor.fetchall()
            for fila in resultados  :
                print("{:<8} {:<34} {:<13} {:<10}".format(fila[0], fila[1],fila[2],fila[3]))
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados 

def actualizarStockLocal (nom,cod,cant)  :
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT id_prod,cant FROM producto WHERE cod_bar = {} and nom='{}'"
            cursor.execute(sentencia.format(cod,nom))
            resultados = cursor.fetchall()
            id_producto=resultados[0][0]
            sentencia = "UPDATE producto SET cant={} WHERE id_prod = {} "
            cursor.execute(sentencia.format(resultados[0][1]+cant,id_producto))
            sentencia = "SELECT cant FROM stock_local WHERE id_prod = {} and id_loc={}"
            cursor.execute(sentencia.format(id_producto,1))
            resultados = cursor.fetchall()
            sentencia = "UPDATE stock_local SET cant={} WHERE id_prod={} and id_loc={}"
            cursor.execute(sentencia.format(resultados[0][0]+cant,id_producto,1))
            conexion.commit()
            print("Registro actualizado con exito") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")

def actualizarStockBodega (nom,cod,cant)  :
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT id_prod,cant FROM producto WHERE cod_bar = {} and nom='{}'"
            cursor.execute(sentencia.format(cod,nom))
            resultados = cursor.fetchall()
            id_producto=resultados[0][0]
            sentencia = "UPDATE producto SET cant={} WHERE id_prod = {} "
            cursor.execute(sentencia.format(resultados[0][1]+cant,id_producto))
            sentencia = "SELECT cant FROM stock_bodega WHERE id_prod = {} and id_bod={}"
            cursor.execute(sentencia.format(id_producto,1))
            resultados = cursor.fetchall()
            sentencia = "UPDATE stock_bodega SET cant={} WHERE id_prod={} and id_bod={}"
            cursor.execute(sentencia.format(resultados[0][0]+cant,id_producto,1))
            conexion.commit()
            print("Registro actualizado con exito") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")

def actualizarStockLocalBodega (nom,cod,cant)  :
    ret=True
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT id_prod,cant FROM producto WHERE cod_bar = {} and nom='{}'"
            cursor.execute(sentencia.format(cod,nom))
            resultados = cursor.fetchall()
            id_producto=resultados[0][0]
            sentencia = "SELECT cant FROM stock_bodega WHERE id_prod = {} and id_bod={}"
            cursor.execute(sentencia.format(id_producto,1))
            resultados = cursor.fetchall()
            resta=resultados[0][0]-cant
            if resta>=0:
                sentencia = "SELECT cant FROM stock_local WHERE id_prod = {} and id_loc={}"
                cursor.execute(sentencia.format(id_producto,1))
                resultados = cursor.fetchall()
                sentencia = "UPDATE stock_local SET cant={} WHERE id_prod={} and id_loc={}"
                cursor.execute(sentencia.format(resultados[0][0]+cant,id_producto,1))
                sentencia = "UPDATE stock_bodega SET cant={} WHERE id_prod={} and id_bod={}"
                cursor.execute(sentencia.format(resta,id_producto,1))
                conexion.commit()
                print("Registro actualizado con exito") 
                ret=True
            else:
                ret=False
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return ret

def stocks_loc_bod(sentencia):
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            cursor.execute(sentencia)
            resultados = cursor.fetchall()
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados 
    
def stock_producto(nom,cod):
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "SELECT id_prod,nom,cant,cod_bar,prec,marca FROM producto WHERE nom='{}' and cod_bar={} and activo=True"
            cursor.execute(sentencia.format(nom,cod))
            resultados = cursor.fetchall()
            id_prod=resultados[0][0]
            sentencia = "select p.nom,p.cod_bar,p.prec,p.marca,p.cant,sl.cant as cant_loc,l.nom as nom_loc,sb.cant as cant_bod,b.direcb from producto as p, stock_local as sl, locall as l, stock_bodega as sb, bodega as b where sl.id_loc=l.id_loc and sl.id_prod=p.id_prod and sb.id_bod=b.id_bod and sb.id_prod=p.id_prod and p.id_prod={};"
            cursor.execute(sentencia.format(id_prod))
            resultados = cursor.fetchall()
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados

def ingresoVentas(lista_id,monto)  :
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
    )
        if conexion.is_connected() :
            print("conexion exitosa.")
            cursor=conexion.cursor()
            sentencia = "select MAX(cod_ven) from venta_diaria;"
            cursor.execute(sentencia)
            resultados = cursor.fetchall()
            if resultados[0][0]==None:
                cod_venta=1
            else:
                cod_venta=resultados[0][0]+1
            sentencia = "INSERT INTO venta_diaria (cod_ven,fecha,hora,mon_tot,id_loc) VALUES({},NOW(),NOW(),{},1);"
            cursor.execute(sentencia.format(cod_venta,monto))
            conexion.commit()
            for dato in lista_id:
                sentencia = "INSERT INTO producto_vendido (id_prod,cant,cod_ven) VALUES({},{},{});"
                cursor.execute(sentencia.format(dato[0],dato[1],cod_venta))
                sentencia = "SELECT p.cant,sl.cant FROM producto as p, stock_local as sl WHERE p.id_prod=sl.id_prod and p.id_prod={};"
                cursor.execute(sentencia.format(dato[0]))
                resultados = cursor.fetchall()
                sentencia = "UPDATE stock_local SET cant={} WHERE id_prod={} and id_loc=1"
                cursor.execute(sentencia.format(resultados[0][1]-dato[1],dato[0]))
                sentencia = "UPDATE producto SET cant={} WHERE id_prod={}"
                cursor.execute(sentencia.format(resultados[0][0]-dato[1],dato[0]))
            conexion.commit()
            print("Registro actualizado con exito") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")

def informeVentas(sentencia,fechaIni,fechaFin):
    resultados=[]
    try :
        conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'admin1234',
        db = 'todomarket_vip'
        )
        if conexion.is_connected() :
            print("Conexion exitosa.")
            cursor=conexion.cursor()
            cursor.execute(sentencia.format(fechaIni,fechaFin))
            resultados = cursor.fetchall()
        else    :
            print("Dato no encontrado") 
    except Error as ex :
        print("Error de conexion", ex)
    finally :
        if  conexion.is_connected() :
            conexion.close() #cierro conexion con la base
            print("Conexion finalizada.")
            return resultados
        return resultados

    #PPRUEBAS
nombre = 'azucar '#'coca cola' #"pampita"
cantidad = 10 #110
codigo_de_barras = 55
precio = 1500 #20000
    
producto = (nombre, cantidad, codigo_de_barras, precio) 
 
#agregarprod(producto)  
#eliminarProd(producto)
#actualizarProd(producto)
#buscarprod('azucar') 
#buscar = buscarstockUnico('leche')
#for fila in buscar  :
    #print(fila[0], fila[1], fila[2])
