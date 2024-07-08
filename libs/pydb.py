import sqlite3
import bcrypt
import datetime

class Pydb:

    db_file ='db/PytuinoDB.db'
    db = None

    def __init__(self):
        self.db=sqlite3.connect(self.db_file)
        self.creartablaUser()
        self.useradm()
        self.creartablaLeds()

    def creartablaUser(self):
        try:
            cursor=self.db.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios(
                id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                correo TEXT NOT NULL UNIQUE,
                rol INTEGER NOT NULL,
                ultimavez TEXT NULL,
                contrasena TEXT NOT NULL
                )
            ''')
            self.db.commit()
            
        except:
            print("No se ha podido crear la tabla usuarios")

    def creartablaLeds(self):
        try:
            cursor=self.db.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS leds(
                id_led INTEGER PRIMARY KEY AUTOINCREMENT,
                instruccion TEXT NOT NULL UNIQUE
                )
            ''')
            self.db.commit()
        except:
            print("No se ha podido crear la leds")

    def searchUsers(self, tabla):
        cursor=self.db.cursor()     
        cursor.execute("SELECT * FROM "+ tabla)
        resultados=cursor.fetchall()
        for row in resultados:
            print(row[0])

    def insertUser(self, usuario, password,nombres,correo):
        try:
            cursor=self.db.cursor()
            passprotegida = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO usuarios ('nombres','usuario','correo','rol','contrasena') VALUES (?,?,?,?,?)",(nombres,usuario,correo,"2",passprotegida))
            self.db.commit()
            
            print("Usuarios registrados correctamente.")
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self.db.close()
    
    def insertLeds(self,combinacion):
        try:
            cursor=self.db.cursor()
            valor=combinacion
            cursor.execute("INSERT INTO leds ('instruccion') VALUES (?)",(valor,))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            print("Ya se ha ingresado ese valor")
            return False
        finally:
            self.db.close()

    def useradm(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT usuario FROM usuarios WHERE id_user = 1")
        resultado = cursor.fetchone()
        if not resultado:
            cursor = self.db.cursor()
            passprotegida = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO usuarios (nombres,usuario,correo,rol,contrasena) VALUES (?,?,?,?,?)",("admin","admin","admin@pytuino.com",1,passprotegida))
            self.db.commit()
            return True

    def vefuser(self, datos):
        cursor = self.db.cursor()
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (datos,))
        resultado = cursor.fetchone()
        print(resultado)
        if resultado and resultado[0] is not None:
            print("El nombre de usuario ya está registrado.")
            return False
        else:
            print("El nombre de usuario está disponible. Puedes registrarte.")
            return True
        
    def vefmail(self, datos):
        cursor = self.db.cursor()
        cursor.execute("SELECT correo FROM usuarios WHERE correo = ?", (datos,))
        resultado = cursor.fetchone()
        print(resultado)
        if resultado and resultado[0] is not None:
            print("El correo ya está registrado.")
            return False
        else:
            print("El correo está disponible. Puedes registrarte.")
            return True

    def loginUser(self, username, passwordu):
        cursor = self.db.cursor()
        cursor.execute("SELECT u.* FROM usuarios u WHERE u.usuario = ?",(username,))
        resultado = cursor.fetchone()
        if resultado:
            contrasena = resultado[6]
            if bcrypt.checkpw(passwordu.encode('utf-8'),contrasena):
                datos = [resultado[1],resultado[2],resultado[3],resultado[4],resultado[5]]
                try:
                    cursor = self.db.cursor()
                    cursor.execute("UPDATE usuarios SET ultimavez=? WHERE usuario = ?",(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),username))
                    self.db.commit()
                except:
                    print("No se ha podido actualizar la fecha de ultima vez")
                return datos
            else:
                print("Contraseña incorrecta")
                return False
        self.db.close()
    
    def obtenerLeds(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT instruccion FROM leds")
        resultado = cursor.fetchall()
        lista_resultado = [fila[0] for fila in resultado]
        print(lista_resultado[0].split("/"))
        return lista_resultado
    
    def comprobarPass(self,usuario,passwo):
        cursor = self.db.cursor()
        passprotegida = bcrypt.hashpw(passwo.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ? AND contrasena = ?",(usuario,passprotegida))
        resultado = cursor.fetchone()
        if resultado:
            print("contrasena correcta")
            return True
        else:
            print("Todo mal :(")
            return False