# 이름은 셸에서 사용하는 ASCII Archivo nombre, Java valorClase/함수는 한국어다.
APP_NAMES := hello udp netcheck stress javac java
APP_SOURCE_javac := Usuario/Java/HerramientaJava.java Usuario/Java/CompiladorJava.java Usuario/Java/ReglasCaracteresIdentificadores.java
APP_ENTRY_javac := CompiladorJava.ponerEnMarcha
APP_SOURCE_java := Usuario/Java/HerramientaJava.java Usuario/Java/MáquinaVirtualJava.java
APP_ENTRY_java := MáquinaVirtualJava.ponerEnMarcha
APP_SOURCE_hello := Usuario/Ejemplos/Saludo.java
APP_ENTRY_hello := Saludo.ponerEnMarcha
APP_SOURCE_udp := Usuario/Ejemplos/ComunicaciónDatos.java
APP_ENTRY_udp := ComunicaciónDatos.ponerEnMarcha
APP_SOURCE_netcheck := Usuario/Ejemplos/pruebaConexiónRed.java
APP_ENTRY_netcheck := pruebaConexiónRed.ponerEnMarcha
APP_SOURCE_stress := Usuario/Ejemplos/bucleRed.java
APP_ENTRY_stress := bucleRed.ponerEnMarcha
