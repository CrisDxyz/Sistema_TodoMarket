from logging import lastResort
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import CON_PROC
import pandas as pd

def cambiarFrame(frame,revVentas,ventas,actDatos,añadirProd,verStock,actStock):
    if frame == "ventas":
        actStock.grid_remove()
        verStock.grid_remove()
        añadirProd.grid_remove()
        actDatos.grid_remove()
        revVentas.grid_remove()
        ventas.grid(row=0, rowspan=100, column=1, columnspan=100, sticky=NSEW)
        ventas.grid_propagate(False)
    if frame == "revVentas":
        actStock.grid_remove()
        verStock.grid_remove()
        añadirProd.grid_remove()
        actDatos.grid_remove()
        ventas.grid_remove()
        revVentas.grid(row=0, rowspan=100, column=1, columnspan=100, sticky=NSEW)
        revVentas.grid_propagate(False)
    if frame == "actDatos":
        actStock.grid_remove()
        verStock.grid_remove()
        añadirProd.grid_remove()
        ventas.grid_remove()
        revVentas.grid_remove()
        actDatos.grid(row=0, rowspan=100, column=1, columnspan=100, sticky=NSEW)
        actDatos.grid_propagate(False)
    if frame == "verDatos":
        actStock.grid_remove()
        verStock.grid_remove()
        ventas.grid_remove()
        revVentas.grid_remove()
        actDatos.grid_remove()
        añadirProd.grid(row=0, rowspan=100, column=1, columnspan=100, sticky=NSEW)
        añadirProd.grid_propagate(False)
    if frame == "verStock":
        actStock.grid_remove()
        añadirProd.grid_remove()
        ventas.grid_remove()
        revVentas.grid_remove()
        actDatos.grid_remove()
        verStock.grid(row=0, rowspan=100, column=1, columnspan=100, sticky=NSEW)
        verStock.grid_propagate(False)
    if frame == "actStock":
        verStock.grid_remove()
        añadirProd.grid_remove()
        ventas.grid_remove()
        revVentas.grid_remove()
        actDatos.grid_remove()
        actStock.grid(row=0, rowspan=100, column=1, columnspan=100, sticky=NSEW)
        actStock.grid_propagate(False)


def buscarAdmVentas(dato,lbox,lista_id):
    resultados=CON_PROC.buscarprodVenta(dato)
    lbox.delete(0, END)
    for item in range(len(resultados)):
        lbox.insert(END, resultados[item][0]+' - "'+resultados[item][4]+'" - ('+str(resultados[item][1])+') - $'+str(resultados[item][3]))
        lbox.itemconfig(item)
        lista_id.append(resultados[item][5])

def getPrecio(dato):
    precio=''
    for letra in reversed(dato):
        if letra == '$' or letra == ' ':
            break
        precio=letra+precio
    return int(precio)

def getCant(dato):
    cantidad1=''
    cantidad=''
    for letra in dato:
        if letra == ')':
            break
        cantidad1=cantidad1+letra
    for letra in reversed(cantidad1):
        if letra == '(':
            break
        cantidad=letra+cantidad
    return int(cantidad)

def updateDatos(datos,cant):
    mitad1=''
    mitad2=''
    for letra in datos:
        mitad1=mitad1+letra
        if letra == '(':
            break
    for letra in reversed(datos):
        mitad2=letra+mitad2
        if letra == ')':
            break
    return mitad1+str(cant)+mitad2

def datosFrame2(datos):
    mitad1=''
    mitad2=''
    for letra in datos:
        if letra == '(':
            break
        mitad1=mitad1+letra
    for letra in reversed(datos):
        if letra == ')':
            break
        mitad2=letra+mitad2
    return mitad1[:len(mitad1)-2]+mitad2

def updateLbox(lbox,cant,datoAct):
    for i in range(lbox.size()):
        if lbox.get(i)==datoAct:
            lbox.delete(i)
            lbox.insert(i, updateDatos(datoAct,cant))

def mismoProducto(dato1,dato2):
    if datosFrame2(dato1)==dato2:
        return True
    else:
        return False

