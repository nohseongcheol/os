// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ESP.l_ast;
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
    public static RandomAccessFile Abrir(String Camín, String Mou) throws IOException {
        return new RandomAccessFile(Camín, Mou);
    }
    public static int Llectura(RandomAccessFile Ficheru, byte[] data) throws IOException {
        return Ficheru.read(data);
    }
    public static void Escritura(RandomAccessFile Ficheru, byte[] data) throws IOException {
        Ficheru.write(data);
    }
    public static void seek(RandomAccessFile Ficheru, long Posición) throws IOException {
        Ficheru.seek(Posición);
    }
    public static void sync(RandomAccessFile Ficheru) throws IOException {
        Ficheru.getFD().sync();
    }
    public static void Zarrar(RandomAccessFile Ficheru) throws IOException {
        Ficheru.close();
    }
    public static void Desaniciar(String Camín) throws IOException {
        Files.delete(Paths.get(Camín));
    }
    public static long Tamañu(String Camín) throws IOException {
        return Files.size(Paths.get(Camín));
    }
    public static Socket Coneutar(String address, int Puertu) throws IOException {
        return new Socket(address, Puertu);
    }
    public static DatagramSocket datagram(int Puertu) throws SocketException {
        return new DatagramSocket(Puertu);
    }
    public static Thread thread(Runnable Aición) {
        Thread thread = new Thread(Aición);
        thread.start();
        return thread;
    }
    public static Process Executar(List<String> Comandu) throws IOException {
        return new ProcessBuilder(Comandu).start();
    }
}
