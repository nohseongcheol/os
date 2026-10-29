// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PRT.l_gl;
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
    public static RandomAccessFile Abrir(String CAMIÑO, String Modo) throws IOException {
        return new RandomAccessFile(CAMIÑO, Modo);
    }
    public static int Lectura(RandomAccessFile Ficheiro, byte[] data) throws IOException {
        return Ficheiro.read(data);
    }
    public static void Escritura(RandomAccessFile Ficheiro, byte[] data) throws IOException {
        Ficheiro.write(data);
    }
    public static void seek(RandomAccessFile Ficheiro, long Posición) throws IOException {
        Ficheiro.seek(Posición);
    }
    public static void sync(RandomAccessFile Ficheiro) throws IOException {
        Ficheiro.getFD().sync();
    }
    public static void Pechar(RandomAccessFile Ficheiro) throws IOException {
        Ficheiro.close();
    }
    public static void Retirar(String CAMIÑO) throws IOException {
        Files.delete(Paths.get(CAMIÑO));
    }
    public static long Tamaño(String CAMIÑO) throws IOException {
        return Files.size(Paths.get(CAMIÑO));
    }
    public static Socket Conectar(String address, int Porto) throws IOException {
        return new Socket(address, Porto);
    }
    public static DatagramSocket datagram(int Porto) throws SocketException {
        return new DatagramSocket(Porto);
    }
    public static Thread thread(Runnable Acción) {
        Thread thread = new Thread(Acción);
        thread.start();
        return thread;
    }
    public static Process Executar(List<String> Orde) throws IOException {
        return new ProcessBuilder(Orde).start();
    }
}
