// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CZE.l_sk;
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
    public static RandomAccessFile Otvoriť(String Cesta, String Mód) throws IOException {
        return new RandomAccessFile(Cesta, Mód);
    }
    public static int Čítanie(RandomAccessFile Súbor, byte[] data) throws IOException {
        return Súbor.read(data);
    }
    public static void Zápis(RandomAccessFile Súbor, byte[] data) throws IOException {
        Súbor.write(data);
    }
    public static void seek(RandomAccessFile Súbor, long Pozícia) throws IOException {
        Súbor.seek(Pozícia);
    }
    public static void sync(RandomAccessFile Súbor) throws IOException {
        Súbor.getFD().sync();
    }
    public static void Zatvoriť(RandomAccessFile Súbor) throws IOException {
        Súbor.close();
    }
    public static void Odstrániť(String Cesta) throws IOException {
        Files.delete(Paths.get(Cesta));
    }
    public static long Veľkosť(String Cesta) throws IOException {
        return Files.size(Paths.get(Cesta));
    }
    public static Socket Pripojiť(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Akcia) {
        Thread thread = new Thread(Akcia);
        thread.start();
        return thread;
    }
    public static Process Spustiť(List<String> Príkaz) throws IOException {
        return new ProcessBuilder(Príkaz).start();
    }
}
