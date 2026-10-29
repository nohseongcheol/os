// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ROU.l_ro;
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
    public static RandomAccessFile Deschide(String Cale, String Mod) throws IOException {
        return new RandomAccessFile(Cale, Mod);
    }
    public static int Citire(RandomAccessFile Fișier, byte[] data) throws IOException {
        return Fișier.read(data);
    }
    public static void Scriere(RandomAccessFile Fișier, byte[] data) throws IOException {
        Fișier.write(data);
    }
    public static void seek(RandomAccessFile Fișier, long Poziție) throws IOException {
        Fișier.seek(Poziție);
    }
    public static void sync(RandomAccessFile Fișier) throws IOException {
        Fișier.getFD().sync();
    }
    public static void Închide(RandomAccessFile Fișier) throws IOException {
        Fișier.close();
    }
    public static void Elimină(String Cale) throws IOException {
        Files.delete(Paths.get(Cale));
    }
    public static long Mărime(String Cale) throws IOException {
        return Files.size(Paths.get(Cale));
    }
    public static Socket Conectează(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable Acțiuni) {
        Thread thread = new Thread(Acțiuni);
        thread.start();
        return thread;
    }
    public static Process Execută(List<String> Comandă) throws IOException {
        return new ProcessBuilder(Comandă).start();
    }
}
