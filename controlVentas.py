"""
21/09/2020 = Gestion de clientes terminada
Se comienza la gestion de ventas

"""
from tkinter import ttk
from tkinter import *
import sqlite3
from datetime import datetime

class clienteVenta:

#++++++++++++++++++++++++++++++++++++++++++++++++++Ventana principal+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	#Constructor / diseño de mi ventana principal
	def __init__(self, window):
		self.wind = window
		self.wind.title('Control de Ventas')
		self.wind.geometry('400x200')

		frameMain = LabelFrame(self.wind, text = 'Bienvenido al menu principal')
		frameMain.grid(row = 3, column = 3, columnspan = 3, pady = 20)

		# Boton para ir a la seccion de clientes 
		ttk.Button(frameMain, text = 'Gestionar Clientes', command = self.gestionCliente).grid(row = 3, columnspan = 2, sticky = W + E)
		#Boton para ir a la seccion de ventas 	
		ttk.Button(frameMain, text = 'Gestionar Ventas', command = self.gestionVenta).grid(row = 4, columnspan = 2, sticky = W + E)	

#++++++++++++++++++++++++++++++++++++++++++++++++++++Gestion de clientes++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	#Diseño / acciones del boton "Gestionar clientes"	
	def gestionCliente(self):
		self.clienteWind = Toplevel()
		self.clienteWind.title('Gestion de Clientes')

		#Diseño de la ventana cliente
		frameCliente = LabelFrame(self.clienteWind, text = 'Registrar nuevo cliente')
		frameCliente.grid(row = 0, column = 0, columnspan = 3, pady = 20)

		# ingresar cedula
		Label(frameCliente, text = 'Cedula: ').grid(row = 1, column = 0)
		self.cedula = Entry(frameCliente)
		self.cedula.focus() #Este metodo es para colocar el cursor en la pimera casilla de una 
		self.cedula.grid(row = 1, column = 1) #Ubicacion de mi cuadro de entrada en la grilla 

		#ingresar nombre
		Label(frameCliente, text = 'Nombre: ').grid(row = 2, column = 0)
		self.nombre = Entry(frameCliente)
		self.nombre.grid(row = 2, column = 1)

		#ingresar apellido
		Label(frameCliente, text = 'Apellido').grid(row = 3, column = 0)
		self.apellido = Entry(frameCliente)
		self.apellido.grid(row = 3, column = 1)

		#ingresar alias
		Label(frameCliente, text = 'Alias').grid(row = 4, column = 0)
		self.alias = Entry(frameCliente)
		self.alias.grid(row = 4, column = 1)

		#ingresar telefono
		Label(frameCliente, text = 'Telefono').grid(row = 5, column = 0)
		self.telefono = Entry(frameCliente)
		self.telefono.grid(row = 5, column = 1)

		#ingresar direccion
		Label(frameCliente, text = 'Direccion').grid(row = 6, column = 0)
		self.direccion = Entry(frameCliente)
		self.direccion.grid(row = 6, column = 1)

		#Botones de gestion de clientes
		#Boton para insertar
		ttk.Button(frameCliente, text = 'Registrar cliente', command = self.registroCliente).grid(row = 7, columnspan = 2, sticky = W + E)
		#Boton para eliminar
		ttk.Button(self.clienteWind, text = 'Eliminar cliente', command = self.eliminarCliente).grid(row = 9, column = 0, sticky = W + E)
		#boton para editar cliente
		ttk.Button(self.clienteWind, text = 'Editar cliente', command = self.editarCliente).grid(row = 9, column = 1, sticky = W + E)

		#Mensajes para el usuario (Modulo cliente)
		#mensaje de error
		self.mensajeError = Label(self.clienteWind, text = '', fg = 'red')
		self.mensajeError.grid(row = 2, column = 0, columnspan = 2, sticky = W + E)
		#Mensaje de accion exitosa
		self.mensajeExito = Label(self.clienteWind, text = '', fg = 'blue')
		self.mensajeExito.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

		# Tabla para mostrar usuarios dentro de la gestion de cientes
		self.tablaCliente = ttk.Treeview(self.clienteWind, height = 10, columns = ('#0', '#1', '#2', '#3', '#4'))
		self.tablaCliente.grid(row = 8, column = 0, columnspan = 6)
		self.tablaCliente.heading('#0', text = 'Cedula', anchor = CENTER)
		self.tablaCliente.heading('#1', text = 'Nombre', anchor = CENTER)
		self.tablaCliente.heading('#2', text = 'Apellido', anchor = CENTER)
		self.tablaCliente.heading('#3', text = 'Alias', anchor = CENTER)
		self.tablaCliente.heading('#4', text = 'Telefono', anchor = CENTER)
		self.tablaCliente.heading('#5', text = 'Direccion', anchor = CENTER)
		self.obtenerClientes()

	#Insertar un numero cliente dentro de la base de datos	
	def registroCliente(self):
		#Borrar algun mensaje que este en la ventana
		self.mensajeError['text'] = ''
		self.mensajeExito['text'] = ''

		#Condicionales para validar las entradas de los campos sensibles 
		if self.validacionCliente() == 'nombre':
			self.mensajeError['text'] = 'Debe ingresar un nombre valido para poder realizar el registro'

		elif self.validacionCliente() == 'cedula':
			self.mensajeError['text'] = 'La cedula debe ser un numero'

		elif self.validacionCliente() == 'telefono':
			self.mensajeError['text'] = 'El telefono debe ser un numero'

		else:		
			query = 'INSERT INTO cliente VALUES(NULL, ?, ?, ?, ?, ?, ?)'
			parametros = (int(self.cedula.get()), 
							self.nombre.get(), 
							self.apellido.get(), 
							self.alias.get(), 
							int(self.telefono.get()), 
							self.direccion.get())
			self.runQuery(query, parametros)
			self.mensajeExito['text'] = 'Cliente {} registrado satisfactoriamente'.format(self.nombre.get())
			self.cedula.delete(0, END)
			self.nombre.delete(0, END)
			self.apellido.delete(0, END)
			self.alias.delete(0, END)
			self.telefono.delete(0, END)
			self.direccion.delete(0, END)
		self.obtenerClientes()

	#Funcion para eliminar los clientes de la BD	
	def eliminarCliente(self):
		#Borrar algun mensaje que este en la ventana
		self.mensajeError['text'] = ''
		self.mensajeExito['text'] = ''
		#Validar si hay algo selecionado para eliminar
		try:
			int(self.tablaCliente.item(self.tablaCliente.selection())['text'])
		except :	
			self.mensajeError['text'] = 'Por favor selecciona el cliente a eliminar'
			return
		self.mensajeError['text'] = ''
		self.mensajeExito['text'] = ''
		cedula = self.tablaCliente.item(self.tablaCliente.selection())['text']
		query = 'DELETE FROM cliente where cedula = ?'
		self.runQuery(query, (cedula,))
		self.mensajeExito['text'] = 'El cliente fue borrado exitosamente'
		self.obtenerClientes()

	#funcion se usara para editar uno o campos de un cliente	
	def editarCliente(self):
		#Borrar algun mensaje que este en la ventana
		self.mensajeError['text'] = ''
		self.mensajeExito['text'] = ''
		#Validacion si se encuntra algo seleccionado para editar
		try:
			int(self.tablaCliente.item(self.tablaCliente.selection())['text'])
		except :	
			self.mensajeError['text'] = 'Por favor selecciona un cliente para Editar'
			return

		#Obtengo lo valores viejos para mostrarlos en la interfaz 	
		self.oldCedula = self.tablaCliente.item(self.tablaCliente.selection())['text'] 	
		self.oldNombre = self.tablaCliente.item(self.tablaCliente.selection())['values'][0]
		self.oldApellido = self.tablaCliente.item(self.tablaCliente.selection())['values'][1]
		self.oldAlias = self.tablaCliente.item(self.tablaCliente.selection())['values'][2]
		self.oldTelefono = self.tablaCliente.item(self.tablaCliente.selection())['values'][3]
		self.oldDireccion = self.tablaCliente.item(self.tablaCliente.selection())['values'][4]

		#ventana emergente para facilitar la edicion del cliente
		self.editarclienteWind = Toplevel()
		self.editarclienteWind.title('Modificar datos del cliente')

		#Frame para los datos
		frameEditarCliente = LabelFrame(self.editarclienteWind, text = 'Actualizacion de cliente')
		frameEditarCliente.grid(row = 0, column = 0, columnspan = 3, pady = 20)


		#vaiables para hacer prueba 
		self.cedulaPrueba = StringVar()
		self.nombrePrueba= StringVar()
		self.apellidoPrueba= StringVar()
		self.aliasPrueba = StringVar()
		self.telefonoPrueba = StringVar()
		self.direccionPrueba = StringVar()

		# modificar cedula
		Label(frameEditarCliente, text = 'Nueva cedula:').grid(row = 1, column = 3)
		self.nuevoCedula = Entry(frameEditarCliente, textvariable = self.cedulaPrueba)
		self.nuevoCedula.insert(0, self.oldCedula)
		self.nuevoCedula.focus()
		self.nuevoCedula.grid(row = 1 , column = 4)	

		#Modificar nombre
		Label(frameEditarCliente, text = 'Nuevo nombre:').grid(row = 2, column = 3)
		self.nuevoNombre = Entry(frameEditarCliente, textvariable = self.nombrePrueba)
		self.nuevoNombre.insert(0, self.oldNombre)
		self.nuevoNombre.grid(row = 2, column = 4)

		#Modificar Apellido
		Label(frameEditarCliente, text = 'Nuevo apellido:').grid(row = 3, column = 3)
		self.nuevoApellido = Entry(frameEditarCliente, textvariable = self.apellidoPrueba)
		self.nuevoApellido.insert(0, self.oldApellido)
		self.nuevoApellido.grid(row = 3, column = 4)

		#Modificar Alias		
		Label(frameEditarCliente, text = 'Nuevo alias: ').grid(row = 4, column = 3)
		self.nuevoAlias = Entry(frameEditarCliente, textvariable = self.aliasPrueba)
		self.nuevoAlias.insert(0, self.oldAlias)
		self.nuevoAlias.grid(row = 4, column = 4)

		#Modificar Telefono
		Label(frameEditarCliente, text = 'Nuevo telefono').grid(row = 5, column = 3)
		self.nuevoTelefono = Entry(frameEditarCliente, textvariable = self.telefonoPrueba)
		self.nuevoTelefono.insert(0, self.oldTelefono)
		self.nuevoTelefono.grid(row = 5, column = 4)

		#Modificar Direccion
		Label(frameEditarCliente, text = 'Nueva direccion').grid(row = 6, column = 3)
		self.nuevoDireccion = Entry(frameEditarCliente, textvariable = self.direccionPrueba)
		self.nuevoDireccion.insert(0, self.oldDireccion)
		self.nuevoDireccion.grid(row = 6, column = 4)

		#Boton para confirmar los cambios
		ttk.Button(self.editarclienteWind, text = 'Aceptar', command = lambda: self.updateCliente(self.cedulaPrueba.get(), self.nombrePrueba.get(), self.apellidoPrueba.get(), self.aliasPrueba.get(), self.telefonoPrueba.get(), self.direccionPrueba.get())).grid(row = 7, column = 4, sticky = W + E)
		self.editarclienteWind.mainloop()

	def updateCliente(self, cedula, nombre, apellido, alias, telefono, direccion):
		#Preparar parametros para la actualizacion
		parametros = (cedula, 
							nombre, 
							apellido, 
							alias, 
							telefono, 
							direccion,
							self.oldCedula,
							self.oldNombre)
		query = 'UPDATE cliente SET cedula = ?, nombre = ?, apellido = ?, alias = ?, telefono = ?, direccion = ? WHERE cedula = ? AND nombre = ?'
		self.runQuery(query, parametros)
		self.editarclienteWind.destroy()
		self.mensajeExito['text'] = 'El cliente fue editado exitosamente'
		self.obtenerClientes()


	#Valida la informacion que entra a cliente
	#nombre no debe ser vacio, telefono y cedula deben ser numeros
	def validacionCliente(self):
		if len(self.nombre.get()) < 1:
			return 'nombre' 
		
		try:
			int(self.cedula.get())
		except: 
			return 'cedula'

		try:
			int(self.telefono.get())
		except:
			return 'telefono'	

	#Esta funcion muestra permanetemente los clientes en la tabla 
	def obtenerClientes(self):
		#Limpiar la tabla para ingresar los nuevos datos
		records = self.tablaCliente.get_children()
		for elemento in records:
			self.tablaCliente.delete(elemento)

		#ingresando los datos nuevos
		query = 'SELECT * FROM cliente ORDER BY nombre DESC'	
		filas = self.runQuery(query)
		for fila in filas:
			self.tablaCliente.insert('', 0, text = fila[1], values = (fila[2], fila[3], fila[4], fila[5], fila[6]))

