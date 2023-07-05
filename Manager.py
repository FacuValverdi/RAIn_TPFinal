# Registro de datos en MySQL desde una GUI en TkInter

from tkinter import Entry, Label, Frame, Tk,Text, Button,ttk, Scrollbar, VERTICAL, HORIZONTAL,StringVar,END
from conexionBD import*
import threading

import webbrowser

class Registro(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
                                    
        self.frame1 = Frame(master)
        self.frame1.grid(columnspan=2, column=0,row=0)
        self.frame2 = Frame(master, bg='red')
        self.frame2.grid(column=0, row=1)
        self.frame3 = Frame(master)
        self.frame3.grid(rowspan=2, column=1, row=1)

        self.frame4 = Frame(master, bg='black')
        self.frame4.grid(column=0, row=2)

        self.buscar = StringVar()
        
       

        self.base_datos = Registro_datos()
        self.create_wietgs()
        

    def create_wietgs(self):
        Label(self.frame1, text = 'REVISOR  \t D E \t AVISOS CLASIFICADOS',bg='gray22',fg='white', font=('Orbitron',15,'bold')).grid(column=0, row=0)
        Label(self.frame2, text = 'OFERTAS!!!',fg='white', bg ='red', font=('Rockwell',12,'bold')).grid(columnspan=2, column=0,row=1, pady=5) 
        #TABLA OFERTA
        self.tablaOfertas = ttk.Treeview(self.frame2, height=15)
        self.tablaOfertas.grid(column=0, row=2)

        
        self.tablaOfertas.column('#0',minwidth=250, width=280, anchor='w')
        self.tablaOfertas.heading('#0', text='¡HAGA CLICK EN LA OFERTA!', anchor ='center')
        estiloOfertas = ttk.Style(self.frame2)
        estiloOfertas.theme_use('classic') #  ('clam', 'alt', 'default', 'classic')
        estiloOfertas.configure(".",font= ('Helvetica', 15, 'bold'), foreground='black')        
        estiloOfertas.configure("Treeview", font= ('Helvetica', 10, 'normal'), foreground='black')
        
        Label(self.frame4, text = 'Control',fg='white', bg ='black', font=('Rockwell',12,'bold')).grid(columnspan=3, column=0,row=0, pady=1, padx=4)         
        
        Button(self.frame4,command= self.scrappear, text='OBTENER DATOS', font=('Arial',10,'bold'), bg='yellow').grid(column=0,row=1, pady=10, padx=4)
        Button(self.frame4,command = self.limpiar_datos, text='LIMPIAR', font=('Arial',10,'bold'), bg='orange red').grid(column=1,row=1, padx=10)        
        Button(self.frame4,command= self.comparar, text='COMPARAR', font=('Arial',10,'bold'), bg='magenta2').grid(column=2,row=1,padx=4)
        Button(self.frame4,command = self.buscar_nombre, text='BUSCAR POR MODELO', font=('Arial',8,'bold'), bg='orange').grid(columnspan=2,column = 1, row=2)
        Entry(self.frame4,textvariable=self.buscar, font=('Arial',12), width=15).grid(column=0,row=2, pady=1, padx=8)
        Button(self.frame4,command = self.mostrar_todo, text='MOSTRAR DATOS', font=('Arial',10,'bold'), bg='green2').grid(columnspan=3,column=0,row=3, pady=8)


        self.tabla = ttk.Treeview(self.frame3, height=25)
        self.tabla.grid(column=0, row=0)

        ladox = Scrollbar(self.frame3, orient = HORIZONTAL, command= self.tabla.xview)
        ladox.grid(column=0, row = 1, sticky='ew') 
        ladoy = Scrollbar(self.frame3, orient =VERTICAL, command = self.tabla.yview)
        ladoy.grid(column = 1, row = 0, sticky='ns')

        self.tabla.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
       
        self.tabla['columns'] = ('Modelo', 'Precio','Moneda', 'Dominio','URL')

        self.tabla.column('#0', minwidth=10, width=30, anchor='w')
        self.tabla.column('Modelo', minwidth=110, width=150 , anchor='w')
        self.tabla.column('Precio', minwidth=60, width=90, anchor='center' )
        self.tabla.column('Moneda', minwidth=10, width=50, anchor='center' )
        self.tabla.column('Dominio', minwidth=40, width=70 , anchor='center')
        self.tabla.column('URL', minwidth=220, width=280, anchor='center')

        self.tabla.heading('#0', text='ID', anchor ='w')
        self.tabla.heading('Modelo', text='Modelo', anchor ='w')
        self.tabla.heading('Precio', text='Precio', anchor ='center')
        self.tabla.heading('Moneda', text='Moneda', anchor ='center')
        self.tabla.heading('Dominio', text='Dominio', anchor ='center')
        self.tabla.heading('URL', text='URL', anchor ='center')
       

        estilo = ttk.Style(self.frame3)
        estilo.theme_use('classic') #  ('clam', 'alt', 'default', 'classic')
        estilo.configure(".",font= ('Helvetica', 15, 'bold'), foreground='black')        
        estilo.configure("Treeview", font= ('Helvetica', 10, 'normal'), foreground='black',  background='white')
        estilo.map('Treeview',background=[('selected', 'green2')], foreground=[('selected','black')] )

        self.tabla.bind("<<TreeviewSelect>>", self.obtener_fila)  # seleccionar  fila
    
    def scrappear(self):
        #print(scrapper.mostrarTabla(scrapper.DOMINIO_OLX,scrapper.dicc1))
        self.base_datos.inserta_autos(scrapper.OLX,scrapper.dicc1)
        #print(scrapper.mostrarTabla(scrapper.DOMINIO_LAVOZ,scrapper.dicc2))
        self.base_datos.inserta_autos(scrapper.AUTOCOSMOS,scrapper.dicc2)
        #print(scrapper.mostrarTabla(scrapper.DOMINIO_LOSANDES,scrapper.dicc3))
        self.base_datos.inserta_autos(scrapper.LAVOZ,scrapper.dicc3)
        #print(scrapper.mostrarTabla(scrapper.DOMINIO_LOSANDES,scrapper.dicc3))
        self.base_datos.inserta_autos(scrapper.MERCADOLIBRE,scrapper.dicc4)
        self.mostrar_todo()
        
    def limpiar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.tablaOfertas.delete(*self.tablaOfertas.get_children())
        self.modelo.set('')
        self.precio.set('')
        self.moneda.set('')
        self.dominio.set('')
        self.URL.set('')
        self.Mensajes.set('')
    def buscar_nombre(self):
        nombre_modelo = self.buscar.get()
        nombre_modelo = str("'%"+nombre_modelo+"%'")
        self.mostrar_Oferta(nombre_modelo)
        nombre_buscado = self.base_datos.busca_autos(nombre_modelo)
        self.tabla.delete(*self.tabla.get_children())
        i = -1
        for dato in nombre_buscado:
            i= i+1                       
            self.tabla.insert("",i,text=nombre_buscado[i][0], values=nombre_buscado[i][1:6])

    def mostrar_Oferta(self,nombre):
        self.tablaOfertas.delete(*self.tablaOfertas.get_children())
        registro = self.base_datos.mostrar_precioBajo(nombre)
        i = -1
        for dato in registro:
            i= i+1                       
            self.tablaOfertas.insert("",i,text=registro[i][0:6])
        self.tablaOfertas.bind("<Double-1>", self.OnDoubleClick)
    def OnDoubleClick(self, event):
        item = self.tablaOfertas.selection()[0]
        url=self.tablaOfertas.item(item,"text")
        aux=url.find("https:")
        string= url[aux::]
        webbrowser.open(string, new=2, autoraise=True)
        
    def mostrar_todo(self):
        self.tabla.delete(*self.tabla.get_children())
        registro = self.base_datos.mostrar_autos()
        i = -1
        for dato in registro:
            i= i+1                       
            self.tabla.insert("",i,text=registro[i][0], values=registro[i][1:6])
        
    
    def obtener_fila(self, event):
        current_item = self.tabla.focus()
        if not current_item:
            return
        data = self.tabla.item(current_item)
        self.nombre_borar = data['values'][0]

    def comparar(self):
        # Crea un hilo
        hilo = threading.Thread(target=self.base_datos.compararPreciosAutos)
        # Inicia el hilo
        hilo.start()
        """notificacion=Notify()
        notificacion.title="OFERTAS"
        notificacion.message="¡¡El modelo "+lista[i].get("Modelo")+" esta en OFERTA!! El precio se encuentra en: "+lista[i].get("Moneda")+str(lista[i].get("Valor"))+".Su producto fue rebajado un "+str(listaAux[j][2]-lista[i].get("Valor"))+" menos.APROVECHE COMPRANDO ACA:"+lista[i].get("URL")
        notificacion.send()
        """
        """notificacion=Notify()
                    notificacion.title="OFERTAS"
        """ 
def main():
    ventana = Tk()
    ventana.wm_title("REVISOR DE AVISOS CLASIFICADOS")
    ventana.config(bg='gray22')
    ventana.geometry('1000x550')
    ventana.resizable(0,0)
    app = Registro(ventana)
    
    app.mainloop()
       

if __name__=="__main__":
    main()     