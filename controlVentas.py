"""

NOTA IMPORTANTE: Las ventas abiertas de cara al cliente y en la BD se llaman DESPACHADAS pero para fines de codigo
es abiertas (Variables, metodos y demas estan nombrados en base a "ABIERTA")

"""

import tkinter as tk
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
		self.wind['bg'] = '#3b5998'
		#midnight blue
		frameMain = LabelFrame(self.wind, text = 'Bienvenido al menu principal')
		frameMain.grid(row = 3, column = 3, columnspan = 3, pady = 20)
		frameMain['bg'] = '#8b9dc3'

		# Boton para ir a la seccion de clientes 
		tk.Button(frameMain, text = 'Gestionar Clientes', bg = '#f7f7f7', command = self.gestionCliente).grid(row = 3, columnspan = 2, sticky = W + E)
		#Boton para ir a la seccion de ventas 	
		tk.Button(frameMain, text = 'Gestionar Ventas', bg = '#ccd2e6', command = self.gestionVenta).grid(row = 4, columnspan = 2, sticky = W + E)	

#++++++++++++++++++++++++++++++++++++++++++++++++++++Gestion de clientes++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	#Diseño / acciones del boton "Gestionar clientes"	
	def gestionCliente(self):
		self.clienteWind = Toplevel()
		self.clienteWind.title('Gestion de Clientes')
		self.clienteWind['bg'] = '#3b5998'

		#Diseño de la ventana cliente
		frameCliente = LabelFrame(self.clienteWind, text = 'Registrar nuevo cliente')
		frameCliente.grid(row = 0, column = 0, columnspan = 3, pady = 20)
		frameCliente['bg'] = '#8b9dc3'

		# ingresar cedula
		Label(frameCliente, text = 'Cedula: ', bg = '#8b9dc3').grid(row = 1, column = 0)
		self.cedula = Entry(frameCliente)
		self.cedula.focus() #Este metodo es para colocar el cursor en la pimera casilla de una 
		self.cedula.grid(row = 1, column = 1) #Ubicacion de mi cuadro de entrada en la grilla 

		#ingresar nombre
		Label(frameCliente, text = 'Nombre: ', bg = '#8b9dc3').grid(row = 2, column = 0)
		self.nombre = Entry(frameCliente)
		self.nombre.grid(row = 2, column = 1)

		#ingresar apellido
		Label(frameCliente, text = 'Apellido', bg = '#8b9dc3').grid(row = 3, column = 0)
		self.apellido = Entry(frameCliente)
		self.apellido.grid(row = 3, column = 1)

		#ingresar alias
		Label(frameCliente, text = 'Alias', bg = '#8b9dc3').grid(row = 4, column = 0)
		self.alias = Entry(frameCliente)
		self.alias.grid(row = 4, column = 1)

		#ingresar telefono
		Label(frameCliente, text = 'Telefono', bg = '#8b9dc3').grid(row = 5, column = 0)
		self.telefono = Entry(frameCliente)
		self.telefono.grid(row = 5, column = 1)

		#ingresar direccion
		Label(frameCliente, text = 'Direccion', bg = '#8b9dc3').grid(row = 6, column = 0)
		self.direccion = Entry(frameCliente)
		self.direccion.grid(row = 6, column = 1)

		#Botones de gestion de clientes
		#Boton para insertar
		tk.Button(frameCliente, text = 'Registrar cliente', bg = '#ccd2e6', command = self.registroCliente).grid(row = 7, columnspan = 2, sticky = W + E)
		#Boton para eliminar
		tk.Button(self.clienteWind, text = 'Eliminar cliente', bg = '#eb919a', command = self.eliminarCliente).grid(row = 4, column = 5, sticky = W + E)
		#boton para editar cliente
		tk.Button(self.clienteWind, text = 'Editar cliente', bg = '#ccd2e6', command = self.editarCliente).grid(row = 4, column = 4, sticky = W + E)

		#Mensajes para el usuario (Modulo cliente)
		#mensaje de error
		self.mensajeError = Label(self.clienteWind, text = '', fg = 'black')
		self.mensajeError.grid(row = 2, column = 0, columnspan = 2, sticky = W + E)
		self.mensajeError['bg'] = '#3b5998'
		#Mensaje de accion exitosa
		self.mensajeExito = Label(self.clienteWind, text = '', fg = 'black')
		self.mensajeExito.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
		self.mensajeExito['bg'] = '#3b5998'

		# Tabla para mostrar usuarios dentro de la gestion de cientes
		self.tablaCliente = ttk.Treeview(self.clienteWind, height = 15, columns = ('#0', '#1', '#2', '#3', '#4'))
		self.tablaCliente.grid(row = 8, column = 0, columnspan = 6)
		self.tablaCliente.heading('#0', text = 'Cedula', anchor = CENTER)
		self.tablaCliente.heading('#1', text = 'Nombre', anchor = CENTER)
		self.tablaCliente.heading('#2', text = 'Apellido', anchor = CENTER)
		self.tablaCliente.heading('#3', text = 'Alias', anchor = CENTER)
		self.tablaCliente.heading('#4', text = 'Telefono', anchor = CENTER)
		self.tablaCliente.heading('#5', text = 'Direccion', anchor = CENTER)
		self.obtenerClientes()

		#Estilo de la tabla
		s = ttk.Style()
		s.theme_use('clam')
		self.tablaCliente.tag_configure('par', background = '#f7f7f7')
		self.tablaCliente.tag_configure('impar', background = '#ccd2e6')

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
		self.editarclienteWind['bg'] = '#3b5998'
	

		#Frame para los datos
		frameEditarCliente = LabelFrame(self.editarclienteWind, text = 'Actualizacion de cliente')
		frameEditarCliente.grid(row = 0, column = 0, columnspan = 3, pady = 20)
		frameEditarCliente['bg'] = '#8b9dc3'


		#vaiables para hacer prueba 
		self.cedulaPrueba = StringVar()
		self.nombrePrueba= StringVar()
		self.apellidoPrueba= StringVar()
		self.aliasPrueba = StringVar()
		self.telefonoPrueba = StringVar()
		self.direccionPrueba = StringVar()

		# modificar cedula
		Label(frameEditarCliente, text = 'Nueva cedula:', bg = '#8b9dc3').grid(row = 1, column = 3)
		self.nuevoCedula = Entry(frameEditarCliente, textvariable = self.cedulaPrueba)
		self.nuevoCedula.insert(0, self.oldCedula)
		self.nuevoCedula.focus()
		self.nuevoCedula.grid(row = 1 , column = 4)	

		#Modificar nombre
		Label(frameEditarCliente, text = 'Nuevo nombre:', bg = '#8b9dc3').grid(row = 2, column = 3)
		self.nuevoNombre = Entry(frameEditarCliente, textvariable = self.nombrePrueba)
		self.nuevoNombre.insert(0, self.oldNombre)
		self.nuevoNombre.grid(row = 2, column = 4)

		#Modificar Apellido
		Label(frameEditarCliente, text = 'Nuevo apellido:', bg = '#8b9dc3').grid(row = 3, column = 3)
		self.nuevoApellido = Entry(frameEditarCliente, textvariable = self.apellidoPrueba)
		self.nuevoApellido.insert(0, self.oldApellido)
		self.nuevoApellido.grid(row = 3, column = 4)

		#Modificar Alias		
		Label(frameEditarCliente, text = 'Nuevo alias: ', bg = '#8b9dc3').grid(row = 4, column = 3)
		self.nuevoAlias = Entry(frameEditarCliente, textvariable = self.aliasPrueba)
		self.nuevoAlias.insert(0, self.oldAlias)
		self.nuevoAlias.grid(row = 4, column = 4)

		#Modificar Telefono
		Label(frameEditarCliente, text = 'Nuevo telefono', bg = '#8b9dc3').grid(row = 5, column = 3)
		self.nuevoTelefono = Entry(frameEditarCliente, textvariable = self.telefonoPrueba)
		self.nuevoTelefono.insert(0, self.oldTelefono)
		self.nuevoTelefono.grid(row = 5, column = 4)

		#Modificar Direccion
		Label(frameEditarCliente, text = 'Nueva direccion', bg = '#8b9dc3').grid(row = 6, column = 3)
		self.nuevoDireccion = Entry(frameEditarCliente, textvariable = self.direccionPrueba)
		self.nuevoDireccion.insert(0, self.oldDireccion)
		self.nuevoDireccion.grid(row = 6, column = 4)

		#Boton para confirmar los cambios
		tk.Button(self.editarclienteWind, text = '   Aceptar   ', bg = '#ccd2e6', command = lambda: self.updateCliente(self.cedulaPrueba.get(), self.nombrePrueba.get(), self.apellidoPrueba.get(), self.aliasPrueba.get(), self.telefonoPrueba.get(), self.direccionPrueba.get())).grid(row = 7, column = 4, sticky = W + E)
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
		i = 0
		for fila in filas:
			if i%2 == 0:
				self.tablaCliente.insert('', 0, text = fila[1], values = (fila[2], fila[3], fila[4], fila[5], fila[6]), tags=('par',))
			else:
				self.tablaCliente.insert('', 0, text = fila[1], values = (fila[2], fila[3], fila[4], fila[5], fila[6]), tags=('impar',))
			i += 1		
