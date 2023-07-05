from bs4 import BeautifulSoup
import requests
#CODIGO PARA RASCAR/RECUPERAR INFORMACION DE PAGINAS WEBs, EN ESTE CASO AVISOS CLASIFICADOS
#CREADO POR FACUNDO VALVERDI


##SCRAPPING WEBS de AVISOS CLASIFICADOS
#---OLX---
OLX="OLX"
DOMINIO_OLX="https://www.olx.com.ar"
urlOLX="https://www.olx.com.ar/autos_c378"

#LIMPIEZA
#LIMPIEZA GENERAL de PRECIOS(SE USA PARA LAS 4 PAGINAS)
def limpiarPrecios(opcion,precios):
    aux=precios.split(sep=" ")
    if (aux[0]=="consultar"):
            if(opcion==0):
                return '$'
            else:
                 return 1  
    else:
            if(opcion==0 and len(aux)!=1):
                return aux[0]
            else:
                if(opcion==0 and len(aux)==1):
                    StrA = "".join(aux)
                    if(StrA[0]=="$"):
                            return "$"
                    else:
                            return "U$S"
                else: 
                    if((opcion==1) and (len(aux)==1)):
                            StrB = "".join(aux)
                            if(StrB[0]=="u"or StrB[0]=="U"):
                                    indice=3
                            else:
                                if(StrB[0]=="$"or StrB[0]!="$"):
                                    indice=1
                                return int(StrB[indice:].replace('.', '')) #Sacar los puntos decimales para realizar operaciones.
                    else:
                        if((opcion==1) and (len(aux)!=1)):
                            return int(aux[1].replace('.', '')) #Sacar
#LIMPIEZA DE URL OLX
def limpiarURL(dominio,url):
    
        if(url("href")is not None):
            if(url.get("href").find("/item/")!=-1):
                return dominio+url.get("href")


#EXTRACCION OLX
def extraerDatos1(soup):
    aux=[]
    for dato in soup:
        modelo = dato.find("div",attrs={"class":"_2Gr10","data-aut-id":"itemTitle"})
        
        if(modelo is not None):
            precio = dato.find("span",attrs={"class":"_1zgtX","data-aut-id":"itemPrice"})
            url = dato.find("a",attrs={"class":""})
            
            aux.append({
                    
                        'Modelo':modelo.text,
                        'Valor':limpiarPrecios(1,precio.text.strip()),
                        'Moneda':limpiarPrecios(0,precio.text.strip()),           
                        'URL':limpiarURL(DOMINIO_OLX,url)
                })
    return aux
#LISTA DE DICCIONARIOS  FORMATO {"Modelo": "titulo" , "Valor": precio ,"Moneda": "tipoDeMoneda", "URL": "url" }
r1=requests.get(urlOLX)
soup1=BeautifulSoup(r1.content, "html.parser")
datos=soup1.find_all("li",attrs={"class":"_3V_Ww","data-aut-id":"itemBox","data-aut-category-id":"378"})
dicc1=extraerDatos1(datos)

##2DA PAGINA DE AVISOS
#---AUTOCOSMOS---
AUTOCOSMOS="AUTOCOSMOS"
DOMINIO_AUTOCOSMOS="https://www.autocosmos.com.ar"
urlAutoCosmos="https://www.autocosmos.com.ar/auto"

#LIMPIEZA 
def unirText(nombre,modelo):
    return (nombre.text+" "+modelo.text).title()
     

def limpiarURL2(dominio,url):
     if(url is not None):
            if(url.get("href").find("/auto/")!=-1):
                return dominio+url.get("href")

#EXTRACCION p/ AUTOCOSMOS
def extraerDatos2(soup,lista):
    for dato in soup:
        modelo2= dato.find("span",attrs={"class":"listing-card__model"})
        
        if(modelo2 is not None):
            precio2= dato.find("span",attrs={"class":"listing-card__price-value","itemprop":"price"})
            nombre2=dato.find("span",attrs={"class":"listing-card__brand"})

            url = dato.find("a",attrs={"itemprop":"url"})
          
            lista.append({
                    
                        'Modelo':unirText(nombre2,modelo2),
                        'Valor':limpiarPrecios(1,precio2.text.strip()),
                        'Moneda':limpiarPrecios(0,precio2.text.strip()),           
                        'URL':limpiarURL2(DOMINIO_AUTOCOSMOS,url)
                })
    return lista


