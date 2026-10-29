// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PHL.l_es;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class LlamadasSistema {
    private LlamadasSistema() { }
    public static RandomAccessFile abrir(String ruta, String modo) throws IOException {
        return new RandomAccessFile(ruta, modo);
    }
    public static int leer(RandomAccessFile archivo, byte[] datos) throws IOException {
        return archivo.read(datos);
    }
    public static void escribir(RandomAccessFile archivo, byte[] datos) throws IOException {
        archivo.write(datos);
    }
    public static void posicionar(RandomAccessFile archivo, long posición) throws IOException {
        archivo.seek(posición);
    }
    public static void sincronizar(RandomAccessFile archivo) throws IOException {
        archivo.getFD().sync();
    }
    public static void cerrar(RandomAccessFile archivo) throws IOException {
        archivo.close();
    }
    public static void eliminar(String ruta) throws IOException {
        Files.delete(Paths.get(ruta));
    }
    public static long tamaño(String ruta) throws IOException {
        return Files.size(Paths.get(ruta));
    }
    public static Socket conectar(String dirección, int númeroPuerto) throws IOException {
        return new Socket(dirección, númeroPuerto);
    }
    public static DatagramSocket datagrama(int númeroPuerto) throws SocketException {
        return new DatagramSocket(númeroPuerto);
    }
    public static Thread hilo(Runnable acción) {
        Thread hilo = new Thread(acción);
        hilo.start();
        return hilo;
    }
    public static Process ejecutar(List<String> orden) throws IOException {
        return new ProcessBuilder(orden).start();
    }
}
