import español

def saludar(nombre):
    saludo = "안녕하세요 " + nombre
    español.escribirArchivo("Saludo.txt", saludo)
    español.Salida(español.decodificarTexto(español.leerArchivo("Saludo.txt")))

saludar("누리")
