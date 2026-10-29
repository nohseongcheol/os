from español import Salida, escribirArchivo, leerArchivo, codificarTexto, decodificarTexto
Datos = "PYTHON Archivo: es 😀\n"
escribirArchivo("python.txt", codificarTexto(Datos))
leerValorTexto = decodificarTexto(leerArchivo("python.txt"))
assert leerValorTexto == Datos
Salida(leerValorTexto, terminación="")