def updateLboxBorrar(lbox,datoAct):
    for i in range(lbox.size()):
        if mismoProducto(lbox.get(i),datoAct):
            datos=lbox.get(i)
            cant=getCant(lbox.get(i))
            lbox.delete(i)
            lbox.insert(i, updateDatos(datos,cant+1))

def agregarAdmVentas(lbox, lbox2,totalVenta,Lista_id,Lista_id_venta):
    selecciones=[]
    for i in lbox.curselection():
        ag = lbox.get(i)
        cant=getCant(ag)
        if cant>0:
            Lista_id_venta.append(Lista_id[i])
            updateLbox(lbox,cant-1,ag)
            selecciones.append(ag)
    for item in range(len(selecciones)):
        venta=getPrecio(selecciones[item])+getPrecio(totalVenta['text'])
        totalVenta['text']="Total: "+str(venta)
        lbox2.insert(END, datosFrame2(selecciones[item]))
        lbox2.itemconfig(item)

def borrarAdmVentas(lbox,lbox2,totalVenta,lista_id_ventas):
    seleccion = lbox2.curselection()
    pos = 0
    for i in seleccion:
        indice = int(i) - pos
        venta=getPrecio(totalVenta['text'])-getPrecio(lbox2.get(indice))
        totalVenta['text']="Total: "+str(venta)
        updateLboxBorrar(lbox,lbox2.get(indice))
        lbox2.delete(indice,indice)
        del lista_id_ventas[indice]
        pos = pos + 1

def venderAdmVentas(lbox,lista_id_ventas,totalLabel_ventas):
    if lista_id_ventas!=[]:
        lista_cant=[]
        lista_cant.append([lista_id_ventas[0],1])
        for i in range(1,len(lista_id_ventas)):
            agregar=True
            for j in range(len(lista_cant)):
                if lista_id_ventas[i]==lista_cant[j][0]:
                    agregar=False
                    lista_cant[j][1]+=1
            if agregar:
                lista_cant.append([lista_id_ventas[i],1])
        CON_PROC.ingresoVentas(lista_cant,getPrecio(totalLabel_ventas['text']))
        lbox.delete(0,END)
        totalLabel_ventas['text']="Total: 0"
        messagebox.showinfo(message="la venta se realizó con éxito", title="Venta")
        

def verificar_datos_act(codigo,precio,label):
    try:
        if codigo!='':
            codigo=int(codigo)
            if codigo<0:
                label['text']='Error en el tipo de dato codigo barra'
                label.grid(row=7,column=5,sticky=NSEW)
                return False
        if precio!='':
            precio=int(precio)
            if precio<=0:
                label['text']='Error precio menor a 0'
                label.grid(row=7,column=5,sticky=NSEW)
                return False
    except:
        label['text']='Error en el tipo de dato'
        label.grid(row=7,column=5,sticky=NSEW)
        return False
    return True

def sentecia_actualizar(nombre,codigo,precio,marca,codigoAntiguo,datoAntiguo):
    sentencia = "UPDATE producto SET"
    segundo=False
    cant=0
    datos=[]
    actualiza=False
    if nombre!='':
        actualiza=True
        sentencia = sentencia+" nom='{}'"
        segundo=True
        datos.append(nombre)
        cant+=1
    if codigo!='':
        actualiza=True
        if segundo:
            sentencia = sentencia+", cod_bar ={}"
            datos.append(codigo)
            cant+=1
        else:
            segundo=True
            sentencia = sentencia+" cod_bar ={}"
            datos.append(codigo)
            cant+=1
    if precio!='':
        actualiza=True
        if segundo:
            sentencia = sentencia+", prec ={}"
            datos.append(precio)
            cant+=1
        else:
            segundo=True
            sentencia = sentencia+" prec ={}"
            datos.append(precio)
            cant+=1
    if marca!='':
        actualiza=True
        if segundo:
            sentencia = sentencia+", marca ='{}'"
            datos.append(marca)
            cant+=1
        else:
            segundo=True
            sentencia = sentencia+" marca ='{}'"
            datos.append(marca)
            cant+=1
    sentencia = sentencia+" WHERE cod_bar = {} and nom='{}' #"
    datos.append(codigoAntiguo)
    datos.append(datoAntiguo)
    while cant < 4:
        sentencia = sentencia+"{}"
        cant+=1
        datos.append(0)
    return actualiza,datos,sentencia