##SCRAPEA 10 PAGs de la URL AUTOCOSMOS
#LISTA DE DICCIONARIOS  FORMATO {"Modelo": "titulo" , "Valor": precio ,"Moneda": "tipoDeMoneda", "URL": "url" }
dicc2=[]
ind2=0
#SCRAPEA LA 1RA PAG
r2=requests.get(urlAutoCosmos)
soup2=BeautifulSoup(r2.content, "html.parser")
datos2=soup2.find_all("article",attrs={"class":"card listing-card","itemtype":"http://schema.org/Car"})
extraerDatos2(datos2,dicc2)
#SCRAPEA LAS PAGINAS RESTANTES
next_footer_element = soup2.find('footer', class_='pagenav')
while next_footer_element is not None and ind2<9:
        next_page_relative_url = next_footer_element.find('a',class_='pagenav btn m-next',href=True)['href']
        page = requests.get(DOMINIO_AUTOCOSMOS+next_page_relative_url)
        soup22=BeautifulSoup(page.content, "html.parser")
        datos22=soup22.find_all("article",attrs={"class":"card listing-card","itemtype":"http://schema.org/Car"})
        extraerDatos2(datos22,dicc2)
        next_footer_element = soup22.find('footer', class_='pagenav')
        ind2+=1

##3RA PAGINA DE AVISOS
#---LAVOZ---
LAVOZ="LA VOZ"
DOMINIO_LAVOZ="https://clasificados.lavoz.com.ar"
urlLaVOZ="https://clasificados.lavoz.com.ar/vehiculos/vehiculos"

def extraerDatos3(soup,lista):
    for dato in soup:
        modelo3= dato.find("h2",attrs={"class":"bold mx0 mt0 pt1 mb1 col-12 title-2lines h4"})
        
        if(modelo3 is not None):
            precio3= dato.find("span",attrs={"class":"price"})
            url = dato.find("a",attrs={"class":"text-decoration-none","target":"_self"})
          
            lista.append({
                        'Modelo':modelo3.text.strip().title(),
                        'Valor':limpiarPrecios(1,precio3.text.strip()),
                        'Moneda':limpiarPrecios(0,precio3.text.strip()),           
                        'URL':url.get("href")
                })
    return lista
##SCRAPEA 10 PAGs de la URL LA VOZ
#LISTA DE DICCIONARIOS  FORMATO {"Modelo": "titulo" , "Valor": precio ,"Moneda": "tipoDeMoneda", "URL": "url" }
dicc3=[]
ind3=0
#SCRAPEA LA 1RA PAG
r3=requests.get(urlLaVOZ)
soup3=BeautifulSoup(r3.content, "html.parser")
datos3=soup3.find_all("div",attrs={"class":"col-6 flex flex-wrap content-start sm-col-3 md-col-3 align-top"})
extraerDatos3(datos3,dicc3)
#SCRAPEA LAS RESTANTES
next_div_element3 = soup3.find("div", attrs={"class":"wrapper py2"})

while next_div_element3 is not None and ind3<9:
     
        next_page_relative_url3 = next_div_element3.find("a",class_='right button-narrow',rel="next",href=True)['href'] 
        page3 = requests.get(next_page_relative_url3)
        soup33=BeautifulSoup(page3.content, "html.parser")
        datos33=soup33.find_all("div",attrs={"class":"col-6 flex flex-wrap content-start sm-col-3 md-col-3 align-top"})
        extraerDatos3(datos33,dicc3)
        next_div_element3 = soup33.find("div", attrs={"class":"wrapper py2"})
        
        ind3+=1

#print(dicc3)