#++++++++++++++++++++++++++++++++++++++++++++++++ Gestion de ventas+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	

	def gestionVenta(self):
		self.ventaWind = Toplevel()
		self.ventaWind.title('Gestion de Ventas')
		self.ventaWind.geometry('400x200')
		self.ventaWind['bg'] = '#3b5998'
		"""
		bg = 'alice blue',
		, bg = '#f7f7f7'
		, bg = '#ccd2e6'
		"""
		frameGestionVenta = LabelFrame(self.ventaWind, text = 'Bienvenido al menu principal')
		frameGestionVenta.grid(row = 3, column = 3, columnspan = 3, pady = 20)
		frameGestionVenta['bg'] = '#8b9dc3'
		#Botones
		tk.Button(frameGestionVenta, text = 'Crear nueva venta', bg = '#f7f7f7', command = self.crearVenta).grid(row = 0, columnspan = 2, sticky = W + E)
		tk.Button(frameGestionVenta, text = 'Consultar ventas despachadas', bg = '#ccd2e6', command =self.ventasAbiertas).grid(row = 1, columnspan = 2, sticky = W + E)
		tk.Button(frameGestionVenta, text = 'Consultar ventas por despachar', bg = '#f7f7f7', command = self.ventasPorDespachar).grid(row = 2, columnspan = 2, sticky = W + E)
		tk.Button(frameGestionVenta, text = 'Consultar ventas cerradas', bg = '#ccd2e6', command = self.ventasCerradas).grid(row = 3, columnspan = 2, sticky = W + E)
		

	#Crea un nuevo registro de venta. utiliza los siguientes metodos
	#seleccionarCliente()
	#obtenerSeleccionClientes()
	#obtenerClienteParametro()
	#calculoVenta()
	#calcular()
	#registrarVenta()
	def crearVenta(self):
		self.crearVentaWind = Toplevel()
		self.crearVentaWind.title('Crear nueva venta')
		self.crearVentaWind.geometry('400x250')
		self.crearVentaWind['bg'] = '#3b5998'

		#Frame para los datos
		frameCrearVenta = LabelFrame(self.crearVentaWind)
		frameCrearVenta.grid(row = 0, column = 0, columnspan = 3, pady = 20)
		frameCrearVenta['bg'] = '#8b9dc3'

		#Diseño esctructura interna de la ventana

		#Ingresar deuda (Se calcula automaticamente)
		Label(frameCrearVenta, text = 'Deuda', bg = '#8b9dc3').grid(row = 1, column = 0)
		self.deuda = Entry(frameCrearVenta)
		self.deuda.grid(row = 1, column = 1)
		#Boton genera una ventana par hacer el total  de la venta 
		tk.Button(frameCrearVenta, text = 'Calcular monto de venta', bg = '#ccd2e6', command = self.calculoVenta).grid(row = 0,  columnspan = 4, sticky = W + E)

		#ingresar la descripcion de la venta (SE realizara automaticamente de acuerdo a la compra)
		Label(frameCrearVenta, text = 'Descripcion', bg = '#8b9dc3').grid(row = 2, column = 0)
		self.descripcion = Entry(frameCrearVenta)
		self.descripcion.grid(row = 2, column = 1)

		#entrada especial que me genera una lista de valores predefinidos
		Label(frameCrearVenta, text = 'Estado', bg = '#8b9dc3').grid(row = 3, column = 0)
		self.estado = ttk.Combobox(frameCrearVenta)
		self.estado = ttk.Combobox(frameCrearVenta, state="readonly")
		self.estado["values"] = ["POR DESPACHAR", "DESPACHADA"]
		self.estado.grid(row = 3, column = 1)

		#Boton de ventana emergente para seleccionar al cliente de una lista que viene de los datos de la BD
		tk.Button(frameCrearVenta, text = 'Seleccionar Comprador', bg = '#ccd2e6', command = self.seleccionarCliente).grid(row = 4, columnspan = 4, sticky = W + E )
		#Boton de la ventana emergente que toma los datos de la nueva venta 
		tk.Button(self.crearVentaWind, text = 'Aceptar', bg = '#ccd2e6', command = lambda: self.registrarVenta(self.descripcion.get(), self.deuda.get(), self.estado.get(), self.cedulaComprador.get(), self.nombreComprador.get() )).grid(row = 1, column = 2, sticky = W + E )

		#inresar cedula del ciente, se inserta atumaticamente desde el metodo obtenerClienteParametro()
		Label(frameCrearVenta, text = 'Cedula', bg = '#8b9dc3').grid(row = 5, column = 0)
		self.cedulaComprador = Entry(frameCrearVenta)
		self.cedulaComprador.grid(row = 5, column = 1)	

		#inresar nombre del ciente, se inserta atumaticamente desde el metodo obtenerClienteParametro()
		Label(frameCrearVenta, text = 'Nombre', bg = '#8b9dc3').grid(row =6, column = 0)
		self.nombreComprador = Entry(frameCrearVenta)
		self.nombreComprador.grid(row = 6, column = 1)	

	#Ventana con la lista de clientes registrados para facilitar el tomar los datos y casar un cliente con un pedido/venta	
	def seleccionarCliente(self):
		self.selecCliente = Toplevel()
		self.selecCliente.title('Clientes registrados')
		self.selecCliente['bg'] = '#3b5998'

		#Tema de la tabla
		s = ttk.Style()
		s.theme_use('clam')
		
		#DEclaracion y diseño de la tabla que contendrá los datos d elos clientes 
		self.tablaSelecCliente = ttk.Treeview(self.selecCliente, height = 10, columns = ('#0', '#1'))
		self.tablaSelecCliente.grid(row = 0, column = 0, columnspan = 6)
		self.tablaSelecCliente.heading('#0', text = 'Cedula', anchor = CENTER)
		self.tablaSelecCliente.heading('#1', text = 'Nombre', anchor = CENTER)
		self.tablaSelecCliente.heading('#2', text = 'Alias', anchor = CENTER)
		self.obtenerSeleccionClientes() 

		#Boton para ejecutar la seleccion de cliente 
		tk.Button(self.selecCliente, text = 'Seleccionar', bg = '#ccd2e6', command = self.obtenerClienteParametro).grid(row = 1, column = 3, columnspan = 3, sticky = W + E )

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
		self.calculoWind['bg'] = '#3b5998'

		frameCalculoVenta = LabelFrame(self.calculoWind, text = 'Ingrese valores en los campos correspondientes')
		frameCalculoVenta.grid(row = 0, column = 0, columnspan = 3, pady = 20)
		frameCalculoVenta['bg'] = '#8b9dc3'

		#Ron
		Label(frameCalculoVenta, text = 'Ron', bg = '#8b9dc3').grid(row = 0, column = 0)
		Label(frameCalculoVenta, text = 'litros', bg = '#8b9dc3').grid(row = 1, column = 0)
		Label(frameCalculoVenta, text = 'Precio', bg = '#8b9dc3').grid(row = 1, column = 2)
		ronl = Entry(frameCalculoVenta)
		ronl.insert(0, '0')
		ronl.grid(row = 1, column = 1)
		ronp = Entry(frameCalculoVenta)
		ronp.insert(0, '0')
		ronp.grid(row = 1, column = 3)

		#Anis
		Label(frameCalculoVenta, text = 'Anis', bg = '#8b9dc3').grid(row = 2, column = 0)
		Label(frameCalculoVenta, text = 'litros', bg = '#8b9dc3').grid(row = 3, column = 0)
		Label(frameCalculoVenta, text = 'Precio', bg = '#8b9dc3').grid(row = 3, column = 2)
		anisl = Entry(frameCalculoVenta)
		anisl.insert(0, '0')
		anisl.grid(row = 3, column = 1)
		anisp = Entry(frameCalculoVenta)
		anisp.insert(0, '0')
		anisp.grid(row = 3, column = 3)

		#canaClara
		Label(frameCalculoVenta, text = 'Caña Clara', bg = '#8b9dc3').grid(row = 4, column = 0)
		Label(frameCalculoVenta, text = 'litros', bg = '#8b9dc3').grid(row = 5, column = 0)
		Label(frameCalculoVenta, text = 'Precio', bg = '#8b9dc3').grid(row = 5, column = 2)
		cClaral = Entry(frameCalculoVenta)
		cClaral.insert(0, '0')
		cClaral.grid(row = 5, column = 1)
		cClarap = Entry(frameCalculoVenta)
		cClarap.insert(0, '0')
		cClarap.grid(row = 5, column = 3)

		tk.Button(self.calculoWind, text = 'Calcular', bg = '#ccd2e6', command = lambda: self.calcular(int(ronl.get()), float(ronp.get()), int(anisl.get()), float(anisp.get()), int(cClaral.get()), float(cClarap.get()))).grid(row = 6, column = 4, sticky = W + E)


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
		self.ventaCerradaWind['bg'] = '#3b5998'

		#Boton para cerrar la ventana (unico boton de esta seccion (Por ahora))
		tk.Button(self.ventaCerradaWind, text = 'Salir', bg = '#eb919a', command = self.cerrarCerradas).grid(row = 9, column = 5, sticky = W + E)	
		#Tema de la tabla
		s = ttk.Style()
		s.theme_use('clam')
		#DEclaracion y diseño de la tabla que contendrá los datos de las ventas cerradas  
		self.tablaVentaCerrada = ttk.Treeview(self.ventaCerradaWind, height = 15, columns = ('#0', '#1', '#2', '#3', '#4', '#5'))
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
		self.ventaPorDespacharWind['bg'] = '#3b5998'

		tk.Button(self.ventaPorDespacharWind, text = 'Salir', bg = '#eb919a', command = self.cerrarPorDespachar).grid(row = 9, column = 5, sticky = W + E)	
		tk.Button(self.ventaPorDespacharWind, text = 'Cambiar estado de la venta', bg = '#ccd2e6', command = self.cambiarEstadoVenta).grid(row = 9, column = 4, sticky = W + E)
		
		#Tema de la tabla
		s = ttk.Style()
		s.theme_use('clam')

		#DEclaracion y diseño de la tabla que contendrá los datos de las ventas por despachar  
		self.tablaVentaPorDespachar = ttk.Treeview(self.ventaPorDespacharWind, height = 15, columns = ('#0', '#1', '#2', '#3', '#4', '#5'))
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
		self.ventaAbiertaWind.title("Ventas Despachadas")
		self.ventaAbiertaWind['bg'] = '#3b5998'

		tk.Button(self.ventaAbiertaWind, text = 'Salir', bg = '#eb919a', command = self.cerrarAbiertas).grid(row = 9, column = 5, sticky = W + E)	
		tk.Button(self.ventaAbiertaWind, text = 'Abono', bg = '#ccd2e6', command= self.abonar).grid(row = 9, column = 4, sticky = W + E)

		#Tema de la tabla
		s = ttk.Style()
		s.theme_use('clam')

		#DEclaracion y diseño de la tabla que contendrá los datos de las ventas abiertas  
		self.tableVentaAbierta = ttk.Treeview(self.ventaAbiertaWind, height = 15, columns = ('#0', '#1', '#2', '#3', '#4', '#5'))
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
		parametro = ('DESPACHADA',)
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
		self.abonarWind['bg'] = '#3b5998'

		#Frame para gestionar el abono
		frameAbonar = LabelFrame(self.abonarWind, text ='Ingresar abono a la venta corresponiente a '+ self.nombreCliente)
		frameAbonar.grid(row = 0, column = 0, columnspan = 3, pady = 20)
		frameAbonar['bg'] = '#8b9dc3'

		#Boton me da acceso a al metodo donde se realizan los cambios en la deuda
		tk.Button(self.abonarWind, text = 'Aceptar', bg = '#ccd2e6', command = lambda: self.editarDeuda(self.entradaAbono.get(), self.idVenta)).grid(row = 1, column = 2, sticky = W + E)	


		#Diseño esctructura interna de la ventana
		#deuda
		Label(frameAbonar, text = 'Deuda actual', bg = '#8b9dc3').grid(row = 0, column = 0)
		self.deudaActual = Entry(frameAbonar, textvariable = StringVar(frameAbonar, value = self.deudaCliente), state = 'readonly')
		self.deudaActual.grid(row = 0 , column = 1)

		#Abono
		Label(frameAbonar, text = 'Abono', bg = '#8b9dc3').grid(row = 1, column = 0)
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
			self.aviso['bg'] = '#3b5998'	

			Label(self.aviso, text = 'EL cliente pago la totalidad de la deuda, La venta fue movida a "Ventas cerradas"', bg = '#8b9dc3').grid(row = 0, column = 0)	
			tk.Button(self.aviso, text = 'OK', bg = '#ccd2e6', command = self.cerrarAviso).grid(row = 1, column = 2)

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
		self.cambiarEstadoWind['bg'] = '#3b5998'

		frameCambiarEstadoWind = LabelFrame(self.cambiarEstadoWind, text ='Estado')
		frameCambiarEstadoWind.grid(row = 0, column = 0, columnspan = 3, pady = 20)
		frameCambiarEstadoWind['bg'] = '#8b9dc3'

		#Boton pata tomar la seleccion del cliente 
		tk.Button(self.cambiarEstadoWind, text = 'Aceptar', bg = '#ccd2e6', command = lambda: self.editarEstado(self.estado.get(), idVenta)).grid(row = 2, column = 2)

		Label(frameCambiarEstadoWind, text = 'Estado', bg = '#8b9dc3').grid(row = 0, column = 0)
		self.estado = ttk.Combobox(frameCambiarEstadoWind, state="readonly")
		self.estado["values"] = ["DESPACHADA","CERRADA"]
		self.estado.grid(row = 1 , column = 0)	

	#Toma los valores dados en cambiarEstadoVenta y los aplica en la bd	
	def editarEstado(self, estado, id):

		if estado == 'DESPACHADA' or estado == 'CERRADA':
			fecha = self.obtenerFeha()
			query = 'UPDATE venta SET estado = ?, fecha_venta = ? WHERE id_venta = ?'
			parametros = (estado, fecha, id)
			self.runQuery(query, parametros)
			self.cambiarEstadoWind.destroy()
			self.obtenerVentasPorDespachar()

			#Ventana de aviso y su contenido
			self.avisoEditar = Toplevel()
			self.avisoEditar.title("AVISO!")
			self.avisoEditar['bg'] = '#3b5998'	

			Label(self.avisoEditar, text = 'La venta fue movida a "{}"'.format(estado), bg = '#8b9dc3').grid(row = 0, column = 0)	
			tk.Button(self.avisoEditar, text = 'OK', bg = '#ccd2e6', command = self.cerrarAvisoEditar).grid(row = 1, column = 2)

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