def separNomCod(dato):
    pos=0
    codigo=[]
    for letra in reversed(dato):
        if letra == ' ':
            break
        pos+=1
    if pos >= len(dato):
        codigo=0
    else:
        codigo=dato[len(dato)-pos:]
    dato=dato[:len(dato)-pos-1]
    if dato[0]=='{':
        dato=dato[1:len(dato)-1]
    return codigo,dato

def actualizar_datos(nombre,codigo,precio,marca,label,datoAntiguo):
    label.grid_remove()
    if datoAntiguo!='':
        codigoAntiguo,datoAntiguo=separNomCod(datoAntiguo)
        if verificar_datos_act(codigo.get(),precio.get(),label):
            if CON_PROC.existe(datoAntiguo,codigoAntiguo):
                actualiza=False
                actualiza,datos,sentencia=sentecia_actualizar(nombre.get(),codigo.get(),precio.get(),marca.get(),codigoAntiguo,datoAntiguo)
                if actualiza:
                    CON_PROC.actualizarProd(datos,sentencia)
                    messagebox.showinfo(message='Se ha actualizado con éxito',title='actualización')
    nombre.delete(0,END)
    codigo.delete(0,END)
    precio.delete(0,END)
    marca.delete(0,END)

def verificar_datos(codigo,precio,label):
    try:
        codigo=int(codigo)
        precio=int(precio)
        if codigo<0:
            label['text']='Error en el tipo de dato codigo barra'
            label.grid(row=6,column=2,stick=NSEW)
            return False
        elif precio<=0:
            label['text']='Error precio menor a 0'
            label.grid( row=6,column=2,stick=NSEW)
            return False
    except:
        label['text']='Error en el tipo de dato'
        label.grid(row=6,column=2,stick=NSEW)
        return False
    return True

def verificar_datos_stock(_local,_bodega,label):
    try:
        local=int(_local)
        bodega=int(_bodega)
        if bodega < 0:
            label['text']='Error cantidad bodega menor a 0'
            label.grid(row=6,column=2,stick=NSEW)
            return False
        elif local<0:
            label['text']='Error cantidad local menor a 0'
            label.grid( row=6,column=2,stick=NSEW)
            return False
    except:
        if _local!='' or _bodega!='':
            label['text']='Error en el tipo de dato'
            label.grid(row=8,column=2,stick=NSEW)
            return False
        return True
    return True

def getCantidad(_cantLocal,_cantBodega):
    cantLocal=_cantLocal
    cantBodega=_cantBodega
    if _cantLocal=='':
        cantLocal=0
    if _cantBodega=='':
        cantBodega=0
    return cantLocal,cantBodega

def añadir_productos(cuadroNombre,cuadroCod,cuadroPrec,cuadroMarca,cuadroLocal,cuadroBodega,label_errorProd):
    label_errorProd.grid_remove()
    if verificar_datos(cuadroCod.get(),cuadroPrec.get(),label_errorProd) and verificar_datos_stock(cuadroLocal.get(),cuadroBodega.get(),label_errorProd):
        cantLocal,cantBodega=getCantidad(cuadroLocal.get(),cuadroBodega.get())
        nuevos_datos(cuadroNombre.get(),cuadroCod.get(),cuadroPrec.get(),cuadroMarca.get(),cantLocal,cantBodega)
    cuadroMarca.delete(0,END)
    cuadroCod.delete(0,END)
    cuadroPrec.delete(0,END)
    cuadroNombre.delete(0,END)
    cuadroLocal.delete(0,END)
    cuadroBodega.delete(0,END)