##4TA PAGINA DE VENTA DE AUTOS
#---MERCADO LIBRE---
MERCADOLIBRE="MERCADO LIBRE"
DOMINIO_ML="https://listado.mercadolibre.com.ar"
urlML="https://listado.mercadolibre.com.ar/autos"

def extraerDatos4(soup,lista):
    for dato in soup:
        modelo4= dato.find("h2",attrs={"class":"ui-search-item__title shops__item-title"})
        
        if(modelo4 is not None):
            precio4= dato.find("span",attrs={"class":"andes-money-amount__fraction","aria-hidden":"true"})
            moneda4=dato.find("span",attrs={"class":"andes-money-amount__currency-symbol"})
            url = dato.find("a",attrs={"class":"ui-search-item__group__element shops__items-group-details ui-search-link","target":"_blank"})
            lista.append({
                        'Modelo':modelo4.text.strip().title(),
                        'Valor':int(precio4.text.replace('.', '')),
                        'Moneda':moneda4.text,           
                        'URL':url.get("href")
                })
    return lista
##SCRAPEA 10 PAGs de la URL MercadoLibre
#LISTA DE DICCIONARIOS  FORMATO {"Modelo": "titulo" , "Valor": precio ,"Moneda": "tipoDeMoneda", "URL": "url" }
dicc4=[]
ind4=0
#SCRAPEA LA 1RA PAG
r4=requests.get(urlML)
soup4=BeautifulSoup(r4.content, "html.parser")
datos4=soup4.find_all("div",attrs={"class":"ui-search-result__content"})
extraerDatos4(datos4,dicc4)
#SCRAPEA LAS RESTANTES
next_li_element4 = soup4.find("li", attrs={"class":"andes-pagination__button andes-pagination__button--next shops__pagination-button"})

while next_li_element4 is not None and ind4<9:
        next_page_relative_url4 = next_li_element4.find("a",attrs={"class":"andes-pagination__link shops__pagination-link ui-search-link","rel":"nofollow","role":"button","title":"Siguiente"})
        page4 = requests.get(next_page_relative_url4.get("href"))
        soup44=BeautifulSoup(page4.content, "html.parser")
        datos44=soup44.find_all("div",attrs={"class":"ui-search-result__content"})
        extraerDatos4(datos44,dicc4)
        next_li_element4 = soup44.find("li", attrs={"class":"andes-pagination__button andes-pagination__button--next shops__pagination-button"})
        ind4+=1

#MOSTRAR LISTA TABULAR DE DIC
def mostrarTabla(dominio,lista):
    print("AVISOS CLASIFICADOS DE AUTOS DE "+dominio)
    print ("{:<25} {:<8} {:<15}".format('Modelo','Precio','URL'))
    for v in lista:        
        print ("{:<25} {:<8} {:<15}".format(v.get('Modelo'),v.get('Moneda')+str(v.get('Valor')),v.get('URL')))

#print(mostrarTabla(DOMINIO_OLX,dicc1,))
#print(mostrarTabla(DOMINIO_LAVOZ,dicc2))
#print(mostrarTabla(DOMINIO_LOSANDES,dicc3))


"""""
##PAGINA DE AVISOS AUXILIAR
#LOSANDES
DOMINIO_LOSANDES="https://clasificados.losandes.com.ar/"
urlLosAndes="https://clasificados.losandes.com.ar/vehiculos/todo"

r3=requests.get(urlLosAndes)
soup3=BeautifulSoup(r3.content, "html.parser")
modelo3= soup3.find_all("h2",attrs={"class":"bold mx0 mt0 pt1 mb1 col-12 title-2lines h4"})
precio3= soup3.find_all("span",attrs={"class":"price"})
url3= soup3.find_all("a",attrs={"class":"text-decoration-none","target":"_self"})

precios3=[i.text for i in precio3]
modelos3=[i.text for i in modelo3]
#urls3=[i.get("href") for i in url3]
#LIMPIAR URL
def limpiarURL3(url):
    aux=[]
    for i in url:
        if i.get("href") not in aux:
            aux.append(i.get("href"))
    return aux
urls3=limpiarURL3(url3)
"""