#++++++++++++++++++++++++++++++++++++++++++++++++ Gestion de ventas+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	

	def gestionVenta(self):
		self.ventaWind = Toplevel()
		self.ventaWind.title('Gestion de Ventas')
		self.ventaWind.geometry('400x200')

		#Botones
		ttk.Button(self.ventaWind, text = 'Crear nueva venta', command = self.crearVenta).grid(row = 0, columnspan = 2, sticky = W + E)
		ttk.Button(self.ventaWind, text = 'Consultar ventas abiertas', command =self.ventasAbiertas).grid(row = 1, columnspan = 2, sticky = W + E)
		ttk.Button(self.ventaWind, text = 'Consultar ventas por despachar', command = self.ventasPorDespachar).grid(row = 2, columnspan = 2, sticky = W + E)
		ttk.Button(self.ventaWind, text = 'Consultar ventas cerradas', command = self.ventasCerradas).grid(row = 3, columnspan = 2, sticky = W + E)
		

	#Crea un nuevo registro de venta. utiliza los siguientes metodos
	#seleccionarCliente()
	#obtenerSeleccionClientes()
	#obtenerClienteParametro()
	#registrarVenta()
	def crearVenta(self):
		self.crearVentaWind = Toplevel()
		self.crearVentaWind.title('Crear nueva venta')
		self.crearVentaWind.geometry('400x250')

		#Frame para los datos
		frameCrearVenta = LabelFrame(self.crearVentaWind)
		frameCrearVenta.grid(row = 0, column = 0, columnspan = 3, pady = 20)

		#Diseño esctructura interna de la ventana

		#Ingresar deuda (Se calcula automaticamente)
		Label(frameCrearVenta, text = 'Deuda').grid(row = 0, column = 0)
		self.deuda = Entry(frameCrearVenta)
		self.deuda.focus()
		self.deuda.grid(row = 0 , column = 2)
		#Boton genera una ventana par hacer el total  de la venta 
		ttk.Button(frameCrearVenta, text = 'Calcular monto de venta', command = self.calculoVenta).grid(row = 0, column = 3)

		#ingresar la descripcion de la venta (SE realizara automaticamente de acuerdo a la compra)
		Label(frameCrearVenta, text = 'Descripcion').grid(row = 1, column = 0)
		self.descripcion = Entry(frameCrearVenta)
		self.descripcion.grid(row = 1, column = 2)

		#entrada especial que me genera una lista de valores predefinidos
		Label(frameCrearVenta, text = 'Estado').grid(row = 2, column = 0)
		self.estado = ttk.Combobox(frameCrearVenta)
		self.estado = ttk.Combobox(frameCrearVenta, state="readonly")
		self.estado["values"] = ["POR DESPACHAR", "ABIERTA"]
		self.estado.grid(row = 2, column = 2)

		#Boton de ventana emergente para seleccionar al cliente de una lista que viene de los datos de la BD
		ttk.Button(frameCrearVenta, text = 'Seleccionar Comprador', command = self.seleccionarCliente).grid(row = 3, columnspan = 4, sticky = W + E )
		#Boton de la ventana emergente que toma los datos de la nueva venta 
		ttk.Button(self.crearVentaWind, text = 'Aceptar', command = lambda: self.registrarVenta(self.descripcion.get(), self.deuda.get(), self.estado.get(), self.cedulaComprador.get(), self.nombreComprador.get() )).grid(row = 1, column = 2, sticky = W + E )

		#inresar cedula del ciente, se inserta atumaticamente desde el metodo obtenerClienteParametro()
		Label(frameCrearVenta, text = 'Cedula').grid(row = 4, column = 0)
		self.cedulaComprador = Entry(frameCrearVenta)
		self.cedulaComprador.grid(row = 4, column = 2)	

		#inresar nombre del ciente, se inserta atumaticamente desde el metodo obtenerClienteParametro()
		Label(frameCrearVenta, text = 'Nombre').grid(row =5, column = 0)
		self.nombreComprador = Entry(frameCrearVenta)
		self.nombreComprador.grid(row = 5, column = 2)	

	#Ventana con la lista de clientes registrados para facilitar el tomar los datos y casar un cliente con un pedido/venta	
	def seleccionarCliente(self):
		self.selecCliente = Toplevel()
		self.selecCliente.title('Clientes registrados')

		#DEclaracion y diseño de la tabla que contendrá los datos d elos clientes 
		self.tablaSelecCliente = ttk.Treeview(self.selecCliente, height = 10, columns = ('#0', '#1'))
		self.tablaSelecCliente.grid(row = 8, column = 0, columnspan = 6)
		self.tablaSelecCliente.heading('#0', text = 'Cedula', anchor = CENTER)
		self.tablaSelecCliente.heading('#1', text = 'Nombre', anchor = CENTER)
		self.tablaSelecCliente.heading('#2', text = 'Alias', anchor = CENTER)
		self.obtenerSeleccionClientes() 

		#Boton para ejecutar la seleccion de cliente 
		ttk.Button(self.selecCliente, text = 'Seleccionar', command = self.obtenerClienteParametro).grid(row = 9, columnspan = 3, sticky = W + E )

	#Llena la tabla de con los clientes registrados 	
	def obtenerSeleccionClientes(self):
		#Limpiar la tabla para ingresar los nuevos datos
		records = self.tablaSelecCliente.get_children()
		for elemento in records:
			self.tablaSelecCliente.delete(elemento)

		#ingresando los datos nuevos
		query = 'SELECT cedula, nombre, alias FROM cliente'	
		filas = self.runQuery(query)
		for fila in filas:
			self.tablaSelecCliente.insert('', 0, text = fila[0], values = (fila[1], fila[2]))

	#Carga en las variables los datos necesarios del cliente para la posterior insercion de la venta en la BD		
	def obtenerClienteParametro(self):
		try:
			int(self.tablaSelecCliente.item(self.tablaSelecCliente.selection())['text'])
		except :	
			return

		self.cedulaCliente = self.tablaSelecCliente.item(self.tablaSelecCliente.selection())['text']	
		self.nombreCliente = self.tablaSelecCliente.item(self.tablaSelecCliente.selection())['values'][0]

		#Inserto los valores en los campos del formulario automaticamente (Comodidad del usuario)
		self.cedulaComprador.insert(0, self.cedulaCliente)
		self.nombreComprador.insert(0, self.nombreCliente)

		self.selecCliente.destroy()

	#ventana para obtener los datos especificos de la venta y posteriormente hacer el calculo
	def calculoVenta(self):
		self.calculoWind = Toplevel()
		self.calculoWind.title('Calculadora')

		#Ron
		Label(self.calculoWind, text = 'Ron').grid(row = 0, column = 0)
		Label(self.calculoWind, text = 'litros').grid(row = 1, column = 0)
		Label(self.calculoWind, text = 'Precio').grid(row = 1, column = 2)
		ronl = Entry(self.calculoWind)
		ronl.insert(0, '0')
		ronl.grid(row = 1, column = 1)
		ronp = Entry(self.calculoWind)
		ronp.insert(0, '0')
		ronp.grid(row = 1, column = 3)

		#Anis
		Label(self.calculoWind, text = 'Anis').grid(row = 2, column = 0)
		Label(self.calculoWind, text = 'litros').grid(row = 3, column = 0)
		Label(self.calculoWind, text = 'Precio').grid(row = 3, column = 2)
		anisl = Entry(self.calculoWind)
		anisl.insert(0, '0')
		anisl.grid(row = 3, column = 1)
		anisp = Entry(self.calculoWind)
		anisp.insert(0, '0')
		anisp.grid(row = 3, column = 3)

		#canaClara
		Label(self.calculoWind, text = 'Ron').grid(row = 4, column = 0)
		Label(self.calculoWind, text = 'litros').grid(row = 5, column = 0)
		Label(self.calculoWind, text = 'Precio').grid(row = 5, column = 2)
		cClaral = Entry(self.calculoWind)
		cClaral.insert(0, '0')
		cClaral.grid(row = 5, column = 1)
		cClarap = Entry(self.calculoWind)
		cClarap.insert(0, '0')
		cClarap.grid(row = 5, column = 3)

		ttk.Button(self.calculoWind, text = 'Calcular', command = lambda: self.calcular(int(ronl.get()), float(ronp.get()), int(anisl.get()), float(anisp.get()), int(cClaral.get()), float(cClarap.get()))).grid(row = 6, column = 4, sticky = W + E)


	#se calcula el monto total de la venta y se inserta en el campo deuda y se crea una descripcion de la venta 
	#Tanto el total como la descripcion se insertan de una vez en los campos correspondientes	
	def calcular(self, ronl, ronp, anisl, anisp, cClaral, cClarap):	
		totalVenta = (ronl*ronp)+(anisl*anisp)+(cClaral*cClarap) 
		self.deuda.insert(0, totalVenta)
		self.calculoWind.destroy()

		#Realizar una descripcion de la venta 
		descripcion = 'Ron:'+str(1*ronl)+' / '+'Anis:'+str(1*anisl)+' / '+'CC:'+str(1*cClaral)
		self.descripcion.insert(0, descripcion)


	#Toma todos los datos captados anteriormente para insertar un nuevo registro de venta en la BD	
	def registrarVenta(self, descripcion, deuda, estado, cedulaComprador, nombreComprador ):
		
		#Obtengo el id del cleinte enla BD para asignar mi clave foranea
		idquery = 'SELECT id_cliente FROM cliente WHERE cedula = ? AND nombre = ?'
		para = (cedulaComprador, nombreComprador)
		idresul = self.runQuery(idquery, para)
		id_cliente = idresul.fetchone()[0]

		fecha = self.obtenerFeha()
		#insercion de la venta en la BD
		query = 'INSERT INTO venta VALUES(NULL, ?, ?, ?, ?, ?)'
		parametros =(int(id_cliente),
						descripcion,
						estado,
						fecha,
						float(deuda))
		self.runQuery(query, parametros)
		self.crearVentaWind.destroy()

	#Ventana para consultar las ventas cerradas y vaciarlas en una tabla	
	def ventasCerradas(self):
		self.ventaCerradaWind = Toplevel()
		self.ventaCerradaWind.title("Ventas Cerradas")

		#Boton para cerrar la ventana (unico boton de esta seccion (Por ahora))
		ttk.Button(self.ventaCerradaWind, text = 'Salir', command = self.cerrarCerradas).grid(row = 9, column = 5, sticky = W + E)	

		#DEclaracion y diseño de la tabla que contendrá los datos de las ventas cerradas  
		self.tablaVentaCerrada = ttk.Treeview(self.ventaCerradaWind, height = 10, columns = ('#0', '#1', '#2', '#3', '#4', '#5'))
		self.tablaVentaCerrada.grid(row = 8, column = 0, columnspan = 6)
		self.tablaVentaCerrada.heading('#0', text = 'Identificador', anchor = CENTER)
		self.tablaVentaCerrada.heading('#1', text = 'Cedula', anchor = CENTER)
		self.tablaVentaCerrada.heading('#2', text = 'Nombre', anchor = CENTER)
		self.tablaVentaCerrada.heading('#3', text = 'Descripcion', anchor = CENTER)
		self.tablaVentaCerrada.heading('#4', text = 'Fecha', anchor = CENTER)
		self.tablaVentaCerrada.heading('#5', text = 'Deuda', anchor = CENTER)
		self.tablaVentaCerrada.heading('#6', text = 'Estado', anchor = CENTER)
		self.obtenerVentasCerradas()

	#llenado de la tabla de ventas cerradas	
	def obtenerVentasCerradas(self):	
		#Consulta para traer todas las ventas en estado CERRADA
		query = 'SELECT v.id_venta, c.cedula, c.nombre, v.descripcion, v.fecha_venta, v.deuda, v.estado FROM cliente AS c JOIN venta AS v ON c.id_cliente = v.id_clientev WHERE v.estado = ?'
		parametro = ('CERRADA',)
		resul = self.runQuery(query, parametro)

		#Limpiar la tabla para ingresar los nuevos datos
		records = self.tablaVentaCerrada.get_children()
		for elemento in records:
			self.tablaVentaCerrada.delete(elemento)
		#ingresando los datos nuevos
		for fila in resul:
			self.tablaVentaCerrada.insert('', 0, text = fila[0], values = (fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))

	#Accion de boton de salir para a ventana de consultar ventas cerradas		
	def cerrarCerradas(self):
		self.ventaCerradaWind.destroy()		

	#Ventana para consultar las ventas por despachar y vaciarlas en una tabla	
	def ventasPorDespachar(self):
		self.ventaPorDespacharWind = Toplevel()
		self.ventaPorDespacharWind.title("Ventas Por Despachar")

		ttk.Button(self.ventaPorDespacharWind, text = 'Salir', command = self.cerrarPorDespachar).grid(row = 9, column = 5, sticky = W + E)	
		ttk.Button(self.ventaPorDespacharWind, text = 'Cambiar estado de la venta', command = self.cambiarEstadoVenta).grid(row = 9, column = 4, sticky = W + E)

		#DEclaracion y diseño de la tabla que contendrá los datos de las ventas por despachar  
		self.tablaVentaPorDespachar = ttk.Treeview(self.ventaPorDespacharWind, height = 10, columns = ('#0', '#1', '#2', '#3', '#4', '#5'))
		self.tablaVentaPorDespachar.grid(row = 8, column = 0, columnspan = 6)
		self.tablaVentaPorDespachar.heading('#0', text = 'Identificador', anchor = CENTER)		
		self.tablaVentaPorDespachar.heading('#1', text = 'Cedula', anchor = CENTER)
		self.tablaVentaPorDespachar.heading('#2', text = 'Nombre', anchor = CENTER)
		self.tablaVentaPorDespachar.heading('#3', text = 'Descripcion', anchor = CENTER)
		self.tablaVentaPorDespachar.heading('#4', text = 'Fecha', anchor = CENTER)
		self.tablaVentaPorDespachar.heading('#5', text = 'Deuda', anchor = CENTER)
		self.tablaVentaPorDespachar.heading('#6', text = 'Estado', anchor = CENTER)	
		self.obtenerVentasPorDespachar()

	#llenado de la tabla de ventas por despachar
	def obtenerVentasPorDespachar(self):	
		#Consulta para traer todas las ventas en estado POR DESPACHAR
		query = 'SELECT v.id_venta, c.cedula, c.nombre, v.descripcion, v.fecha_venta, v.deuda, v.estado FROM cliente AS c JOIN venta AS v ON c.id_cliente = v.id_clientev WHERE v.estado = ?'
		parametro = ('POR DESPACHAR',)
		resul = self.runQuery(query, parametro)

		#Limpiar la tabla para ingresar los nuevos datos
		records = self.tablaVentaPorDespachar.get_children()
		for elemento in records:
			self.tablaVentaPorDespachar.delete(elemento)
		#ingresando los datos nuevos
		for fila in resul:
			self.tablaVentaPorDespachar.insert('', 0, text = fila[0], values = (fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))	

	#Accion de boton de salir para a ventana de consultar ventas por despachar		
	def cerrarPorDespachar(self):
		self.ventaPorDespacharWind.destroy()

	#Ventana para consultar las ventas abiertas y vaciarlas en una tabla	
	def ventasAbiertas(self):
		self.ventaAbiertaWind = Toplevel()
		self.ventaAbiertaWind.title("Ventas Abiertas")

		ttk.Button(self.ventaAbiertaWind, text = 'Salir', command = self.cerrarAbiertas).grid(row = 9, column = 5, sticky = W + E)	
		ttk.Button(self.ventaAbiertaWind, text = 'Abono', command= self.abonar).grid(row = 9, column = 4, sticky = W + E)

		#DEclaracion y diseño de la tabla que contendrá los datos de las ventas abiertas  
		self.tableVentaAbierta = ttk.Treeview(self.ventaAbiertaWind, height = 10, columns = ('#0', '#1', '#2', '#3', '#4', '#5'))
		self.tableVentaAbierta.grid(row = 8, column = 0, columnspan = 6)
		self.tableVentaAbierta.heading('#0', text = 'Identificador', anchor = CENTER)
		self.tableVentaAbierta.heading('#1', text = 'Cedula', anchor = CENTER)
		self.tableVentaAbierta.heading('#2', text = 'Nombre', anchor = CENTER)
		self.tableVentaAbierta.heading('#3', text = 'Descripcion', anchor = CENTER)
		self.tableVentaAbierta.heading('#4', text = 'Fecha', anchor = CENTER)
		self.tableVentaAbierta.heading('#5', text = 'Deuda', anchor = CENTER)
		self.tableVentaAbierta.heading('#6', text = 'Estado', anchor = CENTER)	
		self.obtenerVentasAbiertas()

	#llenado de la tabla de ventas abiertas
	def obtenerVentasAbiertas(self):	
		#Consulta para traer todas las ventas en estado ABIERTAS
		query = 'SELECT v.id_venta, c.cedula, c.nombre, v.descripcion, v.fecha_venta, v.deuda, v.estado FROM cliente AS c JOIN venta AS v ON c.id_cliente = v.id_clientev WHERE v.estado = ?'
		parametro = ('ABIERTA',)
		resul = self.runQuery(query, parametro)

		#Limpiar la tabla para ingresar los nuevos datos
		records = self.tableVentaAbierta.get_children()
		for elemento in records:
			self.tableVentaAbierta.delete(elemento)
		#ingresando los datos nuevos
		#EL campo 7 de value aunque no se muestre, guarda el id de la venta para facilitar su busqueda al momento de hacer el abono
		for fila in resul:
			self.tableVentaAbierta.insert('', 0, text = fila[0], values = (fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))	

	#Accion de boton de salir para a ventana de consultar ventas Abiertas	
	def cerrarAbiertas(self):
		self.ventaAbiertaWind.destroy()	

	#Crea una ventana comoda para realizar un abono a una venta seleccionada	
	def abonar(self):
		try:
			int(self.tableVentaAbierta.item(self.tableVentaAbierta.selection())['text'])
		except :	
			return

		#Obtengo la deuda para mostrarla en la interfaz y otros parametros convenientes	
		self.nombreCliente = self.tableVentaAbierta.item(self.tableVentaAbierta.selection())['values'][1]
		self.deudaCliente =self.tableVentaAbierta.item(self.tableVentaAbierta.selection())['values'][4]
		self.idVenta = self.tableVentaAbierta.item(self.tableVentaAbierta.selection())['text']
		
		#Creo la ventana
		self.abonarWind = Toplevel()
		self.abonarWind.title('Ingresar abono')

		#Frame para gestionar el abono
		frameAbonar = LabelFrame(self.abonarWind, text ='Ingresar abono a la venta corresponiente a '+ self.nombreCliente)
		frameAbonar.grid(row = 0, column = 0, columnspan = 3, pady = 20)

		#Boton me da acceso a al metodo donde se realizan los cambios en la deuda
		ttk.Button(self.abonarWind, text = 'Aceptar', command = lambda: self.editarDeuda(self.entradaAbono.get(), self.idVenta)).grid(row = 1, column = 2, sticky = W + E)	


		#Diseño esctructura interna de la ventana
		#deuda
		Label(frameAbonar, text = 'Deuda actual').grid(row = 0, column = 0)
		self.deudaActual = Entry(frameAbonar, textvariable = StringVar(frameAbonar, value = self.deudaCliente), state = 'readonly')
		self.deudaActual.grid(row = 0 , column = 1)

		#Abono
		Label(frameAbonar, text = 'Abono').grid(row = 1, column = 0)
		self.entradaAbono = Entry(frameAbonar)
		self.entradaAbono.focus()
		self.entradaAbono.grid(row = 1, column = 1) 

	#SE realizan los cambios en la deuda en la BD	
	def editarDeuda(self, abono, id):

		#Obtener deuda actual
		query = 'SELECT deuda FROM venta WHERE id_venta = ? '
		parametro = (id,)
		resul = self.runQuery(query, parametro)
		deuda = resul.fetchone()[0]

		#Calculo la nueva deuda luego del abono
		newDeuda = float(deuda) - float(abono)

		#Este condicional me permite ademas de actuaizar la deuda en la BD, si esta es 0 (Se paga la totalidad de la venta)
		#Se cambia d euna vez el estado d ela venta a CERRADA
		if newDeuda > 0:
			query = 'UPDATE venta SET deuda = ? WHERE id_venta = ? '
			parametros = (newDeuda, id)
			self.runQuery(query, parametros)
			self.abonarWind.destroy()
			self.obtenerVentasAbiertas()
		else:
			fecha = self.obtenerFeha()
			query = 'UPDATE venta SET deuda = ?, estado = ?, fecha_venta = ? WHERE id_venta = ? '
			parametros = (newDeuda, 'CERRADA', fecha, id)
			self.runQuery(query, parametros)
			self.abonarWind.destroy()
			self.obtenerVentasAbiertas()

			#Se crea una ventana para informar que la venta se movio a la seccion de "ventas cerradas"
			self.aviso = Toplevel()
			self.aviso.title("AVISO!")	

			Label(self.aviso, text = 'EL cliente pago la totalidad de la deuda, La venta fue movida a "Ventas cerradas"').grid(row = 0, column = 0)	
			ttk.Button(self.aviso, text = 'OK', command = self.cerrarAviso).grid(row = 1, column = 2)

	#Funcionalidad del boton de la ventana de aviso que informa que la venta se movio a la seccion seleccionada 		
	def cerrarAviso(self):
		self.aviso.destroy()	


	#Cambiar una venta por despachar a cerrada o abierta 	
	def cambiarEstadoVenta(self):
		try:
			int(self.tablaVentaPorDespachar.item(self.tablaVentaPorDespachar.selection())['text'])
		except :	
			return

		idVenta = self.tablaVentaPorDespachar.item(self.tablaVentaPorDespachar.selection())['text']

		self.cambiarEstadoWind = Toplevel()
		self.cambiarEstadoWind.title('Cambiar Estado de la venta')	

		#Boton pata tomar la seleccion del cliente 
		ttk.Button(self.cambiarEstadoWind, text = 'Aceptar', command = lambda: self.editarEstado(self.estado.get(), idVenta)).grid(row = 2, column = 2)

		Label(self.cambiarEstadoWind, text = 'Estado').grid(row = 0, column = 0)
		self.estado = ttk.Combobox(self.cambiarEstadoWind, state="readonly")
		self.estado["values"] = ["ABIERTA","CERRADA"]
		self.estado.grid(row = 1 , column = 0)	

	#Toma los valores dados en cambiarEstadoVenta y los aplica en la bd	
	def editarEstado(self, estado, id):

		fecha = self.obtenerFeha()
		query = 'UPDATE venta SET estado = ?, fecha_venta = ? WHERE id_venta = ?'
		parametros = (estado, fecha, id)
		self.runQuery(query, parametros)
		self.cambiarEstadoWind.destroy()
		self.obtenerVentasPorDespachar()

		#Ventana de aviso y su contenido
		self.avisoEditar = Toplevel()
		self.avisoEditar.title("AVISO!")	

		Label(self.avisoEditar, text = 'La venta fue movida a "{}"'.format(estado)).grid(row = 0, column = 0)	
		ttk.Button(self.avisoEditar, text = 'OK', command = self.cerrarAvisoEditar).grid(row = 1, column = 2)

	#Funcionalidad del boton para cerrar la ventana emergente 	
	def cerrarAvisoEditar(self):
		self.avisoEditar.destroy()			

#++++++++++++++++++++++++++++++++++++++     Funciones en comun para ambas gestiones++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	#Ejecuta cualquier consulta que quiera hacerle a la base de datos
	def runQuery(self, query, parametros = ()):
		db_name = 'database.db'
		with sqlite3.connect(db_name) as conn:
		    cursor = conn.cursor()
		    result = cursor.execute(query, parametros)
		    conn.commit()
		return result	
	#Me da la fecha actual del sistema para llevar mas facilmente el control de las ventas 	
	def obtenerFeha(self):
		fecha = datetime.now()
		return str(fecha.day)+'/'+str(fecha.month)+'/'+str(fecha.year)

if __name__ == '__main__':
	window = Tk()
	app = clienteVenta(window)
	window.mainloop()



