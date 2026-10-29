// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ITA.l_ca;
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
    public static RandomAccessFile Obre(String Camí, String mode) throws IOException {
        return new RandomAccessFile(Camí, mode);
    }
    public static int Lectura(RandomAccessFile Fitxer, byte[] data) throws IOException {
        return Fitxer.read(data);
    }
    public static void Escriptura(RandomAccessFile Fitxer, byte[] data) throws IOException {
        Fitxer.write(data);
    }
    public static void seek(RandomAccessFile Fitxer, long Posició) throws IOException {
        Fitxer.seek(Posició);
    }
    public static void sync(RandomAccessFile Fitxer) throws IOException {
        Fitxer.getFD().sync();
    }
    public static void Tanca(RandomAccessFile Fitxer) throws IOException {
        Fitxer.close();
    }
    public static void Suprimeix(String Camí) throws IOException {
        Files.delete(Paths.get(Camí));
    }
    public static long Mida(String Camí) throws IOException {
        return Files.size(Paths.get(Camí));
    }
    public static Socket Connecta(String Adreça, int port) throws IOException {
        return new Socket(Adreça, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Acció) {
        Thread thread = new Thread(Acció);
        thread.start();
        return thread;
    }
    public static Process Executa(List<String> Ordre) throws IOException {
        return new ProcessBuilder(Ordre).start();
    }
}
