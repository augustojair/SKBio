# -*- coding: utf-8 -*-

import sqlite3


class Controlador:
    #creamos la tabla si es que no existe     
    def __init__(self):
            self.conn = sqlite3.connect('base.db')
            print self.conn
            self.cursor = self.conn.cursor()                
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Asado
            (id INT PRIMARY KEY     NOT NULL,
            direccion      CHAR(50) NOT NULL,
            fecha          CHAR(50) NOT NULL,
            monto_total    INT,
            monto_individual INT);''')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Persona
               (id INT PRIMARY KEY     NOT NULL,
               direccion          CHAR(50) NOT NULL,
               nombre          CHAR(50) NOT NULL,
              telefono        INT);''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Deuda
               (id INT PRIMARY KEY     NOT NULL,
               id_persona         INT NOT NULL,
               id_asado        INT NOT NULL,
              monto        INT);''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Paga
               (id INT PRIMARY KEY     NOT NULL,
               id_persona         INT NOT NULL,
               id_asado        INT NOT NULL,
              monto        INT);''')                

            print "Tablas creadas";
    
        
    #gurdamos los cambios en el momento en 
    def __exit__(self):
        guardar()            
        self.close()

    def ingresar_persona(self, direccion ,nombre, telefono):
        idr = self.cursor.execute("SELECT MAX(id) FROM Persona")
        idrr = idr.fetchall()[0][0]
        if  idrr != None:
            idp = int(idrr)+1
        else:
            idp = 1
        a = (idp, direccion, nombre, telefono)
        self.cursor.execute("INSERT INTO Persona (id,direccion, nombre, telefono) VALUES (?,?,?,?)", a)
        print nombre+" se inserto correctamente"
        self.conn.commit()
        
    def modificar_persona(self,idp,direccion,nombre,telefono):
        a = (direccion,nombre,telefono,idp)
        self.cursor.execute("UPDATE Persona SET direccion = ?, nombre = ?, telefono = ? WHERE id = ?", a)
        print "se modifico correctamente"

    def consultar_usuarios(self):
        user = self.cursor.execute("SELECT nombre FROM Persona")
        return user.fetchall()[0]
        
    def existe_usuario(self,nombre):
        user = self.cursor.execute("SELECT nombre FROM Persona WHERE nombre = %s;" % nombre )
        return user.fetchall() != [] 

    def crear_asado(self,fecha,direccion):
        idr = self.cursor.execute("SELECT MAX(id) FROM Asado")
        idrr = idr.fetchall()[0][0]
        if  idrr != None:
            idp = int(idrr)+1
        else:
            idp = 1

        a = (idp, fecha, direccion, 0, 0)
        self.cursor.execute("INSERT INTO Asado (id,fecha, direccion, monto_individual, monto_total ) VALUES (?,?,?,?,?)", a)
        self.conn.commit()
        print "cambios guardados"
    
        print "el asado se creo correctamente"

    def ultimo_asado(self):
        idr = self.cursor.execute("SELECT MAX(id) FROM Asado")
        idrr = idr.fetchall()[0][0]
        if  idrr != None:
            idp = int(idrr)
        else:
            idp = 0
        return idp   

    def modificar_asado(self,idp,fecha,direccion,monto_total,monto_individual):
        a = (fecha,direccion,monto_total,monto_individual,idp)
        self.cursor.execute("UPDATE Asado SET (fecha = ?,direccion = ? ,monto_total = ? ,monto_individual = ?  WHERE id = ?", a)
        print "se modifico correctamente"

    def ver_tabla(self,tabla):
        q = self.cursor.execute("SELECT * FROM " + tabla)
        return q.fetchall()

    def ingresar_paga(self,idPersona, idAsado, cuantoPaga):
        idr = self.cursor.execute("SELECT MAX(id) FROM Asado")
        idrr = idr.fetchall()[0][0]
        if  idrr != None:
            idp = int(idrr)+1
        else:
            idp = 1
        
        
        
        a = (idp,idPersona,idAsado,cuantoPaga)
        self.cursor.execute("INSERT INTO Paga (id, id_persona, id_asado, monto) VALUES (?,?,?,?)", a)
        self.conn.commit()

    def get_dato(self,tabla,dato,columna,compara):       
        if type(compara) == int: 
                if compara != 0:  
                    a = "SELECT "+dato+" FROM "+tabla+" WHERE "+columna+" = "+str(compara)
                else:
                    a = "SELECT "+dato+" FROM "+tabla+" WHERE "+columna+" = "+str(1)
        else:                
                a = "SELECT "+dato+" FROM "+tabla+" WHERE "+columna+" = '"+compara+"'"
        datof = self.cursor.execute(a) 
        asd =  datof.fetchall()[0][0]        
        return asd


    def guardar(self):
        self.conn.commit()
        print "cambios guardados"
    
