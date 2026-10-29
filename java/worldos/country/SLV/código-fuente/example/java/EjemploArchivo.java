// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class EjemploArchivo {
    public static void ponerEnMarcha() throws español.propio.ExcepciónSalidaEntrada {
        español.propio.Archivo.escribir("java.txt", "JAVA Archivo: Español 😀\n");
        español.propio.Salida.escribir(español.propio.Archivo.leer("java.txt"));
    }
}
