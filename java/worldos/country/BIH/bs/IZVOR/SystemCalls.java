// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BIH.l_bs;
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
    public static RandomAccessFile Otvori(String Putanja, String Režim) throws IOException {
        return new RandomAccessFile(Putanja, Režim);
    }
    public static int Čitaj(RandomAccessFile Fajl, byte[] data) throws IOException {
        return Fajl.read(data);
    }
    public static void Piši(RandomAccessFile Fajl, byte[] data) throws IOException {
        Fajl.write(data);
    }
    public static void seek(RandomAccessFile Fajl, long Pozicija) throws IOException {
        Fajl.seek(Pozicija);
    }
    public static void sync(RandomAccessFile Fajl) throws IOException {
        Fajl.getFD().sync();
    }
    public static void Zatvori(RandomAccessFile Fajl) throws IOException {
        Fajl.close();
    }
    public static void Ukloni(String Putanja) throws IOException {
        Files.delete(Paths.get(Putanja));
    }
    public static long Veličina(String Putanja) throws IOException {
        return Files.size(Paths.get(Putanja));
    }
    public static Socket Spoji_se(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable radnja) {
        Thread thread = new Thread(radnja);
        thread.start();
        return thread;
    }
    public static Process Izvrši(List<String> Naredba) throws IOException {
        return new ProcessBuilder(Naredba).start();
    }
}