def nuevos_datos(nombre,codigo,precio,marca,cantLocal,cantBodega):
    if nombre!='':
        datos=[nombre,int(cantLocal)+int(cantBodega),codigo,precio,marca,cantLocal,cantBodega]
        CON_PROC.agregarprod(datos)
        messagebox.showinfo(message='El producto se añadió con éxito',title='Añadir')
    else:
        messagebox.showinfo(message='No ha insertado nombre de producto',title='Añadir')

def cantCorrecta(cant,label):
    try:
        cant=int(cant)
        if cant<=0:
            label['text']='Cantidad menor o igual a 0'
            return False
        return True
    except:
        label['text']='Tipo de dato erroneo'
        return False

def actualizar_stock(cant,opcion,label,nom,cod,opcionLocal):
    _cant=cant.get()
    cant.delete(0,END)
    label['text']=""
    if nom['text']==" " or cod['text']==" ":
        label['text']="Seleccione un Producto"
    elif opcion == 'None':
        label['text']="Marque un destino"
    elif cantCorrecta(_cant,label):
        if opcion == 'Tienda':
            if opcionLocal=='0' and CON_PROC.existe(nom['text'],cod['text']):
                CON_PROC.actualizarStockLocal(nom['text'],cod['text'],int(_cant))
                messagebox.showinfo(message='El producto se actualizo con éxito',title='Actualizar Datos')
            elif opcionLocal=='1'and CON_PROC.existe(nom['text'],cod['text']):
                if not(CON_PROC.actualizarStockLocalBodega(nom['text'],cod['text'],int(_cant))):
                    label['text']="No hay cantidad suficiente en bodega"
                else:
                    messagebox.showinfo(message='El producto se actualizo con éxito',title='Actualizar Datos')
            else:
                label['text']="Marque una opcion"
        elif opcion == 'Bodega' and CON_PROC.existe(nom['text'],cod['text']):
            CON_PROC.actualizarStockBodega(nom['text'],cod['text'],int(_cant))
            messagebox.showinfo(message='El producto se actualizo con éxito',title='Actualizar Datos')

def actualizarLista(buscarCuadro_revVentas,busqueda):
    lista=CON_PROC.buscarprod(busqueda)
    aux=[]
    for fila in lista:
        aux.append([fila[1],fila[3]])
    buscarCuadro_revVentas['values']=tuple(aux)

def actualizarListaINI(busqueda):
    lista=CON_PROC.buscarprod(busqueda)
    aux=[]
    for fila in lista:
        aux.append([fila[1],fila[3]])
    return tuple(aux)

def MostrarStock(combobox,nombre,codigo,precio,marca,stock,bodega,local):
    if combobox.get() != '':
        cod,nom=separNomCod(combobox.get())
        datos=list(CON_PROC.buscarprodUnico(nom,cod))
        if datos!=[]:
            nombre['text']=str(datos[1])
            codigo['text']=str(datos[3])
            precio['text']=str(datos[4])
            marca['text']=str(datos[5])
            stock['text']=str(datos[2])
            bodega['text']=str(datos[6])
            local['text']=str(datos[7])
        else:
            messagebox.showinfo(message="Error, producto no existente", title="Actualizar Stock")

def actualizarListaStock(buscarCuadro_revVentas,busqueda,opcionStock):
    lista=CON_PROC.buscarprod(busqueda)
    aux=[]
    for fila in lista:
        aux.append([fila[1],fila[3]])
    buscarCuadro_revVentas['values']=tuple(aux)

def mostrarLabel(labelNombre,labelCodigo,labelPrecio,labelMarca,dato):
    if dato != '':
        codigo,dato=separNomCod(dato)
        datos=list(CON_PROC.buscarprodUnico(dato,codigo))
        if datos!=[]:
            labelNombre['text']=str(datos[1])
            labelCodigo['text']=str(datos[3])
            labelPrecio['text']=str(datos[4])
            labelMarca['text']=str(datos[5])

