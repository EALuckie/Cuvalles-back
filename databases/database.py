#database.py
import pymysql.cursors

#Create connection
host: str
user: str
password: str
database: str
port: int
try:
    connection= pymysql.connect(
    host= '127.0.0.1',
    user= 'root',
    password= '',
    database= 'Thesis',
    port= 3306
    )
except:
    print("Connection error")

#Insert User
def InsertUser(no_user: int, pw: str, user_name: str, iD_Tipo= int):
    try:
        cursor= connection.cursor()
        sql= f"INSERT INTO `Usuarios` (`iD_Usuarios`, `Password`, `Nombres`, `Ap_paterno`, `Ap_materno`, `Email`, `Tipo_usuario`, `Foto_perfil`) VALUES ('{no_user}', '{pw}', '{user_name}', 'Herrera', 'Villalobos', 'josue@gm.vcom', '{iD_Tipo}', 'fd');"
        cursor.execute(sql)
        connection.commit()
    except:
        print("INSERT error")

#Select User
def SearchUser(id):
    try:
        cursor= connection.cursor()
        sql= f"SELECT * FROM `Usuarios` WHERE iD_Usuarios={id};"
        cursor.execute(sql)
        records = cursor.fetchall()
        connection.commit()
        username= str(records[-1][0])
        password= str(records[-1][1])
        email= str(records[-1][5])
        return {username:{"username":username,"email":email,"password":password}}
    except:
        {"SearchUser() error":"User not found"}
#Insert Message
#Mejor lo dejo para otro documento
def InsertMessage():
    pass


#Testing
if __name__== "__main__":
    InsertUser(10,1,"Ernesto","Luckie","","",1,)