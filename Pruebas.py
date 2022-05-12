from sqlite3 import DateFromTicks
import time
from time import time as tim
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def instanciaChrome():
	respuesta = False
	try:
		opts = Options()
		opts.add_argument('--ignore-certificate-errors')
		opts.add_argument('--log-level=3')		
		opts.add_argument('--start-maximized')			
		opts.add_experimental_option('excludeSwitches', ['enable-logging'])
		browser = Chrome(options=opts)			
	except:
		print ("[ FAIL ] NO SE PUDO CREAR INSTANCIA DE UN NAVEGADOR")
		return respuesta,0
	else: 
		print ("[  OK  ] CREA INSTANCIA DE NAVEGADOR")
		respuesta = True
		return respuesta, browser

def AbrePagina(chrome, pagina, nombrePag):
	respuesta = False
	inicio = tim()
	try:
		chrome.get(pagina)						
		Buscar = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.ID,"search-input")))
		time.sleep(0.1)				
	except:
		print ("[ FAIL ] NO SE PUDO ABRIR LA PAGINA DE " +nombrePag.upper()+ " ")
		fin = tim()
		total = fin - inicio - 1.1		  
		return respuesta, total
	else:
		print ("[  OK  ] ABRE PAGINA DE " +nombrePag.upper()+ " ")
		fin = tim()
		total = fin - inicio - 1.1
		total1 = str(total)[:4].replace(".",",")		
		print("Tiempo apertura página: %.2f segundos" % (total))		
		respuesta = True
		return respuesta, total
	
def Busqueda(chrome):
	respuesta = False
	try:								
		WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div[2]/button"))).click()																							
		BuscarTXT = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.ID,"js-site-search-input")))
		BuscarTXT.click()
		BuscarTXT.send_keys("Silla Gamer" )
		time.sleep(1)
		BuscarTXT.send_keys(Keys.ENTER)	
		time.sleep(1)				
	except:
		print("[ FAIL ] NO SE PUDO INGRESAR LA BUSQUEDA DEL PRODUCTO")
		return respuesta
	else:		
		print("[  OK  ] SE REALIZO LA BUSQUEDA DEL PRODUCTO CORRECTAMENTE")
		try:	
			Productos = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/section[3]/div/div/div/ul")))								
			seleccion = Productos.find_elements_by_tag_name("a")
			for selection in seleccion:	
				print(selection.text)
			Ordenar = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/section[3]/div/div/div/div[2]/div[1]/div[2]/div/div[4]")))				
			Ordenar.click()		
			PrecioMenor = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/section[3]/div/div/div/div[2]/div[1]/div[2]/div/div[4]/div/div[2]/ul/li[4]")))				
			PrecioMenor.click()
			time.sleep(2)
		except:
			print("[ FAIL ] NO SE PUDO ORDENAR DE MENOR A MAYOR PRECIO")
			return respuesta
		else:
			print("[  OK  ] SE ORDENO DE MENOR A MAYOR PRECIO CORRECTAMENTE")
			respuesta = True			
			return respuesta		

def CarritoCompra(chrome):
	respuesta = False
	try:
		Producto = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/section[3]/div/div/div/ul/li[2]/div[1]/a/div/div/img")))
		Producto.click()		
		time.sleep(2)
		BTNCompra = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[7]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/form[2]/button")))
		BTNCompra.click()	
		time.sleep(1)			
		WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[7]/div[2]/div/div[2]/div/div/div[1]/button"))).click()
		time.sleep(1)
		WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/header/div[2]/div/div/div[2]/nav/ul/li[2]/a/span[1]"))).click()
		time.sleep(2)
	except:
		print("[ FAIL ] NO SE PUDO AGREGAR AL CARRITO EL PRODUCTO MAS BARATO")
		return respuesta 
	else:
		print("[  OK  ] SE AGREGO CORRECTAMENTE AL CARRITO")
		try:
			CantProductos = WebDriverWait(chrome, 1).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div/div/div[1]/div[1]/div/div[1]/div[1]/ul/li/div[3]/div[2]/div[1]/form/span/select/option[4]")))
			CantProductos.click()
			time.sleep(2)
		except:
			print("[ FAIL ] NO SE PUDIERON AUMENTAR LA CANTIDAD DE PRODUCTOS A 3 ")
			return respuesta
		else:
			print("[  OK  ] SE CAMBIARON LA CANTIDAD DE PRODUCTOS CORRECTAMENTE A 3")
			respuesta = True
			time.sleep(2)
			return respuesta

