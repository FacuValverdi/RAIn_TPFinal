import mysql.connector  #pip install mysql-connector-python
import time
import scrapper
from collections import OrderedDict
from notifypy import Notify
from email.message import EmailMessage
import smtplib

class Registro_datos():
    def __init__(self):
        self.conexion = mysql.connector.connect( host='localhost',
                                                port=3306,
                                                database ='vehiculos', 
                                                user = 'root',
                                                passwd ='')
        
    def inserta_autos(self,dominio,lista):
        try:
            cur = self.conexion.cursor()
            sql="INSERT INTO `autos`(`Modelo`, `Precio`, `Moneda`, `Dominio`, `URL`) VALUES (%s,%s,%s,%s,%s)"
            for v in lista:
                    aux=(v.get('Modelo'),v.get('Valor'),v.get('Moneda'),dominio,v.get('URL'))
                    cur.execute(sql,aux)
                    self.conexion.commit()
                    #cur.close()
            print("Se inserto el registo en la tabla correctamente")
        except:
            print("Ocurrio un error a insertar el registro en la tabla")
            
    def mostrar_autos(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM autos " 
        cursor.execute(sql)
        registro = cursor.fetchall()
        return registro
    def busca_autos(self, nombre_auto):
        cur = self.conexion.cursor()
        sql = "select * from `autos`where `Modelo` like {}".format(nombre_auto)#Anteriormente Presc ASC
        cur.execute(sql)
        nombreX = cur.fetchall()  
        return nombreX 
    def mostrar_precioBajo(self,modelo):
        cur2 = self.conexion.cursor()
        sql="SELECT `Modelo`,MIN(`Precio`),`Moneda`,`Dominio`,`URL` FROM `autos` Where `Modelo` like "+modelo+" and `Precio`=(SELECT MIN(`Precio`) FROM `autos` Where `Modelo` like "+modelo+" and `Precio`<>1)  GROUP by `Modelo`"
        cur2.execute(sql)
        registro = cur2.fetchall()  
        return registro
 
    def compararPrecios(self,lista):
        auxS=[]
        listaAux=[]
        notificacion = Notify()
        notificacion.title = "OFERTA DE ULTIMA HORA!"
        for i in range(len(lista)):
            auxS.append(lista[i].get("Modelo"))
        final_list = OrderedDict.fromkeys(auxS)
        cur=self.conexion.cursor()
        cur.execute("SELECT `Modelo`,MIN(`Precio`),`Moneda`,`Dominio`,`URL` FROM `autos` WHERE `Modelo`IN "+str(tuple(final_list))+"AND `Precio`<>1 GROUP BY `Modelo`")
        #print(lista)
        for fila in cur:
                listaAux.append(fila)
        #print(listaAux)
        for i in range(len(lista)):
            for j in range(len(listaAux)):
                if(lista[i].get("Modelo")==listaAux[j][0]):
                    if(lista[i].get("Moneda")==listaAux[j][2]):
                        if(lista[i].get("Valor")>1):
                            if (lista[i].get("Valor")<listaAux[j][1]):
                                #MOSTRAR EN UNA NOTIFICACION POR ESCRITORIO
                                notificacion.message="¡¡El modelo "+lista[i].get("Modelo")+" esta en OFERTA!!"+"\nEl precio se encuentra en: "+lista[i].get("Moneda")+" "+str((lista[i].get("Valor")))+"\nSu producto fue rebajado "+str((listaAux[j][1])-(lista[i].get("Valor")))+" menos.\n APROVECHE COMPRANDO ACA:"+lista[i].get("URL")
                                #MOSTRAR POR CORREO 
                                enviarCorreo("¡¡El modelo "+lista[i].get("Modelo")+" esta en OFERTA!!"+"\nEl precio se encuentra en: "+lista[i].get("Moneda")+" "+str((lista[i].get("Valor")))+"\nSu producto fue rebajado "+str((listaAux[j][1])-(lista[i].get("Valor")))+" menos.\n APROVECHE COMPRANDO ACA:"+lista[i].get("URL"))

                                #MOSTRAR POR CONSOLA
                                print("¡¡El modelo "+lista[i].get("Modelo")+" esta en OFERTA!!")
                                print("ANTES: "+listaAux[j][2]+str(listaAux[j][1])+" .")
                                print("AHORA...")
                                print("El precio se encuentra en: "+lista[i].get("Moneda")+str(lista[i].get("Valor"))+"")
                                print("Su producto fue rebajado un "+str((listaAux[j][1]-lista[i].get("Valor")))+" menos.APROVECHE COMPRANDO ACA:"+lista[i].get("URL"))
                                #self.actualizar_producto(lista[i])
                                notificacion.send()
                                return lista[i]
                        
    def compararPreciosAutos(self):
        while(True):
                            print("estoy comparando precios!")
                            self.compararPrecios(scrapper.dicc1)
                            self.compararPrecios(scrapper.dicc2)
                            self.compararPrecios(scrapper.dicc3)
                            self.compararPrecios(scrapper.dicc4)
                            time.sleep(30)
def enviarCorreo(mensaje):
        remitente = "facu.valverdi14@gmail.com"
        destinatario = "aasaassas@gmail.com"
        email = EmailMessage()
        email["From"] = remitente
        email["To"] = destinatario
        email["Subject"] = "¡¡OFERTA EN UN AVISO DE AUTOS!!"
        email.set_content(mensaje)
        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remitente, "clave") #GENERAR CLAVE EN LA PARTE DE SEGURIDAD DE GOOGLE
        smtp.sendmail(remitente, destinatario, email.as_string())
        smtp.quit()  
         
    
""" def actualizar_precios(self,lista):
        try:
            cur = self.conexion.cursor()
            slqID="SELECT `ID` FROM `autos` WHERE `Modelo`=%s and `URL`=%s"
            sql="UPDATE `autos` SET `Precio`=%s,`Moneda`=%s WHERE `ID`=%s "
            aux1=(lista.get('Modelo'),lista.get('URL'))
            ID=cur.execute(slqID,aux1)
            aux2=(lista.get('Valor'),lista.get('Moneda'),ID)
            cur.execute(sql,aux2)
            self.conexion.commit()
                    #cur.close()
            print("Se actualizo el registo correctamente")
        except:
            print("Ocurrio un error a actualizar la tabla")
"""  