def eliminar_producto(nombre,codigo,labelNom,labelCod,labelPrec,labelMarca,combobox):
    if nombre['text']!='':
        if messagebox.askquestion(message="¿Desea eliminar el producto?", title="Eliminar") == 'yes':
            dato=[nombre['text'],codigo['text']]
            labelNom['text']=''
            labelCod['text']=''
            labelPrec['text']=''
            labelMarca['text']=''
            CON_PROC.eliminarProd(dato)
            combobox.set('')
    else:
        messagebox.showinfo(message="No ha seleccionado ningún producto", title="Eliminar")

def mostrar_opciones(label,rbS,rbN):
    rbN.grid(row=3,column=6,sticky=W)
    rbS.grid(row=2,column=6,sticky=W)
    label.grid(row=1,column=6,sticky=W)

def esconder_opciones(label,rbS,rbN):
        rbS.grid_remove()
        rbN.grid_remove()
        label.grid_remove()

def mostrar_combobox_verStock(combobox,buttom):
    buttom.grid(row=5,column=2,sticky=NSEW)
    combobox.grid(row=5,column=1,sticky=NSEW)

def esconder_combobox_verStock(combobox,buttom):
    buttom.grid_remove()
    combobox.grid_remove()

def frame_verStock(frame,resultado,opcion):
    for widget in frame.winfo_children():
        widget.destroy()
    if opcion=='Producto':
        resultado=resultado[0]
        label='Stock General de '+resultado[0]+' ('+str(resultado[1])+') '+resultado[3]+' $'+str(resultado[2])
        labelNombre=Label(frame,text=label)
        labelNombre.pack()
        tree=ttk.Treeview(frame,column=("c1","c2"),show='headings')
        tree.column("# 1",anchor=CENTER,width=120)
        tree.heading("# 1",text='Almacenamiento')
        tree.column("# 2",anchor=CENTER,width=100)
        tree.heading("# 2",text='Cantidad')
        tree.insert('', 'end',text= "1",values=('General',resultado[4]))
        tree.insert('', 'end',text= "1",values=(resultado[8],resultado[7]))
        tree.insert('', 'end',text= "1",values=(resultado[6],resultado[5]))
        tree.pack(side=TOP,fill=BOTH,expand=True)
        scrollx = Scrollbar(tree,orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly = Scrollbar(tree,orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        tree.config(xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        scrollx.config(command=tree.xview)
        scrolly.config(command=tree.yview)
    else:  
        tree=ttk.Treeview(frame,column=("c1","c2","c3","c4","c5"),show='headings')
        tree.column("# 1",anchor=CENTER,width=70)
        tree.heading("# 1",text='Nombre')
        tree.column("# 2",anchor=CENTER,width=100)
        tree.heading("# 2",text='Codigo Barra')
        tree.column("# 3",anchor=CENTER,width=70)
        tree.heading("# 3",text='Precio')
        tree.column("# 4",anchor=CENTER,width=70)
        tree.heading("# 4",text='Marca')
        tree.column("# 5",anchor=CENTER,width=70)
        tree.heading("# 5",text='Cantidad')
        for dato in resultado:
            tree.insert('', 'end',text= "1",values=dato)
        if opcion=='Bodega': 
            labelNombre=Label(frame,text='Stock en Bodega')
            labelNombre.pack()
            tree.pack(side=TOP,fill=BOTH,expand=True)
            scrollx = Scrollbar(tree,orient=HORIZONTAL)
            scrollx.pack(side=BOTTOM, fill=X)
            scrolly = Scrollbar(tree,orient=VERTICAL)
            scrolly.pack(side=RIGHT, fill=Y)
            tree.config(xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
            scrollx.config(command=tree.xview)
            scrolly.config(command=tree.yview)
        elif opcion=='Tienda':
            labelNombre=Label(frame,text='Stock en Tienda')
            labelNombre.pack()
            tree.pack(side=TOP,fill=BOTH,expand=True)
            scrollx = Scrollbar(tree,orient=HORIZONTAL)
            scrollx.pack(side=BOTTOM, fill=X)
            scrolly = Scrollbar(tree,orient=VERTICAL)
            scrolly.pack(side=RIGHT, fill=Y)
            tree.config(xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
            scrollx.config(command=tree.xview)
            scrolly.config(command=tree.yview)

def GenerarInformeStock(datosProd, opcion, frame):
    resultado = []
    if opcion == 'Producto':
        if datosProd != '':
            codigo, nombre = separNomCod(datosProd)
            resultado = CON_PROC.stock_producto(nombre, codigo)
            frame_verStock(frame, resultado, opcion)
    elif opcion == 'Bodega':
        sentecia = "select p.nom,p.cod_bar,p.prec,p.marca,sb.cant,b.direcb from producto as p, stock_bodega as sb, bodega as b where sb.id_bod=b.id_bod and b.id_bod=1 and sb.id_prod=p.id_prod and p.activo=True;"
        resultado = CON_PROC.stocks_loc_bod(sentecia)
        frame_verStock(frame, resultado, opcion)
    elif opcion == 'Tienda':
        sentecia = "select p.nom,p.cod_bar,p.prec,p.marca,sl.cant,l.nom from producto as p, stock_local as sl, locall as l where sl.id_loc=l.id_loc and l.id_loc=1 and sl.id_prod=p.id_prod and p.activo=True;"
        resultado = CON_PROC.stocks_loc_bod(sentecia)
        frame_verStock(frame, resultado, opcion)

def crearExcelProducto(resultado,nombre):
    dictPD = {"Nombre": [], "Codigo Barra": [], "Precio": [], "Marca": [], "Cantidad General": [], "Local 1":[], "Bodega":[]}
    for item in range(len(resultado)):
        dictPD["Nombre"].insert(item, resultado[item][0])
        dictPD["Codigo Barra"].insert(item, resultado[item][1])
        dictPD["Precio"].insert(item, resultado[item][2])
        dictPD["Marca"].insert(item, resultado[item][3])
        dictPD["Cantidad General"].insert(item, resultado[item][4])
        dictPD["Local 1"].insert(item, resultado[item][5])
        dictPD["Bodega"].insert(item, resultado[item][7])
    stockData = pd.DataFrame(dictPD)
    stockExcel = pd.ExcelWriter(nombre)
    stockData.to_excel(stockExcel)
    stockExcel.save()
    messagebox.showinfo(message="Se genero el archivo correctamente ", title="Informe de Stock")

def crearExcel(resultado,nombre):
    dictPD = {"Nombre": [], "Codigo Barra": [], "Precio": [], "Marca": [], "Cantidad": [], "Local":[]}
    for item in range(len(resultado)):
        dictPD["Nombre"].insert(item, resultado[item][0])
        dictPD["Codigo Barra"].insert(item, resultado[item][1])
        dictPD["Precio"].insert(item, resultado[item][2])
        dictPD["Marca"].insert(item, resultado[item][3])
        dictPD["Cantidad"].insert(item, resultado[item][4])
        dictPD["Local"].insert(item, resultado[item][5])
    stockData = pd.DataFrame(dictPD)
    stockExcel = pd.ExcelWriter(nombre)
    stockData.to_excel(stockExcel)
    stockExcel.save()
    messagebox.showinfo(message="Se genero el archivo correctamente ", title="Informe de Stock")


def ExportarStock(datosProd,opcion):
    resultado=[]
    if opcion=='Producto':
        if datosProd!='':
            codigo,nombre=separNomCod(datosProd)
            resultado=CON_PROC.stock_producto(nombre,codigo)
            if resultado!=[]:
                nombreAr='Stock General '+nombre+' ('+str(codigo)+').xlsx'
                crearExcelProducto(resultado,nombreAr)
    elif opcion=='Bodega':
        sentecia="select p.nom,p.cod_bar,p.prec,p.marca,sb.cant,b.direcb from producto as p, stock_bodega as sb, bodega as b where sb.id_bod=b.id_bod and b.id_bod=1 and sb.id_prod=p.id_prod and p.activo=True;"
        resultado=CON_PROC.stocks_loc_bod(sentecia)
        nombreAr='Stock Bodega.xlsx'
        if resultado!=[]:
            crearExcel(resultado,nombreAr)
    elif opcion=='Tienda':
        sentecia="select p.nom,p.cod_bar,p.prec,p.marca,sl.cant,l.nom from producto as p, stock_local as sl, locall as l where sl.id_loc=l.id_loc and l.id_loc=1 and sl.id_prod=p.id_prod and p.activo=True;"
        resultado=CON_PROC.stocks_loc_bod(sentecia)
        nombreAr='Stock Tienda.xlsx'
        if resultado!=[]:
            crearExcel(resultado,nombreAr)



def rellenarSemanas():
    semanas=[]
    dia_actual=datetime.datetime.today().weekday()
    semanas.append([(datetime.datetime.today()-datetime.timedelta(days=dia_actual)).strftime('%Y-%m-%d'),'/',
    datetime.datetime.today().strftime('%Y-%m-%d')])
    for i in range(6):
        semanas.append(
            [(datetime.datetime.today()-datetime.timedelta(days=dia_actual+(7*(i+1)))).strftime('%Y-%m-%d'),'/',
            (datetime.datetime.today()+datetime.timedelta(days=6-dia_actual)-datetime.timedelta(7*(i+1))).strftime('%Y-%m-%d')]
        )
    return semanas

def rellenarMeses():
    meses=[]
    mesesR=[]
    dia_mes=int((datetime.datetime.today()-datetime.timedelta(days=1)).strftime('%d'))
    mesesR.append(
        [datetime.datetime.today()-datetime.timedelta(days=dia_mes),
        datetime.datetime.today()]
    )
    meses.append(
        [(datetime.datetime.today()-datetime.timedelta(days=dia_mes)).strftime('%Y-%m-%d'),'/',
        datetime.datetime.today().strftime('%Y-%m-%d')]
    )
    for i in range(3):
        dia_mes=int((mesesR[i][0]-datetime.timedelta(days=1)).strftime('%d'))
        mesesR.append(
            [mesesR[i][0]-datetime.timedelta(days=dia_mes),
            mesesR[i][0]-datetime.timedelta(days=1)]
        )
        meses.append(
            [(mesesR[i][0]-datetime.timedelta(days=dia_mes)).strftime('%Y-%m-%d'),'/',
            (mesesR[i][0]-datetime.timedelta(days=1)).strftime('%Y-%m-%d')]
        )
    return meses

def cambiarListaFechas(combobox,listaS,listaM,opcion):
    if opcion=='Semanal':
        combobox['values']=tuple(listaS)
    if opcion=='Mensual':
        combobox['values']=tuple(listaM)

def getFechas(fechas):
    fechaIni=''
    fechaFin=''
    for letra in fechas:
        if letra == ' ':
            break
        fechaIni=fechaIni+letra
    for letra in reversed(fechas):
        if letra == ' ':
            break
        fechaFin=letra+fechaFin
    return fechaIni,fechaFin

def mostrarInformeFrame(frame,label,resultados):
    labelNombre=Label(frame,text=label)
    labelNombre.pack()
    tree=ttk.Treeview(frame,column=("c1","c2","c3","c4","c5","c6"),show='headings')
    tree.column("# 1",anchor=CENTER,width=70)
    tree.heading("# 1",text='Producto')
    tree.column("# 2",anchor=CENTER,width=95)
    tree.heading("# 2",text='Código de Barra')
    tree.column("# 3",anchor=CENTER,width=90)
    tree.heading("# 3",text='Precio Unidad')
    tree.column("# 4",anchor=CENTER,width=70)
    tree.heading("# 4",text='Marca')
    tree.column("# 5",anchor=CENTER,width=90)
    tree.heading("# 5",text='Total Vendido')
    tree.column("# 6",anchor=CENTER,width=80)
    tree.heading("# 6",text='Ganancia')
    for dato in resultados:
        tree.insert('', 'end',text= "1",values=dato)
    tree.pack(side=TOP,fill=BOTH,expand=True)
    scrollx = Scrollbar(tree,orient=HORIZONTAL)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly = Scrollbar(tree,orient=VERTICAL)
    scrolly.pack(side=RIGHT, fill=Y)
    tree.config(xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
    scrollx.config(command=tree.xview)
    scrolly.config(command=tree.yview)

def generarInforme(opcionOrden,listaFechas,frame):
    resultados=[]
    for widget in frame.winfo_children():
        widget.destroy()
    if listaFechas != '':
        fechaIni,fechaFin=getFechas(listaFechas)
        if opcionOrden=='Más':
            sentencia="select p.nom,p.cod_bar,p.prec,p.marca,SUM(pv.cant),(SUM(pv.cant)*p.prec) from producto as p,producto_vendido as pv,venta_diaria as vd where p.id_prod=pv.id_prod and vd.cod_ven=pv.cod_ven and vd.fecha between '{}' and '{}' group by p.id_prod order by SUM(pv.cant) desc;"
            resultados=CON_PROC.informeVentas(sentencia,fechaIni,fechaFin)
        if opcionOrden=='Menos':
            sentencia="select p.nom,p.cod_bar,p.prec,p.marca,SUM(pv.cant),(SUM(pv.cant)*p.prec) from producto as p,producto_vendido as pv,venta_diaria as vd where p.id_prod=pv.id_prod and vd.cod_ven=pv.cod_ven and vd.fecha between '{}' and '{}' group by p.id_prod order by SUM(pv.cant) asc;"
            resultados=CON_PROC.informeVentas(sentencia,fechaIni,fechaFin)
        if resultados!=[]:
            label='Informe de Ventas ('+listaFechas+') - '+opcionOrden+' Vendidos'
            mostrarInformeFrame(frame,label,resultados)

def crearExcelInforme(resultado,nombre):
    dictPD = {"Nombre": [], "Codigo Barra": [], "Precio": [], "Marca": [], "Total Vendidos": [], "Ganancias": []}
    for item in range(len(resultado)):
        dictPD["Nombre"].insert(item, resultado[item][0])
        dictPD["Codigo Barra"].insert(item, resultado[item][1])
        dictPD["Precio"].insert(item, resultado[item][2])
        dictPD["Marca"].insert(item, resultado[item][3])
        dictPD["Total Vendidos"].insert(item, resultado[item][4])
        dictPD["Ganancias"].insert(item, resultado[item][5])
    stockData = pd.DataFrame(dictPD)
    stockExcel = pd.ExcelWriter(nombre)
    stockData.to_excel(stockExcel)
    stockExcel.save()
    messagebox.showinfo(message="Se genero el archivo correctamente ", title="Informe de Ventas")

def generarInformeExcel(opcionOrden,listaFechas):
    resultados = []
    if listaFechas != '':
        fechaIni, fechaFin = getFechas(listaFechas)
        if opcionOrden == 'Más':
            sentencia = "select p.nom,p.cod_bar,p.prec,p.marca,SUM(pv.cant),(SUM(pv.cant)*p.prec) from producto as p,producto_vendido as pv,venta_diaria as vd where p.id_prod=pv.id_prod and vd.cod_ven=pv.cod_ven and vd.fecha between '{}' and '{}' group by p.id_prod order by SUM(pv.cant) desc;"
            resultados = CON_PROC.informeVentas(sentencia, fechaIni, fechaFin)
            nombre='Informe de Ventas'+fechaIni+'--'+fechaFin+' Mas vendidos.xlsx'
            crearExcelInforme(resultados,nombre)
        if opcionOrden == 'Menos':
            sentencia = "select p.nom,p.cod_bar,p.prec,p.marca,SUM(pv.cant),(SUM(pv.cant)*p.prec) from producto as p,producto_vendido as pv,venta_diaria as vd where p.id_prod=pv.id_prod and vd.cod_ven=pv.cod_ven and vd.fecha between '{}' and '{}' group by p.id_prod order by SUM(pv.cant) asc;"
            resultados = CON_PROC.informeVentas(sentencia, fechaIni, fechaFin)
            nombre='Informe de Ventas '+fechaIni+'--'+fechaFin+' Menos vendidos.xlsx'
            crearExcelInforme(resultados,nombre)