def Pagar(chrome):
	respuesta = False	
	try:		
		WebDriverWait(chrome, 4).until(EC.presence_of_element_located((By.ID,"js-go-to-pay"))).click()
		time.sleep(2)
	except:
		print("[ FAIL ] NO SE PUDO PULSAR LA OPCION 'FINALIZAR COMPRA'")
		return respuesta
	else:
		print("[  OK  ] SE PULSO LA OPCION 'FINALIZAR COMPRA' CORRECTAMENTE")
		try:
			Correo = WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div/div/div[1]/div/div/div/div/div[2]/div/form/div[1]/div/div/input")))
			time.sleep(1)
			NumeroCo = random.randint(10000,99999)
			Correo.send_keys("juan"+str(NumeroCo)+"@gmail.com")
			time.sleep(1)			
			Correo.send_keys(Keys.ENTER)
			time.sleep(2)			
		except:
			print("[ FAIL ] NO SE PUDO INGRESAR EL CORREO ELECTRONICO")
			return respuesta
		else:
			print("[  OK  ] SE INGRESO EL CORREO CORRECTAMENTE Y SE AVANZO A AGREGAR DATOS OBLIGATORIOS")
			try:								
				time.sleep(2)
				Datos = WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.ID,"firstName")))
				Datos.send_keys("Juan")
				time.sleep(1)
				Datos.send_keys(Keys.TAB + "Perez" + Keys.TAB + "3201100011")				
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[1]/div/div[1]/form/div[6]/label"))).click()				
				time.sleep(1)															 
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[1]/div/div[2]/div/button"))).click()
				time.sleep(1)
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div[4]/div[1]/div[1]/div[1]/div/div"))).click()
				time.sleep(1)
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div[4]/div[1]/div[1]/div[1]/div/div/div[2]/ul/li[2]"))).click()
				time.sleep(1)
				Cedula = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div[4]/div[1]/div[1]/div[2]/div/div/input")))
				Cedula.send_keys("1000055050" + Keys.TAB + Keys.TAB )															 								
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div[4]/div[1]/div[5]/div[1]/div/div/div"))).click()
				time.sleep(1)
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div[4]/div[1]/div[5]/div[1]/div/div/div/div[2]/ul/li[1]"))).click()
				time.sleep(2)				
				Direccion = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div[4]/div[1]/div[6]/div[2]/div/div[1]/div/input")))
				Direccion.send_keys("KR 10 # 15 - 10" + Keys.TAB + "LA VERACRUZ" + Keys.TAB + Keys.TAB)
				time.sleep(2)															 		
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div[5]/div[2]/label[1]/div/label"))).click()				
				time.sleep(2)				
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[3]/button"))).click()								
				time.sleep(2)				
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]"))).click()				
				time.sleep(1)							
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div/button[2]"))).click()												
				time.sleep(5)	
				WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section/div[2]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/form/button"))).click()
				time.sleep(10)
			except:
				print("[ FAIL ] NO SE PUDIERON INGRESAR LOS DATOS OBLIGATORIOS")
				return respuesta
			else:
				print("[  OK  ] DATOS OBLIGATORIOS INGRESADOS CORRECTAMENTE, SE REALIZO TODO EL PROCEDIMIENTO CORRECTAMENTE")				
				respuesta = True
				return respuesta		

respuestaIC, navegador = instanciaChrome()
pagina = "ktronix"
URL = "https://www."+pagina+".com"
print("AUTOMATIZACION DE PAGINA...", pagina.upper())
respuestaAP, respuestaBP, respuestaCC, respuestaP = 0,0,0,0			
if(respuestaIC):		
	respuestaAP = AbrePagina(navegador, URL, pagina)    		
	if (respuestaAP):
		respuestaBP = Busqueda(navegador)
		if (respuestaBP):
			respuestaCC = CarritoCompra(navegador)
			if (respuestaCC):
				respuestaP = Pagar(navegador)					
				time.sleep(10)
navegador.quit()


