#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys
from PyQt4.uic import *
from bases import Controlador

# Clase principal de la aplicación
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Cargamos la interfaz gráfica
        self.ui=loadUi("SKBio.ui",self)


        # Manejador de la base de datos
        self.base = Controlador()
        self.asados = []         
        print self.base.ultimo_asado()
        for i in range(self.base.ultimo_asado()):        
            print str(i)            
            asado = self.base.get_dato("Asado","fecha","id",i)
            self.asados.append(asado)
        print self.asados
        self.costoTotal = 0
        
        # Definicón de los eventos a suceder
        self.connect(self.ui.btnAgregarPersona, QtCore.SIGNAL('clicked()'), self.crearPersona)
        self.connect(self.ui.btnGuardarAsado, QtCore.SIGNAL('clicked()'), self.crearAsado)


    # Funciones a correr a raíz de los eventos

    def crearPersona(self):
        # Función que crea las nuevas personas que se agregaran
        nombre = str(self.ui.comboBoxPersonas.currentText())
        paga = str(self.ui.lblPaga.displayText())
        self.costoTotal = self.costoTotal + int(paga)
        self.ui.tbAsado.setRowCount(self.ui.tbAsado.rowCount()+1)
        itemNombre = QtGui.QTableWidgetItem(nombre)
        itemPaga = QtGui.QTableWidgetItem(paga)
        self.ui.tbAsado.setItem(self.ui.tbAsado.rowCount()-1, 0, itemNombre)
        self.ui.tbAsado.setItem(self.ui.tbAsado.rowCount()-1, 1, itemPaga)
        self.base.ingresar_persona(u"No se cargó dirección", nombre, u"No se cargó teléfono")
        self.base.guardar()
        idPersona = self.base.get_dato("Persona","id","nombre",nombre)
        idAsado = self.base.get_dato("Asado", "id", "fecha",str(self.ui.txtFecha.displayText()))
        self.base.ingresar_paga(int(idPersona), int(idAsado), int(paga))
        self.calcular(paga)

    def crearAsado(self):
        # Función que creará un nuevo asado
        fechaAsado = str(self.ui.txtFecha.displayText())
        direccionAsado = str(self.ui.comboBoxAsado.currentText())
        self.base.crear_asado(fechaAsado, direccionAsado)
        self.base.guardar()        
        print "Asado creado con éxito!"

    def calcular(self, costoTotal):
        cantPersonas = self.ui.tbAsado.rowCount()
        self.ui.lblMontoTotal.setText(costoTotal)
        self.ui.lblMontoPersona.setText(str(int(costoTotal)/cantPersonas))
        
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
