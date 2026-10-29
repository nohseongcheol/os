// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.FRA.l_oc;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class SystemCalls {
    private SystemCalls() { }
    public static RandomAccessFile Dobrir(String CAMIN, String Mòde) throws IOException {
        return new RandomAccessFile(CAMIN, Mòde);
    }
    public static int Lectura(RandomAccessFile Fichièr, byte[] data) throws IOException {
        return Fichièr.read(data);
    }
    public static void Escritura(RandomAccessFile Fichièr, byte[] data) throws IOException {
        Fichièr.write(data);
    }
    public static void seek(RandomAccessFile Fichièr, long Posicion) throws IOException {
        Fichièr.seek(Posicion);
    }
    public static void sync(RandomAccessFile Fichièr) throws IOException {
        Fichièr.getFD().sync();
    }
    public static void Tampar(RandomAccessFile Fichièr) throws IOException {
        Fichièr.close();
    }
    public static void Suprimir(String CAMIN) throws IOException {
        Files.delete(Paths.get(CAMIN));
    }
    public static long Talha(String CAMIN) throws IOException {
        return Files.size(Paths.get(CAMIN));
    }
    public static Socket Se_connectar(String address, int Pòrt) throws IOException {
        return new Socket(address, Pòrt);
    }
    public static DatagramSocket datagram(int Pòrt) throws SocketException {
        return new DatagramSocket(Pòrt);
    }
    public static Thread thread(Runnable Accion) {
        Thread thread = new Thread(Accion);
        thread.start();
        return thread;
    }
    public static Process Executar(List<String> Comanda) throws IOException {
        return new ProcessBuilder(Comanda).start();
    }
}
